# ReproLens Claim-Evidence Matrix

- Repository: `D:\CODEX\ReproLens\repolens\examples\demo-llm-app`
- Generated at: `2026-10-25T13:45:01.788795+00:00`
- Evidence coverage: **16/25 (64.0%)**
- Claims extracted: **3**

## Matrix

| Claim ID | Claim | Status | Required criteria | Gaps | Evidence |
|---|---|---|---|---|---|
| E-013 | A small retrieval-augmented agent demo. | VERIFIED | LLM-05 | - | E-012, E-010, E-009 |
| E-014 | pip install -r requirements.txt | PARTIALLY VERIFIED | DOC-02, ENV-01, ENV-03 | DOC-02 | E-005, E-002 |
| E-015 | This demo uses an OpenAI-compatible model and a local vector store. The knowledge base is under data/. | VERIFIED | LLM-01, LLM-03, LLM-05, MODEL-02 | - | E-006, E-007, E-008, E-003, E-004, E-012, E-010, E-009 |

## Status Definitions

- **VERIFIED**: every applicable mapped criterion passes with linked evidence.
- **PARTIALLY VERIFIED**: at least one mapped criterion passes but another is partial.
- **UNVERIFIED**: at least one mapped criterion is missing, so the claim is not yet supported.
- **N/A**: none of the mapped criteria apply to this project type.

The matrix verifies documentation claims against repository evidence. It does not execute untrusted code or guarantee semantic correctness.
