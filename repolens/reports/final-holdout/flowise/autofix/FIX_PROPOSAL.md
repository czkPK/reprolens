# ReproLens AutoFix Proposal

- Before score: **56.7**
- After score: **68.1**
- Estimated gain: **+11.4**
- Accepted: **True**

## Generated Files

| File | Reason |
|---|---|
| `data/download.sh` | DATA-02: 提供数据下载脚本入口；URL 需要维护者补充。 |
| `prompts/prompt_metadata.json` | LLM-02: 为当前 prompt 文件生成可核验的版本号和哈希。 |

## Rejected Candidates

- `dataset_card.md`: 修复提案未提升评分，已自动丢弃。
- `model_card.md`: 修复提案未提升评分，已自动丢弃。
- `configs/llm_metadata.yaml`: 修复提案未提升评分，已自动丢弃。
- `eval/README.md`: 修复提案未提升评分，已自动丢弃。

## Criteria Improved

- `DATA-01`
- `EXP-02`
- `EXP-05`
- `LLM-02`
- `LLM-05`

## Remaining Gaps

- `DATA-02`
- `DATA-03`
- `MODEL-03`
- `EXP-01`
- `EXP-02`
- `EXP-03`
- `DOC-02`
- `LLM-03`
- `LLM-04`
- `LLM-05`
- `LLM-07`
- `LLM-08`

## Review Note

Generated templates with TODO fields are intentionally not treated as verified evidence. Candidates that reduce the audit score are automatically rejected.
