# ReproLens Final Holdout 结果

> 日期：2026-10-23
> 目的：在最后一批应用仓库上验证项目类型、前端测试和证据门槛规则。

## 一、Final Holdout 仓库

- flowise：可视化 LLM 工作流应用
- agentgpt：Agent Web 应用

每个仓库标注 14 个关键检查项，共 28 个最终 holdout 标注项。

标注文件：

- `repolens/benchmark/labels/flowise.json`
- `repolens/benchmark/labels/agentgpt.json`

## 二、结果

```text
Labeled exact status accuracy: 25/28 (89.3%)
Detection precision: 1.000
Detection recall: 0.889
Detection F1: 0.941
```

| 仓库 | Exact | Precision 相关 | 说明 |
|---|---:|---|---|
| flowise | 13/14 | 4 TP / 0 FP / 0 FN | LLM-03 被判为 partial，人工标注为 missing |
| agentgpt | 12/14 | 4 TP / 0 FP / 1 FN | DATA-02 被误判为 pass；LLM-03 被判为 N/A |

## 三、误差分析

1. flowise 的 prompt template 文件被当作采样参数线索，LLM-03 从 missing 提升为 partial；
2. agentgpt 的 `scripts/prepare-sync.sh` 被误判为数据预处理脚本，DATA-02 从 N/A 变成 pass；
3. agentgpt 是模型无关应用，LLM-03 被判为 N/A，但人工标注认为该仓库没有固定采样配置、应视为 missing；
4. precision 为 1.000，表示当前没有把“缺失”误报成“通过/部分通过”的情况；主要问题是漏报和 N/A 判断差异。

## 四、结论

1. Final holdout exact accuracy 为 89.3%，检测 F1 为 0.941；
2. 相比第一次 fresh holdout 的 71.4%，通用修复带来了明显提升；
3. 仍存在数据脚本识别和模型无关应用采样参数判断的边界问题；
4. 技术报告应同时报告开发集、旧 holdout、fresh holdout 和 final holdout，并说明它们的使用顺序，避免把用于调参的结果包装成完全独立测试集。

## 五、建议报告写法

> ReproLens 在开发集上进行规则迭代，并在多批 holdout 上评估。最终 holdout 的 exact status accuracy 为 89.3%，检测 F1 为 0.941。主要剩余误差来自数据脚本识别和模型无关应用的采样参数适用性判断。
