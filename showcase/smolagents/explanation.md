# ReproLens Explanation

当前复现就绪度为 **78.8/100（Partially Ready）**。
证据覆盖率为 **15/16（93.8%）**，共抽取 **8** 条 README 声明。

以下结论只基于仓库中已抽取到的证据，没有证据的内容不会被当作已验证事实。

## 声明验证

- `C-001` [已验证] 🧑‍💻 First-class support for Code Agents. Our CodeAgent writes its actions in code (as opposed to "agents being used to write code"). To make it secure, we support executing in sandboxed environments via Blaxel, E2B, Modal, or Docker.（缺口：无）
- `C-002` [部分验证] 🌐 Model-agnostic: smolagents supports any LLM. It can be a local transformers or ollama model, one of many providers on the Hub, or any model from OpenAI, Anthropic and many others via our LiteLLM integration.（缺口：LLM-03）
- `C-003` [部分验证] OpenAI-compatible servers: Together AI（缺口：LLM-03）
- `C-004` [部分验证] OpenAI-compatible servers: OpenRouter（缺口：LLM-03）
- `C-005` [部分验证] Actions are now Python code snippets. Hence, tool calls will be performed as Python function calls. For instance, here is how the agent can perform web search over several websites in one single action:（缺口：LLM-06）
- `C-006` [已验证] Docker — self-hosted container isolation（缺口：无）
- `C-007` [部分验证] Still, we implement several types of agents: CodeAgent writes its actions as Python code snippets, and the more classic ToolCallingAgent leverages built-in tool calling methods. We also have multi-agent hierarchies, import from tool collect（缺口：LLM-06）
- `C-008` [已验证] By the way, why use a framework at all? Well, because a big part of this stuff is non-trivial. For instance, the code agent has to keep a consistent format for code throughout its system prompt, its parser, the execution. So our framework h（缺口：无）

## 主要缺口

- `LLM-04` 是否记录 tokenizer/上下文窗口：没有记录 tokenizer 或上下文窗口。（证据：无）
- `ENV-02` 是否锁定依赖版本或提供容器化配置：有依赖清单，但没有锁定文件或容器配置。（证据：E-002）
- `LLM-02` 是否对 prompt/template 进行版本记录：有 prompt 文件或描述，但没有可核验的版本信息。（证据：E-007, E-014）
- `LLM-07` 是否说明评测集、数据划分和污染风险：只覆盖了评测集/划分/污染中的一部分，或仍有占位内容。（证据：E-021, E-015）
- `LLM-03` 是否记录采样参数：有采样参数或配置线索，但仍需补充可核验值。（证据：E-007）
- `LLM-06` 是否记录 Agent 工具调用轨迹：检测到 Agent 项目，但完整调用轨迹仍需补充。（证据：E-020）
- `LLM-08` 是否说明推理成本或延迟：有成本/硬件线索，但仍需量化数据。（证据：E-016, E-012, E-017）

## 优先整改

- 记录 tokenizer、上下文窗口和截断策略：预计提升 +4.0，理由：避免输入长度和分词差异导致结果变化。
- 添加锁文件或 Dockerfile，固定 Python、CUDA 和依赖版本：预计提升 +4.0，理由：消除环境版本漂移，提升跨机器复现概率。
- 将 prompt/template 版本化并记录在配置或模型卡中：预计提升 +3.0，理由：避免 prompt 漂移导致结果不可复现。
- 说明评测集、数据划分和污染/泄漏风险：预计提升 +3.0，理由：让指标具有可比性，避免高估效果。
- 记录 temperature、top_p、max_tokens 等采样参数：预计提升 +2.5，理由：让生成行为可以复现和比较。
- 保存 Agent 工具调用轨迹、run_id 和关键日志：预计提升 +2.5，理由：让多步调用过程可以审计。
- 说明推理成本、延迟和 token 消耗：预计提升 +2.0，理由：让读者评估复现成本。

## 证据边界

本说明没有补全缺失事实；如果证据不足，ReproLens 会保留 `Evidence Missing`，而不是猜测。
