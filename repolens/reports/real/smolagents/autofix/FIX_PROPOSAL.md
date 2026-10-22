# ReproLens AutoFix Proposal

- Before score: **70.0**
- After score: **78.4**
- Estimated gain: **+8.4**
- Accepted: **True**

## Generated Files

| File | Reason |
|---|---|
| `Dockerfile` | ENV-02: 增加容器化入口，固定 Python 与依赖安装方式。 |
| `data/download.sh` | DATA-02: 提供数据下载脚本入口；URL 需要维护者补充。 |
| `prompts/prompt_metadata.json` | LLM-02: 为当前 prompt 文件生成可核验的版本号和哈希。 |
| `configs/llm_metadata.yaml` | LLM-01/03: 增加模型和采样参数配置模板。 |

## Rejected Candidates

- `dataset_card.md`: 修复提案未提升评分，已自动丢弃。
- `model_card.md`: 修复提案未提升评分，已自动丢弃。
- `eval/README.md`: 修复提案未提升评分，已自动丢弃。

## Criteria Improved

- `ENV-02`
- `DATA-01`
- `LLM-02`
- `LLM-03`

## Remaining Gaps

- `DATA-02`
- `DATA-03`
- `MODEL-03`
- `EXP-02`
- `EXP-03`
- `LLM-03`
- `LLM-04`
- `LLM-05`
- `LLM-06`
- `LLM-07`

## Review Note

Generated templates with TODO fields are intentionally not treated as verified evidence. Candidates that reduce the audit score are automatically rejected.
