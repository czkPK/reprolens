# ReproLens Audit Report

- Repository: `C:\Users\86199\Documents\ChatGPT\全球校园人工智能算法精英大赛\repolens\benchmark\repos\chat-ui`
- Generated at: `2026-10-22T14:42:07.426179+00:00`
- Files scanned: **995**
- Overall score: **44.1 / 100**
- Readiness: **At Risk**

## Dimension Scores

| Dimension | Points | Max | Percent |
|---|---:|---:|---:|
| 环境可复现 | 11.5 | 25.0 | 46.0% |
| 数据可复现 | 11.0 | 22.0 | 50.0% |
| 模型可复现 | 19.0 | 22.0 | 86.4% |
| 实验可复现 | 5.0 | 33.0 | 15.2% |
| 文档可复现 | 8.0 | 17.0 | 47.1% |
| LLM 特有风险 | 16.0 | 41.0 | 39.0% |

## Criteria

| ID | Dimension | Criterion | Status | Points | Evidence |
|---|---|---|---|---:|---|
| ENV-01 | 环境可复现 | 存在依赖清单 | MISSING | 0.0/10.0 | - |
| ENV-02 | 环境可复现 | 依赖版本锁定或容器化 | PASS | 8.0/8.0 | E-002, E-003 |
| ENV-03 | 环境可复现 | 提供安装步骤 | PARTIAL | 3.5/7.0 | E-001 |
| DATA-01 | 数据可复现 | 说明数据来源和获取方式 | PARTIAL | 4.0/8.0 | E-007 |
| DATA-02 | 数据可复现 | 提供数据下载或预处理脚本 | PARTIAL | 4.0/8.0 | E-007 |
| DATA-03 | 数据可复现 | 提供数据集卡或数据许可说明 | PARTIAL | 3.0/6.0 | E-004, E-007 |
| MODEL-01 | 模型可复现 | 提供模型权重、API 或获取方式 | PASS | 8.0/8.0 | E-010, E-008, E-011 |
| MODEL-02 | 模型可复现 | 提供模型卡或版本说明 | PASS | 8.0/8.0 | E-008, E-011 |
| MODEL-03 | 模型可复现 | 说明模型许可和来源 | PARTIAL | 3.0/6.0 | E-004 |
| EXP-01 | 实验可复现 | 提供训练或主运行脚本 | MISSING | 0.0/7.0 | - |
| EXP-02 | 实验可复现 | 提供评测脚本或评测命令 | MISSING | 0.0/8.0 | - |
| EXP-03 | 实验可复现 | 设置并说明随机种子 | MISSING | 0.0/6.0 | - |
| EXP-04 | 实验可复现 | 说明硬件或 API 环境要求 | PASS | 5.0/5.0 | E-010 |
| EXP-05 | 实验可复现 | 给出预期结果和指标 | MISSING | 0.0/7.0 | - |
| DOC-01 | 文档可复现 | 存在 README | PASS | 5.0/5.0 | E-001 |
| DOC-02 | 文档可复现 | 提供快速开始和运行示例 | MISSING | 0.0/6.0 | - |
| DOC-03 | 文档可复现 | 提供测试、CI 或一键复现脚本 | PARTIAL | 3.0/6.0 | E-005 |
| LLM-01 | LLM 特有风险 | 记录模型/API 版本 | PASS | 6.0/6.0 | E-010, E-008, E-011 |
| LLM-02 | LLM 特有风险 | prompt/template 有版本记录 | PARTIAL | 3.0/6.0 | E-006, E-009 |
| LLM-03 | LLM 特有风险 | 记录采样参数 | MISSING | 0.0/5.0 | E-006 |
| LLM-04 | LLM 特有风险 | 记录 tokenizer/上下文窗口 | MISSING | 0.0/4.0 | - |
| LLM-05 | LLM 特有风险 | RAG 索引/知识库有版本记录 | PARTIAL | 2.5/5.0 | E-012 |
| LLM-06 | LLM 特有风险 | Agent 工具调用轨迹可追溯 | PARTIAL | 2.5/5.0 | E-013 |
| LLM-07 | LLM 特有风险 | 说明评测集、数据划分和污染风险 | MISSING | 0.0/6.0 | - |
| LLM-08 | LLM 特有风险 | 说明推理成本或延迟 | PARTIAL | 2.0/4.0 | E-010 |

## Findings

### F-001 [HIGH] 存在依赖清单

