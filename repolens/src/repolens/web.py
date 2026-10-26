from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import shutil
import subprocess
import threading
import time
import urllib.request
import uuid
import webbrowser
import zipfile
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from .cli import run_audit


MAX_BODY_BYTES = 8_192
MAX_FILES_FOR_AUTOFIX = 1_500
MAX_FILES = 20_000
MAX_ARCHIVE_BYTES = 200 * 1024 * 1024
AUDIT_SEMAPHORE = threading.BoundedSemaphore(2)
GITHUB_PART_RE = re.compile(r"^[A-Za-z0-9_.-]+$")
RUN_ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")
IGNORE_DIRS = {
    ".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache",
    ".mypy_cache", "dist", "build", "target", "vendor",
}


def parse_github_url(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("请输入 GitHub 仓库地址。")
    if value.endswith(".git"):
        value = value[:-4]
    parsed = urlparse(value)
    if parsed.scheme != "https" or parsed.netloc.lower() != "github.com":
        raise ValueError("目前只支持 https://github.com/owner/repo 形式的公开仓库。")
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) != 2:
        raise ValueError("链接必须指向仓库主页，而不是文件、Issue 或子目录。")
    owner, repo = parts
    if not GITHUB_PART_RE.fullmatch(owner) or not GITHUB_PART_RE.fullmatch(repo):
        raise ValueError("GitHub 仓库名称不合法。")
    if owner.startswith(".") or repo.startswith("."):
        raise ValueError("GitHub 仓库名称不合法。")
    return f"https://github.com/{owner}/{repo}"


def _count_repo_files(root: Path) -> int:
    count = 0
    for current, dirs, files in os.walk(root):
        dirs[:] = [name for name in dirs if name not in IGNORE_DIRS]
        count += len(files)
        if count > MAX_FILES:
            break
    return count


def _run_git(args: list[str], *, timeout: int = 180) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    return subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
        check=False,
    )


def _github_json(source_url: str) -> dict:
    parsed = urlparse(source_url)
    repo_path = parsed.path.strip("/")
    request = urllib.request.Request(
        f"https://api.github.com/repos/{repo_path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "ReproLens/0.1",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def download_github_archive(source_url: str, destination: Path) -> str:
    metadata = _github_json(source_url)
    if int(metadata.get("size", 0)) * 1024 > MAX_ARCHIVE_BYTES * 2:
        raise RuntimeError("仓库体积过大，超过在线分析上限。")
    branch = metadata.get("default_branch")
    if not branch:
        raise RuntimeError("无法读取 GitHub 默认分支。")
    repo_path = urlparse(source_url).path.strip("/")
    commit_request = urllib.request.Request(
        f"https://api.github.com/repos/{repo_path}/commits/{branch}",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "ReproLens/0.1"},
    )
    with urllib.request.urlopen(commit_request, timeout=30) as response:
        commit = json.loads(response.read().decode("utf-8")).get("sha", "")
    if not commit:
        raise RuntimeError("无法读取 GitHub commit SHA。")

    archive_request = urllib.request.Request(
        f"https://api.github.com/repos/{repo_path}/zipball/{commit}",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "ReproLens/0.1"},
    )
    archive_path = destination.parent / "source.zip"
    total = 0
    with urllib.request.urlopen(archive_request, timeout=120) as response, archive_path.open("wb") as output:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_ARCHIVE_BYTES:
                raise RuntimeError("仓库压缩包超过 200MB 在线分析上限。")
            output.write(chunk)

    extract_dir = destination.parent / "extracted"
    extract_dir.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(archive_path) as archive:
            for member in archive.infolist():
                target = (extract_dir / member.filename).resolve()
                if extract_dir.resolve() not in target.parents and target != extract_dir.resolve():
                    raise RuntimeError("GitHub 压缩包包含不安全路径。")
            archive.extractall(extract_dir)
        roots = [item for item in extract_dir.iterdir() if item.is_dir()]
        if len(roots) != 1:
            raise RuntimeError("GitHub 压缩包结构不符合预期。")
        shutil.move(str(roots[0]), str(destination))
    finally:
        shutil.rmtree(extract_dir, ignore_errors=True)
        archive_path.unlink(missing_ok=True)
    return commit


