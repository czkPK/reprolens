# ReproLens Fresh Holdout 结果

> 日期：2026-10-23
> 目的：使用完全未参与规则调整的新仓库评估泛化效果。

## 一、Fresh Holdout 仓库

- anything-llm：本地/云端 LLM 应用
- open-webui：开源聊天与 RAG 应用

每个仓库标注 14 个关键检查项，共 28 个 fresh holdout 标注项。

标注文件：

- `repolens/benchmark/labels/anything-llm.json`
- `repolens/benchmark/labels/open-webui.json`

## 二、结果

```text
Labeled exact status accuracy: 20/28 (71.4%)
Detection precision: 0.692
Detection recall: 0.750
Detection F1: 0.720
```

| 仓库 | Exact | Precision 相关 | 说明 |
|---|---:|---|---|
| anything-llm | 8/14 | 5 TP / 4 FP / 1 FN | 项目类型和非 Python 测试支持仍有误判 |
| open-webui | 12/14 | 4 TP / 0 FP / 2 FN | RAG 与 Agent trace 证据被高估 |

## 三、主要误差

### anything-llm

- 工具没有识别出它是模型无关应用，导致 MODEL-02、MODEL-03 被错误套用；
- 数据相关指标被错误判为 partial，人工标注为 N/A；
- 项目有测试，但 DOC-03 仍被标为 partial；
- LLM-08 被高估为 pass，实际只有定性成本描述。

### open-webui

- LLM-05 被高估为 pass，实际只有 RAG 支持，没有索引/embedding 版本；
- LLM-06 被高估为 pass，实际有 MCP/session 能力，但没有可追溯的完整 Agent 调用轨迹。

## 四、结论

1. Fresh holdout 是在规则调整前没有使用过的新仓库，因此该结果比旧 holdout 更能代表泛化表现；
2. 当前 fresh holdout exact accuracy 为 71.4%，F1 为 0.720，说明工具已经具备可用性，但仍有明确改进空间；
3. 后续优化应集中在：
   - 项目类型识别；
   - 非 Python 测试识别；
   - RAG 索引和 Agent trace 的证据门槛；
   - 成本指标的量化要求；
4. 技术报告中应如实报告 fresh holdout 结果，不应只报告开发集 100%。

## 五、建议报告写法

> ReproLens 在 3 个开发仓库和 2 个 fresh holdout 仓库上进行了人工标注评估。开发集用于规则迭代；fresh holdout 未参与规则调整，最终 exact status accuracy 为 71.4%，检测 F1 为 0.720。误差主要来自项目类型识别、非 Python 项目支持，以及 RAG/Agent 证据门槛。
