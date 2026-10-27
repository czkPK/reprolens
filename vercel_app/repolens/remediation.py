from __future__ import annotations

from .models import CriterionResult, Finding, Remediation


ACTIONS = {
    "ENV-01": ("补充 requirements.txt / pyproject.toml / environment.yml", "让读者知道项目需要哪些依赖。", "low", "high"),
    "ENV-02": ("添加锁文件或 Dockerfile，固定 Python、CUDA 和依赖版本", "消除环境版本漂移，提升跨机器复现概率。", "medium", "high"),
    "ENV-03": ("在 README 中增加可复制的安装命令", "降低首次运行门槛。", "low", "medium"),
    "DATA-01": ("补充数据来源、获取方式和数据许可说明", "让读者知道数据从哪里来、能否使用。", "low", "high"),
    "DATA-02": ("添加数据下载或预处理脚本", "把数据准备从手工步骤变成可执行流程。", "medium", "high"),
    "DATA-03": ("添加数据集卡或数据许可说明", "明确数据边界和再分发条件。", "low", "medium"),
    "MODEL-01": ("提供模型权重下载地址或权重大小、文件名说明", "让读者能够获得与结果对应的模型。", "medium", "high"),
    "MODEL-02": ("添加模型卡，记录模型版本、结构、超参数和训练数据", "让模型行为可追溯。", "low", "high"),
    "MODEL-03": ("在模型卡中说明模型许可和来源", "避免模型使用和再分发风险。", "low", "medium"),
    "EXP-01": ("添加训练脚本或明确训练命令", "让训练过程可执行。", "medium", "high"),
    "EXP-02": ("添加评测脚本、评测命令和指标计算方式", "让结果可以被独立验证。", "medium", "high"),
    "EXP-03": ("固定并记录随机种子、框架确定性和硬件差异", "降低结果不可重复的随机性。", "low", "high"),
    "EXP-04": ("在 README/模型卡中说明 GPU 型号、显存和驱动要求", "减少环境不匹配导致的失败。", "low", "medium"),
    "EXP-05": ("补充预期指标、日志样例和可接受误差范围", "让读者知道结果是否正确。", "low", "high"),
    "DOC-01": ("添加 README，说明项目目标、安装、运行和结果", "提供复现入口。", "low", "medium"),
    "DOC-02": ("添加快速开始和最小运行示例", "让新用户可以在几分钟内跑通。", "low", "medium"),
    "DOC-03": ("添加测试、CI 或一键复现脚本", "把复现变成持续可验证的工程流程。", "medium", "medium"),
    "LLM-01": ("记录模型提供方、模型 ID 和 API 版本", "避免模型漂移导致输出不可复现。", "low", "high"),
    "LLM-02": ("将 prompt/template 版本化并记录在配置或模型卡中", "避免 prompt 漂移导致结果不可复现。", "low", "high"),
    "LLM-03": ("记录 temperature、top_p、max_tokens 等采样参数", "让生成行为可以复现和比较。", "low", "medium"),
    "LLM-04": ("记录 tokenizer、上下文窗口和截断策略", "避免输入长度和分词差异导致结果变化。", "low", "medium"),
    "LLM-05": ("记录 RAG 索引版本、embedding 模型和 chunk 参数", "让检索结果可以复现。", "medium", "high"),
    "LLM-06": ("保存 Agent 工具调用轨迹、run_id 和关键日志", "让多步调用过程可以审计。", "medium", "high"),
    "LLM-07": ("说明评测集、数据划分和污染/泄漏风险", "让指标具有可比性，避免高估效果。", "low", "high"),
    "LLM-08": ("说明推理成本、延迟和 token 消耗", "让读者评估复现成本。", "low", "low"),
}


def plan_remediations(findings: list[Finding], criteria: list[CriterionResult]) -> list[Remediation]:
    by_id = {item.id: item for item in criteria}
    remediations: list[Remediation] = []
    for finding in findings:
        criterion = by_id.get(finding.criterion_id)
        if not criterion:
            continue
        action, rationale, cost, impact = ACTIONS.get(
            criterion.id,
            ("补充相应证据和文档", "减少复现过程中的不确定性。", "medium", "medium"),
        )
        gain = round(criterion.max_points - criterion.points, 1)
        remediations.append(
            Remediation(
                finding_id=finding.id,
                action=action,
                rationale=rationale,
                cost=cost,
                impact=impact,
                estimated_score_gain=gain,
                evidence_ids=criterion.evidence_ids,
            )
        )
    remediations.sort(key=lambda item: (-item.estimated_score_gain, item.cost))
    return remediations

