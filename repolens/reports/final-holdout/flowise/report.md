# ReproLens Audit Report

- Repository: `C:\Users\86199\Documents\ChatGPT\全球校园人工智能算法精英大赛\repolens\benchmark\repos\flowise`
- Generated at: `2026-10-23T14:57:06.323774+00:00`
- Files scanned: **2450**
- Overall score: **56.7 / 100**
- Readiness: **At Risk**

## Dimension Scores

| Dimension | Points | Max | Percent |
|---|---:|---:|---:|
| 环境可复现 | 25.0 | 25.0 | 100.0% |
| 数据可复现 | 11.0 | 22.0 | 50.0% |
| 模型可复现 | 19.0 | 22.0 | 86.4% |
| 实验可复现 | 5.0 | 33.0 | 15.2% |
| 文档可复现 | 14.0 | 17.0 | 82.4% |
| LLM 特有风险 | 11.0 | 31.0 | 35.5% |

## Criteria

| ID | Dimension | Criterion | Status | Points | Evidence |
|---|---|---|---|---:|---|
| ENV-01 | 环境可复现 | 存在依赖清单 | PASS | 10.0/10.0 | E-002 |
| ENV-02 | 环境可复现 | 依赖版本锁定或容器化 | PASS | 8.0/8.0 | E-003, E-004 |
| ENV-03 | 环境可复现 | 提供安装步骤 | PASS | 7.0/7.0 | E-009 |
| DATA-01 | 数据可复现 | 说明数据来源和获取方式 | PARTIAL | 4.0/8.0 | E-010 |
| DATA-02 | 数据可复现 | 提供数据下载或预处理脚本 | PARTIAL | 4.0/8.0 | E-010 |
| DATA-03 | 数据可复现 | 提供数据集卡或数据许可说明 | PARTIAL | 3.0/6.0 | E-005, E-010 |
| MODEL-01 | 模型可复现 | 提供模型权重、API 或获取方式 | PASS | 8.0/8.0 | E-013, E-011 |
| MODEL-02 | 模型可复现 | 提供模型卡或版本说明 | PASS | 8.0/8.0 | E-011 |
| MODEL-03 | 模型可复现 | 说明模型许可和来源 | PARTIAL | 3.0/6.0 | E-005 |
| EXP-01 | 实验可复现 | 提供训练或主运行脚本 | MISSING | 0.0/7.0 | - |
| EXP-02 | 实验可复现 | 提供评测脚本或评测命令 | MISSING | 0.0/8.0 | - |
| EXP-03 | 实验可复现 | 设置并说明随机种子 | MISSING | 0.0/6.0 | - |
| EXP-04 | 实验可复现 | 说明硬件或 API 环境要求 | PASS | 5.0/5.0 | E-013 |
| EXP-05 | 实验可复现 | 给出预期结果和指标 | MISSING | 0.0/7.0 | - |
| DOC-01 | 文档可复现 | 存在 README | PASS | 5.0/5.0 | E-001 |
| DOC-02 | 文档可复现 | 提供快速开始和运行示例 | PARTIAL | 3.0/6.0 | E-009 |
| DOC-03 | 文档可复现 | 提供测试、CI 或一键复现脚本 | PASS | 6.0/6.0 | E-007, E-006 |
| LLM-01 | LLM 特有风险 | 记录模型/API 版本 | PASS | 6.0/6.0 | E-013, E-011 |
| LLM-02 | LLM 特有风险 | prompt/template 有版本记录 | PARTIAL | 3.0/6.0 | E-008, E-012 |
| LLM-03 | LLM 特有风险 | 记录采样参数 | MISSING | 0.0/5.0 | E-008 |
| LLM-04 | LLM 特有风险 | 记录 tokenizer/上下文窗口 | MISSING | 0.0/4.0 | - |
| LLM-05 | LLM 特有风险 | RAG 索引/知识库有版本记录 | N/A | 0.0/5.0 | - |
| LLM-06 | LLM 特有风险 | Agent 工具调用轨迹可追溯 | N/A | 0.0/5.0 | - |
| LLM-07 | LLM 特有风险 | 说明评测集、数据划分和污染风险 | MISSING | 0.0/6.0 | - |
| LLM-08 | LLM 特有风险 | 说明推理成本或延迟 | PARTIAL | 2.0/4.0 | E-013 |

## Findings

### F-001 [MEDIUM] 说明数据来源和获取方式

- Criterion: `DATA-01`
- Message: 提到了数据，但缺少可执行的获取或处理说明。
- Evidence: `E-010`

### F-002 [MEDIUM] 提供数据下载或预处理脚本

- Criterion: `DATA-02`
- Message: 有数据说明，但没有下载/预处理脚本。
- Evidence: `E-010`

### F-003 [MEDIUM] 提供数据集卡或数据许可说明

- Criterion: `DATA-03`
- Message: 有许可证和数据说明，但没有独立数据集卡。
- Evidence: `E-005`, `E-010`

### F-004 [MEDIUM] 说明模型许可和来源

- Criterion: `MODEL-03`
- Message: 有许可证或模型卡，但模型专用许可和来源仍需补充。
- Evidence: `E-005`

### F-005 [HIGH] 提供训练或主运行脚本

- Criterion: `EXP-01`
- Message: 没有训练脚本或主运行命令。
- Evidence: none

### F-006 [HIGH] 提供评测脚本或评测命令

- Criterion: `EXP-02`
- Message: 没有评测脚本或评测命令。
- Evidence: none

### F-007 [MEDIUM] 设置并说明随机种子

- Criterion: `EXP-03`
- Message: 没有随机种子或确定性设置。
- Evidence: none

### F-008 [HIGH] 给出预期结果和指标

