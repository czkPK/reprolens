# ReproLens Audit Report

- Repository: `https://github.com/huggingface/smolagents @ 96f33faaf028`
- Generated at: `2026-10-27T14:38:51.282918+00:00`
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

| 检查项编号 | 所属维度 | 检查要求 | 状态 | 证据强度 | 得分 | 证据编号 | 证据说明 |
|---|---|---|---|---|---:|---|---|

**读表说明：** PASS = 满足要求；PARTIAL = 只有部分证据；MISSING = 应有但没有找到；N/A = 当前项目类型不适用。Confidence 表示证据支持强度，不代表项目整体质量。

| ENV-01 | 环境可复现 | 是否存在依赖清单 | PASS | MEDIUM | 10.0/10.0 | E-002 | 支持证据：E-002（pyproject.toml:1）：“[build-system]”。 |
| ENV-02 | 环境可复现 | 是否锁定依赖版本或提供容器化配置 | PARTIAL | MEDIUM | 4.0/8.0 | E-002 | 部分证据：E-002（pyproject.toml:1）：“[build-system]”；现有证据不足以完全满足该项。 |
| ENV-03 | 环境可复现 | 是否提供安装步骤 | PASS | MEDIUM | 7.0/7.0 | E-008 | 支持证据：E-008（README.md:57）：“pip install "smolagents[toolkit]"”。 |
| DATA-01 | 数据可复现 | 是否说明数据来源和获取方式 | N/A | N/A | 0.0/8.0 | E-010 | 这是一个模型无关的 Agent 框架，自身不拥有训练数据集，因此不需要提供项目自己的数据下载地址、预处理脚本或数据集卡。 列出的 E-010 只是判断项目类型时看到的识别线索。 |
| DATA-02 | 数据可复现 | 是否提供数据下载或预处理脚本 | N/A | N/A | 0.0/8.0 | E-010 | 这是一个模型无关的 Agent 框架，自身不拥有训练数据集，因此不需要提供项目自己的数据下载地址、预处理脚本或数据集卡。 列出的 E-010 只是判断项目类型时看到的识别线索。 |
| DATA-03 | 数据可复现 | 是否提供数据集卡或数据许可说明 | N/A | N/A | 0.0/6.0 | E-003, E-010 | 这是一个模型无关的 Agent 框架，自身不拥有训练数据集，因此不需要提供项目自己的数据下载地址、预处理脚本或数据集卡。 列出的 E-003、E-010 只是判断项目类型时看到的识别线索。 |
| MODEL-01 | 模型可复现 | 是否提供模型权重、API 或获取方式 | N/A | N/A | 0.0/8.0 | E-017, E-013, E-018 | 这是一个模型无关的 Agent 框架，自身不提供模型权重或模型卡，模型由外部提供方管理，因此不需要提供自有模型卡。 列出的 E-017、E-013、E-018 只是判断项目类型时看到的识别线索。 |
| MODEL-02 | 模型可复现 | 是否提供模型卡或版本说明 | N/A | N/A | 0.0/8.0 | E-013, E-018 | 这是一个模型无关的 Agent 框架，自身不提供模型权重或模型卡，模型由外部提供方管理，因此不需要提供自有模型卡。 列出的 E-013、E-018 只是判断项目类型时看到的识别线索。 |
| MODEL-03 | 模型可复现 | 是否说明模型许可和来源 | N/A | N/A | 0.0/6.0 | E-003 | 这是一个模型无关的 Agent 框架，自身不提供模型权重或模型卡，模型由外部提供方管理，因此不需要提供自有模型卡。 列出的 E-003 只是判断项目类型时看到的识别线索。 |
| EXP-01 | 实验可复现 | 是否提供训练或主运行脚本 | PASS | MEDIUM | 7.0/7.0 | E-009 | 支持证据：E-009（README.md:38）：“🧑‍💻 **First-class support for Code Agents**. Our [`CodeAgent`](https://huggingface.co/d...”。 |
| EXP-02 | 实验可复现 | 是否提供评测脚本或评测命令 | PASS | HIGH | 8.0/8.0 | E-005, E-004 | 支持证据：E-005（tests/conftest.py:1）：“from unittest.mock import patch”；E-004（.github/workflows/build_documentation.yml:1）：“name: Build documentation”。 |
| EXP-03 | 实验可复现 | 是否设置并说明随机种子 | N/A | N/A | 0.0/6.0 | - | 这是一个模型无关的 Agent 框架，不训练固定模型，因此不需要设置训练随机种子。 |
| EXP-04 | 实验可复现 | 是否说明硬件或 API 环境要求 | PASS | HIGH | 5.0/5.0 | E-012, E-017 | 支持证据：E-012（docs/source/en/guided_tour.md:201）：“num_ctx=8192, # ollama default is 2048 which will fail horribly. 8192 works for easy ta...”；E-017（README.md:2）：“Copyright 2024 The HuggingFace Team. All rights reserved.”。 |
| EXP-05 | 实验可复现 | 是否给出预期结果和指标 | PASS | HIGH | 7.0/7.0 | E-011, E-021 | 支持证据：E-011（docs/README.md:264）：“is to be used in inference and also include the expected (ideally sensible)”；E-021（README.md:239）：“Writing actions as code snippets is demonstrated to work better than the current indust...”。 |
| DOC-01 | 文档可复现 | 是否存在 README | PASS | MEDIUM | 5.0/5.0 | E-001 | 支持证据：E-001（README.md:1）：“<!---”。 |
| DOC-02 | 文档可复现 | 是否提供快速开始和运行示例 | PASS | HIGH | 6.0/6.0 | E-008, E-009 | 支持证据：E-008（README.md:57）：“pip install "smolagents[toolkit]"”；E-009（README.md:38）：“🧑‍💻 **First-class support for Code Agents**. Our [`CodeAgent`](https://huggingface.co/d...”。 |
| DOC-03 | 文档可复现 | 是否提供测试、CI 或一键复现脚本 | PASS | HIGH | 6.0/6.0 | E-005, E-004, E-006 | 支持证据：E-005（tests/conftest.py:1）：“from unittest.mock import patch”；E-004（.github/workflows/build_documentation.yml:1）：“name: Build documentation”；E-006（Makefile:1）：“.PHONY: quality style test docs”。 |
| LLM-01 | LLM 特有风险 | 是否记录模型/API 版本 | N/A | N/A | 0.0/6.0 | E-017, E-013, E-018 | 这是一个模型无关的 Agent 框架，不具备该检查项对应的项目产物，因此这项检查不适用。 列出的 E-017、E-013、E-018 只是判断项目类型时看到的识别线索。 |
| LLM-02 | LLM 特有风险 | 是否对 prompt/template 进行版本记录 | PARTIAL | MEDIUM | 3.0/6.0 | E-007, E-014 | 部分证据：E-007（src/smolagents/prompts/code_agent.yaml:1）：“system_prompt: \|-”；E-014（README.md:182）：“# Run with direct prompt and options”；现有证据不足以完全满足该项。 |
| LLM-03 | LLM 特有风险 | 是否记录采样参数 | PARTIAL | MEDIUM | 2.5/5.0 | E-007 | 部分证据：E-007（src/smolagents/prompts/code_agent.yaml:1）：“system_prompt: \|-”；现有证据不足以完全满足该项。 |
| LLM-04 | LLM 特有风险 | 是否记录 tokenizer/上下文窗口 | MISSING | LOW | 0.0/4.0 | - | 未找到可引用证据，因此该项不能判定为通过。 |
| LLM-05 | LLM 特有风险 | 是否记录 RAG 索引/知识库版本 | N/A | N/A | 0.0/5.0 | E-019 | 这是一个模型无关的 Agent 框架，自身不维护固定的 RAG 索引或知识库，因此不需要提供索引版本。 列出的 E-019 只是判断项目类型时看到的识别线索。 |
| LLM-06 | LLM 特有风险 | 是否记录 Agent 工具调用轨迹 | PARTIAL | MEDIUM | 2.5/5.0 | E-020 | 部分证据：E-020（README.md:46）：“🛠️ **Tool-agnostic**: you can use tools from any [MCP server](https://huggingface.co/do...”；现有证据不足以完全满足该项。 |
| LLM-07 | LLM 特有风险 | 是否说明评测集、数据划分和污染风险 | PARTIAL | MEDIUM | 3.0/6.0 | E-021, E-015 | 部分证据：E-021（README.md:239）：“Writing actions as code snippets is demonstrated to work better than the current indust...”；E-015（docs/README.md:243）：“>>> dataset = load_dataset("hf-internal-testing/librispeech_asr_demo", "clean", split="...”；现有证据不足以完全满足该项。 |
| LLM-08 | LLM 特有风险 | 是否说明推理成本或延迟 | PARTIAL | MEDIUM | 2.0/4.0 | E-016, E-012, E-017 | 部分证据：E-016（docs/source/en/tutorials/building_good_agents.md:21）：“This will reduce costs, latency, and error risk!”；E-012（docs/source/en/guided_tour.md:201）：“num_ctx=8192, # ollama default is 2048 which will fail horribly. 8192 works for easy ta...”；E-017（README.md:2）：“Copyright 2024 The HuggingFace Team. All rights reserved.”；现有证据不足以完全满足该项。 |

## Claim-Evidence Matrix

**读表方法：** 每一行先看 README 说了什么，再看验证状态、检查依据、缺口和支持证据。括号内是内部编号对应的中文含义。

| 声明编号 | README 声明 | 验证状态 | 检查依据（需要检查的项） | 还缺什么（缺口） | 支持证据 | 验证说明 |
|---|---|---|---|---|---|---|
| C-001 | 🧑‍💻 First-class support for Code Agents. Our CodeAgent writes its actions in code (as opposed to "agents being used to write code"). To make it secure, we support executing in sandboxed environments via Blaxel, E2B, Modal, or Docker. | 已验证 | DOC-02（是否提供快速开始和运行示例）；ENV-01（是否存在依赖清单）；ENV-03（是否提供安装步骤） | - | `E-008` README.md:57：pip install "smolagents[toolkit]"<br>`E-009` README.md:38：🧑‍💻 **First-class support for Code Agents**. Our [`CodeAgent`](https://huggingface.co/d...<br>`E-002` pyproject.toml:1：[build-system] | 相关检查项均通过，这条 README 声明有证据支持。 |
| C-002 | 🌐 Model-agnostic: smolagents supports any LLM. It can be a local transformers or ollama model, one of many providers on the Hub, or any model from OpenAI, Anthropic and many others via our LiteLLM integration. | 部分验证 | LLM-01（是否记录模型/API 版本）；LLM-03（是否记录采样参数）；MODEL-02（是否提供模型卡或版本说明） | LLM-03（是否记录采样参数） | `E-017` README.md:2：Copyright 2024 The HuggingFace Team. All rights reserved.<br>`E-013` README.md:2：Copyright 2024 The HuggingFace Team. All rights reserved.<br>`E-018` README.md:42：🌐 **Model-agnostic**: smolagents supports any LLM. It can be a local `transformers` or ...<br>`E-007` src/smolagents/prompts/code_agent.yaml:1：system_prompt: \|- | 找到部分证据，但仍有缺口：LLM-03（是否记录采样参数）。 |
| C-003 | OpenAI-compatible servers: Together AI | 部分验证 | LLM-01（是否记录模型/API 版本）；LLM-03（是否记录采样参数）；MODEL-02（是否提供模型卡或版本说明） | LLM-03（是否记录采样参数） | `E-017` README.md:2：Copyright 2024 The HuggingFace Team. All rights reserved.<br>`E-013` README.md:2：Copyright 2024 The HuggingFace Team. All rights reserved.<br>`E-018` README.md:42：🌐 **Model-agnostic**: smolagents supports any LLM. It can be a local `transformers` or ...<br>`E-007` src/smolagents/prompts/code_agent.yaml:1：system_prompt: \|- | 找到部分证据，但仍有缺口：LLM-03（是否记录采样参数）。 |
| C-004 | OpenAI-compatible servers: OpenRouter | 部分验证 | LLM-01（是否记录模型/API 版本）；LLM-03（是否记录采样参数）；MODEL-02（是否提供模型卡或版本说明） | LLM-03（是否记录采样参数） | `E-017` README.md:2：Copyright 2024 The HuggingFace Team. All rights reserved.<br>`E-013` README.md:2：Copyright 2024 The HuggingFace Team. All rights reserved.<br>`E-018` README.md:42：🌐 **Model-agnostic**: smolagents supports any LLM. It can be a local `transformers` or ...<br>`E-007` src/smolagents/prompts/code_agent.yaml:1：system_prompt: \|- | 找到部分证据，但仍有缺口：LLM-03（是否记录采样参数）。 |
| C-005 | Actions are now Python code snippets. Hence, tool calls will be performed as Python function calls. For instance, here is how the agent can perform web search over several websites in one single action: | 部分验证 | LLM-06（是否记录 Agent 工具调用轨迹） | LLM-06（是否记录 Agent 工具调用轨迹） | `E-020` README.md:46：🛠️ **Tool-agnostic**: you can use tools from any [MCP server](https://huggingface.co/do... | 找到部分证据，但仍有缺口：LLM-06（是否记录 Agent 工具调用轨迹）。 |
| C-006 | Docker — self-hosted container isolation | 已验证 | DOC-02（是否提供快速开始和运行示例）；ENV-01（是否存在依赖清单）；ENV-03（是否提供安装步骤） | - | `E-008` README.md:57：pip install "smolagents[toolkit]"<br>`E-009` README.md:38：🧑‍💻 **First-class support for Code Agents**. Our [`CodeAgent`](https://huggingface.co/d...<br>`E-002` pyproject.toml:1：[build-system] | 相关检查项均通过，这条 README 声明有证据支持。 |
| C-007 | Still, we implement several types of agents: CodeAgent writes its actions as Python code snippets, and the more classic ToolCallingAgent leverages built-in tool calling methods. We also have multi-agent hierarchies, import from tool collect | 部分验证 | LLM-05（是否记录 RAG 索引/知识库版本）；LLM-06（是否记录 Agent 工具调用轨迹） | LLM-06（是否记录 Agent 工具调用轨迹） | `E-019` docs/source/zh/conceptual_guides/intro_agents.md:64：在上面的例子中，你可以创建一个多步 agent，它可以访问天气 API 获取天气预报，Google Maps API 计算旅行距离，员工在线仪表板和你的知识库上的 RAG 系统。<br>`E-020` README.md:46：🛠️ **Tool-agnostic**: you can use tools from any [MCP server](https://huggingface.co/do... | 找到部分证据，但仍有缺口：LLM-06（是否记录 Agent 工具调用轨迹）。 |
| C-008 | By the way, why use a framework at all? Well, because a big part of this stuff is non-trivial. For instance, the code agent has to keep a consistent format for code throughout its system prompt, its parser, the execution. So our framework h | 已验证 | DOC-02（是否提供快速开始和运行示例）；DOC-03（是否提供测试、CI 或一键复现脚本）；EXP-02（是否提供评测脚本或评测命令） | - | `E-008` README.md:57：pip install "smolagents[toolkit]"<br>`E-009` README.md:38：🧑‍💻 **First-class support for Code Agents**. Our [`CodeAgent`](https://huggingface.co/d...<br>`E-005` tests/conftest.py:1：from unittest.mock import patch<br>`E-004` .github/workflows/build_documentation.yml:1：name: Build documentation<br>`E-006` Makefile:1：.PHONY: quality style test docs | 相关检查项均通过，这条 README 声明有证据支持。 |

## Findings

### F-001 [MEDIUM] 是否锁定依赖版本或提供容器化配置

- Criterion: `ENV-02`
- Message: 有依赖清单，但没有锁定文件或容器配置。
- Evidence: `E-002`

### F-002 [MEDIUM] 是否对 prompt/template 进行版本记录

- Criterion: `LLM-02`
- Message: 有 prompt 文件或描述，但没有可核验的版本信息。
- Evidence: `E-007`, `E-014`

### F-003 [MEDIUM] 是否记录采样参数

- Criterion: `LLM-03`
- Message: 有采样参数或配置线索，但仍需补充可核验值。
- Evidence: `E-007`

### F-004 [MEDIUM] 是否记录 tokenizer/上下文窗口

- Criterion: `LLM-04`
- Message: 没有记录 tokenizer 或上下文窗口。
- Evidence: none

### F-005 [MEDIUM] 是否记录 Agent 工具调用轨迹

- Criterion: `LLM-06`
- Message: 检测到 Agent 项目，但完整调用轨迹仍需补充。
- Evidence: `E-020`

### F-006 [MEDIUM] 是否说明评测集、数据划分和污染风险

- Criterion: `LLM-07`
- Message: 只覆盖了评测集/划分/污染中的一部分，或仍有占位内容。
- Evidence: `E-021`, `E-015`

### F-007 [MEDIUM] 是否说明推理成本或延迟

- Criterion: `LLM-08`
- Message: 有成本/硬件线索，但仍需量化数据。
- Evidence: `E-016`, `E-012`, `E-017`

## Execution Evidence

| Probe | Status | Return code | Duration | Command |
|---|---|---:|---:|---|
| python-syntax | PASS | 0 | 0.183s | `C:\Program Files\Python313\python.exe -c import ast, pathlib, sys ignore={'.git','.venv','venv','node_modules','__pycache__','.mypy_cache','.pytest_cache','dist','build'} bad=[] fo` |

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
- `E-008` [instruction] `README.md:57` — pip install "smolagents[toolkit]"
- `E-009` [instruction] `README.md:38` — 🧑‍💻 **First-class support for Code Agents**. Our [`CodeAgent`](https://huggingface.co/docs/smolagents/reference/agents#smolagents.CodeAgent) writes its actions in code (as opposed to "agents being used to write code"). To make it secure, we
- `E-010` [data] `README.md:8` — http://www.apache.org/licenses/LICENSE-2.0
- `E-011` [metric] `docs/README.md:264` — is to be used in inference and also include the expected (ideally sensible)
- `E-012` [hardware] `docs/source/en/guided_tour.md:201` — num_ctx=8192, # ollama default is 2048 which will fail horribly. 8192 works for easy tasks, more is better. Check https://huggingface.co/spaces/NyxKrage/LLM-Model-VRAM-Calculator to calculate how much VRAM this will need for the selected mo
- `E-013` [model] `README.md:2` — Copyright 2024 The HuggingFace Team. All rights reserved.
- `E-014` [prompt] `README.md:182` — # Run with direct prompt and options
- `E-015` [evaluation] `docs/README.md:243` — >>> dataset = load_dataset("hf-internal-testing/librispeech_asr_demo", "clean", split="validation")
- `E-016` [cost] `docs/source/en/tutorials/building_good_agents.md:21` — This will reduce costs, latency, and error risk!
- `E-017` [llm-provider] `README.md:2` — Copyright 2024 The HuggingFace Team. All rights reserved.
- `E-018` [model] `README.md:42` — 🌐 **Model-agnostic**: smolagents supports any LLM. It can be a local `transformers` or `ollama` model, one of [many providers on the Hub](https://huggingface.co/blog/inference-providers), or any model from OpenAI, Anthropic and many others 
- `E-019` [rag] `docs/source/zh/conceptual_guides/intro_agents.md:64` — 在上面的例子中，你可以创建一个多步 agent，它可以访问天气 API 获取天气预报，Google Maps API 计算旅行距离，员工在线仪表板和你的知识库上的 RAG 系统。
- `E-020` [agent] `README.md:46` — 🛠️ **Tool-agnostic**: you can use tools from any [MCP server](https://huggingface.co/docs/smolagents/reference/tools#smolagents.ToolCollection.from_mcp), from [LangChain](https://huggingface.co/docs/smolagents/reference/tools#smolagents.Too
- `E-021` [evaluation] `README.md:239` — Writing actions as code snippets is demonstrated to work better than the current industry practice of letting the LLM output a dictionary of the tools it wants to call: [uses 30% fewer steps](https://huggingface.co/papers/2402.01030) (thus 
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
