# ReproLens Audit Report

- Repository: `D:\CODEX\ReproLens\repolens\examples\demo-llm-app`
- Generated at: `2026-10-27T13:53:47.953168+00:00`
- Semantic claim mapping: **rules**
- Files scanned: **6**
- Overall score: **49.1 / 100**
- Readiness: **At Risk**
- Evidence coverage: **16/25 (64.0%)**
- README claims audited: **2**

## Dimension Scores

| Dimension | Points | Max | Percent |
|---|---:|---:|---:|
| 环境可复现 | 21.0 | 25.0 | 84.0% |
| 数据可复现 | 0.0 | 22.0 | 0.0% |
| 模型可复现 | 16.0 | 22.0 | 72.7% |
| 实验可复现 | 8.0 | 33.0 | 24.2% |
| 文档可复现 | 8.0 | 17.0 | 47.1% |
| LLM 特有风险 | 25.5 | 41.0 | 62.2% |

## Top 3 Priority Actions

1. **补充数据来源、获取方式和数据许可说明** — expected gain **+8.0**; 让读者知道数据从哪里来、能否使用。
2. **添加数据下载或预处理脚本** — expected gain **+8.0**; 把数据准备从手工步骤变成可执行流程。
3. **添加评测脚本、评测命令和指标计算方式** — expected gain **+8.0**; 让结果可以被独立验证。

## Criteria

| 检查项编号 | 所属维度 | 检查要求 | 状态 | 证据强度 | 得分 | 证据编号 | 证据说明 |
|---|---|---|---|---|---:|---|---|

**读表说明：** PASS = 满足要求；PARTIAL = 只有部分证据；MISSING = 应有但没有找到；N/A = 当前项目类型不适用。Confidence 表示证据支持强度，不代表项目整体质量。

