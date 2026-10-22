# ReproLens AutoFix Proposal

- Before score: **49.1**
- After score: **63.4**
- Estimated gain: **+14.3**
- Accepted: **True**

## Generated Files

| File | Reason |
|---|---|
| `Dockerfile` | ENV-02: 增加容器化入口，固定 Python 与依赖安装方式。 |
| `reproduce.sh` | DOC-03: 提供一键复现入口。 |
| `tests/test_smoke.py` | DOC-03: 增加最小烟雾测试，验证关键项目文件存在。 |
| `data/download.sh` | DATA-02: 提供数据下载脚本入口；URL 需要维护者补充。 |
| `dataset_card.md` | DATA-03: 增加数据集卡模板；来源和许可需要维护者确认。 |
| `model_card.md` | MODEL-02/03: 增加模型卡，记录可核验的模型来源。 |
| `prompts/prompt_metadata.json` | LLM-02: 为当前 prompt 文件生成可核验的版本号和哈希。 |

## Rejected Candidates

- `configs/llm_metadata.yaml`: 修复提案未提升评分，已自动丢弃。
- `eval/README.md`: 修复提案未提升评分，已自动丢弃。

## Criteria Improved

- `ENV-02`
- `DATA-02`
- `DATA-03`
- `MODEL-03`
- `DOC-03`
- `LLM-02`

## Remaining Gaps

- `DATA-01`
- `DATA-02`
- `DATA-03`
- `MODEL-03`
- `EXP-01`
- `EXP-02`
- `EXP-03`
- `EXP-05`
- `DOC-02`
- `LLM-04`
- `LLM-06`
- `LLM-07`
- `LLM-08`

## Review Note

Generated templates with TODO fields are intentionally not treated as verified evidence. Candidates that reduce the audit score are automatically rejected.
