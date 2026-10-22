# ReproLens Audit Report

- Repository: `C:\Users\86199\Documents\ChatGPT\全球校园人工智能算法精英大赛\repolens\examples\demo-llm-app`
- Generated at: `2026-10-22T13:42:03.810057+00:00`
- Files scanned: **6**
- Overall score: **49.1 / 100**
- Readiness: **At Risk**

## Dimension Scores

| Dimension | Points | Max | Percent |
|---|---:|---:|---:|
| 环境可复现 | 21.0 | 25.0 | 84.0% |
| 数据可复现 | 0.0 | 22.0 | 0.0% |
| 模型可复现 | 16.0 | 22.0 | 72.7% |
| 实验可复现 | 8.0 | 33.0 | 24.2% |
| 文档可复现 | 8.0 | 17.0 | 47.1% |
| LLM 特有风险 | 25.5 | 41.0 | 62.2% |

## Criteria

| ID | Dimension | Criterion | Status | Points | Evidence |
|---|---|---|---|---:|---|
| ENV-01 | 环境可复现 | 存在依赖清单 | PASS | 10.0/10.0 | E-002 |
| ENV-02 | 环境可复现 | 依赖版本锁定或容器化 | PARTIAL | 4.0/8.0 | E-002 |
| ENV-03 | 环境可复现 | 提供安装步骤 | PASS | 7.0/7.0 | E-005 |
| DATA-01 | 数据可复现 | 说明数据来源和获取方式 | MISSING | 0.0/8.0 | - |
| DATA-02 | 数据可复现 | 提供数据下载或预处理脚本 | MISSING | 0.0/8.0 | - |
| DATA-03 | 数据可复现 | 提供数据集卡或数据许可说明 | MISSING | 0.0/6.0 | - |
| MODEL-01 | 模型可复现 | 提供模型权重、API 或获取方式 | PASS | 8.0/8.0 | E-006, E-007 |
| MODEL-02 | 模型可复现 | 提供模型卡或版本说明 | PASS | 8.0/8.0 | E-007 |
| MODEL-03 | 模型可复现 | 说明模型许可和来源 | MISSING | 0.0/6.0 | - |
| EXP-01 | 实验可复现 | 提供训练或主运行脚本 | MISSING | 0.0/7.0 | - |
| EXP-02 | 实验可复现 | 提供评测脚本或评测命令 | MISSING | 0.0/8.0 | - |
| EXP-03 | 实验可复现 | 设置并说明随机种子 | PARTIAL | 3.0/6.0 | E-008 |
| EXP-04 | 实验可复现 | 说明硬件或 API 环境要求 | PASS | 5.0/5.0 | E-006 |
| EXP-05 | 实验可复现 | 给出预期结果和指标 | MISSING | 0.0/7.0 | - |
| DOC-01 | 文档可复现 | 存在 README | PASS | 5.0/5.0 | E-001 |
| DOC-02 | 文档可复现 | 提供快速开始和运行示例 | PARTIAL | 3.0/6.0 | E-005 |
| DOC-03 | 文档可复现 | 提供测试、CI 或一键复现脚本 | MISSING | 0.0/6.0 | - |
| LLM-01 | LLM 特有风险 | 记录模型/API 版本 | PASS | 6.0/6.0 | E-006, E-007 |
| LLM-02 | LLM 特有风险 | prompt/template 有版本记录 | PARTIAL | 3.0/6.0 | E-004 |
| LLM-03 | LLM 特有风险 | 记录采样参数 | PASS | 5.0/5.0 | E-008, E-003 |
| LLM-04 | LLM 特有风险 | 记录 tokenizer/上下文窗口 | PARTIAL | 2.0/4.0 | E-008 |
| LLM-05 | LLM 特有风险 | RAG 索引/知识库有版本记录 | PASS | 5.0/5.0 | E-010, E-009 |
| LLM-06 | LLM 特有风险 | Agent 工具调用轨迹可追溯 | PARTIAL | 2.5/5.0 | E-011 |
| LLM-07 | LLM 特有风险 | 说明评测集、数据划分和污染风险 | MISSING | 0.0/6.0 | - |
| LLM-08 | LLM 特有风险 | 说明推理成本或延迟 | PARTIAL | 2.0/4.0 | E-006 |

