from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from .models import CriterionResult, Finding
from .scanner import RepoSnapshot


@dataclass(frozen=True)
class CriterionSpec:
    id: str
    dimension: str
    title: str
    max_points: float
    severity: str


SPECS = [
    CriterionSpec("ENV-01", "环境可复现", "是否存在依赖清单", 10, "high"),
    CriterionSpec("ENV-02", "环境可复现", "是否锁定依赖版本或提供容器化配置", 8, "high"),
    CriterionSpec("ENV-03", "环境可复现", "是否提供安装步骤", 7, "medium"),
    CriterionSpec("DATA-01", "数据可复现", "是否说明数据来源和获取方式", 8, "high"),
    CriterionSpec("DATA-02", "数据可复现", "是否提供数据下载或预处理脚本", 8, "high"),
    CriterionSpec("DATA-03", "数据可复现", "是否提供数据集卡或数据许可说明", 6, "medium"),
    CriterionSpec("MODEL-01", "模型可复现", "是否提供模型权重、API 或获取方式", 8, "high"),
    CriterionSpec("MODEL-02", "模型可复现", "是否提供模型卡或版本说明", 8, "high"),
    CriterionSpec("MODEL-03", "模型可复现", "是否说明模型许可和来源", 6, "medium"),
    CriterionSpec("EXP-01", "实验可复现", "是否提供训练或主运行脚本", 7, "high"),
    CriterionSpec("EXP-02", "实验可复现", "是否提供评测脚本或评测命令", 8, "high"),
    CriterionSpec("EXP-03", "实验可复现", "是否设置并说明随机种子", 6, "high"),
    CriterionSpec("EXP-04", "实验可复现", "是否说明硬件或 API 环境要求", 5, "medium"),
    CriterionSpec("EXP-05", "实验可复现", "是否给出预期结果和指标", 7, "high"),
    CriterionSpec("DOC-01", "文档可复现", "是否存在 README", 5, "medium"),
    CriterionSpec("DOC-02", "文档可复现", "是否提供快速开始和运行示例", 6, "medium"),
    CriterionSpec("DOC-03", "文档可复现", "是否提供测试、CI 或一键复现脚本", 6, "medium"),
    CriterionSpec("LLM-01", "LLM 特有风险", "是否记录模型/API 版本", 6, "high"),
    CriterionSpec("LLM-02", "LLM 特有风险", "是否对 prompt/template 进行版本记录", 6, "high"),
    CriterionSpec("LLM-03", "LLM 特有风险", "是否记录采样参数", 5, "medium"),
    CriterionSpec("LLM-04", "LLM 特有风险", "是否记录 tokenizer/上下文窗口", 4, "medium"),
    CriterionSpec("LLM-05", "LLM 特有风险", "是否记录 RAG 索引/知识库版本", 5, "high"),
    CriterionSpec("LLM-06", "LLM 特有风险", "是否记录 Agent 工具调用轨迹", 5, "high"),
    CriterionSpec("LLM-07", "LLM 特有风险", "是否说明评测集、数据划分和污染风险", 6, "high"),
    CriterionSpec("LLM-08", "LLM 特有风险", "是否说明推理成本或延迟", 4, "low"),
]


def _result(
    spec: CriterionSpec,
    status: str,
    note: str,
    evidence_ids: list[str] | None = None,
    applicable: bool = True,
) -> CriterionResult:
    if not applicable:
        status = "not_applicable"
    if status == "pass":
        points = spec.max_points
    elif status == "partial":
        points = round(spec.max_points / 2, 1)
    else:
        points = 0.0
    return CriterionResult(
        id=spec.id,
        dimension=spec.dimension,
        title=spec.title,
        status=status,
        points=points,
        max_points=spec.max_points,
        applicable=applicable,
        note=note,
        evidence_ids=evidence_ids or [],
    )


