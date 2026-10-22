# ReproLens

开源 AI 项目复现就绪度审计与整改智能体。

## 目录结构

- `repolens/`：主项目代码、示例仓库、单元测试和演示报告。
- `licenselens/`：许可证合规子模块原型，后续作为 ReproLens 的合规模块。
- `docs/`：赛题分析、竞品调研、国赛方案和 11 天执行计划。

## 快速运行

```powershell
cd repolens
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
python -m repolens audit examples/demo-ai-repo --out-dir reports/demo-ai-repo
```

## 当前能力

- 扫描本地 Python AI 仓库；
- 提取 README、依赖、脚本、配置、模型卡、数据集卡、CI 和许可证证据；
- 按环境、数据、模型、实验、文档和 AI 特有风险六个维度评分；
- 输出 `report.md`、`score.json`、`evidence.json`、`remediation.json`；
- 生成带证据 ID 的整改计划和预计提分。

## 说明

本目录用于最终提交项目代码与方案文档。第三方论文、获奖名单等调研资料未放入本目录，避免最终压缩包混入无关材料。