| ENV-01 | 环境可复现 | 是否存在依赖清单 | PASS | MEDIUM | 10.0/10.0 | E-002 | 支持证据：E-002（requirements.txt:1）：“openai>=1.0”。 |
| ENV-02 | 环境可复现 | 是否锁定依赖版本或提供容器化配置 | PARTIAL | MEDIUM | 4.0/8.0 | E-002 | 部分证据：E-002（requirements.txt:1）：“openai>=1.0”；现有证据不足以完全满足该项。 |
| ENV-03 | 环境可复现 | 是否提供安装步骤 | PASS | MEDIUM | 7.0/7.0 | E-005 | 支持证据：E-005（README.md:8）：“pip install -r requirements.txt”。 |
| DATA-01 | 数据可复现 | 是否说明数据来源和获取方式 | MISSING | LOW | 0.0/8.0 | - | 未找到可引用证据，因此该项不能判定为通过。 |
| DATA-02 | 数据可复现 | 是否提供数据下载或预处理脚本 | MISSING | LOW | 0.0/8.0 | - | 未找到可引用证据，因此该项不能判定为通过。 |
| DATA-03 | 数据可复现 | 是否提供数据集卡或数据许可说明 | MISSING | LOW | 0.0/6.0 | - | 未找到可引用证据，因此该项不能判定为通过。 |
| MODEL-01 | 模型可复现 | 是否提供模型权重、API 或获取方式 | PASS | HIGH | 8.0/8.0 | E-006, E-007 | 支持证据：E-006（README.md:17）：“This demo uses an OpenAI-compatible model and a local vector store. The knowledge base ...”；E-007（configs/app.yaml:3）：“name: gpt-4o-mini”。 |
| MODEL-02 | 模型可复现 | 是否提供模型卡或版本说明 | PASS | MEDIUM | 8.0/8.0 | E-007 | 支持证据：E-007（configs/app.yaml:3）：“name: gpt-4o-mini”。 |
| MODEL-03 | 模型可复现 | 是否说明模型许可和来源 | MISSING | LOW | 0.0/6.0 | - | 未找到可引用证据，因此该项不能判定为通过。 |
| EXP-01 | 实验可复现 | 是否提供训练或主运行脚本 | MISSING | LOW | 0.0/7.0 | - | 未找到可引用证据，因此该项不能判定为通过。 |
| EXP-02 | 实验可复现 | 是否提供评测脚本或评测命令 | MISSING | LOW | 0.0/8.0 | - | 未找到可引用证据，因此该项不能判定为通过。 |
| EXP-03 | 实验可复现 | 是否设置并说明随机种子 | PARTIAL | MEDIUM | 3.0/6.0 | E-008 | 部分证据：E-008（configs/app.yaml:4）：“temperature: 0.2”；现有证据不足以完全满足该项。 |
| EXP-04 | 实验可复现 | 是否说明硬件或 API 环境要求 | PASS | MEDIUM | 5.0/5.0 | E-006 | 支持证据：E-006（README.md:17）：“This demo uses an OpenAI-compatible model and a local vector store. The knowledge base ...”。 |
| EXP-05 | 实验可复现 | 是否给出预期结果和指标 | MISSING | LOW | 0.0/7.0 | - | 未找到可引用证据，因此该项不能判定为通过。 |
| DOC-01 | 文档可复现 | 是否存在 README | PASS | MEDIUM | 5.0/5.0 | E-001 | 支持证据：E-001（README.md:1）：“# Demo LLM RAG App”。 |
| DOC-02 | 文档可复现 | 是否提供快速开始和运行示例 | PARTIAL | MEDIUM | 3.0/6.0 | E-005 | 部分证据：E-005（README.md:8）：“pip install -r requirements.txt”；现有证据不足以完全满足该项。 |
| DOC-03 | 文档可复现 | 是否提供测试、CI 或一键复现脚本 | MISSING | LOW | 0.0/6.0 | - | 未找到可引用证据，因此该项不能判定为通过。 |
| LLM-01 | LLM 特有风险 | 是否记录模型/API 版本 | PASS | HIGH | 6.0/6.0 | E-006, E-007 | 支持证据：E-006（README.md:17）：“This demo uses an OpenAI-compatible model and a local vector store. The knowledge base ...”；E-007（configs/app.yaml:3）：“name: gpt-4o-mini”。 |
| LLM-02 | LLM 特有风险 | 是否对 prompt/template 进行版本记录 | PARTIAL | MEDIUM | 3.0/6.0 | E-004 | 部分证据：E-004（prompts/system.txt:1）：“You are a helpful assistant. Answer using the retrieved context.”；现有证据不足以完全满足该项。 |
| LLM-03 | LLM 特有风险 | 是否记录采样参数 | PASS | HIGH | 5.0/5.0 | E-008, E-003, E-004 | 支持证据：E-008（configs/app.yaml:4）：“temperature: 0.2”；E-003（configs/app.yaml:1）：“model:”；E-004（prompts/system.txt:1）：“You are a helpful assistant. Answer using the retrieved context.”。 |
| LLM-04 | LLM 特有风险 | 是否记录 tokenizer/上下文窗口 | PARTIAL | MEDIUM | 2.0/4.0 | E-008 | 部分证据：E-008（configs/app.yaml:4）：“temperature: 0.2”；现有证据不足以完全满足该项。 |
| LLM-05 | LLM 特有风险 | 是否记录 RAG 索引/知识库版本 | PASS | HIGH | 5.0/5.0 | E-012, E-010, E-009 | 支持证据：E-012（configs/app.yaml:9）：“embedding_model: text-embedding-3-small”；E-010（configs/app.yaml:8）：“vector_store: faiss”；E-009（README.md:1）：“# Demo LLM RAG App”。 |
| LLM-06 | LLM 特有风险 | 是否记录 Agent 工具调用轨迹 | PARTIAL | MEDIUM | 2.5/5.0 | E-011 | 部分证据：E-011（README.md:3）：“A small retrieval-augmented agent demo.”；现有证据不足以完全满足该项。 |
| LLM-07 | LLM 特有风险 | 是否说明评测集、数据划分和污染风险 | MISSING | LOW | 0.0/6.0 | - | 未找到可引用证据，因此该项不能判定为通过。 |
| LLM-08 | LLM 特有风险 | 是否说明推理成本或延迟 | PARTIAL | MEDIUM | 2.0/4.0 | E-006 | 部分证据：E-006（README.md:17）：“This demo uses an OpenAI-compatible model and a local vector store. The knowledge base ...”；现有证据不足以完全满足该项。 |

## Claim-Evidence Matrix

**读表方法：** 每一行先看 README 说了什么，再看验证状态、检查依据、缺口和支持证据。括号内是内部编号对应的中文含义。

| 声明编号 | README 声明 | 验证状态 | 检查依据（需要检查的项） | 还缺什么（缺口） | 支持证据 | 验证说明 |
|---|---|---|---|---|---|---|
| C-001 | A small retrieval-augmented agent demo. | 已验证 | LLM-05（是否记录 RAG 索引/知识库版本） | - | `E-012` configs/app.yaml:9：embedding_model: text-embedding-3-small<br>`E-010` configs/app.yaml:8：vector_store: faiss<br>`E-009` README.md:1：# Demo LLM RAG App | 相关检查项均通过，这条 README 声明有证据支持。 |
| C-002 | This demo uses an OpenAI-compatible model and a local vector store. The knowledge base is under data/. | 已验证 | LLM-01（是否记录模型/API 版本）；LLM-03（是否记录采样参数）；LLM-05（是否记录 RAG 索引/知识库版本）；MODEL-02（是否提供模型卡或版本说明） | - | `E-006` README.md:17：This demo uses an OpenAI-compatible model and a local vector store. The knowledge base ...<br>`E-007` configs/app.yaml:3：name: gpt-4o-mini<br>`E-008` configs/app.yaml:4：temperature: 0.2<br>`E-003` configs/app.yaml:1：model:<br>`E-004` prompts/system.txt:1：You are a helpful assistant. Answer using the retrieved context.<br>`E-012` configs/app.yaml:9：embedding_model: text-embedding-3-small<br>`E-010` configs/app.yaml:8：vector_store: faiss<br>`E-009` README.md:1：# Demo LLM RAG App | 相关检查项均通过，这条 README 声明有证据支持。 |

