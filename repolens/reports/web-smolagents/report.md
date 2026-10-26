# ReproLens Audit Report

- Repository: `https://github.com/huggingface/smolagents @ 96f33faaf028`
- Generated at: `2026-10-26T13:19:39.679427+00:00`
- Semantic claim mapping: **rules-fallback**
- Source: [https://github.com/huggingface/smolagents](https://github.com/huggingface/smolagents)
- Source commit: `96f33faaf028479119ec8d34507b47694cf14e34`
- Files scanned: **185**
- Overall score: **78.8 / 100**
- Readiness: **Partially Ready**
- Evidence coverage: **15/16 (93.8%)**
- README claims audited: **8**

## Dimension Scores

| Dimension | Points | Max | Percent |
|---|---:|---:|---:|
| 环境可复现 | 21.0 | 25.0 | 84.0% |
| 数据可复现 | 0.0 | 0.0 | 100.0% |
| 模型可复现 | 0.0 | 0.0 | 100.0% |
| 实验可复现 | 27.0 | 27.0 | 100.0% |
| 文档可复现 | 17.0 | 17.0 | 100.0% |
| LLM 特有风险 | 13.0 | 30.0 | 43.3% |

## Top 3 Priority Actions

1. **记录 tokenizer、上下文窗口和截断策略** — expected gain **+4.0**; 避免输入长度和分词差异导致结果变化。
2. **添加锁文件或 Dockerfile，固定 Python、CUDA 和依赖版本** — expected gain **+4.0**; 消除环境版本漂移，提升跨机器复现概率。
3. **将 prompt/template 版本化并记录在配置或模型卡中** — expected gain **+3.0**; 避免 prompt 漂移导致结果不可复现。

## Criteria

| ID | Dimension | Criterion | Status | Confidence | Points | Evidence |
|---|---|---|---|---|---:|---|
| ENV-01 | 环境可复现 | 存在依赖清单 | PASS | MEDIUM | 10.0/10.0 | E-002 |
| ENV-02 | 环境可复现 | 依赖版本锁定或容器化 | PARTIAL | MEDIUM | 4.0/8.0 | E-002 |
| ENV-03 | 环境可复现 | 提供安装步骤 | PASS | MEDIUM | 7.0/7.0 | E-008 |
| DATA-01 | 数据可复现 | 说明数据来源和获取方式 | N/A | N/A | 0.0/8.0 | E-010 |
| DATA-02 | 数据可复现 | 提供数据下载或预处理脚本 | N/A | N/A | 0.0/8.0 | E-010 |
| DATA-03 | 数据可复现 | 提供数据集卡或数据许可说明 | N/A | N/A | 0.0/6.0 | E-003, E-010 |
| MODEL-01 | 模型可复现 | 提供模型权重、API 或获取方式 | N/A | N/A | 0.0/8.0 | E-017, E-013, E-018 |
| MODEL-02 | 模型可复现 | 提供模型卡或版本说明 | N/A | N/A | 0.0/8.0 | E-013, E-018 |
| MODEL-03 | 模型可复现 | 说明模型许可和来源 | N/A | N/A | 0.0/6.0 | E-003 |
| EXP-01 | 实验可复现 | 提供训练或主运行脚本 | PASS | MEDIUM | 7.0/7.0 | E-009 |
| EXP-02 | 实验可复现 | 提供评测脚本或评测命令 | PASS | HIGH | 8.0/8.0 | E-005, E-004 |
| EXP-03 | 实验可复现 | 设置并说明随机种子 | N/A | N/A | 0.0/6.0 | - |
| EXP-04 | 实验可复现 | 说明硬件或 API 环境要求 | PASS | HIGH | 5.0/5.0 | E-012, E-017 |
| EXP-05 | 实验可复现 | 给出预期结果和指标 | PASS | HIGH | 7.0/7.0 | E-011, E-021 |
| DOC-01 | 文档可复现 | 存在 README | PASS | MEDIUM | 5.0/5.0 | E-001 |
| DOC-02 | 文档可复现 | 提供快速开始和运行示例 | PASS | HIGH | 6.0/6.0 | E-008, E-009 |
| DOC-03 | 文档可复现 | 提供测试、CI 或一键复现脚本 | PASS | HIGH | 6.0/6.0 | E-005, E-004, E-006 |
| LLM-01 | LLM 特有风险 | 记录模型/API 版本 | N/A | N/A | 0.0/6.0 | E-017, E-013, E-018 |
| LLM-02 | LLM 特有风险 | prompt/template 有版本记录 | PARTIAL | MEDIUM | 3.0/6.0 | E-007, E-014 |
| LLM-03 | LLM 特有风险 | 记录采样参数 | PARTIAL | MEDIUM | 2.5/5.0 | E-007 |
| LLM-04 | LLM 特有风险 | 记录 tokenizer/上下文窗口 | MISSING | LOW | 0.0/4.0 | - |
| LLM-05 | LLM 特有风险 | RAG 索引/知识库有版本记录 | N/A | N/A | 0.0/5.0 | E-019 |
| LLM-06 | LLM 特有风险 | Agent 工具调用轨迹可追溯 | PARTIAL | MEDIUM | 2.5/5.0 | E-020 |
| LLM-07 | LLM 特有风险 | 说明评测集、数据划分和污染风险 | PARTIAL | MEDIUM | 3.0/6.0 | E-021, E-015 |
| LLM-08 | LLM 特有风险 | 说明推理成本或延迟 | PARTIAL | MEDIUM | 2.0/4.0 | E-016, E-012, E-017 |

## Claim-Evidence Matrix

README claims are mapped to the criteria that must be supported before the claim can be treated as reproducible.

| Claim | Status | Required criteria | Gaps | Evidence |
|---|---|---|---|---|
| 🧑‍💻 First-class support for Code Agents. Our CodeAgent writes its actions in code (as opposed to "agents being used to write code"). To make it secure, we support executing in sandboxed environments via Blaxel, E2B, Modal, or Docker. | VERIFIED | DOC-02, ENV-01, ENV-03 | - | E-008, E-009, E-002 |
| 🌐 Model-agnostic: smolagents supports any LLM. It can be a local transformers or ollama model, one of many providers on the Hub, or any model from OpenAI, Anthropic and many others via our LiteLLM integration. | PARTIALLY VERIFIED | LLM-01, LLM-03, MODEL-02 | LLM-03 | E-017, E-013, E-018, E-007 |
| OpenAI-compatible servers: Together AI | PARTIALLY VERIFIED | LLM-01, LLM-03, MODEL-02 | LLM-03 | E-017, E-013, E-018, E-007 |
| OpenAI-compatible servers: OpenRouter | PARTIALLY VERIFIED | LLM-01, LLM-03, MODEL-02 | LLM-03 | E-017, E-013, E-018, E-007 |
| Actions are now Python code snippets. Hence, tool calls will be performed as Python function calls. For instance, here is how the agent can perform web search over several websites in one single action: | PARTIALLY VERIFIED | LLM-06 | LLM-06 | E-020 |
| Docker — self-hosted container isolation | VERIFIED | DOC-02, ENV-01, ENV-03 | - | E-008, E-009, E-002 |
| Still, we implement several types of agents: CodeAgent writes its actions as Python code snippets, and the more classic ToolCallingAgent leverages built-in tool calling methods. We also have multi-agent hierarchies, import from tool collect | PARTIALLY VERIFIED | LLM-05, LLM-06 | LLM-06 | E-019, E-020 |
| By the way, why use a framework at all? Well, because a big part of this stuff is non-trivial. For instance, the code agent has to keep a consistent format for code throughout its system prompt, its parser, the execution. So our framework h | VERIFIED | DOC-02, DOC-03, EXP-02 | - | E-008, E-009, E-005, E-004, E-006 |

## Findings

### F-001 [MEDIUM] 依赖版本锁定或容器化

- Criterion: `ENV-02`
- Message: 有依赖清单，但没有锁定文件或容器配置。
- Evidence: `E-002`

### F-002 [MEDIUM] prompt/template 有版本记录

- Criterion: `LLM-02`
- Message: 有 prompt 文件或描述，但没有可核验的版本信息。
- Evidence: `E-007`, `E-014`

### F-003 [MEDIUM] 记录采样参数

- Criterion: `LLM-03`
- Message: 有采样参数或配置线索，但仍需补充可核验值。
- Evidence: `E-007`

### F-004 [MEDIUM] 记录 tokenizer/上下文窗口

- Criterion: `LLM-04`
- Message: 没有记录 tokenizer 或上下文窗口。
- Evidence: none

### F-005 [MEDIUM] Agent 工具调用轨迹可追溯

- Criterion: `LLM-06`
- Message: 检测到 Agent 项目，但完整调用轨迹仍需补充。
- Evidence: `E-020`

### F-006 [MEDIUM] 说明评测集、数据划分和污染风险

- Criterion: `LLM-07`
- Message: 只覆盖了评测集/划分/污染中的一部分，或仍有占位内容。
- Evidence: `E-021`, `E-015`

### F-007 [MEDIUM] 说明推理成本或延迟

- Criterion: `LLM-08`
- Message: 有成本/硬件线索，但仍需量化数据。
- Evidence: `E-016`, `E-012`, `E-017`

## Execution Evidence

| Probe | Status | Return code | Duration | Command |
|---|---|---:|---:|---|
| python-syntax | PASS | 0 | 0.185s | `C:\Program Files\Python313\python.exe -c import ast, pathlib, sys ignore={'.git','.venv','venv','node_modules','__pycache__','.mypy_cache','.pytest_cache','dist','build'} bad=[] fo` |

## Minimal Remediation Plan

### F-004 - 记录 tokenizer、上下文窗口和截断策略

- Rationale: 避免输入长度和分词差异导致结果变化。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+4.0**
- Evidence: none

### F-001 - 添加锁文件或 Dockerfile，固定 Python、CUDA 和依赖版本

- Rationale: 消除环境版本漂移，提升跨机器复现概率。
- Cost: **medium**
- Impact: **high**
- Estimated score gain: **+4.0**
- Evidence: `E-002`

### F-002 - 将 prompt/template 版本化并记录在配置或模型卡中

- Rationale: 避免 prompt 漂移导致结果不可复现。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+3.0**
- Evidence: `E-007`, `E-014`

### F-006 - 说明评测集、数据划分和污染/泄漏风险

- Rationale: 让指标具有可比性，避免高估效果。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+3.0**
- Evidence: `E-021`, `E-015`

### F-003 - 记录 temperature、top_p、max_tokens 等采样参数

- Rationale: 让生成行为可以复现和比较。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+2.5**
- Evidence: `E-007`

### F-005 - 保存 Agent 工具调用轨迹、run_id 和关键日志

- Rationale: 让多步调用过程可以审计。
- Cost: **medium**
- Impact: **high**
- Estimated score gain: **+2.5**
- Evidence: `E-020`

### F-007 - 说明推理成本、延迟和 token 消耗

- Rationale: 让读者评估复现成本。
- Cost: **low**
- Impact: **low**
- Estimated score gain: **+2.0**
- Evidence: `E-016`, `E-012`, `E-017`

## Evidence Appendix

- `E-001` [readme] `README.md:1` — <!---
- `E-002` [dependency-manifest] `pyproject.toml:1` — [build-system]
- `E-003` [license] `LICENSE:1` — Apache License
- `E-004` [ci] `.github/workflows/build_documentation.yml:1` — name: Build documentation
- `E-005` [tests] `tests/conftest.py:1` — from unittest.mock import patch
- `E-006` [script] `Makefile:1` — .PHONY: quality style test docs
- `E-007` [prompt] `src/smolagents/prompts/code_agent.yaml:1` — system_prompt: |-
- `E-008` [instruction] `README.md:57` — pip install
- `E-009` [instruction] `README.md:38` — make it secure, we support executing in sandboxed environments via [Blaxel](https://blaxel.ai), [E2B](https://e2b.dev/), [Modal](https://modal.com/), or Docker.
- `E-010` [data] `README.md:8` — http://
- `E-011` [metric] `docs/README.md:264` — expected
- `E-012` [hardware] `docs/source/en/guided_tour.md:201` — VRAM
- `E-013` [model] `README.md:2` — HuggingFace
- `E-014` [prompt] `README.md:182` — prompt
- `E-015` [evaluation] `docs/README.md:243` — split
- `E-016` [cost] `docs/source/en/tutorials/building_good_agents.md:21` — cost
- `E-017` [llm-provider] `README.md:2` — HuggingFace
- `E-018` [model] `README.md:42` — llama
- `E-019` [rag] `docs/source/zh/conceptual_guides/intro_agents.md:64` — RAG
- `E-020` [agent] `README.md:46` — MCP
- `E-021` [evaluation] `README.md:239` — benchmark
- `E-022` [claim] `README.md:38` — 🧑‍💻 First-class support for Code Agents. Our CodeAgent writes its actions in code (as opposed to "agents being used to write code"). To make it secure, we support executing in sandboxed environments via Blaxel, E2B, Modal, or Docker.
- `E-023` [claim] `README.md:42` — 🌐 Model-agnostic: smolagents supports any LLM. It can be a local transformers or ollama model, one of many providers on the Hub, or any model from OpenAI, Anthropic and many others via our LiteLLM integration.
- `E-024` [claim] `README.md:106` — OpenAI-compatible servers: Together AI
- `E-025` [claim] `README.md:120` — OpenAI-compatible servers: OpenRouter
- `E-026` [claim] `README.md:232` — Actions are now Python code snippets. Hence, tool calls will be performed as Python function calls. For instance, here is how the agent can perform web search over several websites in one single action:
- `E-027` [claim] `README.md:243` — Docker — self-hosted container isolation
- `E-028` [claim] `README.md:252` — Still, we implement several types of agents: CodeAgent writes its actions as Python code snippets, and the more classic ToolCallingAgent leverages built-in tool calling methods. We also have multi-agent hierarchies, import from tool collect
- `E-029` [claim] `README.md:254` — By the way, why use a framework at all? Well, because a big part of this stuff is non-trivial. For instance, the code agent has to keep a consistent format for code throughout its system prompt, its parser, the execution. So our framework h

## Scope and Limitations

- This is static reproduction readiness analysis, not proof that the project reproduces successfully.
- No untrusted repository code is executed by default.
- Execution probes are optional and require explicit --execute; GitHub Action integration is available in the repository.
- AI-generated explanations must be reviewed by the team before submission or release.