- Criterion: `ENV-01`
- Message: 依赖清单是复现的第一入口。
- Evidence: none

### F-002 [MEDIUM] 提供安装步骤

- Criterion: `ENV-03`
- Message: 有 README，但没有明显安装命令。
- Evidence: `E-001`

### F-003 [MEDIUM] 说明数据来源和获取方式

- Criterion: `DATA-01`
- Message: 提到了数据，但缺少可执行的获取或处理说明。
- Evidence: `E-007`

### F-004 [MEDIUM] 提供数据下载或预处理脚本

- Criterion: `DATA-02`
- Message: 有数据说明，但没有下载/预处理脚本。
- Evidence: `E-007`

### F-005 [MEDIUM] 提供数据集卡或数据许可说明

- Criterion: `DATA-03`
- Message: 有许可证和数据说明，但没有独立数据集卡。
- Evidence: `E-004`, `E-007`

### F-006 [MEDIUM] 说明模型许可和来源

- Criterion: `MODEL-03`
- Message: 有许可证或模型卡，但模型专用许可和来源仍需补充。
- Evidence: `E-004`

### F-007 [HIGH] 提供训练或主运行脚本

- Criterion: `EXP-01`
- Message: 没有训练脚本或主运行命令。
- Evidence: none

### F-008 [HIGH] 提供评测脚本或评测命令

- Criterion: `EXP-02`
- Message: 没有评测脚本或评测命令。
- Evidence: none

### F-009 [MEDIUM] 设置并说明随机种子

- Criterion: `EXP-03`
- Message: 没有随机种子或确定性设置。
- Evidence: none

### F-010 [HIGH] 给出预期结果和指标

- Criterion: `EXP-05`
- Message: 没有预期结果或指标。
- Evidence: none

### F-011 [MEDIUM] 提供快速开始和运行示例

- Criterion: `DOC-02`
- Message: 没有快速开始或运行示例。
- Evidence: none

### F-012 [MEDIUM] 提供测试、CI 或一键复现脚本

- Criterion: `DOC-03`
- Message: 只有测试、CI 或一键复现脚本中的一项。
- Evidence: `E-005`

### F-013 [MEDIUM] prompt/template 有版本记录

- Criterion: `LLM-02`
- Message: 有 prompt 文件或描述，但没有可核验的版本信息。
- Evidence: `E-006`, `E-009`

### F-014 [MEDIUM] 记录采样参数

- Criterion: `LLM-03`
- Message: 没有记录 temperature、top_p 等采样参数。
- Evidence: `E-006`

### F-015 [MEDIUM] 记录 tokenizer/上下文窗口

- Criterion: `LLM-04`
- Message: 没有记录 tokenizer 或上下文窗口。
- Evidence: none

### F-016 [MEDIUM] RAG 索引/知识库有版本记录

- Criterion: `LLM-05`
- Message: 检测到 RAG 项目，但索引/embedding 版本仍需补充。
- Evidence: `E-012`

### F-017 [MEDIUM] Agent 工具调用轨迹可追溯

- Criterion: `LLM-06`
- Message: 检测到 Agent 项目，但调用轨迹仍需补充。
- Evidence: `E-013`

### F-018 [MEDIUM] 说明评测集、数据划分和污染风险

- Criterion: `LLM-07`
- Message: 没有说明评测集、数据划分或污染风险。
- Evidence: none

### F-019 [MEDIUM] 说明推理成本或延迟

- Criterion: `LLM-08`
- Message: 有成本/硬件线索，但仍需量化数据。
- Evidence: `E-010`

## Execution Evidence

| Probe | Status | Return code | Duration | Command |
|---|---|---:|---:|---|
| python-syntax | PASS | 0 | 0.082s | `C:\Program Files\Python313\python.exe -c import ast, pathlib, sys ignore={'.git','.venv','venv','node_modules','__pycache__','.mypy_cache','.pytest_cache','dist','build'} bad=[] fo` |

## Minimal Remediation Plan

### F-001 - 补充 requirements.txt / pyproject.toml / environment.yml

- Rationale: 让读者知道项目需要哪些依赖。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+10.0**
- Evidence: none

### F-008 - 添加评测脚本、评测命令和指标计算方式

- Rationale: 让结果可以被独立验证。
- Cost: **medium**
- Impact: **high**
- Estimated score gain: **+8.0**
- Evidence: none

### F-010 - 补充预期指标、日志样例和可接受误差范围

