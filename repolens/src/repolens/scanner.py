from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .models import Evidence


TEXT_SUFFIXES = {
    ".md", ".rst", ".txt", ".py", ".toml", ".yaml", ".yml", ".json", ".cfg",
    ".ini", ".sh", ".ps1", ".dockerfile", ".c", ".cpp", ".h", ".hpp", ".java",
    ".js", ".ts", ".tsx", ".jsx", ".ipynb", ".csv", ".tsv",
}
SPECIAL_NAMES = {
    "Dockerfile", "Makefile", "LICENSE", "COPYING", "requirements.txt",
    "environment.yml", "environment.yaml", "Pipfile", "poetry.lock", "uv.lock",
    "package-lock.json", "README", "README.md", "README.rst",
}
IGNORE_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".mypy_cache", ".pytest_cache", "dist", "build"}
MAX_TEXT_BYTES = 400_000
PLACEHOLDER_RE = re.compile(r"TODO|PLACEHOLDER|CHANGE[_ -]?ME|YOUR_[A-Z_]+|REPLACE_ME|unversioned|not specified|TBD", re.IGNORECASE)


@dataclass
class RepoSnapshot:
    root: Path
    files: list[Path]
    texts: dict[str, str]
    evidence: list[Evidence] = field(default_factory=list)
    flags: dict[str, bool] = field(default_factory=dict)
    flags_evidence: dict[str, list[str]] = field(default_factory=dict)
    placeholder_flags: set[str] = field(default_factory=set)

    def rel(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()

    def add_evidence(self, kind: str, path: Path, line: int | None, excerpt: str) -> str:
        evidence_id = f"E-{len(self.evidence) + 1:03d}"
        self.evidence.append(
            Evidence(
                id=evidence_id,
                kind=kind,
                path=self.rel(path),
                line=line,
                excerpt=excerpt.strip()[:240],
            )
        )
        return evidence_id

    def mark(self, flag: str, evidence_id: str | None = None) -> None:
        self.flags[flag] = True
        if evidence_id:
            self.flags_evidence.setdefault(flag, []).append(evidence_id)

    def has(self, flag: str) -> bool:
        return bool(self.flags.get(flag))

    def has_placeholder(self, flag: str) -> bool:
        return flag in self.placeholder_flags

    def mark_placeholder(self, flag: str) -> None:
        self.placeholder_flags.add(flag)

    def evidence_for(self, *flags: str) -> list[str]:
        result: list[str] = []
        for flag in flags:
            for item in self.flags_evidence.get(flag, []):
                if item not in result:
                    result.append(item)
        return result

    def text_blob(self) -> str:
        return "\n".join(self.texts.values())

    def deps_text(self) -> str:
        names = {"requirements.txt", "pyproject.toml", "environment.yml", "environment.yaml", "pipfile"}
        parts = [text for path, text in self.texts.items() if Path(path).name.lower() in names]
        return "\n".join(parts)


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _first_match(text: str, pattern: str) -> re.Match[str] | None:
    return re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)


