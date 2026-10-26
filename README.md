# ReproLens / 复现镜

面向开源 LLM、RAG 和 Agent 项目的复现就绪度审计与最小整改智能体。

## 核心问题

代码公开并不等于项目可以复现。依赖、数据、模型版本、prompt、评测协议、RAG 索引和 Agent 轨迹经常散落在不同文件中；README 声称的能力也未必有证据支持。

ReproLens 把“文件检查”升级为“声明—证据—缺口”审计：

- 六维 25 项复现检查；
- 文件、行号和证据 ID；
- README 声明状态与证据覆盖率；
- 证据置信度；
- 最小整改方案；
- 隔离副本中的 AutoFix 复测；
- 可点击的 HTML 证据附录；
- Top 3 优先整改动作；
- README 复现徽章；
- GitHub Action Job Summary；
- 可选 LLM 语义声明映射，异常时回退确定性规则。

## 三种使用方式

### 1. 网页版：任意公开 GitHub 仓库

双击：

```text
repolens\Start-ReproLens-Web.cmd
```

粘贴任意公开 GitHub 仓库地址，系统会固定到具体 commit SHA，浅克隆后生成报告。不会执行仓库代码。

### 2. 本地版：选择本地仓库

双击：

```text
repolens\Start-ReproLens.cmd
```

### 3. GitHub Action：持续集成

根目录提供可复用 `action.yml`，接入方式见：

```text
docs\GitHub-Action使用指南.md
```

## 当前验证结果

- 27 个单元测试通过；
- 演示项目 49.1 → 68.4（+19.3）；
- fresh holdout 初次独立结果 26/28（92.9%，F1 0.900）；
- fresh holdout 修复后复跑 27/28（96.4%，F1 1.000）；
- final holdout 修复后 28/28（100%，F1 1.000，post-fix validation）；
- 真实网页端到端验证：`huggingface/smolagents`，185 个文件，78.8 → 85.9。

## 材料

- `docs/作品简介_300字.md`
- `docs/技术报告初稿.md`
- `docs/开源及第三方资源使用清单.md`
- `docs/AI工具使用说明.md`
- `docs/GitHub-Action使用指南.md`
- `docs/工具验证指南.md`
- `docs/验收测试记录.md`
- `docs/用户试用说明与记录模板.md`
- `repolens/reports/`：演示报告和真实仓库报告

项目还提供 `CHANGELOG.md`、`CONTRIBUTING.md` 和 `SECURITY.md`，便于评审检查版本、贡献和风险边界。

## 许可证

项目代码采用 MIT License。第三方评测仓库只作为本地测试输入，不随仓库分发。

代码仓库：https://github.com/czkPK/reprolens