- Criterion: `EXP-05`
- Message: 没有预期结果或指标。
- Evidence: none

### F-009 [MEDIUM] 提供快速开始和运行示例

- Criterion: `DOC-02`
- Message: 只有安装或运行说明中的一项。
- Evidence: `E-009`

### F-010 [MEDIUM] prompt/template 有版本记录

- Criterion: `LLM-02`
- Message: 有 prompt 文件或描述，但没有可核验的版本信息。
- Evidence: `E-008`, `E-012`

### F-011 [MEDIUM] 记录采样参数

- Criterion: `LLM-03`
- Message: 没有记录 temperature、top_p 等采样参数。
- Evidence: `E-008`

### F-012 [MEDIUM] 记录 tokenizer/上下文窗口

- Criterion: `LLM-04`
- Message: 没有记录 tokenizer 或上下文窗口。
- Evidence: none

### F-013 [MEDIUM] 说明评测集、数据划分和污染风险

- Criterion: `LLM-07`
- Message: 没有说明评测集、数据划分或污染风险。
- Evidence: none

### F-014 [MEDIUM] 说明推理成本或延迟

- Criterion: `LLM-08`
- Message: 有成本/硬件线索，但仍需量化数据。
- Evidence: `E-013`

## Execution Evidence

| Probe | Status | Return code | Duration | Command |
|---|---|---:|---:|---|
| python-syntax | PASS | 0 | 0.108s | `C:\Program Files\Python313\python.exe -c import ast, pathlib, sys ignore={'.git','.venv','venv','node_modules','__pycache__','.mypy_cache','.pytest_cache','dist','build'} bad=[] fo` |

## Minimal Remediation Plan

### F-006 - 添加评测脚本、评测命令和指标计算方式

- Rationale: 让结果可以被独立验证。
- Cost: **medium**
- Impact: **high**
- Estimated score gain: **+8.0**
- Evidence: none

### F-008 - 补充预期指标、日志样例和可接受误差范围

- Rationale: 让读者知道结果是否正确。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+7.0**
- Evidence: none

### F-005 - 添加训练脚本或明确训练命令

- Rationale: 让训练过程可执行。
- Cost: **medium**
- Impact: **high**
- Estimated score gain: **+7.0**
- Evidence: none

### F-007 - 固定并记录随机种子、框架确定性和硬件差异

- Rationale: 降低结果不可重复的随机性。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+6.0**
- Evidence: none

### F-013 - 说明评测集、数据划分和污染/泄漏风险

- Rationale: 让指标具有可比性，避免高估效果。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+6.0**
- Evidence: none

### F-011 - 记录 temperature、top_p、max_tokens 等采样参数

- Rationale: 让生成行为可以复现和比较。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+5.0**
- Evidence: `E-008`

### F-001 - 补充数据来源、获取方式和数据许可说明

- Rationale: 让读者知道数据从哪里来、能否使用。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+4.0**
- Evidence: `E-010`

### F-012 - 记录 tokenizer、上下文窗口和截断策略

- Rationale: 避免输入长度和分词差异导致结果变化。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+4.0**
- Evidence: none

### F-002 - 添加数据下载或预处理脚本

- Rationale: 把数据准备从手工步骤变成可执行流程。
- Cost: **medium**
- Impact: **high**
- Estimated score gain: **+4.0**
- Evidence: `E-010`

### F-003 - 添加数据集卡或数据许可说明

- Rationale: 明确数据边界和再分发条件。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+3.0**
- Evidence: `E-005`, `E-010`

### F-004 - 在模型卡中说明模型许可和来源

- Rationale: 避免模型使用和再分发风险。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+3.0**
- Evidence: `E-005`

### F-009 - 添加快速开始和最小运行示例

- Rationale: 让新用户可以在几分钟内跑通。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+3.0**
- Evidence: `E-009`

### F-010 - 将 prompt/template 版本化并记录在配置或模型卡中

- Rationale: 避免 prompt 漂移导致结果不可复现。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+3.0**
- Evidence: `E-008`, `E-012`

### F-014 - 说明推理成本、延迟和 token 消耗

- Rationale: 让读者评估复现成本。
- Cost: **low**
- Impact: **low**
- Estimated score gain: **+2.0**
- Evidence: `E-013`

## Evidence Appendix

- `E-001` [readme] `README.md:1` — <!-- markdownlint-disable MD030 -->
- `E-002` [dependency-manifest] `package.json:1` — {
- `E-003` [lockfile] `packages/observe/examples/package-lock.json:1` — {
- `E-004` [container] `Dockerfile:1` — # Build local monorepo image
- `E-005` [license] `LICENSE.md:1` — Copyright (c) 2023-present FlowiseAI, Inc.
- `E-006` [ci] `.github/workflows/docker-image-dockerhub.yml:1` — name: Docker Image CI - Docker Hub
- `E-007` [tests] `packages/ui/src/utils/genericHelper.test.js:1` — import { applyVisibleInputDefaults, showHideInputs } from './genericHelper'
- `E-008` [prompt] `packages/components/nodes/prompts/ChatPromptTemplate/ChatPromptTemplate.ts:1` — import { ICommonObject, IDatabaseEntity, INode, INodeData, INodeParams } from '../../../src/Interface'
- `E-009` [instruction] `README.md:71` — docker build
- `E-010` [data] `README.md:4` — https://
- `E-011` [model] `README.md:203` — HuggingFace
- `E-012` [prompt] `README.md:193` — template
- `E-013` [llm-provider] `README.md:203` — HuggingFace

## Scope and Limitations

- This is static reproduction readiness analysis, not proof that the project reproduces successfully.
- No untrusted repository code is executed by default.
- Execution probes and GitHub Action integration are planned next.
- AI-generated explanations must be reviewed by the team before submission or release.
