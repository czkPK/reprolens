# ReproLens 声明—证据—缺口矩阵

- Repository: `D:\CODEX\ReproLens\repolens\examples\demo-llm-app`
- Generated at: `2026-10-26T14:47:13.939641+00:00`
- Evidence coverage: **16/25 (64.0%)**
- Claims extracted: **2**

## Matrix

| 声明编号 | README 声明 | 验证状态 | 需要检查的项 | 缺口 | 支持证据 | 验证说明 |
|---|---|---|---|---|---|---|
| E-013 | A small retrieval-augmented agent demo. | 已验证 | LLM-05 | - | E-012, E-010, E-009 | 相关检查项均通过，这条 README 声明有证据支持。 |
| E-014 | This demo uses an OpenAI-compatible model and a local vector store. The knowledge base is under data/. | 已验证 | LLM-01, LLM-03, LLM-05, MODEL-02 | - | E-006, E-007, E-008, E-003, E-004, E-012, E-010, E-009 | 相关检查项均通过，这条 README 声明有证据支持。 |

## Status Definitions

- **已验证**：相关检查项全部通过，并且有证据支持。
- **部分验证**：找到部分证据，但仍有缺口。
- **未验证**：关键证据缺失，当前声明不能视为已验证。
- **不适用**：相关检查项不适用于当前项目类型。

读表方法：Claim 是 README 原句；Required criteria 是验证这句话需要检查的项；Gaps 是仍未满足的检查项；Evidence 是支持证据编号。该矩阵不执行第三方代码，也不保证语义完全正确。
