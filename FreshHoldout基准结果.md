# ReproLens Fresh Holdout 结果

> 日期：2026-10-25（复核）
> 目的：记录 fresh holdout 的独立初次评估，以及后续边界修复后的复跑结果。

## 一、Fresh Holdout 仓库

- anything-llm：本地/云端 LLM 应用
- open-webui：开源聊天与 RAG 应用

每个仓库标注 14 个关键检查项，共 28 个 fresh holdout 标注项。

标注文件：

- `repolens/benchmark/labels/anything-llm.json`
- `repolens/benchmark/labels/open-webui.json`

## 二、结果

### 1. 独立初次评估（规则修复前）

```text
Labeled exact status accuracy: 26/28 (92.9%)
Detection precision: 1.000
Detection recall: 0.818
Detection F1: 0.900
```

| 仓库 | 初次 Exact | 说明 |
|---|---:|---|
| anything-llm | 14/14 | 5 TP / 0 FP / 0 FN | 已修复项目类型和非 Python 测试识别 |
| open-webui | 12/14 | 4 TP / 0 FP / 2 FN | RAG 与 Agent trace 证据仍被高估 |

### 2. 当前代码修复后复跑

```text
Labeled exact status accuracy: 27/28 (96.4%)
Detection precision: 1.000
Detection recall: 1.000
Detection F1: 1.000
```

| 仓库 | 当前 Exact | TP / FP / FN | 说明 |
|---|---:|---|---|
| anything-llm | 14/14 | 5 / 0 / 0 | 与人工标注一致 |
| open-webui | 13/14 | 6 / 0 / 0 | 仅 LLM-03 的 exact 状态不一致 |

> 重要说明：初次评估使用 26/28 作为独立泛化结果；后续针对 open-webui 的 RAG/Agent 证据门槛进行了修复，因此当前 27/28 属于修复后复跑，不能替代初次独立结果。

## 三、主要误差

### anything-llm

- 已修复模型无关应用识别；
- 已新增 `package.json`、`__tests__` 和 `.test.js` 识别；
- 当前 14/14 与人工标注一致。

### open-webui（初次评估）

- LLM-05 被高估为 pass，实际只有 RAG 支持，没有索引/embedding 版本；
- LLM-06 被高估为 pass，实际有 MCP/session 能力，但没有可追溯的完整 Agent 调用轨迹。

### open-webui（当前复跑）

- LLM-05 与 LLM-06 已与人工标注一致；
- 剩余差异为 LLM-03：人工标注为 `partial`，当前规则输出 `missing`；
- `partial` 与 `missing` 在检测指标中都属于“有缺口”，因此 Precision、Recall 和 F1 仍为 1.000，只影响 exact status accuracy。

## 四、结论

1. 初次独立评估为 26/28（92.9%），F1 为 0.900，应作为核心泛化证据；
2. 当前代码复跑为 27/28（96.4%），F1 为 1.000，但该复跑发生在针对证据门槛修复之后；
3. 当前剩余 exact 差异只有 open-webui 的 LLM-03 状态粒度；
4. 技术报告中应同时说明初次独立结果和修复后复跑，不能只报告更高的复跑结果。

## 五、建议报告写法

> ReproLens 在 3 个开发仓库和 2 个 fresh holdout 仓库上进行了人工标注评估。开发集用于规则迭代；fresh holdout 的初次独立 exact status accuracy 为 92.9%，检测 F1 为 0.900。对 RAG/Agent 证据门槛修复后，当前代码复跑为 96.4%，检测 F1 为 1.000；该复跑不作为未参与迭代的独立结果。
