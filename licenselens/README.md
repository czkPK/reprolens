# LicenseLens

Evidence-constrained open-source license conflict diagnosis and remediation planner.

## Quick start

```powershell
$env:PYTHONPATH = "src"
python -m licenselens analyze examples/demo-saas --usage saas --project-license MIT --out-dir reports/demo-saas
```

Outputs: `report.md`, `analysis.json`, `graph.json`, `remediation.json`, `notice.md`.

## Current MVP scope

- Python `requirements.txt` and `pyproject.toml`
- npm `package.json` and `package-lock.json` license hints
- local `licenses.json` overrides
- usage-aware conflict rules
- evidence IDs and remediation actions
- deterministic offline mode

The LLM adapter and evaluation harness are the next implementation slice.
