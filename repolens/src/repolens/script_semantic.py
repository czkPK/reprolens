from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path


SCRIPT_SUFFIXES = {".py", ".sh", ".ps1", ".js", ".ts", ".jsx", ".tsx", ".ipynb"}
TRAIN_NAME_RE = re.compile(r"(^|[_/.-])(train|training|finetune|pretrain)", re.IGNORECASE)
EVAL_NAME_RE = re.compile(r"(^|[_/.-])(eval|evaluate|evaluation|test|infer|predict)", re.IGNORECASE)
DATA_NAME_RE = re.compile(r"(^|[_/.-])(data|dataset|download|prepare|preprocess|process)", re.IGNORECASE)
MODEL_NAME_RE = re.compile(r"(^|[_/.-])(model|checkpoint|weight|weights|hub)", re.IGNORECASE)


@dataclass(frozen=True)
class ScriptSignal:
    criterion_id: str
    kind: str
    line: int | None
    excerpt: str
    reason: str
    confidence: str = "medium"


def _line_for(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _line_excerpt(text: str, offset: int) -> str:
    start = text.rfind("\n", 0, offset) + 1
    end = text.find("\n", offset)
    end = len(text) if end < 0 else end
    return text[start:end].strip()[:220]


def _python_signals(text: str, path: str) -> list[ScriptSignal]:
    try:
        tree = ast.parse(text, filename=path)
    except SyntaxError:
        return []

    signals: list[ScriptSignal] = []
    seen: set[str] = set()

    def add(criterion_id: str, kind: str, line: int | None, excerpt: str, reason: str, confidence: str = "medium") -> None:
        key = criterion_id + ":" + kind
        if key in seen:
            return
        seen.add(key)
        signals.append(ScriptSignal(criterion_id, kind, line, excerpt, reason, confidence))

    names: list[tuple[str, ast.AST]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            parts: list[str] = []
            current = node.func
            while isinstance(current, ast.Attribute):
                parts.append(current.attr)
                current = current.value
            if isinstance(current, ast.Name):
                parts.append(current.id)
            names.append((".".join(reversed(parts)), node))

    for name, node in names:
        lower = name.lower()
        line = getattr(node, "lineno", None)
        if any(token in lower for token in ("manual_seed", "seed_everything", "set_seed", "random.seed")):
            add("EXP-03", "seed-setting", line, f"{name}(...)", "检测到随机种子或确定性设置。", "high")
        if any(token in lower for token in ("fit", "train", "backward", "optimizer.step", "optimizer")):
            add("EXP-01", "training-script", line, f"{name}(...)", "检测到训练循环、优化器或训练入口。", "medium")
        if any(token in lower for token in ("evaluate", "evaluation", "test_step", "predict", "compute_metrics")):
            add("EXP-02", "evaluation-script", line, f"{name}(...)", "检测到评测或指标计算入口。", "medium")
        if any(token in lower for token in ("load_dataset", "prepare_data", "download_data", "preprocess_data", "process_data")):
            add("DATA-02", "data-script", line, f"{name}(...)", "检测到数据下载、加载或预处理调用。", "medium")
        if any(token in lower for token in ("from_pretrained", "load_state_dict", "torch.load", "hf_hub_download")):
            add("MODEL-01", "model-loading", line, f"{name}(...)", "检测到模型权重加载或下载调用。", "medium")

    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            value = node.value.lower()
            line = getattr(node, "lineno", None)
            if any(token in value for token in ("train", "finetune", "pretrain")):
                add("EXP-01", "training-script", line, node.value[:160], "脚本文本描述了训练或微调操作。", "low")
            if any(token in value for token in ("evaluate", "test set", "validation", "metric")):
                add("EXP-02", "evaluation-script", line, node.value[:160], "脚本文本描述了评测或指标计算。", "low")

    return signals


def _text_signals(text: str, path: str) -> list[ScriptSignal]:
    lower = text.lower()
    name = Path(path).name.lower()
    signals: list[ScriptSignal] = []
    seen: set[str] = set()

    def add(criterion_id: str, kind: str, pattern: str, reason: str, confidence: str = "medium") -> None:
        match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
        if not match or criterion_id in seen:
            return
        seen.add(criterion_id)
        signals.append(ScriptSignal(criterion_id, kind, _line_for(text, match.start()), _line_excerpt(text, match.start()), reason, confidence))

    if TRAIN_NAME_RE.search(name) or re.search(r"\btorchrun\b|\baccelerate\s+launch\b|\bdeepspeed\b|python(?:3)?\s+-m\s+[^\n]*(?:train|main)|\bpython(?:3)?\s+[^\n]*train[^\n]*\.py", text, re.IGNORECASE):
        add("EXP-01", "training-script", r"torchrun|accelerate\s+launch|deepspeed|python(?:3)?\s+-m|train", "检测到训练命令或训练脚本入口。", "high")
    if EVAL_NAME_RE.search(name) or re.search(r"\bevaluate\.py\b|\beval\.py\b|--eval|-m\s+[^\n]*eval", text, re.IGNORECASE):
        add("EXP-02", "evaluation-script", r"evaluate|eval|test|predict", "检测到评测脚本或评测命令。")
    if re.search(r"manual_seed|seed_everything|random\.seed|numpy\.random\.seed|--seed\b", text, re.IGNORECASE):
        add("EXP-03", "seed-setting", r"manual_seed|seed_everything|random\.seed|--seed", "检测到随机种子或确定性设置。", "high")
    if DATA_NAME_RE.search(name) or re.search(r"\b(?:download_data|prepare_data|preprocess_data|process_data|load_dataset)\b", text, re.IGNORECASE):
        add("DATA-02", "data-script", r"download_data|prepare_data|preprocess_data|process_data|load_dataset", "检测到数据下载、加载或预处理脚本。")
    if MODEL_NAME_RE.search(name) or re.search(r"from_pretrained|load_state_dict|hf_hub_download|torch\.load", text, re.IGNORECASE):
        add("MODEL-01", "model-loading", r"from_pretrained|load_state_dict|hf_hub_download|torch\.load", "检测到模型权重加载或下载代码。")
    if re.search(r"pip\s+install|conda\s+(?:create|install)|poetry\s+install|npm\s+install", text, re.IGNORECASE):
        add("ENV-03", "install-script", r"pip\s+install|conda\s+(?:create|install)|poetry\s+install|npm\s+install", "检测到安装命令。")
    return signals


def _is_entrypoint(path: str, text: str, suffix: str) -> bool:
    name = Path(path).name.lower()
    parts = {part.lower() for part in Path(path).parts}
    if suffix in {".sh", ".ps1"}:
        return True
    if name in {
        "train.py", "finetune.py", "pretrain.py", "evaluate.py", "eval.py",
        "infer.py", "predict.py", "main.py", "run.py", "prepare.py", "preprocess.py",
        "download.py", "download_data.py", "prepare_data.py", "run.sh", "train.sh",
        "evaluate.sh", "prepare.sh", "download.sh", "makefile", "dockerfile",
    }:
        return True
    if parts & {"scripts", "script", "tools", "bin", "examples", "demo"}:
        return True
    return "if __name__" in text and "__main__" in text


def analyze_script(path: str, text: str) -> list[ScriptSignal]:
    suffix = Path(path).suffix.lower()
    if suffix not in SCRIPT_SUFFIXES and Path(path).name.lower() not in {"makefile", "dockerfile"}:
        return []
    if not _is_entrypoint(path, text, suffix):
        return []
    signals: list[ScriptSignal] = []
    if suffix == ".py":
        signals.extend(_python_signals(text, path))
    signals.extend(_text_signals(text, path))
    # Keep evidence bounded per file while preserving the highest-value signals.
    result: list[ScriptSignal] = []
    seen: set[str] = set()
    for signal in signals:
        if signal.criterion_id in seen:
            continue
        seen.add(signal.criterion_id)
        result.append(signal)
    return result
