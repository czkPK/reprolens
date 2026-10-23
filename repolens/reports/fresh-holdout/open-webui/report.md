# ReproLens Audit Report

- Repository: `C:\Users\86199\Documents\ChatGPT\全球校园人工智能算法精英大赛\repolens\benchmark\repos\open-webui`
- Generated at: `2026-10-23T14:41:18.162441+00:00`
- Files scanned: **5182**
- Overall score: **86.1 / 100**
- Readiness: **Ready**

## Dimension Scores

| Dimension | Points | Max | Percent |
|---|---:|---:|---:|
| 环境可复现 | 25.0 | 25.0 | 100.0% |
| 数据可复现 | 0.0 | 0.0 | 100.0% |
| 模型可复现 | 0.0 | 0.0 | 100.0% |
| 实验可复现 | 27.0 | 27.0 | 100.0% |
| 文档可复现 | 17.0 | 17.0 | 100.0% |
| LLM 特有风险 | 20.5 | 35.0 | 58.6% |

## Criteria

| ID | Dimension | Criterion | Status | Points | Evidence |
|---|---|---|---|---:|---|
| ENV-01 | 环境可复现 | 存在依赖清单 | PASS | 10.0/10.0 | E-002 |
| ENV-02 | 环境可复现 | 依赖版本锁定或容器化 | PASS | 8.0/8.0 | E-003, E-004 |
| ENV-03 | 环境可复现 | 提供安装步骤 | PASS | 7.0/7.0 | E-012 |
| DATA-01 | 数据可复现 | 说明数据来源和获取方式 | N/A | 0.0/8.0 | E-014 |
| DATA-02 | 数据可复现 | 提供数据下载或预处理脚本 | N/A | 0.0/8.0 | E-014 |
| DATA-03 | 数据可复现 | 提供数据集卡或数据许可说明 | N/A | 0.0/6.0 | E-005, E-014 |
| MODEL-01 | 模型可复现 | 提供模型权重、API 或获取方式 | N/A | 0.0/8.0 | E-011 |
| MODEL-02 | 模型可复现 | 提供模型卡或版本说明 | N/A | 0.0/8.0 | E-017, E-022 |
| MODEL-03 | 模型可复现 | 说明模型许可和来源 | N/A | 0.0/6.0 | E-005 |
| EXP-01 | 实验可复现 | 提供训练或主运行脚本 | PASS | 7.0/7.0 | E-013 |
| EXP-02 | 实验可复现 | 提供评测脚本或评测命令 | PASS | 8.0/8.0 | E-007, E-006 |
| EXP-03 | 实验可复现 | 设置并说明随机种子 | N/A | 0.0/6.0 | - |
| EXP-04 | 实验可复现 | 说明硬件或 API 环境要求 | PASS | 5.0/5.0 | E-016, E-021 |
| EXP-05 | 实验可复现 | 给出预期结果和指标 | PASS | 7.0/7.0 | E-015 |
| DOC-01 | 文档可复现 | 存在 README | PASS | 5.0/5.0 | E-001 |
| DOC-02 | 文档可复现 | 提供快速开始和运行示例 | PASS | 6.0/6.0 | E-012, E-013 |
| DOC-03 | 文档可复现 | 提供测试、CI 或一键复现脚本 | PASS | 6.0/6.0 | E-007, E-006, E-009 |
| LLM-01 | LLM 特有风险 | 记录模型/API 版本 | N/A | 0.0/6.0 | E-021, E-017, E-022 |
| LLM-02 | LLM 特有风险 | prompt/template 有版本记录 | PARTIAL | 3.0/6.0 | E-010, E-018 |
| LLM-03 | LLM 特有风险 | 记录采样参数 | PARTIAL | 2.5/5.0 | E-010 |
| LLM-04 | LLM 特有风险 | 记录 tokenizer/上下文窗口 | MISSING | 0.0/4.0 | - |
| LLM-05 | LLM 特有风险 | RAG 索引/知识库有版本记录 | PASS | 5.0/5.0 | E-024, E-023 |
| LLM-06 | LLM 特有风险 | Agent 工具调用轨迹可追溯 | PASS | 5.0/5.0 | E-026, E-025 |
| LLM-07 | LLM 特有风险 | 说明评测集、数据划分和污染风险 | PARTIAL | 3.0/6.0 | E-019 |
| LLM-08 | LLM 特有风险 | 说明推理成本或延迟 | PARTIAL | 2.0/4.0 | E-020, E-016, E-021 |

## Findings

### F-001 [MEDIUM] prompt/template 有版本记录

- Criterion: `LLM-02`
- Message: 有 prompt 文件或描述，但没有可核验的版本信息。
- Evidence: `E-010`, `E-018`

