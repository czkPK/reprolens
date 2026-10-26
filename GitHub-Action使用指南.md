# ReproLens GitHub Action 使用指南

ReproLens Action 用于在 Pull Request 或手动触发时，对当前 GitHub 仓库执行复现就绪度审计。

## 最小接入方式

在目标仓库中创建：

```text
.github/workflows/reprolens.yml
```

填入：

```yaml
name: ReproLens Audit

on:
  workflow_dispatch:
  pull_request:

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - uses: czkPK/reprolens@main
        with:
          path: "."
          out-dir: "repolens-report"
          explain: "true"
          autofix: "false"
      - uses: actions/upload-artifact@v4
        with:
          name: reprolens-report
          path: repolens-report/
```

## 输入参数

| 参数 | 默认值 | 说明 |
|---|---|---|
| `path` | `.` | 要审计的仓库路径 |
| `out-dir` | `repolens-report` | 报告输出目录 |
| `autofix` | `false` | 是否在隔离副本中生成并复测修复提案 |
| `explain` | `true` | 是否生成证据约束解释 |

## 输出与 Job Summary

Action 会自动生成：

- `report.html` / `report.md`；
- `score.json` / `evidence.json`；
- `claims.md` / `claims.json`；
- `badge.svg` / `badge.json`；
- 运行摘要中的总分、就绪等级、证据覆盖率和前五项问题。

下游步骤可以读取：

```yaml
- id: reprolens
  uses: czkPK/reprolens@main

- run: echo "Score: ${{ steps.reprolens.outputs.score }}"
- run: echo "Badge: ${{ steps.reprolens.outputs.badge-path }}"
```

## 安全边界

- Action 默认不执行被审计仓库的业务代码；
- 不安装被审计仓库的依赖；
- 不自动修改原始仓库；
- AutoFix 只写入隔离 staging 副本，原始代码保持不变；
- 建议在公开仓库或受信任环境中使用。

## 与网页版的分工

- **网页版**：任意公开仓库，无需安装，适合快速体验和评审演示；
- **GitHub Action**：已经在 GitHub 上维护的项目，适合持续集成和 PR 检查；
- **CLI**：本地深度分析、离线运行和二次开发；
- **GitHub App**：后续面向组织的自动评论与权限管理形态。
