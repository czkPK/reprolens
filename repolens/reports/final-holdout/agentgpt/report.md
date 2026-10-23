# ReproLens Audit Report

- Repository: `C:\Users\86199\Documents\ChatGPT\全球校园人工智能算法精英大赛\repolens\benchmark\repos\agentgpt`
- Generated at: `2026-10-23T14:56:38.864011+00:00`
- Files scanned: **571**
- Overall score: **63.9 / 100**
- Readiness: **At Risk**

## Dimension Scores

| Dimension | Points | Max | Percent |
|---|---:|---:|---:|
| 环境可复现 | 21.5 | 25.0 | 86.0% |
| 数据可复现 | 19.0 | 22.0 | 86.4% |
| 模型可复现 | 11.0 | 22.0 | 50.0% |
| 实验可复现 | 20.0 | 33.0 | 60.6% |
| 文档可复现 | 14.0 | 17.0 | 82.4% |
| LLM 特有风险 | 13.5 | 36.0 | 37.5% |

## Criteria

| ID | Dimension | Criterion | Status | Points | Evidence |
|---|---|---|---|---:|---|
| ENV-01 | 环境可复现 | 存在依赖清单 | PASS | 10.0/10.0 | E-002 |
| ENV-02 | 环境可复现 | 依赖版本锁定或容器化 | PASS | 8.0/8.0 | E-003, E-004 |
| ENV-03 | 环境可复现 | 提供安装步骤 | PARTIAL | 3.5/7.0 | E-001 |
| DATA-01 | 数据可复现 | 说明数据来源和获取方式 | PASS | 8.0/8.0 | E-011, E-008 |
| DATA-02 | 数据可复现 | 提供数据下载或预处理脚本 | PASS | 8.0/8.0 | E-008 |
| DATA-03 | 数据可复现 | 提供数据集卡或数据许可说明 | PARTIAL | 3.0/6.0 | E-005, E-011 |
| MODEL-01 | 模型可复现 | 提供模型权重、API 或获取方式 | PARTIAL | 4.0/8.0 | E-014 |
| MODEL-02 | 模型可复现 | 提供模型卡或版本说明 | PARTIAL | 4.0/8.0 | E-014 |
| MODEL-03 | 模型可复现 | 说明模型许可和来源 | PARTIAL | 3.0/6.0 | E-005 |
| EXP-01 | 实验可复现 | 提供训练或主运行脚本 | PASS | 7.0/7.0 | E-010 |
| EXP-02 | 实验可复现 | 提供评测脚本或评测命令 | PASS | 8.0/8.0 | E-007, E-006 |
| EXP-03 | 实验可复现 | 设置并说明随机种子 | MISSING | 0.0/6.0 | - |
| EXP-04 | 实验可复现 | 说明硬件或 API 环境要求 | PASS | 5.0/5.0 | E-014 |
| EXP-05 | 实验可复现 | 给出预期结果和指标 | MISSING | 0.0/7.0 | - |
| DOC-01 | 文档可复现 | 存在 README | PASS | 5.0/5.0 | E-001 |
| DOC-02 | 文档可复现 | 提供快速开始和运行示例 | PARTIAL | 3.0/6.0 | E-010 |
| DOC-03 | 文档可复现 | 提供测试、CI 或一键复现脚本 | PASS | 6.0/6.0 | E-007, E-006, E-009 |
| LLM-01 | LLM 特有风险 | 记录模型/API 版本 | PARTIAL | 3.0/6.0 | E-014 |
| LLM-02 | LLM 特有风险 | prompt/template 有版本记录 | PARTIAL | 3.0/6.0 | E-012 |
| LLM-03 | LLM 特有风险 | 记录采样参数 | MISSING | 0.0/5.0 | - |
| LLM-04 | LLM 特有风险 | 记录 tokenizer/上下文窗口 | MISSING | 0.0/4.0 | - |
| LLM-05 | LLM 特有风险 | RAG 索引/知识库有版本记录 | N/A | 0.0/5.0 | - |
| LLM-06 | LLM 特有风险 | Agent 工具调用轨迹可追溯 | PARTIAL | 2.5/5.0 | E-015 |
| LLM-07 | LLM 特有风险 | 说明评测集、数据划分和污染风险 | PARTIAL | 3.0/6.0 | E-013 |
| LLM-08 | LLM 特有风险 | 说明推理成本或延迟 | PARTIAL | 2.0/4.0 | E-014 |