### F-002 [MEDIUM] 记录采样参数

- Criterion: `LLM-03`
- Message: 有采样参数或配置线索，但仍需补充可核验值。
- Evidence: `E-010`

### F-003 [MEDIUM] 记录 tokenizer/上下文窗口

- Criterion: `LLM-04`
- Message: 没有记录 tokenizer 或上下文窗口。
- Evidence: none

### F-004 [MEDIUM] 说明评测集、数据划分和污染风险

- Criterion: `LLM-07`
- Message: 只覆盖了评测集/划分/污染中的一部分，或仍有占位内容。
- Evidence: `E-019`

### F-005 [MEDIUM] 说明推理成本或延迟

- Criterion: `LLM-08`
- Message: 有成本/硬件线索，但仍需量化数据。
- Evidence: `E-020`, `E-016`, `E-021`

## Execution Evidence

| Probe | Status | Return code | Duration | Command |
|---|---|---:|---:|---|
| python-syntax | PASS | 0 | 0.837s | `C:\Program Files\Python313\python.exe -c import ast, pathlib, sys ignore={'.git','.venv','venv','node_modules','__pycache__','.mypy_cache','.pytest_cache','dist','build'} bad=[] fo` |

## Minimal Remediation Plan

### F-003 - 记录 tokenizer、上下文窗口和截断策略

- Rationale: 避免输入长度和分词差异导致结果变化。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+4.0**
- Evidence: none

### F-001 - 将 prompt/template 版本化并记录在配置或模型卡中

- Rationale: 避免 prompt 漂移导致结果不可复现。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+3.0**
- Evidence: `E-010`, `E-018`

### F-004 - 说明评测集、数据划分和污染/泄漏风险

- Rationale: 让指标具有可比性，避免高估效果。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+3.0**
- Evidence: `E-019`

### F-002 - 记录 temperature、top_p、max_tokens 等采样参数

- Rationale: 让生成行为可以复现和比较。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+2.5**
- Evidence: `E-010`

### F-005 - 说明推理成本、延迟和 token 消耗

- Rationale: 让读者评估复现成本。
- Cost: **low**
- Impact: **low**
- Estimated score gain: **+2.0**
- Evidence: `E-020`, `E-016`, `E-021`

## Evidence Appendix

- `E-001` [readme] `README.md:1` — # Open WebUI 👋
- `E-002` [dependency-manifest] `package.json:1` — {
- `E-003` [lockfile] `package-lock.json` — package-lock.json
- `E-004` [container] `docker-compose.yaml:1` — services:
- `E-005` [license] `LICENSE:1` — Open WebUI License
- `E-006` [ci] `.github/workflows/backend.yaml:1` — # ─────────────────────────────────────────────────────────────────────────────
- `E-007` [tests] `src/lib/components/workspace/common/versionDiff.test.ts:1` — import { describe, expect, it } from 'vitest';
- `E-008` [script] `backend/open_webui/routers/evaluations.py:1` — import logging
- `E-009` [script] `Makefile:1` — ifneq ($(shell which docker-compose 2>/dev/null),)
- `E-010` [prompt] `src/routes/(app)/workspace/prompts/+page.svelte` — +page.svelte
- `E-011` [weights] `test/test_files/image_gen/sd-empty.pt` — sd-empty.pt
- `E-012` [instruction] `README.md:118` — pip install
- `E-013` [instruction] `README.md:136` — make sure to include the `-v open-webui:/app/backend/data` in your Docker command. This step is crucial as it ensures your database is properly mounted and prevents any loss of data.
- `E-014` [data] `README.md:3` — https://
- `E-015` [metric] `backend/open_webui/retrieval/loaders/main.py:644` — expected
- `E-016` [hardware] `README.md:26` — cuda
- `E-017` [model] `README.md:54` — Transformers
- `E-018` [prompt] `README.md:48` — prompt
- `E-019` [evaluation] `backend/open_webui/main.py:1180` — split
- `E-020` [cost] `README.md:68` — cost
- `E-021` [llm-provider] `README.md:13` — Ollama
- `E-022` [model] `README.md:13` — llama
- `E-023` [rag] `README.md:58` — RAG
- `E-024` [rag] `backend/open_webui/main.py:708` — embedding_model
- `E-025` [agent] `README.md:32` — MCP
- `E-026` [agent] `backend/open_webui/main.py:241` — session_id

## Scope and Limitations

- This is static reproduction readiness analysis, not proof that the project reproduces successfully.
- No untrusted repository code is executed by default.
- Execution probes and GitHub Action integration are planned next.
- AI-generated explanations must be reviewed by the team before submission or release.
