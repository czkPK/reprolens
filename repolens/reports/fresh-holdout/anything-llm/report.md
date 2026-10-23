# ReproLens Audit Report

- Repository: `C:\Users\86199\Documents\ChatGPT\全球校园人工智能算法精英大赛\repolens\benchmark\repos\anything-llm`
- Generated at: `2026-10-23T14:41:17.677356+00:00`
- Files scanned: **1580**
- Overall score: **71.2 / 100**
- Readiness: **Partially Ready**

## Dimension Scores

| Dimension | Points | Max | Percent |
|---|---:|---:|---:|
| 环境可复现 | 21.5 | 25.0 | 86.0% |
| 数据可复现 | 0.0 | 0.0 | 100.0% |
| 模型可复现 | 0.0 | 0.0 | 100.0% |
| 实验可复现 | 20.0 | 20.0 | 100.0% |
| 文档可复现 | 14.0 | 17.0 | 82.4% |
| LLM 特有风险 | 10.0 | 30.0 | 33.3% |

## Criteria

| ID | Dimension | Criterion | Status | Points | Evidence |
|---|---|---|---|---:|---|
| ENV-01 | 环境可复现 | 存在依赖清单 | PASS | 10.0/10.0 | E-002 |
| ENV-02 | 环境可复现 | 依赖版本锁定或容器化 | PASS | 8.0/8.0 | E-003 |
| ENV-03 | 环境可复现 | 提供安装步骤 | PARTIAL | 3.5/7.0 | E-001 |
| DATA-01 | 数据可复现 | 说明数据来源和获取方式 | N/A | 0.0/8.0 | E-008 |
| DATA-02 | 数据可复现 | 提供数据下载或预处理脚本 | N/A | 0.0/8.0 | E-008 |
| DATA-03 | 数据可复现 | 提供数据集卡或数据许可说明 | N/A | 0.0/6.0 | E-004, E-008 |
| MODEL-01 | 模型可复现 | 提供模型权重、API 或获取方式 | N/A | 0.0/8.0 | E-012, E-013 |
| MODEL-02 | 模型可复现 | 提供模型卡或版本说明 | N/A | 0.0/8.0 | E-013 |
| MODEL-03 | 模型可复现 | 说明模型许可和来源 | N/A | 0.0/6.0 | E-004 |
| EXP-01 | 实验可复现 | 提供训练或主运行脚本 | PASS | 7.0/7.0 | E-007 |
| EXP-02 | 实验可复现 | 提供评测脚本或评测命令 | PASS | 8.0/8.0 | E-006, E-005 |
| EXP-03 | 实验可复现 | 设置并说明随机种子 | N/A | 0.0/6.0 | - |
| EXP-04 | 实验可复现 | 说明硬件或 API 环境要求 | PASS | 5.0/5.0 | E-009, E-012 |
| EXP-05 | 实验可复现 | 给出预期结果和指标 | N/A | 0.0/7.0 | - |
| DOC-01 | 文档可复现 | 存在 README | PASS | 5.0/5.0 | E-001 |
| DOC-02 | 文档可复现 | 提供快速开始和运行示例 | PARTIAL | 3.0/6.0 | E-007 |
| DOC-03 | 文档可复现 | 提供测试、CI 或一键复现脚本 | PASS | 6.0/6.0 | E-006, E-005 |
| LLM-01 | LLM 特有风险 | 记录模型/API 版本 | N/A | 0.0/6.0 | E-012, E-013 |
| LLM-02 | LLM 特有风险 | prompt/template 有版本记录 | PARTIAL | 3.0/6.0 | E-010 |
| LLM-03 | LLM 特有风险 | 记录采样参数 | N/A | 0.0/5.0 | - |
| LLM-04 | LLM 特有风险 | 记录 tokenizer/上下文窗口 | MISSING | 0.0/4.0 | - |
| LLM-05 | LLM 特有风险 | RAG 索引/知识库有版本记录 | PARTIAL | 2.5/5.0 | E-014 |
| LLM-06 | LLM 特有风险 | Agent 工具调用轨迹可追溯 | PARTIAL | 2.5/5.0 | E-015 |
| LLM-07 | LLM 特有风险 | 说明评测集、数据划分和污染风险 | MISSING | 0.0/6.0 | - |
| LLM-08 | LLM 特有风险 | 说明推理成本或延迟 | PARTIAL | 2.0/4.0 | E-011, E-009, E-012 |

## Findings

### F-001 [MEDIUM] 提供安装步骤

- Criterion: `ENV-03`
- Message: 有 README，但没有明显安装命令。
- Evidence: `E-001`

### F-002 [MEDIUM] 提供快速开始和运行示例

