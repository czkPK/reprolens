from __future__ import annotations

import difflib
import hashlib
import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .autofix_report import tree_fingerprint, write_autofix_html
from .models import AuditResult
from .rules import evaluate_criteria
from .scanner import scan_repo
from .scoring import total_score


@dataclass
class AutoFixFile:
    path: str
    reason: str
    content: str


def _prompt_hashes(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        low = path.relative_to(root).as_posix().lower()
        if "prompt" not in low:
            continue
        if any(part in path.parts for part in (".git", ".venv", "node_modules", "__pycache__")):
            continue
        try:
            data = path.read_bytes()
        except OSError:
            continue
        result[path.relative_to(root).as_posix()] = hashlib.sha256(data).hexdigest()
    return result


def _extract_llm_values(root: Path) -> dict[str, str]:
    texts: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix().lower()
        if not (
            rel.startswith(("configs/", "config/", "conf/"))
            or rel.endswith("readme.md")
            or path.name.lower() in {"app.py", "main.py"}
        ):
            continue
        try:
            texts.append(path.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            pass
    blob = "\n".join(texts)
    patterns = {
        "provider": r"(?im)^\s*provider\s*[:=]\s*([A-Za-z0-9_.-]+)",
        "model_id": r"(?im)^\s*(?:name|model_id|model_name)\s*[:=]\s*([A-Za-z0-9_.:/-]+)",
        "temperature": r"(?im)^\s*temperature\s*[:=]\s*([0-9.]+)",
        "top_p": r"(?im)^\s*top_p\s*[:=]\s*([0-9.]+)",
        "max_tokens": r"(?im)^\s*max_tokens\s*[:=]\s*([0-9]+)",
    }
    values: dict[str, str] = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, blob)
        if match:
            values[key] = match.group(1)
    return values


def _build_proposal(root: Path, result: AuditResult) -> list[AutoFixFile]:
    status = {item.id: item.status for item in result.criteria}
    files: list[AutoFixFile] = []

    def add(path: str, reason: str, content: str) -> None:
        target = root / path
        if target.exists():
            return
        files.append(AutoFixFile(path=path, reason=reason, content=content.rstrip() + "\n"))

    if status.get("ENV-02") != "pass":
        add(
            "Dockerfile",
            "ENV-02: 增加容器化入口，固定 Python 与依赖安装方式。",
            """FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN if [ -f requirements.txt ]; then python -m pip install --no-cache-dir -r requirements.txt; fi
RUN if [ -f pyproject.toml ]; then python -m pip install --no-cache-dir -e .; fi
CMD ["python", "-c", "print('Configure the project entry point')"]
""",
        )

    if status.get("DOC-03") != "pass":
        add(
            "reproduce.sh",
            "DOC-03: 提供一键复现入口。",
            """#!/usr/bin/env bash
set -euo pipefail
if [ -f requirements.txt ]; then python -m pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then python -m pip install -e .; fi
python -m compileall -q .
echo "Environment and syntax checks completed. Add the project-specific run command here."
""",
        )

    if status.get("DOC-03") != "pass":
        add(
            "tests/test_smoke.py",
            "DOC-03: 增加最小烟雾测试，验证关键项目文件存在。",
            """import unittest
from pathlib import Path


class SmokeTest(unittest.TestCase):
    def test_project_files_exist(self):
        root = Path(__file__).resolve().parents[1]
        self.assertTrue((root / "README.md").exists())


if __name__ == "__main__":
    unittest.main()
""",
        )

    if status.get("DATA-02") != "pass":
        add(
            "data/download.sh",
            "DATA-02: 提供数据下载脚本入口；URL 需要维护者补充。",
            """#!/usr/bin/env bash
set -euo pipefail
DATA_URL="${DATA_URL:-TODO}"
if [ "$DATA_URL" = "TODO" ]; then
  echo "Set DATA_URL before running this script." >&2
  exit 2
fi
curl -L "$DATA_URL" -o data/raw.zip
""",
        )

    if status.get("DATA-03") != "pass":
        add(
            "dataset_card.md",
            "DATA-03: 增加数据集卡模板；来源和许可需要维护者确认。",
            """# Dataset Card

- Dataset name: TODO
- Source: TODO
- Version: TODO
- License: TODO
- Redistribution allowed: TODO
- Preprocessing: TODO
- Known limitations: TODO
""",
        )

    model_values = _extract_llm_values(root)
    if status.get("MODEL-02") != "pass" or status.get("MODEL-03") != "pass":
        provider = model_values.get("provider", "TODO")
        model_id = model_values.get("model_id", "TODO")
        add(
            "model_card.md",
            "MODEL-02/03: 增加模型卡，记录可核验的模型来源。",
            f"""# Model Card

- Provider: {provider}
- Model ID: {model_id}
- Model version: {model_id}
- Source: repository documentation
""",
        )

    hashes = _prompt_hashes(root)
    if status.get("LLM-02") != "pass" and hashes:
        metadata = {
            "prompt_version": "1.0.0",
            "versioning_method": "sha256 of current prompt files",
            "prompt_files": hashes,
            "note": "Generated by ReproLens AutoFix. Review before publishing.",
        }
        add(
            "prompts/prompt_metadata.json",
            "LLM-02: 为当前 prompt 文件生成可核验的版本号和哈希。",
            json.dumps(metadata, ensure_ascii=False, indent=2),
        )

    if any(status.get(item) != "pass" for item in ("LLM-01", "LLM-03", "LLM-04")):
        provider = model_values.get("provider", "TODO")
        model_id = model_values.get("model_id", "TODO")
        temperature = model_values.get("temperature", "TODO")
        top_p = model_values.get("top_p", "TODO")
        max_tokens = model_values.get("max_tokens", "TODO")
        add(
            "configs/llm_metadata.yaml",
            "LLM-01/03: 增加模型和采样参数配置模板。",
            f"""model:
  provider: {provider}
  model_id: {model_id}
  model_version: {model_id}
sampling:
  temperature: {temperature}
  top_p: {top_p}
  max_tokens: {max_tokens}
""",
        )

    if status.get("LLM-07") != "pass":
        add(
            "eval/README.md",
            "LLM-07: 增加评测协议模板；评测集、数据划分和污染分析需要维护者确认。",
            """# Evaluation Protocol

- Evaluation dataset: TODO
- Train/validation/test split: TODO
- Contamination analysis: TODO
- Metric definition: TODO
- Expected result: TODO
""",
        )

    return files


def _copy_repo(root: Path, staging: Path) -> None:
    if staging.exists():
        shutil.rmtree(staging)
    ignore = shutil.ignore_patterns(
        ".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache",
        ".mypy_cache", "dist", "build", "benchmark", "reports",
    )
    shutil.copytree(root, staging, ignore=ignore)


def generate_autofix(root: Path, result: AuditResult, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    proposal_dir = out_dir / "proposal"
    staging_dir = out_dir / "staging"
    if proposal_dir.exists():
        shutil.rmtree(proposal_dir)
    proposal_dir.mkdir(parents=True, exist_ok=True)

    original_fingerprint = tree_fingerprint(root)
    files = _build_proposal(root, result)
    _copy_repo(root, staging_dir)

    accepted: list[AutoFixFile] = []
    rejected: list[dict[str, str]] = []
    current_score = result.total_score
    current_criteria = result.criteria

    for item in files:
        target = staging_dir / item.path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(item.content, encoding="utf-8")
        candidate_criteria = evaluate_criteria(scan_repo(staging_dir))
        candidate_score = total_score(candidate_criteria)
        if candidate_score > current_score:
            accepted.append(item)
            current_score = candidate_score
            current_criteria = candidate_criteria
        else:
            target.unlink(missing_ok=True)
            rejected.append({"path": item.path, "reason": "修复提案未提升评分，已自动丢弃。"})

    for item in accepted:
        target = proposal_dir / item.path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(item.content, encoding="utf-8")

    before = {item.id: item.status for item in result.criteria}
    after = {item.id: item.status for item in current_criteria}
    fixed = [cid for cid in before if before[cid] != "pass" and after.get(cid) == "pass"]
    improved = [cid for cid in before if before[cid] != after.get(cid)]
    remaining = [cid for cid, state in after.items() if state in {"missing", "partial"}]

    patch_lines: list[str] = []
    for item in accepted:
        patch_lines.extend(
            difflib.unified_diff(
                [],
                item.content.splitlines(),
                fromfile="/dev/null",
                tofile=f"b/{item.path}",
                lineterm="",
            )
        )
    (out_dir / "remediation.patch").write_text("\n".join(patch_lines) + "\n", encoding="utf-8")

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "before_score": result.total_score,
        "after_score": current_score,
        "delta": round(current_score - result.total_score, 1),
        "accepted": bool(accepted),
        "generated_files": [{"path": item.path, "reason": item.reason} for item in accepted],
        "rejected_files": rejected,
        "fixed_criteria": fixed,
        "changed_criteria": improved,
        "remaining_gaps": remaining,
        "proposal_dir": str(proposal_dir),
        "staging_dir": str(staging_dir),
        "execution_probes": "Run the normal audit with --execute on a trusted staging copy if needed.",
        "original_fingerprint": original_fingerprint,
        "original_unchanged": tree_fingerprint(root) == original_fingerprint,
    }
    (out_dir / "autofix.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# ReproLens AutoFix Proposal",
        "",
        f"- Before score: **{result.total_score:.1f}**",
        f"- After score: **{current_score:.1f}**",
        f"- Estimated gain: **+{current_score - result.total_score:.1f}**",
        f"- Accepted: **{bool(accepted)}**",
        "",
        "## Generated Files",
        "",
        "| File | Reason |",
        "|---|---|",
    ]
    for item in accepted:
        lines.append(f"| `{item.path}` | {item.reason} |")
    if not accepted:
        lines.append("| - | No proposal improved the score; nothing was accepted. |")
    if rejected:
        lines.extend(["", "## Rejected Candidates", ""])
        for item in rejected:
            lines.append(f"- `{item['path']}`: {item['reason']}")
    lines.extend(["", "## Criteria Improved", ""])
    lines.extend(f"- `{cid}`" for cid in improved) if improved else lines.append("- None")
    lines.extend(["", "## Remaining Gaps", ""])
    lines.extend(f"- `{cid}`" for cid in remaining) if remaining else lines.append("- None")
    lines.extend(["", "## Review Note", "", "Generated templates with TODO fields are intentionally not treated as verified evidence. Candidates that reduce the audit score are automatically rejected."])
    (out_dir / "FIX_PROPOSAL.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_autofix_html(report, out_dir)
    return report
