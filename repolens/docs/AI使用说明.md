# ReproLens AI 使用说明

## 1. AI 模块名称

ReproLens-SmallSemantic-v1：本地开源语义原型分类器。

## 2. AI 在系统中的位置

AI 只负责将 README 中的自然语言能力声明映射到固定检查项候选。最终检查状态、评分和证据编号由本地规则引擎和仓库证据决定。

处理链路：

```text
仓库文本扫描
→ 证据编号和原文
→ 规则引擎生成检查项状态
→ 本地语义模型推荐检查项候选
→ 校验检查项目录和证据编号
→ 生成声明矩阵和缺口
```

## 3. AI 不做什么

- 不直接计算总分；
- 不生成仓库中不存在的证据；
- 不执行第三方代码；
- 不在低置信度时强行判定通过；
- 不允许模型通过修改提示词绕开固定检查项目录。

## 4. 本地运行

默认模式为 `local`，不需要 API Key，不向外部网络发送仓库内容：

```bash
REPROLENS_SEMANTIC_MODE=local python -m repolens audit examples/demo-llm-app --out-dir reports/demo --ai-review
```

可选模式：

```text
local   使用仓库自带的本地语义模型（默认）
off     关闭语义增强，只使用确定性规则
llm     使用可选的 OpenAI-compatible 外部模型
```

## 5. 模型和评测

- 模型文件：`src/repolens/data/reprolens-small-semantic-v1.json`
- 训练数据：`src/repolens/data/semantic_training.json`
- 模型卡：`docs/ReproLens-SmallSemantic-v1模型卡.md`
- 独立评测集：`benchmark/semantic_claims.json`
- 评测结果：`benchmark/semantic_evaluation.json`
- 训练脚本：`scripts/train_local_semantic_model.py`
- 评测脚本：`scripts/evaluate_local_semantic.py`

当前独立评测的 Top-1 映射准确率为 96.7%，候选覆盖率为 100%。这组数据来自独立整理的声明测试集，仍需在更多真实仓库上继续验证。

## 6. 数据与隐私

默认本地模式只处理公开 GitHub 仓库文本，不调用外部 API，不上传私有仓库、个人信息或访问凭证。外部 LLM 模式是可选后端，只有部署者显式配置 API 后才启用。

## 7. 许可和开源

本地模型、训练数据、训练脚本和评测集均随 ReproLens 以 MIT License 开放。模型卡披露了方法、训练数据、适用范围和限制。

## 8. 失败回退

如果模型文件缺失、模型输出格式错误、检查项编号不存在或证据校验失败，系统会回退到确定性规则模式，并在 `ai-review.json` 中记录原因。
