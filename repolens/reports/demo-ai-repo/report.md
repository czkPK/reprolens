# ReproLens Audit Report

- Repository: `C:\Users\86199\Documents\ChatGPT\全球校园人工智能算法精英大赛\repolens\examples\demo-ai-repo`
- Generated at: `2026-10-21T14:44:07.271372+00:00`
- Files scanned: **6**
- Overall score: **54.2 / 100**
- Readiness: **At Risk**

## Dimension Scores

| Dimension | Points | Max | Percent |
|---|---:|---:|---:|
| 环境可复现 | 21.0 | 25.0 | 84.0% |
| 数据可复现 | 8.0 | 22.0 | 36.4% |
| 模型可复现 | 0.0 | 22.0 | 0.0% |
| 实验可复现 | 24.5 | 33.0 | 74.2% |
| 文档可复现 | 11.0 | 17.0 | 64.7% |
| LLM 特有风险 | 0.0 | 0.0 | 100.0% |

## Criteria

| ID | Dimension | Criterion | Status | Points | Evidence |
|---|---|---|---|---:|---|
| ENV-01 | 环境可复现 | 存在依赖清单 | PASS | 10.0/10.0 | E-002 |
| ENV-02 | 环境可复现 | 依赖版本锁定或容器化 | PARTIAL | 4.0/8.0 | E-002 |
| ENV-03 | 环境可复现 | 提供安装步骤 | PASS | 7.0/7.0 | E-006 |
| DATA-01 | 数据可复现 | 说明数据来源和获取方式 | PARTIAL | 4.0/8.0 | E-008 |
| DATA-02 | 数据可复现 | 提供数据下载或预处理脚本 | PARTIAL | 4.0/8.0 | E-008 |
| DATA-03 | 数据可复现 | 提供数据集卡或数据许可说明 | MISSING | 0.0/6.0 | - |
| MODEL-01 | 模型可复现 | 提供模型权重、API 或获取方式 | MISSING | 0.0/8.0 | - |
| MODEL-02 | 模型可复现 | 提供模型卡或版本说明 | MISSING | 0.0/8.0 | - |
| MODEL-03 | 模型可复现 | 说明模型许可和来源 | MISSING | 0.0/6.0 | - |
| EXP-01 | 实验可复现 | 提供训练或主运行脚本 | PASS | 7.0/7.0 | E-003, E-007 |
| EXP-02 | 实验可复现 | 提供评测脚本或评测命令 | PASS | 8.0/8.0 | E-004 |
| EXP-03 | 实验可复现 | 设置并说明随机种子 | MISSING | 0.0/6.0 | - |
| EXP-04 | 实验可复现 | 说明硬件或 API 环境要求 | PARTIAL | 2.5/5.0 | E-002 |
| EXP-05 | 实验可复现 | 给出预期结果和指标 | PASS | 7.0/7.0 | E-009, E-011 |
| DOC-01 | 文档可复现 | 存在 README | PASS | 5.0/5.0 | E-001 |
| DOC-02 | 文档可复现 | 提供快速开始和运行示例 | PASS | 6.0/6.0 | E-006, E-007 |
| DOC-03 | 文档可复现 | 提供测试、CI 或一键复现脚本 | MISSING | 0.0/6.0 | - |
| LLM-01 | LLM 特有风险 | 记录模型/API 版本 | N/A | 0.0/6.0 | - |
| LLM-02 | LLM 特有风险 | prompt/template 有版本记录 | N/A | 0.0/6.0 | - |
| LLM-03 | LLM 特有风险 | 记录采样参数 | N/A | 0.0/5.0 | E-005 |
| LLM-04 | LLM 特有风险 | 记录 tokenizer/上下文窗口 | N/A | 0.0/4.0 | - |
| LLM-05 | LLM 特有风险 | RAG 索引/知识库有版本记录 | N/A | 0.0/5.0 | - |
| LLM-06 | LLM 特有风险 | Agent 工具调用轨迹可追溯 | N/A | 0.0/5.0 | - |
| LLM-07 | LLM 特有风险 | 说明评测集、数据划分和污染风险 | N/A | 0.0/6.0 | E-011, E-010 |
| LLM-08 | LLM 特有风险 | 说明推理成本或延迟 | N/A | 0.0/4.0 | - |

## Findings

### F-001 [MEDIUM] 依赖版本锁定或容器化

- Criterion: `ENV-02`
- Message: 有依赖清单，但没有锁定文件或容器配置。
- Evidence: `E-002`

### F-002 [MEDIUM] 说明数据来源和获取方式

- Criterion: `DATA-01`
- Message: 提到了数据，但缺少可执行的获取或处理说明。
- Evidence: `E-008`

### F-003 [MEDIUM] 提供数据下载或预处理脚本