- Criterion: `DOC-02`
- Message: 只有安装或运行说明中的一项。
- Evidence: `E-007`

### F-003 [MEDIUM] prompt/template 有版本记录

- Criterion: `LLM-02`
- Message: 有 prompt 文件或描述，但没有可核验的版本信息。
- Evidence: `E-010`

### F-004 [MEDIUM] 记录 tokenizer/上下文窗口

- Criterion: `LLM-04`
- Message: 没有记录 tokenizer 或上下文窗口。
- Evidence: none

### F-005 [MEDIUM] RAG 索引/知识库有版本记录

- Criterion: `LLM-05`
- Message: 检测到 RAG 项目，但索引/embedding 版本仍需补充。
- Evidence: `E-014`

### F-006 [MEDIUM] Agent 工具调用轨迹可追溯

- Criterion: `LLM-06`
- Message: 检测到 Agent 项目，但调用轨迹仍需补充。
- Evidence: `E-015`

### F-007 [MEDIUM] 说明评测集、数据划分和污染风险

- Criterion: `LLM-07`
- Message: 没有说明评测集、数据划分或污染风险。
- Evidence: none

### F-008 [MEDIUM] 说明推理成本或延迟

- Criterion: `LLM-08`
- Message: 有成本/硬件线索，但仍需量化数据。
- Evidence: `E-011`, `E-009`, `E-012`

## Execution Evidence

| Probe | Status | Return code | Duration | Command |
|---|---|---:|---:|---|
| python-syntax | PASS | 0 | 0.122s | `C:\Program Files\Python313\python.exe -c import ast, pathlib, sys ignore={'.git','.venv','venv','node_modules','__pycache__','.mypy_cache','.pytest_cache','dist','build'} bad=[] fo` |

## Minimal Remediation Plan

### F-007 - 说明评测集、数据划分和污染/泄漏风险

- Rationale: 让指标具有可比性，避免高估效果。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+6.0**
- Evidence: none

### F-004 - 记录 tokenizer、上下文窗口和截断策略

- Rationale: 避免输入长度和分词差异导致结果变化。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+4.0**
- Evidence: none

### F-001 - 在 README 中增加可复制的安装命令

- Rationale: 降低首次运行门槛。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+3.5**
- Evidence: `E-001`

### F-002 - 添加快速开始和最小运行示例

- Rationale: 让新用户可以在几分钟内跑通。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+3.0**
- Evidence: `E-007`

### F-003 - 将 prompt/template 版本化并记录在配置或模型卡中

- Rationale: 避免 prompt 漂移导致结果不可复现。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+3.0**
- Evidence: `E-010`

### F-005 - 记录 RAG 索引版本、embedding 模型和 chunk 参数

- Rationale: 让检索结果可以复现。
- Cost: **medium**
- Impact: **high**
- Estimated score gain: **+2.5**
- Evidence: `E-014`

### F-006 - 保存 Agent 工具调用轨迹、run_id 和关键日志

- Rationale: 让多步调用过程可以审计。
- Cost: **medium**
- Impact: **high**
- Estimated score gain: **+2.5**
- Evidence: `E-015`

### F-008 - 说明推理成本、延迟和 token 消耗

- Rationale: 让读者评估复现成本。
- Cost: **low**
- Impact: **low**
- Estimated score gain: **+2.0**
- Evidence: `E-011`, `E-009`, `E-012`

## Evidence Appendix

- `E-001` [readme] `README.md:1` — <a name="readme-top"></a>
- `E-002` [dependency-manifest] `package.json:1` — {
- `E-003` [container] `docker/docker-compose.yml:1` — name: anythingllm
- `E-004` [license] `LICENSE:1` — The MIT License
- `E-005` [ci] `.github/workflows/build-and-push-image-semver.yaml:1` — name: Publish AnythingLLM Docker image on Release (amd64 & arm64)
- `E-006` [tests] `server/__tests__/endpoints/agentWebsocket.test.js:1` — /* eslint-env jest */
- `E-007` [instruction] `README.md:227` — make product and roadmap decisions, specifically:
- `E-008` [data] `README.md:4` — https://
- `E-009` [hardware] `README.md:62` — GPU
- `E-010` [prompt] `README.md:65` — prompt
- `E-011` [cost] `README.md:66` — token usage
- `E-012` [llm-provider] `README.md:88` — OpenAI
- `E-013` [model] `README.md:62` — llama
- `E-014` [rag] `README.md:165` — Pinecone
- `E-015` [agent] `README.md:65` — agent

## Scope and Limitations

- This is static reproduction readiness analysis, not proof that the project reproduces successfully.
- No untrusted repository code is executed by default.
- Execution probes and GitHub Action integration are planned next.
- AI-generated explanations must be reviewed by the team before submission or release.
