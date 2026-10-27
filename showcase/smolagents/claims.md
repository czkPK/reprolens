# ReproLens 声明—证据—缺口矩阵

- Repository: `https://github.com/huggingface/smolagents @ 96f33faaf028`
- Generated at: `2026-10-27T14:38:51.282918+00:00`
- Evidence coverage: **15/16 (93.8%)**
- Claims extracted: **8**

## Matrix

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

## Status Definitions

- **已验证**：相关检查项全部通过，并且有证据支持。
- **部分验证**：找到部分证据，但仍有缺口。
- **未验证**：关键证据缺失，当前声明不能视为已验证。
- **不适用**：相关检查项不适用于当前项目类型。

读表方法：Claim 是 README 原句；Required criteria 是验证这句话需要检查的项；Gaps 是仍未满足的检查项；Evidence 是支持证据编号。该矩阵不执行第三方代码，也不保证语义完全正确。
