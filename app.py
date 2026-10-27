from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from repolens.web import run_remote_audit  # noqa: E402
from vercel_ui import LANDING_HTML  # noqa: E402

app = FastAPI(title="ReproLens", docs_url=None, redoc_url=None)


class AuditRequest(BaseModel):
    url: str = Field(min_length=1, max_length=500)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


@app.get("/", response_class=HTMLResponse)
def home() -> HTMLResponse:
    return HTMLResponse(LANDING_HTML)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/audit")
def audit(payload: AuditRequest) -> dict:
    temp_root = Path(tempfile.mkdtemp(prefix="repolens-vercel-"))
    try:
        summary = run_remote_audit(payload.url, temp_root, autofix=True)
        run_dir = temp_root / summary["run_id"]
        files = {
            "report.html": _read_text(run_dir / "report.html"),
            "claims.html": _read_text(run_dir / "claims.html"),
            "autofix.html": _read_text(run_dir / "autofix.html"),
            "score.json": _read_text(run_dir / "score.json"),
        }
        autofix_files: dict[str, str] = {}
        autofix_root = run_dir / "autofix"
        if autofix_root.is_dir():
            for path in sorted(autofix_root.rglob("*")):
                if not path.is_file() or "staging" in path.relative_to(autofix_root).parts:
                    continue
                key = path.relative_to(run_dir).as_posix()
                autofix_files[key] = _read_text(path)
        return {
            "summary": summary,
            "report_html": files["report.html"],
            "claims_html": files["claims.html"],
            "autofix_html": files["autofix.html"],
            "score_json": files["score.json"],
            "autofix_files": autofix_files,
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except subprocess.TimeoutExpired as exc:
        raise HTTPException(status_code=504, detail="仓库获取超时，请稍后重试或换一个较小的仓库。") from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)[:500]) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"分析失败：{str(exc)[:400]}") from exc
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)