## Findings

### F-001 [MEDIUM] 提供安装步骤

- Criterion: `ENV-03`
- Message: 有 README，但没有明显安装命令。
- Evidence: `E-001`

### F-002 [MEDIUM] 提供数据集卡或数据许可说明

- Criterion: `DATA-03`
- Message: 有许可证和数据说明，但没有独立数据集卡。
- Evidence: `E-005`, `E-011`

### F-003 [MEDIUM] 提供模型权重、API 或获取方式

- Criterion: `MODEL-01`
- Message: 有模型说明，但没有发现权重、下载地址或明确 API 模型版本。
- Evidence: `E-014`

### F-004 [MEDIUM] 提供模型卡或版本说明

- Criterion: `MODEL-02`
- Message: 有模型卡、版本或提供方信息，但仍需补充完整。
- Evidence: `E-014`

### F-005 [MEDIUM] 说明模型许可和来源

- Criterion: `MODEL-03`
- Message: 有许可证或模型卡，但模型专用许可和来源仍需补充。
- Evidence: `E-005`

### F-006 [MEDIUM] 设置并说明随机种子

- Criterion: `EXP-03`
- Message: 没有随机种子或确定性设置。
- Evidence: none

### F-007 [HIGH] 给出预期结果和指标

- Criterion: `EXP-05`
- Message: 没有预期结果或指标。
- Evidence: none

### F-008 [MEDIUM] 提供快速开始和运行示例

- Criterion: `DOC-02`
- Message: 只有安装或运行说明中的一项。
- Evidence: `E-010`

### F-009 [MEDIUM] 记录模型/API 版本

- Criterion: `LLM-01`
- Message: 只记录了模型提供方/版本，或仍有待补充字段。
- Evidence: `E-014`

### F-010 [MEDIUM] prompt/template 有版本记录

- Criterion: `LLM-02`
- Message: 有 prompt 文件或描述，但没有可核验的版本信息。
- Evidence: `E-012`

### F-011 [MEDIUM] 记录采样参数

- Criterion: `LLM-03`
- Message: 没有记录 temperature、top_p 等采样参数。
- Evidence: none

### F-012 [MEDIUM] 记录 tokenizer/上下文窗口

- Criterion: `LLM-04`
- Message: 没有记录 tokenizer 或上下文窗口。
- Evidence: none

### F-013 [MEDIUM] Agent 工具调用轨迹可追溯

- Criterion: `LLM-06`
- Message: 检测到 Agent 项目，但完整调用轨迹仍需补充。
- Evidence: `E-015`

### F-014 [MEDIUM] 说明评测集、数据划分和污染风险

- Criterion: `LLM-07`
- Message: 只覆盖了评测集/划分/污染中的一部分，或仍有占位内容。
- Evidence: `E-013`

### F-015 [MEDIUM] 说明推理成本或延迟

- Criterion: `LLM-08`
- Message: 有成本/硬件线索，但仍需量化数据。
- Evidence: `E-014`

## Execution Evidence

| Probe | Status | Return code | Duration | Command |
|---|---|---:|---:|---|
| python-syntax | PASS | 0 | 0.118s | `C:\Program Files\Python313\python.exe -c import ast, pathlib, sys ignore={'.git','.venv','venv','node_modules','__pycache__','.mypy_cache','.pytest_cache','dist','build'} bad=[] fo` |

## Minimal Remediation Plan

### F-007 - 补充预期指标、日志样例和可接受误差范围

- Rationale: 让读者知道结果是否正确。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+7.0**
- Evidence: none