def evaluate_criteria(snapshot: RepoSnapshot) -> list[CriterionResult]:
    ev = snapshot.evidence_for

    def concrete(flag: str) -> bool:
        return snapshot.has(flag) and not snapshot.has_placeholder(flag)

    results: list[CriterionResult] = []
    by_id = {spec.id: spec for spec in SPECS}

    def add(criterion_id: str, status: str, note: str, evidence_ids: list[str] | None = None, applicable: bool = True) -> None:
        results.append(_result(by_id[criterion_id], status, note, evidence_ids, applicable))

    def has_pinned_dependencies() -> bool:
        pinned_names = {
            "requirements.txt", "pyproject.toml", "environment.yml",
            "environment.yaml", "pipfile", "package.json",
        }
        for rel_path, text in snapshot.texts.items():
            name = Path(rel_path).name.lower()
            if name not in pinned_names:
                continue
            if re.search(r"(?m)^\s*[A-Za-z0-9_.-]+\s*(?:==|===)\s*[^\s#]+", text):
                return True
            if name.startswith("environment") and re.search(r"(?m)^\s*-?\s*[A-Za-z0-9_.-]+\s*=\s*[^\s#]+", text):
                return True
            if name == "pyproject.toml" and re.search(r"(?:==|===)", text):
                return True
        return False

    is_llm = snapshot.has("llm_project")
    is_rag = snapshot.has("rag_project")
    is_agent = snapshot.has("agent_project")
    is_ml = snapshot.has("ml_project")
    project_type = snapshot.project_type
    is_sdk = project_type == "sdk"
    is_agent_fw = project_type == "agent_framework"
    is_memory_fw = project_type == "memory_framework"
    is_framework = is_agent_fw or is_memory_fw
    model_agnostic = is_sdk or is_framework or (project_type == "application" and snapshot.has("model_agnostic"))
    has_data_artifact = snapshot.has("data_script") or snapshot.has("dataset_card")
    data_applicable = (not model_agnostic) or has_data_artifact

    add("ENV-01", "pass" if snapshot.has("deps") else "missing", "已发现依赖清单。" if snapshot.has("deps") else "依赖清单是复现的第一入口。", ev("deps"))
    if snapshot.has("lockfile") or snapshot.has("container"):
        add("ENV-02", "pass", "已发现锁定文件或容器配置。", ev("lockfile", "container"))
    elif snapshot.has("deps") and has_pinned_dependencies():
        add("ENV-02", "pass", "依赖清单已固定关键依赖版本。", ev("deps"))
    elif snapshot.has("deps"):
        add("ENV-02", "partial", "有依赖清单，但未固定关键依赖版本，也没有锁定文件或容器配置。", ev("deps"))
    else:
        add("ENV-02", "missing", "没有锁定文件或容器配置。")

    if snapshot.has("install_instructions"):
        add("ENV-03", "pass", "已发现安装步骤。", ev("install_instructions"))
    elif snapshot.has("readme"):
        add("ENV-03", "partial", "有 README，但没有明显安装命令。", ev("readme"))
    else:
        add("ENV-03", "missing", "没有安装步骤。")

    if snapshot.has("data_source_link"):
        add("DATA-01", "pass", "已发现明确的数据集下载或获取链接。", ev("data_source_link"), applicable=data_applicable)
    elif snapshot.has("data_mention") and (snapshot.has("data_script") or snapshot.has("dataset_card")):
        add("DATA-01", "pass", "已发现数据来源，并配有脚本或数据集卡。", ev("data_mention", "data_script", "dataset_card"), applicable=data_applicable)
    elif snapshot.has("data_mention"):
        add("DATA-01", "partial", "只看到数据名称或论文说明，缺少可直接访问的数据获取链接。", ev("data_mention"), applicable=data_applicable)
    else:
        add("DATA-01", "missing", "没有数据来源说明。", applicable=data_applicable)

    if concrete("data_script"):
        add("DATA-02", "pass", "已发现数据下载或预处理脚本。", ev("data_script"), applicable=data_applicable)
    elif snapshot.has("data_download_command"):
        add("DATA-02", "pass", "README 提供了可直接执行的数据下载或加载命令。", ev("data_download_command"), applicable=data_applicable)
    elif snapshot.has("data_script"):
        add("DATA-02", "partial", "存在数据脚本，但其中仍包含 TODO/占位内容。", ev("data_script"), applicable=data_applicable)
    else:
        add("DATA-02", "missing", "没有数据下载或预处理脚本。", applicable=data_applicable)

    if concrete("dataset_card"):
        add("DATA-03", "pass", "已发现数据集卡。", ev("dataset_card"), applicable=data_applicable)
    elif snapshot.has("data_source_link") and snapshot.has("data_license"):
        add("DATA-03", "pass", "已提供数据集卡链接并说明数据许可。", ev("data_source_link", "data_license"), applicable=data_applicable)
    elif snapshot.has("dataset_card"):
        add("DATA-03", "partial", "数据集卡已生成，但仍有待补充字段。", ev("dataset_card"), applicable=data_applicable)
    elif snapshot.has("license") and (snapshot.has("data_source_link") or snapshot.has("data_mention")):
        add("DATA-03", "partial", "有项目许可证和数据获取线索，但没有独立数据集卡或单独的数据许可说明。", ev("license", "data_source_link", "data_mention"), applicable=data_applicable)
    else:
        add("DATA-03", "missing", "没有数据集卡或明确的数据许可说明。", applicable=data_applicable)

    if snapshot.has("weights"):
        add("MODEL-01", "pass", "已发现模型权重文件。", ev("weights"), applicable=not model_agnostic)
    elif snapshot.has("model_source_link"):
        add("MODEL-01", "pass", "已发现明确的模型下载或获取链接。", ev("model_source_link"), applicable=not model_agnostic)
    elif is_llm and snapshot.has("model_provider") and snapshot.has("model_version"):
        add("MODEL-01", "pass", "已发现 API/模型提供方和模型版本信息。", ev("model_provider", "model_version"), applicable=not model_agnostic)
    elif snapshot.has("model_version") or snapshot.has("model_provider"):
        add("MODEL-01", "partial", "有模型说明，但没有发现权重、下载地址或明确 API 模型版本。", ev("model_version", "model_provider"), applicable=not model_agnostic)
    else:
        add("MODEL-01", "missing", "没有模型权重、API 或获取方式。", applicable=(is_ml or is_llm) and not model_agnostic)

    if concrete("model_card") or snapshot.has("model_source_link") or (is_llm and concrete("model_version")):
        add("MODEL-02", "pass", "已发现模型卡、模型版本或明确模型来源。", ev("model_card", "model_source_link", "model_version"), applicable=not model_agnostic)
    elif snapshot.has("model_card") or snapshot.has("model_version") or snapshot.has("model_provider"):
        add("MODEL-02", "partial", "有模型卡、版本或提供方信息，但仍需补充完整。", ev("model_card", "model_version", "model_provider"), applicable=not model_agnostic)
    else:
        add("MODEL-02", "missing", "没有模型卡或版本说明。", applicable=(is_ml or is_llm) and not model_agnostic)

    if concrete("model_card") and concrete("license"):
        add("MODEL-03", "pass", "模型卡和许可证均已发现。", ev("model_card", "license"), applicable=not model_agnostic)
    elif snapshot.has("license") or snapshot.has("model_card"):
        add("MODEL-03", "partial", "有许可证或模型卡，但模型专用许可和来源仍需补充。", ev("license", "model_card"), applicable=not model_agnostic)
    else:
        add("MODEL-03", "missing", "没有模型许可或来源说明。", applicable=(is_ml or is_llm) and not model_agnostic)

    if snapshot.has("train_script") or snapshot.has("train_instruction") or (is_llm and snapshot.has("run_instructions")):
        add("EXP-01", "pass", "已发现训练脚本或 README 训练命令。", ev("train_script", "train_instruction", "run_instructions"))
    elif snapshot.has("run_instructions"):
        add("EXP-01", "partial", "有运行命令，但没有独立训练或主运行脚本。", ev("run_instructions"))
    else:
        add("EXP-01", "missing", "没有训练脚本或主运行命令。", applicable=(is_ml or is_llm) and not model_agnostic)

    if project_type != "ml_project" and (snapshot.has("tests") or snapshot.has("ci")):
        add("EXP-02", "pass", "软件项目通过测试套件和 CI 提供可执行验证。", ev("tests", "ci"))
    elif snapshot.has("eval_script"):
        add("EXP-02", "pass", "已发现评测脚本。", ev("eval_script"))
    elif snapshot.has("expected_results"):
        add("EXP-02", "partial", "有指标描述，但没有评测脚本。", ev("expected_results"))
    else:
        add("EXP-02", "missing", "没有评测脚本或评测命令。", applicable=(is_ml or is_llm) and not model_agnostic)

    if snapshot.has("seed"):
        add("EXP-03", "pass", "已发现随机种子或确定性设置。", ev("seed"), applicable=(is_ml or is_llm) and not model_agnostic)
    elif snapshot.has("sampling_params"):
        add("EXP-03", "partial", "有采样参数，但没有明确随机种子或确定性设置。", ev("sampling_params"), applicable=(is_ml or is_llm) and not model_agnostic)
    else:
        add("EXP-03", "missing", "没有随机种子或确定性设置。", applicable=(is_ml or is_llm) and not model_agnostic)

    if snapshot.has("hardware") or snapshot.has("model_provider"):
        add("EXP-04", "pass", "已发现硬件或 API 环境说明。", ev("hardware", "model_provider"))
    elif snapshot.has("deps"):
        add("EXP-04", "partial", "有依赖清单，但没有明确硬件或 API 环境要求。", ev("deps"))
    else:
        add("EXP-04", "missing", "没有硬件或 API 环境要求。", applicable=(is_ml or is_llm) and not model_agnostic)

    if snapshot.has("expected_results") or snapshot.has("eval_dataset"):
        add("EXP-05", "pass", "已发现预期结果、指标或评测集。", ev("expected_results", "eval_dataset"))
    elif snapshot.has("eval_script"):
        add("EXP-05", "partial", "有评测脚本，但没有声明预期指标。", ev("eval_script"))
    else:
        add("EXP-05", "missing", "没有预期结果或指标。", applicable=(is_ml or is_llm) and not model_agnostic)

    add("DOC-01", "pass" if snapshot.has("readme") else "missing", "已发现 README。" if snapshot.has("readme") else "没有 README。", ev("readme"))

    if snapshot.has("install_instructions") and snapshot.has("run_instructions"):
        add("DOC-02", "pass", "安装和运行示例均已发现。", ev("install_instructions", "run_instructions"))
    elif snapshot.has("install_instructions") or snapshot.has("run_instructions"):
        add("DOC-02", "partial", "只有安装或运行说明中的一项。", ev("install_instructions", "run_instructions"))
    else:
        add("DOC-02", "missing", "没有快速开始或运行示例。")

    doc_signals = [snapshot.has("tests"), snapshot.has("ci"), snapshot.has("reproduce_script")]
    if sum(doc_signals) >= 2:
        add("DOC-03", "pass", "已有测试、CI 或一键复现脚本中的至少两项。", ev("tests", "ci", "reproduce_script"))
    elif sum(doc_signals) == 1:
        add("DOC-03", "partial", "只有测试、CI 或一键复现脚本中的一项。", ev("tests", "ci", "reproduce_script"))
    else:
        add("DOC-03", "missing", "没有测试、CI 或一键复现脚本。")

    llm01_pass = concrete("model_provider") and concrete("model_version")
    llm01_partial = snapshot.has("model_provider") or snapshot.has("model_version")
    add("LLM-01",
        "pass" if llm01_pass else ("partial" if llm01_partial else "missing"),
        "已记录模型提供方和版本。" if llm01_pass else ("只记录了模型提供方/版本，或仍有待补充字段。" if llm01_partial else "没有记录模型/API 版本。"),
        ev("model_provider", "model_version"), applicable=is_llm and not model_agnostic)

    llm02_pass = concrete("prompt_files") and concrete("prompt_version")
    llm02_partial = snapshot.has("prompt_files") or snapshot.has("prompt_mention")
    add("LLM-02",
        "pass" if llm02_pass else ("partial" if llm02_partial else "missing"),
        "已发现版本化 prompt/template。" if llm02_pass else ("有 prompt 文件或描述，但没有可核验的版本信息。" if llm02_partial else "没有 prompt/template 版本记录。"),
        ev("prompt_files", "prompt_version", "prompt_mention"), applicable=is_llm and not is_sdk and (not model_agnostic or snapshot.has("prompt_files") or snapshot.has("prompt_mention")))

    llm03_partial = snapshot.has("sampling_params") or snapshot.has("config") or (is_framework and snapshot.has("prompt_files"))
    add("LLM-03",
        "pass" if concrete("sampling_params") and not model_agnostic else ("partial" if llm03_partial else "missing"),
        "已记录采样参数。" if concrete("sampling_params") and not model_agnostic else ("有采样参数或配置线索，但仍需补充可核验值。" if llm03_partial else "没有记录 temperature、top_p 等采样参数。"),
        ev("sampling_params", "config", "prompt_files"), applicable=is_llm and not is_sdk and (not model_agnostic or snapshot.has("sampling_params") or snapshot.has("config") or snapshot.has("prompt_files")))

    add("LLM-04",
        "pass" if concrete("tokenizer") else ("partial" if snapshot.has("tokenizer") or snapshot.has("sampling_params") else "missing"),
        "已记录 tokenizer 或上下文窗口。" if concrete("tokenizer") else ("有相关配置，但 tokenizer/上下文窗口仍需补充。" if snapshot.has("tokenizer") or snapshot.has("sampling_params") else "没有记录 tokenizer 或上下文窗口。"),
        ev("tokenizer", "sampling_params"), applicable=is_llm and not is_sdk)

    llm05_applicable = is_rag and not is_agent_fw and not is_sdk
    add("LLM-05",
        "pass" if concrete("rag_config") else ("partial" if is_rag else "missing"),
        "已记录 RAG 索引/知识库的可复现配置。" if concrete("rag_config") else ("检测到 RAG 项目，但索引/embedding 版本仍需补充。" if is_rag else "不适用。"),
        ev("rag_config", "rag_index", "rag_project"), applicable=llm05_applicable)

    add("LLM-06",
        "pass" if concrete("agent_trace_artifact") else ("partial" if is_agent else "missing"),
        "已记录可追溯的 Agent 工具调用轨迹。" if concrete("agent_trace_artifact") else ("检测到 Agent 项目，但完整调用轨迹仍需补充。" if is_agent else "不适用。"),
        ev("agent_trace_artifact", "agent_trace", "agent_project"), applicable=is_agent and not is_memory_fw and not is_sdk)

    llm07_pass = concrete("eval_dataset") and concrete("eval_split") and concrete("contamination")
    llm07_partial = snapshot.has("eval_dataset") or snapshot.has("eval_split") or snapshot.has("contamination")
    add("LLM-07",
        "pass" if llm07_pass else ("partial" if llm07_partial else "missing"),
        "已说明评测集、数据划分和污染风险。" if llm07_pass else ("只覆盖了评测集/划分/污染中的一部分，或仍有占位内容。" if llm07_partial else "没有说明评测集、数据划分或污染风险。"),
        ev("eval_dataset", "eval_split", "contamination"), applicable=is_llm and not is_sdk)

    llm08_partial = snapshot.has("hardware") or snapshot.has("model_provider") or (model_agnostic and snapshot.has("cost"))
    add("LLM-08",
        "pass" if snapshot.has("cost") and not model_agnostic else ("partial" if llm08_partial or snapshot.has("cost") else "missing"),
        "已说明推理成本或延迟。" if snapshot.has("cost") and not model_agnostic else ("有成本/硬件线索，但仍需量化数据。" if llm08_partial or snapshot.has("cost") else "没有说明推理成本或延迟。"),
        ev("cost", "hardware", "model_provider"), applicable=is_llm and not is_sdk)

    return results


def build_findings(criteria: list[CriterionResult]) -> list[Finding]:
    findings: list[Finding] = []
    for item in criteria:
        if item.status in {"missing", "partial"} and item.applicable:
            severity = "high" if item.status == "missing" and item.max_points >= 7 else "medium"
            if item.status == "partial":
                severity = "medium"
            findings.append(
                Finding(
                    id=f"F-{len(findings) + 1:03d}",
                    severity=severity,
                    criterion_id=item.id,
                    title=item.title,
                    message=item.note,
                    evidence_ids=item.evidence_ids,
                )
            )
    return findings
