> 最新定位：在主方向基础上进一步收窄为“开源 LLM/RAG/Agent 项目的复现就绪度审计”。详见 ReproLens-全网竞品调研与最终定位.md。

# ReproLens 竞品分析与深耕方向

> 调研时间：2026-10-19。调研范围：AIC 官网、GitHub、arXiv、现有开源工具。
> 结论：ReproLens 不应做成“论文复现智能体”或“实验管理平台”，而应聚焦“开源 AI 仓库的复现就绪度审计 + 最小整改方案 + GitHub 工作流”。

## 一、现有工作分类

### 1. 论文/制品复现评测智能体

- **ArtifactCopilot / ArtifactGuide**（arXiv:2602.02235）：面向软件工程论文的 artifact evaluation，按 ACM badge 规则收集证据并给出 badge 决策。60 个真实 artifact，badge 一致率 70.56%。
- **An Agentic Approach Towards Replication Package Quality Evaluation**（arXiv:2606.02006）：把 34 个来源的 380 条要求压缩为 51 条可复现性标准，其中 31 条可自动检查；5 个 replication package，平均正确率 75.4%。
- **Supporting Artifact Evaluation with LLMs**（arXiv:2603.06862）：面向安全论文的 artifact evaluation，可做文本可复现性评分、沙箱环境准备和方法论缺陷检测；环境自动准备成功率约 28%，评分准确率约 72%。
- **CORE-Bench**（arXiv:2409.11363）：270 个任务、90 篇论文，评估智能体用代码和数据复现结果的能力；最难任务最好成绩约 21%。
- **PaperBench**（arXiv:2504.01848）：20 篇 ICML 2024 论文、8316 个可评分任务，最佳智能体平均复现得分约 21%。
- **REPRO-Bench / REPRO-Agent**（arXiv:2507.18901）：112 个社会科学论文复现评估任务，现有智能体最好只有 21.4% 准确率，REPRO-Agent 改进后提升 71%。
- **AutoReproduce**（arXiv:2505.20662）：用 paper lineage 和多智能体自动生成实验代码，强调端到端复现。
- **ResearchCodeAgent**（arXiv:2504.20117）：把论文方法自动转成代码，46.9% 生成代码高质量且无错误，平均减少 57.9% 编码时间。

### 2. 环境/工作流/实验管理工具

- **ReproZip**（VIDA-NYU/reprozip，BSD-3-Clause）：追踪命令执行并打包依赖，重放实验。
- **Popper**（getpopper/popper，MIT）：容器原生工作流，用 YAML 定义和复跑实验。
- **Whole Tale**（whole-tale/whole-tale，BSD-3-Clause）：可复现研究平台。
- **DVC**（iterative/dvc，Apache-2.0）：数据版本和实验管理。
- **MLflow**（mlflow/mlflow，Apache-2.0）：实验跟踪、模型管理。
- **Sacred**（IDSIA/sacred，MIT）：实验配置、日志和复现。
- **MLCube**（mlcommons/mlcube，Apache-2.0）：模型可移植、可复现运行。
- **marimo**（marimo-team/marimo，Apache-2.0）：可复现的响应式 Python notebook。
- **Kedro**（kedro-org/kedro）：可复现的数据科学流水线。
- **mlf-core**、**Trixi**、**Gokart**、**IBM mi-prometheus**：面向实验管理或流水线的可复现性支持。

### 3. 清单/规范类工作

- NeurIPS 2019 Reproducibility Program（arXiv:2003.12206）：代码提交政策、复现挑战、机器学习可复现性清单。
- MICCAI Reproducibility Checklist、checklib、reproChecklist 等：主要是人工清单或 issue 模板。
- LLM-for-SE Reproducibility Crisis（arXiv:2512.00651）：分析 640 篇论文，提出 7 类 reproducibility smell：代码与执行、数据、文档、环境与工具、版本管理、模型、访问与法律。

## 二、现有工作的共同不足

1. **偏论文/artifact evaluation，不偏开源仓库维护**
   - 多数工具输入是论文 PDF + replication package，输出是 badge 或评审报告；
   - 开源项目维护者需要的是“我的仓库还缺什么、先补什么、补完能到什么程度”，而不是评审结论。