### F-006 - 固定并记录随机种子、框架确定性和硬件差异

- Rationale: 降低结果不可重复的随机性。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+6.0**
- Evidence: none

### F-011 - 记录 temperature、top_p、max_tokens 等采样参数

- Rationale: 让生成行为可以复现和比较。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+5.0**
- Evidence: none

### F-004 - 添加模型卡，记录模型版本、结构、超参数和训练数据

- Rationale: 让模型行为可追溯。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+4.0**
- Evidence: `E-014`

### F-012 - 记录 tokenizer、上下文窗口和截断策略

- Rationale: 避免输入长度和分词差异导致结果变化。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+4.0**
- Evidence: none

### F-003 - 提供模型权重下载地址或权重大小、文件名说明

- Rationale: 让读者能够获得与结果对应的模型。
- Cost: **medium**
- Impact: **high**
- Estimated score gain: **+4.0**
- Evidence: `E-014`

### F-001 - 在 README 中增加可复制的安装命令

- Rationale: 降低首次运行门槛。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+3.5**
- Evidence: `E-001`

### F-002 - 添加数据集卡或数据许可说明

- Rationale: 明确数据边界和再分发条件。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+3.0**
- Evidence: `E-005`, `E-011`

### F-005 - 在模型卡中说明模型许可和来源

- Rationale: 避免模型使用和再分发风险。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+3.0**
- Evidence: `E-005`

### F-008 - 添加快速开始和最小运行示例

- Rationale: 让新用户可以在几分钟内跑通。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+3.0**
- Evidence: `E-010`

### F-009 - 记录模型提供方、模型 ID 和 API 版本

- Rationale: 避免模型漂移导致输出不可复现。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+3.0**
- Evidence: `E-014`

### F-010 - 将 prompt/template 版本化并记录在配置或模型卡中

- Rationale: 避免 prompt 漂移导致结果不可复现。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+3.0**
- Evidence: `E-012`

### F-014 - 说明评测集、数据划分和污染/泄漏风险

- Rationale: 让指标具有可比性，避免高估效果。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+3.0**
- Evidence: `E-013`

### F-013 - 保存 Agent 工具调用轨迹、run_id 和关键日志

- Rationale: 让多步调用过程可以审计。
- Cost: **medium**
- Impact: **high**
- Estimated score gain: **+2.5**
- Evidence: `E-015`

### F-015 - 说明推理成本、延迟和 token 消耗

- Rationale: 让读者评估复现成本。
- Cost: **low**
- Impact: **low**
- Estimated score gain: **+2.0**
- Evidence: `E-014`

## Evidence Appendix

- `E-001` [readme] `README.md:1` — <p align="center">
- `E-002` [dependency-manifest] `cli/package.json:1` — {
- `E-003` [lockfile] `cli/package-lock.json:1` — {
- `E-004` [container] `docker-compose.yml:1` — version: '3.9'
- `E-005` [license] `LICENSE:1` — GNU GENERAL PUBLIC LICENSE
- `E-006` [ci] `.github/workflows/node.js.yml:1` — name: Node.js CI
- `E-007` [tests] `platform/reworkd_platform/tests/test_dependancies.py:1` — import pytest
- `E-008` [script] `scripts/prepare-sync.sh:1` — cd "$(dirname "$0")" || exit 1
- `E-009` [script] `setup.sh:1` — #!/usr/bin/env bash
- `E-010` [instruction] `README.md:47` — make sure you have the following installed:
- `E-011` [data] `README.md:2` — https://
- `E-012` [prompt] `README.md:84` — template
- `E-013` [evaluation] `README.md:90` — Validation
- `E-014` [llm-provider] `README.md:53` — OpenAI
- `E-015` [agent] `README.md:5` — Agent

## Scope and Limitations

- This is static reproduction readiness analysis, not proof that the project reproduces successfully.
- No untrusted repository code is executed by default.
- Execution probes and GitHub Action integration are planned next.
- AI-generated explanations must be reviewed by the team before submission or release.