## Findings

### F-001 [MEDIUM] 依赖版本锁定或容器化

- Criterion: `ENV-02`
- Message: 有依赖清单，但没有锁定文件或容器配置。
- Evidence: `E-002`

### F-002 [HIGH] 说明数据来源和获取方式

- Criterion: `DATA-01`
- Message: 没有数据来源说明。
- Evidence: none

### F-003 [HIGH] 提供数据下载或预处理脚本

- Criterion: `DATA-02`
- Message: 没有数据下载或预处理脚本。
- Evidence: none

### F-004 [MEDIUM] 提供数据集卡或数据许可说明

- Criterion: `DATA-03`
- Message: 没有数据集卡或明确的数据许可说明。
- Evidence: none

### F-005 [MEDIUM] 说明模型许可和来源

- Criterion: `MODEL-03`
- Message: 没有模型许可或来源说明。
- Evidence: none

### F-006 [HIGH] 提供训练或主运行脚本

- Criterion: `EXP-01`
- Message: 没有训练脚本或主运行命令。
- Evidence: none

### F-007 [HIGH] 提供评测脚本或评测命令

- Criterion: `EXP-02`
- Message: 没有评测脚本或评测命令。
- Evidence: none

### F-008 [MEDIUM] 设置并说明随机种子

- Criterion: `EXP-03`
- Message: 有采样参数，但没有明确随机种子或确定性设置。
- Evidence: `E-008`

### F-009 [HIGH] 给出预期结果和指标

- Criterion: `EXP-05`
- Message: 没有预期结果或指标。
- Evidence: none

### F-010 [MEDIUM] 提供快速开始和运行示例

- Criterion: `DOC-02`
- Message: 只有安装或运行说明中的一项。
- Evidence: `E-005`

### F-011 [MEDIUM] 提供测试、CI 或一键复现脚本

- Criterion: `DOC-03`
- Message: 没有测试、CI 或一键复现脚本。
- Evidence: none

### F-012 [MEDIUM] prompt/template 有版本记录

- Criterion: `LLM-02`
- Message: 有 prompt 文件或描述，但没有可核验的版本信息。
- Evidence: `E-004`

### F-013 [MEDIUM] 记录 tokenizer/上下文窗口

- Criterion: `LLM-04`
- Message: 有相关配置，但 tokenizer/上下文窗口仍需补充。
- Evidence: `E-008`

### F-014 [MEDIUM] Agent 工具调用轨迹可追溯

- Criterion: `LLM-06`
- Message: 检测到 Agent 项目，但调用轨迹仍需补充。
- Evidence: `E-011`

### F-015 [MEDIUM] 说明评测集、数据划分和污染风险

- Criterion: `LLM-07`
- Message: 没有说明评测集、数据划分或污染风险。
- Evidence: none

### F-016 [MEDIUM] 说明推理成本或延迟

- Criterion: `LLM-08`
- Message: 有硬件/API 信息，但没有成本或延迟说明。
- Evidence: `E-006`

## Execution Evidence

| Probe | Status | Return code | Duration | Command |
|---|---|---:|---:|---|
| python-syntax | PASS | 0 | 0.078s | `C:\Program Files\Python313\python.exe -c import ast, pathlib, sys ignore={'.git','.venv','venv','node_modules','__pycache__','.mypy_cache','.pytest_cache','dist','build'} bad=[] fo` |

## Minimal Remediation Plan

### F-002 - 补充数据来源、获取方式和数据许可说明

- Rationale: 让读者知道数据从哪里来、能否使用。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+8.0**
- Evidence: none

### F-003 - 添加数据下载或预处理脚本

