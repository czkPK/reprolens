# ReproLens-SmallSemantic-v1 模型卡

## 基本信息

- 模型名称：ReproLens-SmallSemantic-v1
- 版本：1.0.0
- 类型：本地文本语义原型分类器
- 许可证：MIT
- 运行方式：CPU、本地、离线
- 外部 API：不需要
- 模型文件：`src/repolens/data/reprolens-small-semantic-v1.json`
- 训练数据：`src/repolens/data/semantic_training.json`
- 训练脚本：`scripts/train_local_semantic_model.py`

## 用途

该模型只负责把 README 中的自然语言声明映射到 ReproLens 的固定检查项候选，例如：

- “重复运行产生相同结果” -> `EXP-03`
- “预训练权重可从 Baidu Pan 下载” -> `MODEL-01`
- “Agent 记录工具调用轨迹” -> `LLM-06`

模型输出只包含检查项候选、相似度和置信度，不生成文件、不生成证据编号，也不直接决定项目分数。

## 方法

采用字符 n-gram 和词级特征哈希，结合 TF-IDF 权重和按检查项聚合的语义原型。输入声明与 25 个检查项原型计算余弦相似度，返回相似度最高的一个或两个候选检查项。

该方法不需要下载外部大模型、不需要 GPU，也不向第三方发送仓库内容。

## 训练数据

训练数据由项目作者为 25 个固定检查项编写的中英文声明示例组成。示例覆盖依赖、数据、模型、训练、评测、文档、许可证以及 LLM 特有风险。训练数据不包含个人隐私、私有仓库内容或 API Key。

## 输出和校验

模型输出会经过 `validate_ai_rows` 校验：

- `claim_id` 必须存在于规则生成的声明矩阵；
- `criterion_ids` 必须来自固定检查项目录；
- 证据编号从仓库实际证据中读取，不从模型输出中读取；
- 不在目录中的候选会被丢弃；
- 低置信度结果不会被当作最终通过。

## 本地评测结果

在 30 条单独整理、且未原样放入训练集的中英文声明上：

- 候选覆盖率：100%
- Top-1 映射准确率：96.7%
- Top-2 命中率：96.7%

评测集见 `benchmark/semantic_claims.json`，结果见 `benchmark/semantic_evaluation.json`，可通过 `scripts/evaluate_local_semantic.py` 复现。

## 置信度

- `high`：高相似度；
- `medium`：中等相似度；
- `low`：低相似度，建议人工复核。

当前模型只返回最多两个候选检查项，避免把所有声明都映射到大量规则上。

## 适用范围

适用于 AI、计算机及相关工程论文公开仓库的 README 声明语义初筛。对以下情况需要人工复核：

- 非标准语言或大量领域缩写；
- 极短、含糊或纯链接声明；
- 与训练示例差异很大的表达；
- 需要理解完整论文上下文才能判断的声明。

## 已知限制

该模型是轻量级本地分类器，不声称具备通用大模型的世界知识。它只负责缩小候选检查项范围，不能替代证据扫描、规则评分和人工复核。外部 LLM 是可选后端，不是本模型的必需依赖。

## 复现

```bash
python scripts/train_local_semantic_model.py
python -m unittest discover -s tests -v
```

模型文件和训练数据均随开源仓库提供，模型卡、训练方法和校验逻辑均可审计。
