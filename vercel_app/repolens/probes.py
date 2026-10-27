from __future__ import annotations

import shutil
import subprocess
import sys
import time
from pathlib import Path

from .models import ProbeResult


_IGNORE = {".git", ".venv", "venv", "node_modules", "__pycache__", ".mypy_cache", ".pytest_cache", "dist", "build"}


def _run(name: str, command: list[str], root: Path, timeout: int) -> ProbeResult:
    start = time.perf_counter()
    try:
        completed = subprocess.run(
            command,
            cwd=root,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        duration = round(time.perf_counter() - start, 3)
        status = "pass" if completed.returncode == 0 else "fail"
        return ProbeResult(
            name=name,
            command=" ".join(command),
            status=status,
            returncode=completed.returncode,
            duration_seconds=duration,
            stdout=(completed.stdout or "")[:4000],
            stderr=(completed.stderr or "")[:4000],
        )
    except subprocess.TimeoutExpired as exc:
        duration = round(time.perf_counter() - start, 3)
        return ProbeResult(
            name=name,
            command=" ".join(command),
            status="timeout",
            returncode=None,
            duration_seconds=duration,
            stdout=(exc.stdout or "")[:4000] if isinstance(exc.stdout, str) else "",
            stderr=(exc.stderr or "")[:4000] if isinstance(exc.stderr, str) else "",
        )
    except OSError as exc:
        duration = round(time.perf_counter() - start, 3)
        return ProbeResult(
            name=name,
            command=" ".join(command),
            status="error",
            returncode=None,
            duration_seconds=duration,
            stdout="",
            stderr=str(exc)[:4000],
        )


def _syntax_script() -> str:
    return (
        "import ast, pathlib, sys\n"
        "ignore={'.git','.venv','venv','node_modules','__pycache__','.mypy_cache','.pytest_cache','dist','build'}\n"
        "bad=[]\n"
        "for p in pathlib.Path('.').rglob('*.py'):\n"
        "    if any(part in ignore for part in p.parts): continue\n"
        "    try: ast.parse(p.read_text(encoding='utf-8', errors='ignore'))\n"
        "    except Exception as e: bad.append(f'{p}: {e}')\n"
        "print('\\n'.join(bad))\n"
        "sys.exit(1 if bad else 0)\n"
    )


def run_probes(root: Path, execute: bool = False) -> list[ProbeResult]:
    """Run safe static probes by default; execute repository scripts only when explicitly enabled."""
    probes: list[ProbeResult] = []
    probes.append(_run("python-syntax", [sys.executable, "-c", _syntax_script()], root, 30))

    if not execute:
        return probes

    scripts: list[Path] = []
    for pattern in ("train*.py", "finetune*.py", "eval*.py", "evaluate*.py", "infer*.py", "predict*.py", "app.py"):
        for path in root.rglob(pattern):
            if path.is_file() and not any(part in _IGNORE for part in path.parts):
                scripts.append(path)
                break
        if len(scripts) >= 2:
            break

    for script in scripts[:2]:
        rel = script.relative_to(root).as_posix()
        probes.append(_run(f"help:{rel}", [sys.executable, str(script), "--help"], root, 20))

    pytest_path = shutil.which("pytest")
    if pytest_path:
        probes.append(_run("pytest-collect", [pytest_path, "--collect-only", "-q"], root, 30))

    return probes
