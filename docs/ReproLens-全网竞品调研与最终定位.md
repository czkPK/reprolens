# ReproLens 全网竞品调研与最终定位

> 调研时间：2026-10-21。来源：AIC 官网、GitHub、arXiv、OpenAlex、Bing。
> 说明：公开网络无法证明“绝对没有任何相似工作”，但可以确认“没有发现与 ReproLens 完全同定位的现成产品”。

## 一、最接近的现有工作

| 工作 | 它做什么 | 它没有做什么 |
|---|---|---|
| **ReproRepo**（arXiv:2606.18237，EMNLP 2026） | 用 GitHub issue 作为监督，构建 paper-repo 对的复现审计 benchmark；评估 LLM agent 能否发现真实复现阻塞 | 它是 benchmark，不是维护者工具；不生成最小整改方案，不做修复后复测，不进入 PR/CI |
| **ArtifactCopilot / ArtifactGuide**（arXiv:2602.02235） | 按 ACM badge 规则评审论文 artifact，给出 badge 决策 | 不面向开源 AI 仓库；不覆盖 LLM 特有风险；不做整改规划 |
| **Agentic Replication Package Quality Evaluation**（arXiv:2606.02006） | 把开放科学要求变成可自动检查的标准，输出改进报告 | 偏论文 replication package；标准刚性，存在 “if applicable” 误判；不做最小整改和 CI |
| **Supporting Artifact Evaluation with LLMs**（arXiv:2603.06862） | 面向安全论文的 artifact evaluation，沙箱准备环境、评分、检测方法论缺陷 | 偏安全论文评审；环境自动准备成功率约 28%；不做仓库级整改 |
| **CORE-Bench / PaperBench / REPRO-Bench** | 评估 agent 复现论文或评估复现性的能力 | 是 benchmark，不是开源项目维护工具；成本高，偏研究评测 |
| **AutoReproduce / ResearchCodeAgent** | 从论文自动生成或复现代码 | 需要论文和较重执行资源；不是轻量审计与最小整改工具 |
| **ReproZip / Popper / MLCube / Whole Tale** | 环境打包、容器工作流、可复现运行 | 需要作者主动采用；不能直接审计任意第三方仓库 |
| **DVC / MLflow / Sacred / Kedro / marimo** | 作者侧实验管理、数据版本、流水线 | 不解决第三方仓库的复现审计、证据链和整改规划 |
| **人工 checklist / metacheck / MICCAI checklist** | 规范清晰、可人工执行 | 不可扩展、主观、缺少可追溯证据 |

## 二、关键结论

现有工作主要集中在四类：

1. **论文复现 benchmark**：CORE-Bench、PaperBench、REPRO-Bench、ReproRepo；
2. **论文 artifact badge 评审**：ArtifactCopilot、LLM artifact evaluation；
3. **作者侧实验管理/环境打包**：DVC、MLflow、Sacred、ReproZip、Popper、MLCube；
4. **人工规范/清单**：NeurIPS checklist、MICCAI checklist、metacheck。

它们共同留下了五个空位：

1. 面向**开源仓库维护者**，而不是论文评审；
2. 面向**LLM/RAG/Agent 项目**，而不是泛机器学习；
3. 输出**最小整改方案**，而不是问题清单；
4. 做**修复后复测**，而不是一次性报告；
5. 进入 **GitHub PR/CI 工作流**，而不是离线评审。

## 三、最终定位

> **ReproLens：面向开源 LLM/RAG/Agent 项目的复现就绪度审计与最小整改智能体。**

一句话：

> 输入一个开源 LLM 应用仓库，判断它能不能被别人复现，指出缺什么、先补什么、补完能提升多少，并把整改建议接入 GitHub 工作流。

### 为什么从“泛 AI 仓库”收窄到“LLM/RAG/Agent 仓库”

泛 AI 仓库的可复现性已经有不少通用工具和标准，差异化不够。LLM/RAG/Agent 项目有一批通用工具没有覆盖的风险：

- 模型名称和版本漂移；
- API 非确定性；
- prompt/template 版本；
- tokenizer 和上下文截断；
- 采样参数（temperature、top_p 等）；
- 知识库/索引版本；
- 评测集污染和数据泄漏；
- 工具调用轨迹不可复现；
- 推理成本；
- 第三方模型/数据许可。