- Rationale: 把数据准备从手工步骤变成可执行流程。
- Cost: **medium**
- Impact: **high**
- Estimated score gain: **+8.0**
- Evidence: none

### F-007 - 添加评测脚本、评测命令和指标计算方式

- Rationale: 让结果可以被独立验证。
- Cost: **medium**
- Impact: **high**
- Estimated score gain: **+8.0**
- Evidence: none

### F-009 - 补充预期指标、日志样例和可接受误差范围

- Rationale: 让读者知道结果是否正确。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+7.0**
- Evidence: none

### F-006 - 添加训练脚本或明确训练命令

- Rationale: 让训练过程可执行。
- Cost: **medium**
- Impact: **high**
- Estimated score gain: **+7.0**
- Evidence: none

### F-004 - 添加数据集卡或数据许可说明

- Rationale: 明确数据边界和再分发条件。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+6.0**
- Evidence: none

### F-005 - 在模型卡中说明模型许可和来源

- Rationale: 避免模型使用和再分发风险。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+6.0**
- Evidence: none

### F-015 - 说明评测集、数据划分和污染/泄漏风险

- Rationale: 让指标具有可比性，避免高估效果。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+6.0**
- Evidence: none

### F-011 - 添加测试、CI 或一键复现脚本

- Rationale: 把复现变成持续可验证的工程流程。
- Cost: **medium**
- Impact: **medium**
- Estimated score gain: **+6.0**
- Evidence: none

### F-001 - 添加锁文件或 Dockerfile，固定 Python、CUDA 和依赖版本

- Rationale: 消除环境版本漂移，提升跨机器复现概率。
- Cost: **medium**
- Impact: **high**
- Estimated score gain: **+4.0**
- Evidence: `E-002`

### F-008 - 固定并记录随机种子、框架确定性和硬件差异

- Rationale: 降低结果不可重复的随机性。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+3.0**
- Evidence: `E-008`

### F-010 - 添加快速开始和最小运行示例

- Rationale: 让新用户可以在几分钟内跑通。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+3.0**
- Evidence: `E-005`

### F-012 - 将 prompt/template 版本化并记录在配置或模型卡中

- Rationale: 避免 prompt 漂移导致结果不可复现。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+3.0**
- Evidence: `E-004`

### F-014 - 保存 Agent 工具调用轨迹、run_id 和关键日志

- Rationale: 让多步调用过程可以审计。
- Cost: **medium**
- Impact: **high**
- Estimated score gain: **+2.5**
- Evidence: `E-011`

### F-013 - 记录 tokenizer、上下文窗口和截断策略

- Rationale: 避免输入长度和分词差异导致结果变化。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+2.0**
- Evidence: `E-008`

### F-016 - 说明推理成本、延迟和 token 消耗

- Rationale: 让读者评估复现成本。
- Cost: **low**
- Impact: **low**
- Estimated score gain: **+2.0**
- Evidence: `E-006`

## Evidence Appendix

- `E-001` [readme] `README.md:1` — # Demo LLM RAG App
- `E-002` [dependency-manifest] `requirements.txt:1` — openai>=1.0
- `E-003` [config] `configs/app.yaml:1` — model:
- `E-004` [prompt] `prompts/system.txt:1` — You are a helpful assistant. Answer using the retrieved context.
- `E-005` [instruction] `README.md:8` — pip install
- `E-006` [llm-provider] `README.md:17` — OpenAI
- `E-007` [model] `configs/app.yaml:3` — gpt-4
- `E-008` [llm-config] `configs/app.yaml:4` — temperature
- `E-009` [rag] `README.md:1` — RAG
- `E-010` [rag] `configs/app.yaml:8` — vector_store
- `E-011` [agent] `README.md:3` — agent

## Scope and Limitations

- This is static reproduction readiness analysis, not proof that the project reproduces successfully.
- No untrusted repository code is executed by default.
- Execution probes and GitHub Action integration are planned next.
- AI-generated explanations must be reviewed by the team before submission or release.
