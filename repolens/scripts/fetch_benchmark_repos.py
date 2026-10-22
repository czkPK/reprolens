from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path


def codeload_url(repo_url: str, branch: str) -> str:
    parsed = urllib.parse.urlparse(repo_url)
    path = parsed.path.strip("/")
    if path.endswith(".git"):
        path = path[:-4]
    return f"https://codeload.github.com/{path}/zip/refs/heads/{branch}"


def download_zip(repo_url: str, target: Path) -> bool:
    target.parent.mkdir(parents=True, exist_ok=True)
    for branch in ("main", "master"):
        url = codeload_url(repo_url, branch)
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "ReproLens benchmark fetcher"})
            with urllib.request.urlopen(request, timeout=120) as response:
                payload = response.read()
            with tempfile.TemporaryDirectory() as tmp:
                archive = Path(tmp) / "repo.zip"
                archive.write_bytes(payload)
                extract_root = Path(tmp) / "extract"
                with zipfile.ZipFile(archive) as zf:
                    zf.extractall(extract_root)
                children = [p for p in extract_root.iterdir() if p.is_dir()]
                if not children:
                    raise RuntimeError("zip has no top-level directory")
                if target.exists():
                    shutil.rmtree(target)
                shutil.move(str(children[0]), str(target))
            print(f"downloaded {repo_url} ({branch})")
            return True
        except Exception as exc:
            print(f"zip fallback failed for {url}: {exc}")
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch public benchmark repositories.")
    parser.add_argument("--name", action="append", help="Only fetch the named repository. Can be repeated.")
    parser.add_argument("--method", choices=("auto", "git", "zip"), default="auto")
    args = parser.parse_args()

    base = Path(__file__).resolve().parents[1]
    repos = json.loads((base / "benchmark" / "repos.json").read_text(encoding="utf-8"))
    if args.name:
        wanted = set(args.name)
        repos = [item for item in repos if item["name"] in wanted]

    target_root = base / "benchmark" / "repos"
    target_root.mkdir(parents=True, exist_ok=True)

    for item in repos:
        target = target_root / item["name"]
        if target.exists() and any(target.iterdir()):
            print(f"skip {item['name']}: already exists")
            continue
        success = False
        if args.method in {"auto", "git"}:
            command = ["git", "clone", "--depth", "1", "--single-branch", item["url"], str(target)]
            print("run", " ".join(command))
            result = subprocess.run(command, check=False)
            success = result.returncode == 0
        if not success and args.method in {"auto", "zip"}:
            success = download_zip(item["url"], target)
        if not success:
            print(f"failed {item['name']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