- Criterion: `DATA-02`
- Message: 有数据说明，但没有下载/预处理脚本。
- Evidence: `E-008`

### F-004 [MEDIUM] 提供数据集卡或数据许可说明

- Criterion: `DATA-03`
- Message: 没有数据集卡或明确的数据许可说明。
- Evidence: none

### F-005 [HIGH] 提供模型权重、API 或获取方式

- Criterion: `MODEL-01`
- Message: 没有模型权重、API 或获取方式。
- Evidence: none

### F-006 [HIGH] 提供模型卡或版本说明

- Criterion: `MODEL-02`
- Message: 没有模型卡或版本说明。
- Evidence: none

### F-007 [MEDIUM] 说明模型许可和来源

- Criterion: `MODEL-03`
- Message: 没有模型许可或来源说明。
- Evidence: none

### F-008 [MEDIUM] 设置并说明随机种子

- Criterion: `EXP-03`
- Message: 没有随机种子或确定性设置。
- Evidence: none

### F-009 [MEDIUM] 说明硬件或 API 环境要求

- Criterion: `EXP-04`
- Message: 有依赖清单，但没有明确硬件或 API 环境要求。
- Evidence: `E-002`

### F-010 [MEDIUM] 提供测试、CI 或一键复现脚本

- Criterion: `DOC-03`
- Message: 没有测试、CI 或一键复现脚本。
- Evidence: none

## Execution Evidence

| Probe | Status | Return code | Duration | Command |
|---|---|---:|---:|---|
| python-syntax | PASS | 0 | 0.052s | `C:\Program Files\Python313\python.exe -c import ast, pathlib, sys ignore={'.git','.venv','venv','node_modules','__pycache__','.mypy_cache','.pytest_cache','dist','build'} bad=[] fo` |

## Minimal Remediation Plan

### F-006 - 添加模型卡，记录模型版本、结构、超参数和训练数据

- Rationale: 让模型行为可追溯。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+8.0**
- Evidence: none

### F-005 - 提供模型权重下载地址或权重大小、文件名说明

- Rationale: 让读者能够获得与结果对应的模型。
- Cost: **medium**
- Impact: **high**
- Estimated score gain: **+8.0**
- Evidence: none

### F-004 - 添加数据集卡或数据许可说明

- Rationale: 明确数据边界和再分发条件。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+6.0**
- Evidence: none

### F-007 - 在模型卡中说明模型许可和来源

- Rationale: 避免模型使用和再分发风险。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+6.0**
- Evidence: none

### F-008 - 固定并记录随机种子、框架确定性和硬件差异

- Rationale: 降低结果不可重复的随机性。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+6.0**
- Evidence: none

### F-010 - 添加测试、CI 或一键复现脚本

- Rationale: 把复现变成持续可验证的工程流程。
- Cost: **medium**
- Impact: **medium**
- Estimated score gain: **+6.0**
- Evidence: none

### F-002 - 补充数据来源、获取方式和数据许可说明

- Rationale: 让读者知道数据从哪里来、能否使用。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+4.0**
- Evidence: `E-008`

### F-001 - 添加锁文件或 Dockerfile，固定 Python、CUDA 和依赖版本

- Rationale: 消除环境版本漂移，提升跨机器复现概率。
- Cost: **medium**
- Impact: **high**
- Estimated score gain: **+4.0**
- Evidence: `E-002`

### F-003 - 添加数据下载或预处理脚本

- Rationale: 把数据准备从手工步骤变成可执行流程。
- Cost: **medium**
- Impact: **high**
- Estimated score gain: **+4.0**
- Evidence: `E-008`

### F-009 - 在 README/模型卡中说明 GPU 型号、显存和驱动要求

- Rationale: 减少环境不匹配导致的失败。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+2.5**
- Evidence: `E-002`

## Evidence Appendix

- `E-001` [readme] `README.md:1` — # Demo AI Project
- `E-002` [dependency-manifest] `requirements.txt:1` — torch>=2.0
- `E-003` [script] `train.py:1` — import torch
- `E-004` [script] `eval.py:1` — import torch
- `E-005` [config] `configs/default.yaml:1` — seed: null
- `E-006` [instruction] `README.md:8` — pip install
- `E-007` [instruction] `README.md:14` — python train
- `E-008` [data] `README.md:18` — dataset
- `E-009` [metric] `README.md:18` — Expected
- `E-010` [evaluation] `README.md:18` — split
- `E-011` [evaluation] `data/README.md:3` — benchmark

## Scope and Limitations

- This is static reproduction readiness analysis, not proof that the project reproduces successfully.
- No untrusted repository code is executed by default.
- Execution probes and GitHub Action integration are planned next.
- AI-generated explanations must be reviewed by the team before submission or release.