2. **清单刚性，缺少适用性判断**
   - 现有 agentic replication package 评估的最大问题之一是 “if applicable” 场景：复现研究不应被要求提供新模型权重，合成数据不应被要求做人类受试者匿名化；
   - 固定 checklist 容易产生假阳性/假阴性。

3. **缺少 AI/ML 特有风险**
   - 通用复现标准不覆盖：模型版本漂移、API 非确定性、prompt/template 版本、tokenizer、随机种子、GPU/驱动差异、数据污染、评测 split、checkpoint、推理成本等；
   - 这正是“AI+开源”赛道的差异化空间。

4. **静态检查多，执行证据少**
   - 现有工具能读 README，但往往不能证明“这条命令真的能跑”；
   - 需要轻量执行探针：导入检查、`--help`、单元测试、dry-run、样例推理，而不是完整训练。

5. **只诊断，不规划整改**
   - 多数工具输出问题列表；
   - 维护者真正需要的是“最小修复集”：补哪个文件、改哪条命令、预计提升多少分、成本多大、残余风险是什么。

6. **缺少 GitHub 原生工作流**
   - 现有工具多是离线评审或研究原型；
   - 如果能在 PR/CI 中自动评论、生成建议 patch、给出复现 badge，才真正进入开源协作流程。

7. **评估样本小、场景窄**
   - Agentic replication package 评估只有 5 个 package、7 位研究者；
   - LLM artifact evaluation 的环境自动准备成功率只有 28%；
   - 尚缺少面向“开源 AI 仓库”的公开基准。

8. **隐私与模型依赖**
   - 部分原型依赖商业 LLM，不适合未公开代码；
   - 需要本地/离线模式和证据约束，避免代码与数据泄露。

## 三、ReproLens 的深耕方向

### 定位

> **开源 AI 仓库的复现就绪度审计与最小整改智能体。**

不是“论文复现智能体”，不是“实验管理平台”，也不是“又一个 artifact badge 工具”。

### 核心差异化

1. **AI/ML 专用复现本体**
   - 在通用五维（环境、数据、模型、实验、文档）上增加 AI 特有维度：
     - 模型版本与权重；
     - prompt/template 版本；
     - tokenizer 与预处理；
     - 随机种子与硬件非确定性；
     - 评测 split 与指标定义；
     - 数据许可与污染风险；
     - 推理/训练成本。
   - 每条标准带“适用条件”，解决 “if applicable” 误判。

2. **证据图 + 轻量执行探针**
   - 静态抽取：README、requirements、pyproject、Dockerfile、config、model card、dataset card、脚本、CI；
   - 动态探针：`python -c import`、`--help`、pytest、dry-run、最小样例推理；
   - 每个结论绑定证据 ID：文件路径、行号、命令、退出码、日志片段。
   - 不追求完整训练复现，追求“可验证的复现就绪度”。

3. **反事实最小整改计划**
   - 对每个缺口生成候选动作：补依赖锁定、加数据下载脚本、固定种子、补评测命令、加模型卡、替换许可证不清的依赖；
   - 估算成本、影响和残余风险；
   - 重新运行审计，展示“修复后分数变化”，形成可验证闭环。

4. **GitHub 原生工作流**
   - GitHub Action：PR 中自动评论复现体检结果；
   - 生成建议 patch：README 复现章节、requirements 锁定、`reproduce.sh`；
   - 生成复现 badge：Pass / Partial / Fail / Evidence Missing；
   - 这是现有论文型工具没有覆盖的工程落地层。

5. **开放基准**
   - 30 个开源 AI 仓库，覆盖 PyTorch、TensorFlow、Hugging Face、传统 ML 项目；
   - 人工标注“缺失证据”和“整改后状态”；
   - 公开标注规则、评测脚本和基线结果；
   - 与关键词基线、纯 LLM 基线、ArtifactCopilot 风格 checklist 基线对比。

6. **隐私友好的本地模式**
   - 支持 OpenAI-compatible 接口；
   - 支持本地开源模型或确定性模板回退；
   - 默认不上传代码，只上传用户显式选择的证据片段；
   - 报告中说明 AI 使用环节和人工审核。

## 四、与现有工作的对比