def clone_public_repo(source_url: str, destination: Path) -> str:
    git_error = ""
    for attempt in range(2):
        if destination.exists():
            shutil.rmtree(destination, ignore_errors=True)
        clone = _run_git(
            ["clone", "--depth", "1", "--single-branch", "--no-tags", source_url, str(destination)]
        )
        if clone.returncode == 0:
            commit = _run_git(["-C", str(destination), "rev-parse", "HEAD"], timeout=30)
            if commit.returncode == 0:
                return commit.stdout.strip()
        message = (clone.stderr or clone.stdout or "git clone failed").strip().splitlines()
        git_error = message[-1][:240] if message else "git clone failed"
        if attempt == 0:
            time.sleep(1.5)
    try:
        return download_github_archive(source_url, destination)
    except Exception as archive_error:
        raise RuntimeError(
            f"GitHub 克隆失败；API 回退也失败：{str(archive_error)[:240]}（git: {git_error}）"
        ) from archive_error


def run_remote_audit(source_url: str, runs_dir: Path, *, autofix: bool = True) -> dict:
    source_url = parse_github_url(source_url)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:8]
    run_dir = runs_dir / run_id
    source_dir = run_dir / "source"
    run_dir.mkdir(parents=True, exist_ok=False)
    try:
        commit = clone_public_repo(source_url, source_dir)
        files = _count_repo_files(source_dir)
        if files > MAX_FILES:
            raise RuntimeError(f"仓库文件过多（{files}），超过在线分析上限 {MAX_FILES}。")
        autofix_ran = bool(autofix and files <= MAX_FILES_FOR_AUTOFIX)
        run = run_audit(
            source_dir,
            run_dir,
            execute=False,
            autofix=autofix_ran,
            explain=True,
            ai_review=True,
            source_url=source_url,
            source_commit=commit,
        )
        shutil.rmtree(source_dir, ignore_errors=True)
        shutil.rmtree(run_dir / "autofix" / "staging", ignore_errors=True)
        result = run["result"]
        autofix_summary = run["autofix_result"]
        if autofix_summary:
            autofix_summary = dict(autofix_summary)
            autofix_summary.pop("proposal_dir", None)
            autofix_summary.pop("staging_dir", None)
        summary = {
            "run_id": run_id,
            "source_url": source_url,
            "source_commit": commit,
            "score": result.total_score,
            "readiness": result.readiness,
            "files_scanned": result.files_scanned,
            "claims": len(result.claim_matrix),
            "evidence_coverage": run["coverage"],
            "ai_mode": result.ai_metadata.get("mode", "rules"),
            "autofix_ran": autofix_ran,
            "autofix": autofix_summary,
            "report_url": f"/reports/{run_id}/report.html",
            "claims_url": f"/reports/{run_id}/claims.md",
            "score_url": f"/reports/{run_id}/score.json",
            "badge_url": f"/reports/{run_id}/badge.svg",
        }
        (run_dir / "web-result.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return summary
    except Exception:
        shutil.rmtree(run_dir, ignore_errors=True)
        raise


LANDING_HTML = r'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ReproLens - 开源 AI 项目复现体检</title>
<style>
:root { --ink:#152033; --muted:#64748b; --line:#dbe4f0; --blue:#2457d6; --blue2:#0ea5e9; --green:#0f8a5f; --amber:#b66a06; --red:#b42336; --paper:#fff; --bg:#f4f7fc; }
* { box-sizing:border-box; }
body { margin:0; font-family:"Segoe UI","Microsoft YaHei",system-ui,sans-serif; color:var(--ink); background:
  radial-gradient(circle at 10% 0%, rgba(36,87,214,.14), transparent 34%),
  radial-gradient(circle at 90% 12%, rgba(14,165,233,.12), transparent 30%), var(--bg); min-height:100vh; }
main { max-width:1100px; margin:0 auto; padding:54px 22px 70px; }
.hero { display:grid; grid-template-columns:1.3fr .7fr; gap:34px; align-items:center; }
.eyebrow { color:var(--blue); font-weight:800; letter-spacing:.08em; text-transform:uppercase; font-size:12px; }
h1 { font-size:clamp(34px,6vw,64px); line-height:1.04; margin:12px 0 18px; letter-spacing:-.045em; }
.grad { background:linear-gradient(90deg,var(--blue),var(--blue2)); -webkit-background-clip:text; background-clip:text; color:transparent; }
.lead { color:var(--muted); font-size:17px; line-height:1.75; max-width:720px; }
.badges { display:flex; flex-wrap:wrap; gap:8px; margin-top:20px; }
.badge { padding:7px 11px; border:1px solid var(--line); border-radius:999px; background:rgba(255,255,255,.7); font-size:12px; font-weight:700; color:#40516c; }
.panel { background:rgba(255,255,255,.92); border:1px solid rgba(219,228,240,.9); border-radius:22px; box-shadow:0 18px 50px rgba(25,48,89,.10); padding:24px; }
.search { display:flex; gap:10px; margin-top:12px; }
input { flex:1; min-width:0; border:1px solid var(--line); border-radius:12px; padding:14px 15px; font-size:15px; outline:none; background:#fbfdff; }
input:focus { border-color:#7ba0ff; box-shadow:0 0 0 4px rgba(36,87,214,.10); }
button { border:0; border-radius:12px; padding:14px 20px; background:linear-gradient(135deg,var(--blue),var(--blue2)); color:white; font-size:15px; font-weight:800; cursor:pointer; white-space:nowrap; }
button:disabled { opacity:.55; cursor:wait; }
.samples { display:flex; flex-wrap:wrap; gap:8px; margin-top:12px; }
.sample { background:#eef3fb; color:#36506f; padding:7px 10px; border-radius:999px; font-size:12px; cursor:pointer; }
.hint { color:var(--muted); font-size:12px; margin-top:12px; line-height:1.6; }
.status { display:none; margin-top:16px; padding:12px 14px; border-radius:12px; background:#eef3fb; color:#31507a; font-size:14px; }
.status.error { display:block; background:#fff0f2; color:#9e1f31; }
.status.loading { display:block; }
.result { display:none; margin-top:18px; border-top:1px solid var(--line); padding-top:18px; }
.result.show { display:block; }
.score-row { display:flex; gap:24px; align-items:center; }
.score { font-size:52px; line-height:1; font-weight:900; color:var(--blue); }
.score small { font-size:16px; color:var(--muted); font-weight:600; }
.readiness { display:inline-block; padding:5px 10px; border-radius:999px; background:#e8eefc; color:var(--blue); font-weight:800; font-size:12px; }
.metrics { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin:18px 0; }
.metric { background:#f8faff; border:1px solid #edf2f9; border-radius:12px; padding:12px; }
.metric b { display:block; font-size:20px; margin-bottom:3px; }
.metric span { color:var(--muted); font-size:12px; }
.actions { display:flex; flex-wrap:wrap; gap:10px; }
.actions a { color:var(--blue); text-decoration:none; font-weight:800; padding:10px 13px; border-radius:10px; background:#eef3fb; }
.steps { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-top:34px; }
.step { background:rgba(255,255,255,.72); border:1px solid var(--line); border-radius:16px; padding:18px; }
.step b { display:block; margin-bottom:8px; }
.step p { margin:0; color:var(--muted); line-height:1.6; font-size:13px; }
.note { margin-top:18px; color:var(--muted); font-size:12px; line-height:1.7; }
@media (max-width:800px){ .hero{grid-template-columns:1fr}.steps{grid-template-columns:1fr}.search{flex-direction:column}.metrics{grid-template-columns:1fr 1fr} }
</style>
</head>
<body><main>
<section class="hero">
  <div>
    <div class="eyebrow">Evidence-constrained repository audit</div>
    <h1>给开源 AI 项目做一次<br><span class="grad">复现体检</span></h1>
    <p class="lead">粘贴任意公开 GitHub 仓库地址，ReproLens 会检查环境、数据、模型、实验、文档和 AI 特有风险，并把 README 声明与仓库证据一一对应。</p>
    <div class="badges"><span class="badge">25 项检查</span><span class="badge">证据可追溯</span><span class="badge">声明验证</span><span class="badge">AutoFix 复测</span><span class="badge">不执行第三方代码</span></div>
  </div>
  <div class="panel">
    <strong>分析公开仓库</strong>
    <div class="search"><input id="repo" placeholder="https://github.com/owner/repo" autocomplete="off"><button id="run">开始体检</button></div>
    <div class="samples"><span class="sample" data-url="https://github.com/huggingface/smolagents">huggingface/smolagents</span><span class="sample" data-url="https://github.com/mem0ai/mem0">mem0ai/mem0</span><span class="sample" data-url="https://github.com/openai/openai-python">openai/openai-python</span></div>
    <div class="hint">仅分析公开仓库；按默认分支最新 commit 生成可追溯报告；不会运行仓库代码或安装依赖。</div>
    <div id="status" class="status"></div>
    <div id="result" class="result">
      <div class="score-row"><div id="score" class="score"></div><div><div id="readiness" class="readiness"></div><div id="commit" class="hint"></div></div></div>
      <div class="metrics"><div class="metric"><b id="files"></b><span>扫描文件</span></div><div class="metric"><b id="coverage"></b><span>证据覆盖率</span></div><div class="metric"><b id="claims"></b><span>README 声明</span></div></div>
      <div id="autofix" class="hint"></div>
      <div id="links" class="actions"></div>
    </div>
  </div>
</section>
<section class="steps">
  <div class="step"><b>1. 先找证据</b><p>每条 PASS / PARTIAL 都有 Evidence ID，可以回到文件与行号，不靠猜。</p></div>
  <div class="step"><b>2. 再验声明</b><p>README 说“能复现、支持某模型、可运行”，工具检查对应证据是否真的存在。</p></div>
  <div class="step"><b>3. 最后整改</b><p>生成最小修复提案，在隔离副本中复测，只保留能提高评分的修改。</p></div>
</section>
<p class="note">报告固定到 commit SHA。证据覆盖率表示“有多少适用检查项存在关联证据”，不代表全部通过；最终结论仍需人工复核。</p>
</main>
<script>
const repo = document.getElementById('repo');
const run = document.getElementById('run');
const status = document.getElementById('status');
const result = document.getElementById('result');
document.querySelectorAll('.sample').forEach(el => el.addEventListener('click', () => { repo.value = el.dataset.url; repo.focus(); }));
function setText(id, value){ document.getElementById(id).textContent = value; }
function addLink(label, href){ const a=document.createElement('a'); a.textContent=label; a.href=href; a.target='_blank'; a.rel='noopener noreferrer'; document.getElementById('links').appendChild(a); }
run.addEventListener('click', async () => {
  const value = repo.value.trim();
  if(!value) { status.className='status error'; status.textContent='请先输入 GitHub 仓库地址。'; return; }
  run.disabled=true; result.classList.remove('show'); document.getElementById('links').replaceChildren();
  status.className='status loading'; status.textContent='正在浅克隆仓库并执行静态审计，大型仓库可能需要几十秒…';
  try {
    const response = await fetch('/api/audit', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({url:value})});
    const data = await response.json();
    if(!response.ok) throw new Error(data.error || '分析失败');
    status.className='status'; status.textContent='分析完成。';
    setText('score', data.score.toFixed(1)); document.getElementById('score').insertAdjacentHTML('beforeend','<small> / 100</small>');
    setText('readiness', data.readiness); setText('commit', 'commit ' + data.source_commit.slice(0,12));
    setText('files', data.files_scanned); setText('coverage', data.evidence_coverage.percent.toFixed(1)+'%'); setText('claims', data.claims);
    const fixText = data.autofix ? `AutoFix：${data.autofix.before_score.toFixed(1)} → ${data.autofix.after_score.toFixed(1)}（+${data.autofix.delta.toFixed(1)}）` : (data.autofix_ran ? 'AutoFix 已完成。' : '仓库较大，本次跳过 AutoFix，仅执行静态审计。');
    setText('autofix', fixText + '  |  语义映射：' + data.ai_mode);
    addLink('打开完整报告', data.report_url); addLink('查看声明矩阵', data.claims_url); addLink('下载评分 JSON', data.score_url); addLink('复现徽章', data.badge_url);
    result.classList.add('show');
  } catch (error) {
    status.className='status error'; status.textContent = error.message;
  } finally { run.disabled=false; }
});
</script>
</body></html>'''


class ReproLensWebHandler(BaseHTTPRequestHandler):
    server_version = "ReproLensWeb/0.1"

    @property
    def runs_dir(self) -> Path:
        return self.server.runs_dir  # type: ignore[attr-defined]

    def log_message(self, fmt: str, *args: object) -> None:
        return

    def _json(self, payload: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _html(self, html: str) -> None:
        body = html.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._html(LANDING_HTML)
            return
        if parsed.path == "/api/health":
            self._json({"status": "ok"})
            return
        if parsed.path.startswith("/reports/"):
            self._serve_report(parsed.path.removeprefix("/reports/"))
            return
        self._json({"error": "Not found"}, HTTPStatus.NOT_FOUND)

    def _serve_report(self, relative: str) -> None:
        parts = [part for part in relative.split("/") if part]
        if len(parts) != 2 or not RUN_ID_RE.fullmatch(parts[0]):
            self._json({"error": "Not found"}, HTTPStatus.NOT_FOUND)
            return
        target = (self.runs_dir / parts[0] / parts[1]).resolve()
        runs_root = self.runs_dir.resolve()
        if runs_root not in target.parents or not target.is_file():
            self._json({"error": "Not found"}, HTTPStatus.NOT_FOUND)
            return
        body = target.read_bytes()
        content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type + ("; charset=utf-8" if content_type.startswith("text/") else ""))
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        if self.path != "/api/audit":
            self._json({"error": "Not found"}, HTTPStatus.NOT_FOUND)
            return
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length <= 0 or length > MAX_BODY_BYTES:
            self._json({"error": "请求内容过大或为空。"}, HTTPStatus.BAD_REQUEST)
            return
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            source_url = parse_github_url(str(payload.get("url", "")))
        except (ValueError, json.JSONDecodeError) as exc:
            self._json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
            return
        if not AUDIT_SEMAPHORE.acquire(blocking=False):
            self._json({"error": "当前分析任务较多，请稍后重试。"}, HTTPStatus.TOO_MANY_REQUESTS)
            return
        try:
            summary = run_remote_audit(source_url, self.runs_dir, autofix=True)
            self._json(summary)
        except subprocess.TimeoutExpired:
            self._json({"error": "克隆仓库超时，请换一个较小的仓库或稍后重试。"}, HTTPStatus.GATEWAY_TIMEOUT)
        except Exception as exc:
            self._json({"error": str(exc)[:500]}, HTTPStatus.INTERNAL_SERVER_ERROR)
        finally:
            AUDIT_SEMAPHORE.release()


class ReproLensHTTPServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address: tuple[str, int], runs_dir: Path):
        super().__init__(address, ReproLensWebHandler)
        self.runs_dir = runs_dir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="repolens.web", description="ReproLens web interface.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--data-dir", default="web-runs")
    parser.add_argument("--open", action="store_true", help="Open the browser after startup.")
    args = parser.parse_args(argv)
    runs_dir = Path(args.data_dir).expanduser().resolve()
    runs_dir.mkdir(parents=True, exist_ok=True)
    server = ReproLensHTTPServer((args.host, args.port), runs_dir)
    url = f"http://{args.host}:{args.port}/"
    print(f"ReproLens Web running at {url}")
    print("Press Ctrl+C to stop. Public repositories only; repository code is not executed.")
    if args.open:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping ReproLens Web.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
