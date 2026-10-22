# Labeling Rubric

Statuses:

- `pass`: explicit, inspectable evidence in the repository.
- `partial`: some evidence exists, but key fields, commands, or verification data are missing.
- `missing`: applicable criterion has no evidence.
- `not_applicable`: the project type does not own the artifact being checked.

Rules:

- Do not infer PASS from a generic mention in a document.
- `TODO`, `TBD`, and `Not specified` are not valid evidence.
- SDK and model-agnostic framework repositories mark project-owned model, dataset, and experiment criteria as `not_applicable`.
- Every status must include a path and rationale in the label JSON.

Build `benchmark/cases.json` from labels:

```powershell
python scripts/build_label_cases.py
```