| 现有工作 | 它擅长什么 | 它没有解决什么 | ReproLens 的差异 |
|---|---|---|---|
| ArtifactCopilot / Agentic replication package evaluation | 论文 artifact badge、结构化评分 | AI/ML 特有风险、GitHub 工作流、最小整改 | 面向开源 AI 仓库，强调整改与 CI |
| CORE-Bench / PaperBench / REPRO-Bench | 评估智能体复现论文的能力 | 不是维护者工具，成本高，偏 benchmark | 轻量审计，面向真实仓库维护 |
| AutoReproduce / ResearchCodeAgent | 自动生成/复现实验代码 | 需要论文和大量执行资源，难以日常使用 | 先诊断再修复，低成本、可解释 |
| ReproZip / Popper / MLCube | 环境打包、工作流执行 | 需要作者主动采用，不能审计任意仓库 | 对任意仓库做 readiness audit |
| DVC / MLflow / Sacred | 作者侧实验管理 | 不解决第三方仓库审计和整改 | 第三方视角、证据图、整改计划 |
| 人工 checklist / metacheck | 规范清晰、易理解 | 不可扩展、主观、缺少证据 | LLM 抽取 + 规则校验 + 可复核证据 |

## 五、技术架构

```text
Repo input
  -> file inventory + language/framework detection
  -> static evidence extractor (README, configs, scripts, model/data cards)
  -> lightweight execution probes (import, help, tests, dry-run)
  -> evidence graph builder
  -> applicability-aware rule engine
  -> five-dimension + AI-specific score
  -> counterfactual remediation planner
  -> report.md / score.json / evidence.json / patch suggestions
  -> GitHub Action / PR comment
```

关键原则：

- LLM 只做“抽取、解释、候选方案表达”；
- 规则引擎负责“事实校验、评分、冲突判断”；
- 每个结论必须有证据 ID；
- 没有证据时输出 `Evidence Missing`，不猜测；
- 执行探针失败也作为证据，不伪造成功。

## 六、验证方案

### 基准集

- 30 个开源 AI 仓库；
- 10 个文档较完整，10 个有明显缺口，10 个为受控修改版本；
- 每个仓库标注：环境、数据、模型、实验、文档、AI 特有风险。

### 指标

- 缺口识别 Precision / Recall / F1；
- 证据引用准确率；
- 评分与人工评分的一致性；
- 整改计划有效率；
- 修复后分数提升；
- 审计耗时；
- 与纯 LLM 基线相比的幻觉率。

### 实验

- Baseline A：文件存在性/关键词检查；
- Baseline B：纯 LLM 阅读 README；
- Baseline C：通用 checklist；
- Ours：证据图 + 执行探针 + 反事实整改；
- Ablation：去掉执行探针、去掉适用性判断、去掉整改重算。

### 真实复现

选 5 个小型仓库实际执行：
- 安装依赖；
- 运行 `--help` 或最小样例；
- 运行测试或 dry-run；
- 记录失败原因和修复前后差异。

## 七、11 天 MVP 范围

- 只支持 Python ML/DL 项目；
- 识别 README、requirements、pyproject、environment.yml、Dockerfile、config、scripts、model card、dataset card；
- 轻量执行探针只做 import、`--help`、pytest/dry-run，不做完整训练；
- 输出 `report.md`、`score.json`、`evidence.json`、`remediation.json`；
- 提供 CLI + 简单 Web UI；
- GitHub Action 作为加分项，时间不足则先做 PR 评论脚本；
- LicenseLens 作为许可证子模块。

## 八、结论

现有工作已经把“论文复现”和“artifact evaluation”做得比较深，但普遍停留在：

- 论文/制品评审，而不是开源仓库维护；
- 静态清单，而不是 AI 特有风险；
- 诊断问题，而不是最小整改；
- 离线报告，而不是 GitHub 工作流；
- 商业模型，而不是隐私友好本地模式。

ReproLens 的机会不是“比 PaperBench 更强”，而是：

> **做开源 AI 仓库维护者真正会日常使用的复现体检工具：能审计、能解释、能整改、能进 CI。**

这也是本赛道“AI 开发工具与开源协作”最合适、最容易做出差异化的方向。