def scan_repo(root: Path) -> RepoSnapshot:
    files: list[Path] = []
    texts: dict[str, str] = {}

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        files.append(path)
        if path.name in SPECIAL_NAMES or path.suffix.lower() in TEXT_SUFFIXES:
            try:
                if path.stat().st_size <= MAX_TEXT_BYTES:
                    texts[path.relative_to(root).as_posix()] = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                pass

    snapshot = RepoSnapshot(root=root, files=files, texts=texts)
    def preferred_text_items():
        for rel_path, text in texts.items():
            low = rel_path.lower()
            name = Path(rel_path).name.lower()
            if any(part in low for part in (
                "changelog", "code_of_conduct", "contributing", "security",
                "api.md", "helpers.md", "bedrock.md", ".github/", "tests/",
                ".inline-snapshot", ".vscode", ".devcontainer", "pre-commit",
                "issue_template", ".castiron", "conftest.py", "setup.py",
                "openapi", "llms.txt", "_toctree",
            )):
                continue
            is_root_readme = "/" not in rel_path and name.startswith("readme")
            is_docs_readme = low in {"docs/readme.md", "docs/readme.rst"}
            is_relevant_doc = low.startswith("docs/") and any(
                token in name for token in ("readme", "index", "quickstart", "install", "getting_started", "tutorial", "guide", "agent", "rag", "prompt")
            )
            is_config = low.startswith(("configs/", "config/", "conf/")) or (low.startswith("config") and "/" not in low)
            is_prompt = low.startswith("prompts/") or (name.startswith("prompt") and "/" not in low)
            is_script = name in {"app.py", "main.py", "train.py", "eval.py", "evaluate.py", "infer.py", "predict.py", "reproduce.sh", "run.sh"}
            is_card = "model_card" in name or "dataset_card" in name
            if is_root_readme or is_docs_readme or is_relevant_doc or is_config or is_prompt or is_script or is_card:
                yield rel_path, text

    def first_matching(pattern: str) -> Path | None:
        regex = re.compile(pattern, re.IGNORECASE)
        for path in files:
            if regex.search(path.relative_to(root).as_posix()):
                return path
        return None

    def add_file_flag(flag: str, pattern: str, kind: str, exclude_github: bool = False) -> None:
        path = first_matching(pattern)
        if path and exclude_github and ".github/" in path.relative_to(root).as_posix().lower():
            path = None
        if path:
            text = texts.get(snapshot.rel(path), "")
            snippet = text.strip().splitlines()[0] if text.strip() else path.name
            evidence_id = snapshot.add_evidence(kind, path, 1 if text.strip() else None, snippet)
            snapshot.mark(flag, evidence_id)
            if PLACEHOLDER_RE.search(text):
                snapshot.mark_placeholder(flag)

    add_file_flag("readme", r"(^|/)readme(\.md|\.rst|\.txt)?$", "readme")
    add_file_flag("deps", r"(^|/)requirements\.txt$|(^|/)pyproject\.toml$|(^|/)environment\.ya?ml$|(^|/)pipfile$", "dependency-manifest")
    add_file_flag("lockfile", r"(^|/)(poetry\.lock|uv\.lock|requirements\.lock|pipfile\.lock|package-lock\.json)$", "lockfile")
    add_file_flag("container", r"(^|/)dockerfile$|(^|/)docker-compose\.ya?ml$", "container")
    add_file_flag("model_card", r"(^|/)model[_-]?card\.(md|txt|ya?ml)$", "model-card")
    add_file_flag("dataset_card", r"(^|/)dataset[_-]?card\.(md|txt|ya?ml)$", "dataset-card")
    add_file_flag("license", r"(^|/)(license|copying)(\.|$)", "license")
    add_file_flag("ci", r"(^|/)\.github/workflows/.*\.ya?ml$", "ci")
    add_file_flag("tests", r"(^|/)tests?/.*\.py$|(^|/)test_.*\.py$", "tests")
    add_file_flag("train_script", r"(^|/)(train|finetune|pretrain)[^/]*\.py$", "script")
    add_file_flag("eval_script", r"(^|/)(eval|evaluate|infer|predict)[^/]*\.py$", "script")
    add_file_flag("data_script", r"(^|/)(download|prepare|preprocess|process_data)[^/]*\.(py|sh)$", "script")
    add_file_flag("reproduce_script", r"(^|/)(reproduce|run|setup)[^/]*\.(sh|ps1)$|(^|/)makefile$", "script")
    add_file_flag("config", r"(^|/)(configs?|conf)/.*\.(ya?ml|json|toml)$|^config[^/]*\.(py|ya?ml|json)$", "config")
    add_file_flag("prompt_files", r"(^|/)prompts?/|^prompt[^/]*\.(txt|md|ya?ml|json)$", "prompt", exclude_github=True)
    weight_path = first_matching(r"\.(pt|pth|ckpt|bin|safetensors)$")
    if weight_path and not any(part in {"docs", "tests", "examples", ".inline-snapshot"} for part in weight_path.parts):
        snapshot.mark("weights", snapshot.add_evidence("weights", weight_path, None, weight_path.name))

    def find_text(pattern: str, flag: str, kind: str) -> None:
        for rel_path, text in preferred_text_items():
            match = _first_match(text, pattern)
            if not match:
                continue
            path = root / rel_path
            line = _line_number(text, match.start())
            evidence_id = snapshot.add_evidence(kind, path, line, match.group(0))
            around = text[max(0, match.start() - 80):match.end() + 80]
            if PLACEHOLDER_RE.search(around):
                snapshot.mark_placeholder(flag)
            else:
                snapshot.mark(flag, evidence_id)
            return

    def is_prompt_or_config(rel_path: str) -> bool:
        low = rel_path.lower()
        name = Path(rel_path).name.lower()
        return low.startswith(("prompts/", "configs/", "config/", "conf/")) or name.startswith(("prompt", "config")) or "prompt" in low

    def is_config_or_script(rel_path: str) -> bool:
        low = rel_path.lower()
        name = Path(rel_path).name.lower()
        return (
            low.startswith(("configs/", "config/", "conf/"))
            or name.startswith(("config", "app", "main", "train", "eval", "evaluate", "infer", "predict", "run", "reproduce"))
            or name.endswith(('.yaml', '.yml', '.toml', '.json'))
        )

    def find_text_scoped(pattern: str, flag: str, kind: str, predicate) -> None:
        for rel_path, text in preferred_text_items():
            if not predicate(rel_path):
                continue
            match = _first_match(text, pattern)
            if not match:
                continue
            path = root / rel_path
            line = _line_number(text, match.start())
            evidence_id = snapshot.add_evidence(kind, path, line, match.group(0))
            around = text[max(0, match.start() - 80):match.end() + 80]
            if PLACEHOLDER_RE.search(around):
                snapshot.mark_placeholder(flag)
            else:
                snapshot.mark(flag, evidence_id)
            return

    find_text(r"pip install|conda env|docker build|uv sync|poetry install", "install_instructions", "instruction")
    find_text(r"python[^\n]*(train|finetune)|bash[^\n]*\.sh|make[^\n]*", "run_instructions", "instruction")
    find_text(r"https?://|download|dataset", "data_mention", "data")
    find_text(r"accuracy|f1|bleu|rouge|psnr|ssim|expected|reproduce", "expected_results", "metric")
    find_text(r"torch\.manual_seed\s*\(\s*\d+|np\.random\.seed\s*\(\s*\d+|random_state\s*=\s*\d+|seed\s*[:=]\s*\d+", "seed", "determinism")
    find_text(r"cuda|gpu|a100|v100|h100|vram|nvidia", "hardware", "hardware")
    find_text(r"model_name|model version|checkpoint|huggingface|transformers", "model_version", "model")
    find_text(r"prompt|system message|template", "prompt_mention", "prompt")
    find_text(r"train[/_-]?(val|test)|validation|split", "eval_split", "evaluation")
    find_text(r"contamination|leakage|data leak", "contamination", "evaluation")
    find_text(r"gpu hour|training time|inference cost|inference latency|token usage|tokens per second|cost", "cost", "cost")
    find_text(r"openai|anthropic|azure openai|gemini|cohere|ollama|vllm|huggingface|transformers|litellm|bedrock", "model_provider", "llm-provider")
    find_text(r"model_name|model_id|model version|api version|gpt-[0-9]|claude-[0-9]|llama|qwen|mistral|gemini", "model_version", "model")
    find_text_scoped(r"prompt_version|template_version|prompt[^\n]*version|version[^\n]*prompt", "prompt_version", "prompt", is_prompt_or_config)
    find_text_scoped(r"temperature|top_p|top_k|max_tokens|presence_penalty|frequency_penalty", "sampling_params", "llm-config", is_config_or_script)
    find_text_scoped(r"tokenizer|context_window|context window|max_context|tiktoken|sentencepiece", "tokenizer", "llm-config", is_config_or_script)
    find_text(r"\brag\b|retrieval|retriever|embedding|vector store|faiss|chroma|pinecone|weaviate|qdrant|milvus|langchain|llamaindex", "rag_project", "rag")
    find_text_scoped(r"index_name|index_version|collection_name|vector_store|embedding_model|chunk_size|chunk_overlap|knowledge base", "rag_index", "rag", is_config_or_script)
    find_text(r"\bagent\b|tool_call|tool call|langgraph|autogen|crewai|mcp|function calling", "agent_project", "agent")
    find_text_scoped(r"trace|trajectory|tool_call|tool call|run_id|session_id", "agent_trace", "agent", is_config_or_script)
    find_text(r"eval dataset|evaluation set|benchmark|golden set|test set", "eval_dataset", "evaluation")

    deps_text = snapshot.deps_text().lower()
    all_text = snapshot.text_blob().lower()
    if (
        snapshot.has("train_script")
        or snapshot.has("eval_script")
        or any(name in deps_text for name in ("torch", "tensorflow", "jax", "keras", "scikit-learn", "sklearn", "transformers", "xgboost", "lightgbm"))
    ):
        snapshot.mark("ml_project", snapshot.evidence_for("train_script", "eval_script", "deps"))
    if (
        snapshot.has("prompt_mention")
        or snapshot.has("prompt_files")
        or snapshot.has("model_provider")
        or snapshot.has("rag_project")
        or snapshot.has("agent_project")
        or any(name in all_text for name in ("openai", "anthropic", "huggingface", "transformers", "llm", "chat model", "retrieval augmented"))
    ):
        snapshot.mark("llm_project", snapshot.evidence_for("prompt_mention", "prompt_files", "model_provider", "model_version", "rag_project", "agent_project", "deps"))

    return snapshot


