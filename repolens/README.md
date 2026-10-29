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

### Local semantic model and optional LLM

ReproLens includes `ReproLens-SmallSemantic-v1`, a local open-source semantic classifier for mapping README claims to the fixed audit criteria. It runs offline with no API key and is the default semantic mode.

`REPROLENS_SEMANTIC_MODE` selects the semantic backend:

- `local` (default): use the bundled local semantic model;
- `llm`: use an optional OpenAI-compatible model API;
- `off`: disable semantic enhancement and use deterministic rules only.

The optional external LLM backend uses `REPROLENS_LLM_BASE_URL`, `REPROLENS_LLM_API_KEY`, and `REPROLENS_LLM_MODEL`. The external model is never allowed to invent evidence IDs or directly determine the final score.

Model card: `repolens/docs/ReproLens-SmallSemantic-v1模型卡.md`.

## AutoFix

AutoFix never modifies the original repository. It writes a proposal under `autofix/proposal/`, copies the repository to `autofix/staging/`, applies the proposal there, and re-runs the audit.

Generated templates containing `TODO`, `TBD` or `Not specified` remain partial or missing by design. They are not treated as verified evidence until a maintainer fills in project-specific facts.

Demo result:

```text
before: 49.1
after:  68.4
delta:  +19.3
```

## Webhook 与群机器人

`score.json` 可以被外部自动化程序直接读取。内置消费器支持通用 JSON、飞书自定义机器人和钉钉自定义机器人：

```powershell
# 通用 Webhook
python -m repolens.integrations score.json --min-score 65 --webhook-url "<接收地址>"

# 飞书自定义机器人（安全设置建议使用关键词：ReproLens）
python -m repolens.integrations score.json --min-score 65 --format feishu --webhook-url "<飞书机器人地址>"

# 钉钉自定义机器人（安全设置建议使用关键词：ReproLens）
python -m repolens.integrations score.json --min-score 65 --format dingtalk --webhook-url "<钉钉机器人地址>"

# 钉钉加签模式（可选）
python -m repolens.integrations score.json --min-score 65 --format dingtalk --webhook-url "<钉钉机器人地址>" --webhook-secret "<签名密钥>"
```

当分数低于 `--min-score` 时，命令返回退出码 `1`，可直接作为 CI 质量门禁。Webhook URL 和签名密钥属于敏感配置，不应提交到仓库。

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

- Python-first AI/ML research repository scanning, including LLM/RAG/Agent projects; non-Python and model-agnostic SDK projects may yield N/A for some criteria.
- static evidence extraction
- applicability-aware criteria
- README claim-evidence matrix with gap tracing
- bundled local semantic model with no API dependency
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
