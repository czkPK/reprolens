# ReproLens Claim-Evidence Matrix

- Repository: `https://github.com/huggingface/smolagents @ 96f33faaf028`
- Generated at: `2026-10-26T13:19:39.679427+00:00`
- Evidence coverage: **15/16 (93.8%)**
- Claims extracted: **8**

## Matrix

| Claim ID | Claim | Status | Required criteria | Gaps | Evidence |
|---|---|---|---|---|---|
| E-022 | 🧑‍💻 First-class support for Code Agents. Our CodeAgent writes its actions in code (as opposed to "agents being used to write code"). To make it secure, we support executing in sandboxed environments via Blaxel, E2B, Modal, or Docker. | VERIFIED | DOC-02, ENV-01, ENV-03 | - | E-008, E-009, E-002 |
| E-023 | 🌐 Model-agnostic: smolagents supports any LLM. It can be a local transformers or ollama model, one of many providers on the Hub, or any model from OpenAI, Anthropic and many others via our LiteLLM integration. | PARTIALLY VERIFIED | LLM-01, LLM-03, MODEL-02 | LLM-03 | E-017, E-013, E-018, E-007 |
| E-024 | OpenAI-compatible servers: Together AI | PARTIALLY VERIFIED | LLM-01, LLM-03, MODEL-02 | LLM-03 | E-017, E-013, E-018, E-007 |
| E-025 | OpenAI-compatible servers: OpenRouter | PARTIALLY VERIFIED | LLM-01, LLM-03, MODEL-02 | LLM-03 | E-017, E-013, E-018, E-007 |
| E-026 | Actions are now Python code snippets. Hence, tool calls will be performed as Python function calls. For instance, here is how the agent can perform web search over several websites in one single action: | PARTIALLY VERIFIED | LLM-06 | LLM-06 | E-020 |
| E-027 | Docker — self-hosted container isolation | VERIFIED | DOC-02, ENV-01, ENV-03 | - | E-008, E-009, E-002 |
| E-028 | Still, we implement several types of agents: CodeAgent writes its actions as Python code snippets, and the more classic ToolCallingAgent leverages built-in tool calling methods. We also have multi-agent hierarchies, import from tool collect | PARTIALLY VERIFIED | LLM-05, LLM-06 | LLM-06 | E-019, E-020 |
| E-029 | By the way, why use a framework at all? Well, because a big part of this stuff is non-trivial. For instance, the code agent has to keep a consistent format for code throughout its system prompt, its parser, the execution. So our framework h | VERIFIED | DOC-02, DOC-03, EXP-02 | - | E-008, E-009, E-005, E-004, E-006 |

## Status Definitions

- **VERIFIED**: every applicable mapped criterion passes with linked evidence.
- **PARTIALLY VERIFIED**: at least one mapped criterion passes but another is partial.
- **UNVERIFIED**: at least one mapped criterion is missing, so the claim is not yet supported.
- **N/A**: none of the mapped criteria apply to this project type.

The matrix verifies documentation claims against repository evidence. It does not execute untrusted code or guarantee semantic correctness.
