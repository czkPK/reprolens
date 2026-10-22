# ReproLens

Evidence-constrained reproduction readiness auditor for open-source LLM / RAG / Agent repositories.

## What it does

Given a local repository, ReproLens:

1. scans files and extracts reproduction evidence;
2. scores environment, data, model, experiment and documentation readiness;
3. adds LLM-specific checks: model/API version, prompt/template version, sampling parameters, tokenizer/context window, RAG index version, agent trace, evaluation contamination and inference cost;
4. runs a safe Python syntax probe by default; `--execute` enables `--help` and pytest collection probes on trusted repositories;
5. reports gaps with evidence IDs;
6. proposes a minimal remediation plan and estimates the score gain;
7. with `--autofix`, generates a conservative fix proposal and re-audits a staging copy.

## Quick start

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
python -m repolens audit examples/demo-llm-app --out-dir reports/demo-llm-app --autofix
python -m repolens.benchmark
```

Outputs: `report.md`, `report.html`, `score.json`, `evidence.json`, `remediation.json`, `execution.json`, and `autofix/FIX_PROPOSAL.md` when `--autofix` is used.

## AutoFix

AutoFix never modifies the original repository. It writes a proposal under `autofix/proposal/`, copies the repository to `autofix/staging/`, applies the proposal there, and re-runs the audit.

Generated templates containing `TODO`, `TBD` or `Not specified` remain partial or missing by design. They are not treated as verified evidence until a maintainer fills in project-specific facts.

Demo result:

```text
before: 49.1
after:  63.4
delta:  +14.3
```

## Benchmark

```powershell
python scripts/fetch_benchmark_repos.py --name mem0 --name haystack
python -m repolens.benchmark
```

The repository list is in `benchmark/repos.json`; labeled expectations are in `benchmark/cases.json`.

## GitHub Action

See `.github/workflows/repolens.yml`. It audits the repository and uploads the report as an artifact.

## Current MVP

- Python LLM/RAG/Agent repository scanning
- static evidence extraction
- applicability-aware criteria
- five general dimensions plus LLM-specific checks
- safe syntax probe + optional execution probes
- HTML and Markdown reports
- conservative AutoFix proposal + staging re-audit
- benchmark harness for fixture and real-repository cases
- deterministic offline mode

Execution probes run repository scripts only with `--execute`. Do not use that flag on untrusted code.
