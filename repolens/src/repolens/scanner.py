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
HTML_TAG_RE = re.compile(r"<[^>]+>")
MARKDOWN_IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
PLAIN_URL_RE = re.compile(r"https?://\S+")


@dataclass
class RepoSnapshot:
    root: Path
    files: list[Path]
    texts: dict[str, str]
    evidence: list[Evidence] = field(default_factory=list)
    flags: dict[str, bool] = field(default_factory=dict)
    flags_evidence: dict[str, list[str]] = field(default_factory=dict)
    placeholder_flags: set[str] = field(default_factory=set)
    project_type: str = "unknown"

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
        names = {"requirements.txt", "pyproject.toml", "environment.yml", "environment.yaml", "pipfile", "package.json"}
        parts = [text for path, text in self.texts.items() if Path(path).name.lower() in names]
        return "\n".join(parts)


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _line_excerpt(text: str, offset: int) -> str:
    start = text.rfind("\n", 0, offset) + 1
    end = text.find("\n", offset)
    if end < 0:
        end = len(text)
    return text[start:end].strip()


def _first_match(text: str, pattern: str) -> re.Match[str] | None:
    return re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)


def _clean_claim_line(value: str) -> str:
    value = MARKDOWN_IMAGE_RE.sub("", value)
    value = MARKDOWN_LINK_RE.sub(r"\1", value)
    value = HTML_TAG_RE.sub(" ", value)
    value = PLAIN_URL_RE.sub("", value)
    value = value.replace("**", "").replace("__", "").replace("`", "")
    value = re.sub(r"^[#>*\-\s]+", "", value)
    return re.sub(r"\s+", " ", value).strip()


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
            is_model_source = name in {"__init__.py", "model.py", "models.py", "hub.py", "download.py"} or "/models/" in low
            if is_root_readme or is_docs_readme or is_relevant_doc or is_config or is_prompt or is_script or is_card or is_model_source:
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
    add_file_flag("deps", r"(^|/)requirements\.txt$|(^|/)pyproject\.toml$|(^|/)environment\.ya?ml$|(^|/)pipfile$|(^|/)package\.json$", "dependency-manifest")
    add_file_flag("lockfile", r"(^|/)(poetry\.lock|uv\.lock|requirements\.lock|pipfile\.lock|package-lock\.json)$", "lockfile")
    add_file_flag("container", r"(^|/)dockerfile$|(^|/)docker-compose\.ya?ml$", "container")
    add_file_flag("model_card", r"(^|/)model[_-]?card\.(md|txt|ya?ml)$", "model-card")
    add_file_flag("dataset_card", r"(^|/)dataset[_-]?card\.(md|txt|ya?ml)$", "dataset-card")
    add_file_flag("license", r"(^|/)(license|copying)(\.|$)", "license")
    add_file_flag("ci", r"(^|/)\.github/workflows/.*\.ya?ml$", "ci")
    add_file_flag("tests", r"(^|/)tests?/.*\.py$|(^|/)test_.*\.py$|\.(test|spec)\.(js|jsx|ts|tsx)$|(^|/)__tests__/|(^|/)playwright\.config\.ts$", "tests")
    add_file_flag("train_script", r"(^|/)(train|finetune|pretrain)[^/]*\.py$", "script")
    add_file_flag("eval_script", r"(^|/)(eval|evaluate|infer|predict)[^/]*\.py$", "script")
    add_file_flag("data_script", r"(^|/)data/.*(download|prepare|preprocess|process_data)[^/]*\.(py|sh)$|^(download|prepare|preprocess|process_data)(_data)?[^/]*\.(py|sh)$|^data_(download|prepare|preprocess|process)[^/]*\.(py|sh)$", "script")
    add_file_flag("reproduce_script", r"(^|/)(reproduce|run|setup)[^/]*\.(sh|ps1)$|(^|/)makefile$", "script")
    add_file_flag("config", r"(^|/)(configs?|conf)/.*\.(ya?ml|json|toml)$|^config[^/]*\.(py|ya?ml|json)$", "config")
    add_file_flag("prompt_files", r"(^|/)prompts?/|^prompt[^/]*\.(txt|md|ya?ml|json)$", "prompt", exclude_github=True)
    weight_path = first_matching(r"\.(pt|pth|ckpt|bin|safetensors)$")
    if weight_path and not any(part in {"docs", "tests", "examples", ".inline-snapshot"} for part in weight_path.parts):
        snapshot.mark("weights", snapshot.add_evidence("weights", weight_path, None, weight_path.name))

    def find_text(pattern: str, flag: str, kind: str) -> bool:
        for rel_path, text in preferred_text_items():
            match = _first_match(text, pattern)
            if not match:
                continue
            path = root / rel_path
            line = _line_number(text, match.start())
            evidence_id = snapshot.add_evidence(kind, path, line, _line_excerpt(text, match.start()))
            around = text[max(0, match.start() - 80):match.end() + 80]
            if PLACEHOLDER_RE.search(around):
                snapshot.mark_placeholder(flag)
            else:
                snapshot.mark(flag, evidence_id)
            return True
        return False

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

    def is_config_only(rel_path: str) -> bool:
        low = rel_path.lower()
        name = Path(rel_path).name.lower()
        return low.startswith(("configs/", "config/", "conf/")) or (name.startswith("config") and name.endswith((".yaml", ".yml", ".toml", ".json")))

    def find_text_scoped(pattern: str, flag: str, kind: str, predicate) -> None:
        for rel_path, text in preferred_text_items():
            if not predicate(rel_path):
                continue
            match = _first_match(text, pattern)
            if not match:
                continue
            path = root / rel_path
            line = _line_number(text, match.start())
            evidence_id = snapshot.add_evidence(kind, path, line, _line_excerpt(text, match.start()))
            around = text[max(0, match.start() - 80):match.end() + 80]
            if PLACEHOLDER_RE.search(around):
                snapshot.mark_placeholder(flag)
            else:
                snapshot.mark(flag, evidence_id)
            return

    def find_model_source_link() -> None:
        artifact_url_re = re.compile(
            r"huggingface\.co/(?!(?:datasets|docs|blog|papers|spaces)/)[^/\s)]+/[^\s)]+"
            r"|(?:pan\.baidu\.com|drive\.google\.com|1drv\.ms|dropbox\.com|mega\.nz)[^\s)]*"
            r"|(?:storage\.googleapis\.com|dl\.fbaipublicfiles\.com|openaipublic\.azureedge\.net)[^\s)]*(?:(?:models?|checkpoints?|weights?)[^\s)]*|\.(?:pt|pth|ckpt|bin|safetensors|zip|npz)(?:[?#][^\s)]*)?)"
            r"|github\.com/[^\s)]+/releases/download[^\s)]*"
            r"|https?://[^\s)]+\.(?:pt|pth|ckpt|bin|safetensors|zip|npz)(?:[?#][^\s)]*)?",
            re.IGNORECASE,
        )
        model_re = re.compile(r"model|checkpoint|weights|pre-?trained", re.IGNORECASE)
        for rel_path, text in preferred_text_items():
            lines = text.splitlines()
            for index, line in enumerate(lines):
                for match in artifact_url_re.finditer(line):
                    context = " ".join(lines[max(0, index - 4): min(len(lines), index + 3)])
                    if not model_re.search(context):
                        continue
                    path = root / rel_path
                    evidence_id = snapshot.add_evidence("model-source", path, index + 1, line.strip())
                    snapshot.mark("model_source_link", evidence_id)
                    snapshot.mark("model_version", evidence_id)
                    return

    def find_data_license() -> None:
        license_re = re.compile(
            r"\bCC[ -]?BY(?:[ -][A-Z0-9.]+)?\b|\bCreative Commons\b|"
            r"\b(?:released|distributed|licensed)\s+under[^\n]{0,100}\blicen[cs]e\b",
            re.IGNORECASE,
        )
        data_re = re.compile(
            r"\b(?:data|datasets?|data sets?|training data|validation data|evaluation data|corpus|data source)\b",
            re.IGNORECASE,
        )
        for rel_path, text in preferred_text_items():
            lines = text.splitlines()
            for index, line in enumerate(lines):
                match = license_re.search(line)
                if not match:
                    continue
                line_has_data = bool(data_re.search(line))
                heading_has_data_license = any(
                    data_re.search(context_line) and re.search(r"licen[cs]e", context_line, re.IGNORECASE)
                    for context_line in lines[max(0, index - 4): index]
                )
                if not line_has_data and not heading_has_data_license:
                    continue
                path = root / rel_path
                evidence_id = snapshot.add_evidence(
                    "data-license",
                    path,
                    index + 1,
                    line.strip(),
                )
                snapshot.mark("data_license", evidence_id)
                return

    find_text(r"pip install|conda env|docker build|uv sync|poetry install", "install_instructions", "instruction")
    train_instruction_pattern = (
        r"(?:\bpython(?:3)?\b[^\n]*(?:\btrain(?:ing)?\b|finetun|--train|--finetune|(?:^|\s)-m\s+[^\n]*\b(?:train|main)\b))"
        r"|(?:\b(?:torchrun|accelerate\s+launch|deepspeed)\b[^\n]*(?:train|finetun|\.py))"
        r"|(?:\b(?:bash|sh)\b[^\n]*(?:train|finetun)[^\n]*\.sh)"
        r"|(?:\bmake\s+(?:train|finetune|finetuning)\b)"
    )
    run_instruction_pattern = (
        r"^\s*(?:\$ )?(?:python(?:3)?|pip|conda|uv|poetry|bash\s+\S+|sh\s+\S+|"
        r"docker\s+\w+|torchrun|accelerate\s+launch|deepspeed)\b[^\n]+"
    )
    if find_text(train_instruction_pattern, "train_instruction", "training-command"):
        train_evidence = snapshot.evidence_for("train_instruction")
        if train_evidence:
            snapshot.mark("run_instructions", train_evidence[0])
    else:
        find_text(run_instruction_pattern, "run_instructions", "instruction")
    dataset_link_pattern = (
        r"(?:huggingface\.co/datasets/|kaggle\.com/|zenodo\.org/|figshare\.com/|drive\.google\.com/)"
        r"|(?:\b(?:download|获取|下载)\b[^\n]{0,100}\b(?:dataset|data set|training data)\b)"
        r"|(?:\b(?:dataset|data set|training data)\b[^\n]{0,100}(?:https?://|huggingface|google drive|kaggle|zenodo|figshare))"
    )
    data_mention_pattern = r"\b(?:dataset|data sets?|training data|validation data|evaluation data|test data|data source)\b"
    if find_text(dataset_link_pattern, "data_source_link", "data-source"):
        source_evidence = snapshot.evidence_for("data_source_link")
        if source_evidence:
            snapshot.mark("data_mention", source_evidence[0])
    else:
        find_text(data_mention_pattern, "data_mention", "data")
    data_download_pattern = (
        r"(?:\b(?:hf|huggingface-cli)\s+download\b[^\n]*(?:--repo-type\s+dataset|dataset))"
        r"|(?:\bload_dataset\s*\()"
        r"|(?:\bgit\s+clone\b[^\n]*(?:dataset|data))"
        r"|(?:\b(?:wget|curl)\b[^\n]*(?:dataset|data))"
        r"|(?:\bpython\b[^\n]*(?:download|prepare|preprocess)\w*[^\n]*(?:data|dataset))"
    )
    find_text(data_download_pattern, "data_download_command", "data-command")
    find_data_license()
    find_text(r"accuracy|f1|bleu|rouge|psnr|ssim|expected|reproduce", "expected_results", "metric")
    find_text(r"torch\.manual_seed\s*\(\s*\d+|np\.random\.seed\s*\(\s*\d+|random_state\s*=\s*\d+|seed\s*[:=]\s*\d+", "seed", "determinism")
    find_text(r"cuda|gpu|a100|v100|h100|vram|nvidia", "hardware", "hardware")
    find_model_source_link()
    model_version_pattern = (
        r"model_name|model_id|model version|api version|model[_ -]?checkpoint|"
        r"huggingface\.co/(?!datasets/)[^\s)]+|gpt-[0-9]|claude-[0-9]|"
        r"llama[- ]?[0-9]|qwen[- ]?[0-9]|mistral-[0-9]|gemini-[0-9]"
    )
    find_text(model_version_pattern, "model_version", "model")
    find_text(r"prompt|system message|template", "prompt_mention", "prompt")
    find_text(r"train[/_-]?(val|test)|validation|split", "eval_split", "evaluation")
    find_text(r"contamination|leakage|data leak", "contamination", "evaluation")
    find_text(r"gpu hour|training time|inference cost|inference latency|token usage|tokens per second|cost", "cost", "cost")
    model_provider_pattern = (
        r"openai\s*(?:api|api key|\.com/v1)|openai-compatible|anthropic\s*api|"
        r"azure\s*openai|gemini\s*api|cohere\s*api|\bollama\b|\bvllm\b|"
        r"\blitellm\b|aws\s*bedrock"
    )
    find_text(model_provider_pattern, "model_provider", "llm-provider")
    llm_explicit_pattern = (
        r"\blarge language models?\b|\bLLMs?\b|chatgpt|prompt template|"
        r"system message|retrieval[- ]augmented(?: generation)?|\bRAG\b|"
        r"llm agent|tool call|function calling|openai-compatible"
    )
    find_text(llm_explicit_pattern, "llm_explicit", "llm")
    find_text_scoped(r"prompt_version|template_version|prompt[^\n]*version|version[^\n]*prompt", "prompt_version", "prompt", is_prompt_or_config)
    find_text_scoped(r"temperature|top_p|top_k|max_tokens|presence_penalty|frequency_penalty", "sampling_params", "llm-config", is_config_or_script)
    find_text_scoped(r"tokenizer|context_window|context window|max_context|tiktoken|sentencepiece", "tokenizer", "llm-config", is_config_or_script)
    find_text(r"retrieval[- ]augmented generation|\bRAG\b|retriever|vector store|vector database|faiss|chroma|pinecone|weaviate|qdrant|milvus", "rag_project", "rag")
    find_text_scoped(r"index_name|index_version|collection_name|vector_store|embedding_model|chunk_size|chunk_overlap|knowledge base", "rag_index", "rag", is_config_or_script)
    find_text(r"tool_call|tool call|langgraph|autogen|crewai|\bMCP\b|function calling|llm agent|retrieval[- ]augmented agent|multi-agent system", "agent_project", "agent")
    find_text_scoped(r"agent[_ -]?trace|tool[_ -]?trace|trajectory|tool_call|tool call|run_id|session_id|trace_id", "agent_trace", "agent", is_config_or_script)
    find_text_scoped(r"chunk_size|chunk_overlap|index_name|collection_name|index_version|embedding_model", "rag_config", "rag", is_config_only)
    find_text_scoped(r"run_id|session_id|trace_id|trace_path|log_path", "agent_trace_artifact", "agent", lambda rel_path: is_config_only(rel_path) or "trace" in rel_path.lower() or "log" in rel_path.lower())
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
        snapshot.has("llm_explicit")
        or snapshot.has("rag_project")
        or snapshot.has("agent_project")
        or (snapshot.has("model_provider") and snapshot.has("prompt_mention"))
    ):
        snapshot.mark("llm_project", snapshot.evidence_for("llm_explicit", "prompt_files", "model_provider", "model_version", "rag_project", "agent_project", "deps"))

    root_readme_text = "\n".join(
        text for rel_path, text in texts.items()
        if "/" not in rel_path and Path(rel_path).name.lower().startswith("readme")
    ).lower()
    if any(phrase in root_readme_text for phrase in (
        "any llm", "almost any llm", "choice of model", "models are discovered",
        "multiple models", "model providers", "openai-compatible apis", "cloud and local",
        "local or cloud llm", "closed and open-source llm", "dynamic model routing", "all popular",
        "external model api",
    )):
        snapshot.mark("model_agnostic", snapshot.evidence_for("readme"))
    has_app_entry = any(
        "/" not in rel_path and Path(rel_path).name.lower() in {"app.py", "main.py"}
        for rel_path in texts
    ) or any(rel_path.lower().startswith(("server/", "ui/", "web/", "frontend/", "backend/")) for rel_path in texts)
    is_demo_app = any(
        phrase in root_readme_text
        for phrase in ("demo llm", "demo app", "web app", "chat app", "assistant app", "rag app")
    )
    has_frontend_app = any(
        rel_path.lower() in {"server.js", "vite.config.ts", "next.config.js", "svelte.config.js"}
        for rel_path in texts
    ) or (
        any(rel_path.lower() == "package.json" for rel_path in texts)
        and any(rel_path.lower().startswith(("packages/ui/", "src/routes/", "src/lib/")) for rel_path in texts)
    )
    has_python_cli = any(rel_path.lower().endswith("/__main__.py") for rel_path in texts) and any(
        token in root_readme_text for token in ("cli", "command line", "pair program")
    )
    if "memory layer" in root_readme_text or "memory framework" in root_readme_text:
        snapshot.project_type = "memory_framework"
    elif has_app_entry or has_frontend_app or has_python_cli or is_demo_app:
        snapshot.project_type = "application"
    elif snapshot.has("agent_project") and snapshot.has("prompt_files"):
        snapshot.project_type = "agent_framework"
    elif "api library" in root_readme_text or "sdk" in root_readme_text or "client library" in root_readme_text:
        snapshot.project_type = "sdk"
    elif snapshot.has("ml_project"):
        snapshot.project_type = "ml_project"
    else:
        snapshot.project_type = "unknown"
    if snapshot.has("model_agnostic") and snapshot.project_type not in {"sdk", "agent_framework", "memory_framework", "application"}:
        snapshot.flags["model_agnostic"] = False

    claim_keywords = (
        "reproduce", "benchmark", "accuracy", "f1", "bleu", "rouge",
        "install", "quickstart", "docker", "pytest", "dataset", "seed",
        "rag", "retrieval", "vector store", "embedding", "tool call",
        "trace", "prompt version", "model version", "model provider",
        "api version", "openai", "huggingface", "evaluation dataset",
    )
    claim_excludes = (
        "copyright", "all rights reserved", "full documentation",
        "documentation can be found", "changelog", "contributing",
        "check out", "learn more", "read the docs", "for more information",
        "install the package", "launch blog",
    )
    claim_count = 0
    seen_claims: set[str] = set()
    in_code_block = False
    for rel_path, text in texts.items():
        if "/" in rel_path or not Path(rel_path).name.lower().startswith("readme"):
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            if len(stripped) < 30 or stripped.startswith(("[![", "<img", "<!--", "|", "```")):
                continue
            cleaned = _clean_claim_line(stripped)
            cleaned_lower = cleaned.lower()
            if any(excluded in cleaned_lower for excluded in claim_excludes):
                continue
            if cleaned.startswith(("$", ">", "{", "}", "pip ", "python ", "from ", "import ", "api_base=")):
                continue
            if any(keyword in cleaned_lower for keyword in claim_keywords):
                key = cleaned.lower()
                if len(cleaned) < 24 or key in seen_claims:
                    continue
                seen_claims.add(key)
                snapshot.add_evidence("claim", root / rel_path, line_no, cleaned)
                claim_count += 1
                if claim_count >= 8:
                    break
        if claim_count >= 8:
            break

    return snapshot


