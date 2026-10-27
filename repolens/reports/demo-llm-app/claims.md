# ReproLens 声明—证据—缺口矩阵

- Repository: `D:\CODEX\ReproLens\repolens\examples\demo-llm-app`
- Generated at: `2026-10-27T07:24:46.864767+00:00`
- Evidence coverage: **16/25 (64.0%)**
- Claims extracted: **2**

## Matrix

| 声明编号 | README 声明 | 验证状态 | 检查依据（需要检查的项） | 还缺什么（缺口） | 支持证据 | 验证说明 |
|---|---|---|---|---|---|---|
| C-001 | A small retrieval-augmented agent demo. | 已验证 | LLM-05（是否记录 RAG 索引/知识库版本） | - | `E-012` configs/app.yaml:9：embedding_model: text-embedding-3-small<br>`E-010` configs/app.yaml:8：vector_store: faiss<br>`E-009` README.md:1：# Demo LLM RAG App | 相关检查项均通过，这条 README 声明有证据支持。 |
| C-002 | This demo uses an OpenAI-compatible model and a local vector store. The knowledge base is under data/. | 已验证 | LLM-01（是否记录模型/API 版本）；LLM-03（是否记录采样参数）；LLM-05（是否记录 RAG 索引/知识库版本）；MODEL-02（是否提供模型卡或版本说明） | - | `E-006` README.md:17：This demo uses an OpenAI-compatible model and a local vector store. The knowledge base ...<br>`E-007` configs/app.yaml:3：name: gpt-4o-mini<br>`E-008` configs/app.yaml:4：temperature: 0.2<br>`E-003` configs/app.yaml:1：model:<br>`E-004` prompts/system.txt:1：You are a helpful assistant. Answer using the retrieved context.<br>`E-012` configs/app.yaml:9：embedding_model: text-embedding-3-small<br>`E-010` configs/app.yaml:8：vector_store: faiss<br>`E-009` README.md:1：# Demo LLM RAG App | 相关检查项均通过，这条 README 声明有证据支持。 |

## Status Definitions

- **已验证**：相关检查项全部通过，并且有证据支持。
- **部分验证**：找到部分证据，但仍有缺口。
- **未验证**：关键证据缺失，当前声明不能视为已验证。
- **不适用**：相关检查项不适用于当前项目类型。

读表方法：Claim 是 README 原句；Required criteria 是验证这句话需要检查的项；Gaps 是仍未满足的检查项；Evidence 是支持证据编号。该矩阵不执行第三方代码，也不保证语义完全正确。
