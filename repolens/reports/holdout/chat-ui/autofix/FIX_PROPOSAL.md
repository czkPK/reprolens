# ReproLens AutoFix Proposal

- Before score: **44.1**
- After score: **62.8**
- Estimated gain: **+18.7**
- Accepted: **True**

## Generated Files

| File | Reason |
|---|---|
| `reproduce.sh` | DOC-03: 提供一键复现入口。 |
| `data/download.sh` | DATA-02: 提供数据下载脚本入口；URL 需要维护者补充。 |
| `prompts/prompt_metadata.json` | LLM-02: 为当前 prompt 文件生成可核验的版本号和哈希。 |
| `configs/llm_metadata.yaml` | LLM-01/03: 增加模型和采样参数配置模板。 |

## Rejected Candidates

- `tests/test_smoke.py`: 修复提案未提升评分，已自动丢弃。
- `dataset_card.md`: 修复提案未提升评分，已自动丢弃。
- `model_card.md`: 修复提案未提升评分，已自动丢弃。
- `eval/README.md`: 修复提案未提升评分，已自动丢弃。

## Criteria Improved

- `ENV-03`
- `DATA-01`
- `EXP-02`
- `EXP-05`
- `DOC-02`
- `DOC-03`
- `LLM-02`
- `LLM-03`

## Remaining Gaps

- `ENV-01`
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
- `LLM-06`
- `LLM-07`
- `LLM-08`

## Review Note

Generated templates with TODO fields are intentionally not treated as verified evidence. Candidates that reduce the audit score are automatically rejected.
