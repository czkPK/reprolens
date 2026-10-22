# ReproLens AutoFix Proposal

- Before score: **78.8**
- After score: **85.9**
- Estimated gain: **+7.1**
- Accepted: **True**

## Generated Files

| File | Reason |
|---|---|
| `Dockerfile` | ENV-02: 增加容器化入口，固定 Python 与依赖安装方式。 |
| `prompts/prompt_metadata.json` | LLM-02: 为当前 prompt 文件生成可核验的版本号和哈希。 |

## Rejected Candidates

- `data/download.sh`: 修复提案未提升评分，已自动丢弃。
- `dataset_card.md`: 修复提案未提升评分，已自动丢弃。
- `model_card.md`: 修复提案未提升评分，已自动丢弃。
- `configs/llm_metadata.yaml`: 修复提案未提升评分，已自动丢弃。
- `eval/README.md`: 修复提案未提升评分，已自动丢弃。

## Criteria Improved

- `ENV-02`
- `LLM-02`

## Remaining Gaps

- `LLM-03`
- `LLM-04`
- `LLM-06`
- `LLM-07`
- `LLM-08`

## Review Note

Generated templates with TODO fields are intentionally not treated as verified evidence. Candidates that reduce the audit score are automatically rejected.
