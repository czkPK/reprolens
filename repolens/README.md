# ReproLens

Evidence-constrained reproduction readiness auditor for open-source LLM / RAG / Agent repositories.

## Simplest way to use it

### Analyze any public GitHub repository in the browser

1. Double-click `Start-ReproLens-Web.cmd`.
2. Paste a URL such as `https://github.com/huggingface/smolagents`.
3. Wait for the report to open.

The web runner pins the report to a commit SHA, uses a shallow clone with a GitHub archive fallback, and does not execute repository code.

### Analyze a local repository

1. Double-click `Start-ReproLens.cmd`.
2. Select the repository folder.
3. Wait for the audit to finish.
4. The HTML report opens automatically.

You do not need to set `PYTHONPATH` or type any command.

To try the built-in example, double-click `Run-Demo.cmd`.

## What it does

Given a local repository, ReproLens:

1. scans files and extracts reproduction evidence;
2. scores environment, data, model, experiment and documentation readiness;
3. adds LLM-specific checks: model/API version, prompt/template version, sampling parameters, tokenizer/context window, RAG index version, agent trace, evaluation contamination and inference cost;
4. runs a safe Python syntax probe by default; `--execute` enables `--help` and pytest collection probes on trusted repositories;
5. reports gaps with evidence IDs;
6. maps README claims to verification criteria and reports verified, partially verified and unverified claims;
7. assigns high/medium/low evidence confidence and reports evidence coverage;
8. proposes a minimal remediation plan and estimates the score gain;
9. with `--autofix`, generates a conservative fix proposal and re-audits a staging copy;
10. with `--explain`, generates an evidence-grounded explanation, with an offline deterministic fallback.

## Quick start

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
python -m repolens audit examples/demo-llm-app --out-dir reports/demo-llm-app --autofix --explain
python -m repolens.web --open
python -m repolens.benchmark
```

Outputs: `report.md`, `report.html`, `claims.md`, `claims.json`, `ai-review.json`, `score.json`, `badge.svg`, `badge.json`, `evidence.json`, `remediation.json`, `execution.json`, `explanation.md` when `--explain` is used, and `autofix/FIX_PROPOSAL.md` when `--autofix` is used.

Optional LLM environment variables: `REPROLENS_LLM_BASE_URL`, `REPROLENS_LLM_API_KEY`, `REPROLENS_LLM_MODEL`. With these variables, `--ai-review` performs evidence-constrained semantic claim mapping. Without them, the tool falls back to deterministic rules.

## AutoFix

AutoFix never modifies the original repository. It writes a proposal under `autofix/proposal/`, copies the repository to `autofix/staging/`, applies the proposal there, and re-runs the audit.

Generated templates containing `TODO`, `TBD` or `Not specified` remain partial or missing by design. They are not treated as verified evidence until a maintainer fills in project-specific facts.

Demo result:

```text
before: 49.1
after:  68.4
delta:  +19.3
```

## Benchmark

```powershell
python scripts/fetch_benchmark_repos.py --name mem0 --name haystack
python -m repolens.benchmark
```

The repository list is in `benchmark/repos.json`; labeled expectations are in `benchmark/cases.json`.

## 跨领域论文仓库验证

仓库提供 `benchmark/paper_repos.json`，覆盖自然语言处理、语音识别、医疗影像、多模态、具身智能、时间序列和计算机视觉等论文官方仓库。跨领域误报修复与真实运行结果见 `docs/跨领域泛化验证-2026-10-28.md`。

## GitHub Action

The repository root contains a reusable composite Action (`action.yml`). See `docs/GitHub-Action使用指南.md` for a workflow example. It audits the current repository, writes a concise Job Summary, outputs the score and badge path, and can upload the generated report as an artifact.

## Current MVP

- Python LLM/RAG/Agent repository scanning
- static evidence extraction
- applicability-aware criteria
- README claim-evidence matrix with gap tracing
- optional LLM-assisted semantic claim mapping with evidence-ID validation
- evidence confidence and coverage metrics
- web analysis for any public GitHub repository, pinned to commit SHA
- five general dimensions plus LLM-specific checks
- safe syntax probe + optional execution probes
- HTML and Markdown reports
- conservative AutoFix proposal + staging re-audit
- benchmark harness for fixture and real-repository cases
- deterministic offline mode

Execution probes run repository scripts only with `--execute`. Do not use that flag on untrusted code.