## Findings

### F-001 [MEDIUM] 是否锁定依赖版本或提供容器化配置

- Criterion: `ENV-02`
- Message: 有依赖清单，但没有锁定文件或容器配置。
- Evidence: `E-002`

### F-002 [HIGH] 是否说明数据来源和获取方式

- Criterion: `DATA-01`
- Message: 没有数据来源说明。
- Evidence: none

### F-003 [HIGH] 是否提供数据下载或预处理脚本

- Criterion: `DATA-02`
- Message: 没有数据下载或预处理脚本。
- Evidence: none

### F-004 [MEDIUM] 是否提供数据集卡或数据许可说明

- Criterion: `DATA-03`
- Message: 没有数据集卡或明确的数据许可说明。
- Evidence: none

### F-005 [MEDIUM] 是否说明模型许可和来源

- Criterion: `MODEL-03`
- Message: 没有模型许可或来源说明。
- Evidence: none

### F-006 [HIGH] 是否提供训练或主运行脚本

- Criterion: `EXP-01`
- Message: 没有训练脚本或主运行命令。
- Evidence: none

### F-007 [HIGH] 是否提供评测脚本或评测命令

- Criterion: `EXP-02`
- Message: 没有评测脚本或评测命令。
- Evidence: none

### F-008 [MEDIUM] 是否设置并说明随机种子

- Criterion: `EXP-03`
- Message: 有采样参数，但没有明确随机种子或确定性设置。
- Evidence: `E-008`

### F-009 [HIGH] 是否给出预期结果和指标

- Criterion: `EXP-05`
- Message: 没有预期结果或指标。
- Evidence: none

### F-010 [MEDIUM] 是否提供快速开始和运行示例

- Criterion: `DOC-02`
- Message: 只有安装或运行说明中的一项。
- Evidence: `E-005`

### F-011 [MEDIUM] 是否提供测试、CI 或一键复现脚本

- Criterion: `DOC-03`
- Message: 没有测试、CI 或一键复现脚本。
- Evidence: none

### F-012 [MEDIUM] 是否对 prompt/template 进行版本记录

- Criterion: `LLM-02`
- Message: 有 prompt 文件或描述，但没有可核验的版本信息。
- Evidence: `E-004`

### F-013 [MEDIUM] 是否记录 tokenizer/上下文窗口

- Criterion: `LLM-04`
- Message: 有相关配置，但 tokenizer/上下文窗口仍需补充。
- Evidence: `E-008`

### F-014 [MEDIUM] 是否记录 Agent 工具调用轨迹

- Criterion: `LLM-06`
- Message: 检测到 Agent 项目，但完整调用轨迹仍需补充。
- Evidence: `E-011`

### F-015 [MEDIUM] 是否说明评测集、数据划分和污染风险

- Criterion: `LLM-07`
- Message: 没有说明评测集、数据划分或污染风险。
- Evidence: none

### F-016 [MEDIUM] 是否说明推理成本或延迟

- Criterion: `LLM-08`
- Message: 有成本/硬件线索，但仍需量化数据。
- Evidence: `E-006`

## Execution Evidence

| Probe | Status | Return code | Duration | Command |
|---|---|---:|---:|---|
| python-syntax | PASS | 0 | 0.061s | `C:\Program Files\Python313\python.exe -c import ast, pathlib, sys ignore={'.git','.venv','venv','node_modules','__pycache__','.mypy_cache','.pytest_cache','dist','build'} bad=[] fo` |

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
- `E-005` [instruction] `README.md:8` — pip install -r requirements.txt
- `E-006` [llm-provider] `README.md:17` — This demo uses an OpenAI-compatible model and a local vector store. The knowledge base is under `data/`.
- `E-007` [model] `configs/app.yaml:3` — name: gpt-4o-mini
- `E-008` [llm-config] `configs/app.yaml:4` — temperature: 0.2
- `E-009` [rag] `README.md:1` — # Demo LLM RAG App
- `E-010` [rag] `configs/app.yaml:8` — vector_store: faiss
- `E-011` [agent] `README.md:3` — A small retrieval-augmented agent demo.
- `E-012` [rag] `configs/app.yaml:9` — embedding_model: text-embedding-3-small
- `E-013` [claim] `README.md:3` — A small retrieval-augmented agent demo.
- `E-014` [claim] `README.md:17` — This demo uses an OpenAI-compatible model and a local vector store. The knowledge base is under data/.

## Scope and Limitations

- This is static reproduction readiness analysis, not proof that the project reproduces successfully.
- No untrusted repository code is executed by default.
- Execution probes are optional and require explicit --execute; GitHub Action integration is available in the repository.
- AI-generated explanations must be reviewed by the team before submission or release.