这些风险在现有复现工具中覆盖不足，而且与 2026 年的 AI 开源生态高度相关。

## 四、五个核心创新

### 1. LLM 专用复现本体

在通用五维（环境、数据、模型、实验、文档）之上增加：

- 模型版本/API 版本；
- prompt/template 版本；
- tokenizer/上下文窗口；
- 采样参数；
- RAG 索引/知识库版本；
- 工具调用轨迹；
- 评测集污染；
- 推理成本。

每条标准带“适用条件”，避免对非 LLM 项目误判。

### 2. 证据图 + 轻量执行探针

静态抽取：

- README、requirements、pyproject、Dockerfile；
- config、prompt 文件、模型卡、数据集卡；
- 训练/评测/推理脚本。

动态探针：

- import；
- `--help`；
- pytest；
- dry-run；
- 最小样例推理。

每个结论绑定文件、行号、命令、退出码和日志片段。

### 3. 反事实最小整改计划

不只列问题，而是给出：

- 先补哪个文件；
- 改哪条命令；
- 预计提升多少分；
- 成本多大；
- 残余风险是什么。

修复后重新审计，展示前后分数变化。

### 4. GitHub 原生工作流

- GitHub Action 在 PR 中自动评论；
- 生成建议 patch；
- 输出复现 badge；
- 记录上游 Issue/PR。

### 5. 开放基准

- 30 个开源 LLM/RAG/Agent 项目；
- 人工标注复现证据和缺口；
- 公开规则、评测脚本和基线结果；
- 与关键词基线、纯 LLM 基线、通用 checklist 基线对比。

## 五、与 ReproRepo 的关键区别

> **ReproRepo 回答“agent 能不能发现复现问题”；ReproLens 回答“维护者应该先修什么、怎么修、修完有没有变好”。**

ReproRepo 是 benchmark，ReproLens 是维护者工具；ReproRepo 输出问题匹配，ReproLens 输出整改闭环；ReproRepo 偏论文-仓库对，ReproLens 偏 LLM/RAG/Agent 开源仓库。

这是最关键的差异化，也是答辩时最应该讲清楚的一句话。

## 六、如何满足 AIC 评分

| 评分项 | 对应设计 |
|---|---|
| 问题与场景价值 15 | LLM 开源项目复现难、版本漂移、prompt/索引不可追溯 |
| 创新性 20 | LLM 专用复现本体 + 反事实整改 + 证据约束 |
| AI 与开源融合 20 | 以开源 LLM/RAG/Agent 仓库为分析对象；LLM 做证据抽取和解释 |
| 实现完成度 25 | CLI/HTML 报告、30 个仓库基准、5 个实际 dry-run、消融实验 |
| 开放成果 15 | 代码、规则包、基准集、评测脚本、GitHub Action、上游 Issue/PR |
| 材料规范 5 | 15 页报告、3—5 分钟视频、资源清单、可访问链接 |

## 七、创新性边界

不能保证“绝对独一无二”，因为：

- 论文和开源项目会持续出现；
- 评审对“创新”的判断有主观性；
- 同类工具可能在局部功能上重叠。

但可以保证：

1. 没有发现完全相同的“LLM/RAG/Agent 仓库复现审计 + 最小整改 + GitHub 工作流”产品；
2. 与 ReproRepo、ArtifactCopilot、CORE-Bench 等直接竞品有清晰边界；
3. 创新点是可演示、可验证、可写成实验的，而不是概念包装。

## 八、下一步实现优先级

1. 把扫描器从“泛 AI 仓库”收窄到“LLM/RAG/Agent 仓库”；
2. 增加 LLM 特有证据抽取：模型名、API、prompt、tokenizer、采样参数、索引版本；
3. 增加轻量执行探针；
4. 建 30 个仓库基准；
5. 做最小整改和修复前后复测；
6. 最后再做 Web UI、GitHub Action、视频和技术报告。

结论：

> **不要做“又一个论文复现 agent”。做“开源 LLM 应用维护者的复现体检工具”。这是目前最清晰、最有差异化、也最适合 9 天冲刺的定位。**
