# ReproLens Holdout 基准结果

> 日期：2026-10-23
> 目的：使用未参与规则调整的仓库评估泛化效果。

## 一、Holdout 仓库

- aider：LLM CLI Agent 应用
- browser-use：浏览器 Agent 框架/应用
- chat-ui：开源聊天前端应用

标注文件：

- `repolens/benchmark/labels/aider.json`
- `repolens/benchmark/labels/browser-use.json`
- `repolens/benchmark/labels/chat-ui.json`

每个仓库标注 14 个关键检查项，共 42 个 holdout 标注项。

## 二、结果

```text
Labeled exact status accuracy: 19/42 (45.2%)
Detection precision: 0.368
Detection recall: 0.500
Detection F1: 0.424
```

开发集结果为 56/56，holdout 结果明显下降。这说明当前规则在未参与调参的仓库上仍存在明显泛化差距。

## 三、主要失败原因

### 1. 项目类型识别仍不稳定

- browser-use 被识别成 SDK，导致 Agent 相关指标被错误标记为 N/A；
- aider 被识别为 unknown，模型无关应用被错误套用模型卡、随机种子等指标；
- chat-ui 是前端应用，但当前扫描器主要按 Python 项目设计。

### 2. 非 Python 项目支持不足

chat-ui 依赖 `package.json`，但 ENV-01 只识别 Python 依赖清单，导致依赖清单被误判为缺失。Playwright 测试也没有被识别为 EXP-02。

### 3. 文档提及仍会污染判断

aider 的 README 提到模型示例，工具把示例中的模型信息当成项目自有模型信息；chat-ui 的 MCP 提及也被当成 Agent trace。

### 4. “模型无关应用”与“模型项目”没有完全区分

aider、browser-use、chat-ui 都支持多个模型，不应要求项目自有模型卡；当前只有部分指标正确处理了这一点。

## 四、结论

1. 开发集 100% 不能代表真实泛化能力；
2. holdout 结果暴露了项目类型识别、非 Python 项目支持和文档证据污染问题；
3. 这些错误不能通过继续在同一批 holdout 上调规则来解决，否则 holdout 会变成开发集；
4. 下一步应修复通用问题，并重新准备一批新的 holdout 仓库。

## 五、下一步

1. 改进项目类型识别：application、agent_framework、memory_framework、sdk、web_frontend；
2. 增加 `package.json`、Playwright、npm test 等前端项目支持；
3. 增加“模型无关应用”的显式判定；
4. 修复后重新准备 2—3 个新的 holdout 仓库；
5. 在技术报告中同时报告开发集和 holdout 两组结果。