- Rationale: 让读者知道结果是否正确。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+7.0**
- Evidence: none

### F-007 - 添加训练脚本或明确训练命令

- Rationale: 让训练过程可执行。
- Cost: **medium**
- Impact: **high**
- Estimated score gain: **+7.0**
- Evidence: none

### F-009 - 固定并记录随机种子、框架确定性和硬件差异

- Rationale: 降低结果不可重复的随机性。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+6.0**
- Evidence: none

### F-011 - 添加快速开始和最小运行示例

- Rationale: 让新用户可以在几分钟内跑通。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+6.0**
- Evidence: none

### F-018 - 说明评测集、数据划分和污染/泄漏风险

- Rationale: 让指标具有可比性，避免高估效果。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+6.0**
- Evidence: none

### F-014 - 记录 temperature、top_p、max_tokens 等采样参数

- Rationale: 让生成行为可以复现和比较。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+5.0**
- Evidence: `E-006`

### F-003 - 补充数据来源、获取方式和数据许可说明

- Rationale: 让读者知道数据从哪里来、能否使用。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+4.0**
- Evidence: `E-007`

### F-015 - 记录 tokenizer、上下文窗口和截断策略

- Rationale: 避免输入长度和分词差异导致结果变化。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+4.0**
- Evidence: none

### F-004 - 添加数据下载或预处理脚本

- Rationale: 把数据准备从手工步骤变成可执行流程。
- Cost: **medium**
- Impact: **high**
- Estimated score gain: **+4.0**
- Evidence: `E-007`

### F-002 - 在 README 中增加可复制的安装命令

- Rationale: 降低首次运行门槛。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+3.5**
- Evidence: `E-001`

### F-005 - 添加数据集卡或数据许可说明

- Rationale: 明确数据边界和再分发条件。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+3.0**
- Evidence: `E-004`, `E-007`

### F-006 - 在模型卡中说明模型许可和来源

- Rationale: 避免模型使用和再分发风险。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+3.0**
- Evidence: `E-004`

### F-013 - 将 prompt/template 版本化并记录在配置或模型卡中

- Rationale: 避免 prompt 漂移导致结果不可复现。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+3.0**
- Evidence: `E-006`, `E-009`

### F-012 - 添加测试、CI 或一键复现脚本

- Rationale: 把复现变成持续可验证的工程流程。
- Cost: **medium**
- Impact: **medium**
- Estimated score gain: **+3.0**
- Evidence: `E-005`

### F-016 - 记录 RAG 索引版本、embedding 模型和 chunk 参数

- Rationale: 让检索结果可以复现。
- Cost: **medium**
- Impact: **high**
- Estimated score gain: **+2.5**
- Evidence: `E-012`

### F-017 - 保存 Agent 工具调用轨迹、run_id 和关键日志

- Rationale: 让多步调用过程可以审计。
- Cost: **medium**
- Impact: **high**
- Estimated score gain: **+2.5**
- Evidence: `E-013`

### F-019 - 说明推理成本、延迟和 token 消耗

- Rationale: 让读者评估复现成本。
- Cost: **low**
- Impact: **low**
- Estimated score gain: **+2.0**
- Evidence: `E-010`

## Evidence Appendix

- `E-001` [readme] `README.md:1` — # Chat UI
- `E-002` [lockfile] `package-lock.json` — package-lock.json
- `E-003` [container] `docker-compose.yml:1` — # For development only
- `E-004` [license] `LICENSE:1` — Copyright 2018- The Hugging Face team. All rights reserved.
- `E-005` [ci] `.github/workflows/build-docs.yml:1` — name: Build documentation
- `E-006` [prompt] `src/routes/conversation/[id]/message/[messageId]/prompt/+server.ts:1` — import { buildPrompt } from "$lib/buildPrompt";
- `E-007` [data] `README.md:3` — https://
- `E-008` [model] `README.md:3` — huggingface
- `E-009` [prompt] `README.md:42` — template
- `E-010` [llm-provider] `README.md:3` — huggingface
- `E-011` [model] `README.md:16` — llama
- `E-012` [rag] `README.md:16` — embedding
- `E-013` [agent] `README.md:130` — MCP

## Scope and Limitations

- This is static reproduction readiness analysis, not proof that the project reproduces successfully.
- No untrusted repository code is executed by default.
- Execution probes and GitHub Action integration are planned next.
- AI-generated explanations must be reviewed by the team before submission or release.
