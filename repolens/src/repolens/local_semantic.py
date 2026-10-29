from __future__ import annotations

import hashlib
import json
import math
import re
import unicodedata
from pathlib import Path
from typing import Any

from .models import AuditResult

MODEL_PATH = Path(__file__).with_name("data") / "reprolens-small-semantic-v1.json"
_WORD_RE = re.compile(r"[a-z0-9][a-z0-9_.+-]*|[\u4e00-\u9fff]+", re.IGNORECASE)
_CJK_RE = re.compile(r"^[\u4e00-\u9fff]+$")
_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "for", "from",
    "has", "have", "in", "is", "it", "of", "on", "or", "that", "the", "this",
    "to", "using", "we", "with", "will", "our", "project", "repository",
}


def _bucket(token: str, dimension: int) -> int:
    digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "big") % dimension


def _tokens(text: str) -> list[str]:
    normalized = unicodedata.normalize("NFKC", text).lower()
    features: list[str] = []
    for word in _WORD_RE.findall(normalized):
        if word in _STOPWORDS:
            continue
        features.append(f"w:{word}")
        if _CJK_RE.fullmatch(word):
            for size in (2, 3):
                features.extend(f"c:{word[i:i + size]}" for i in range(len(word) - size + 1))
        else:
            for size in (3, 4, 5):
                if len(word) >= size:
                    features.extend(f"c:{word[i:i + size]}" for i in range(len(word) - size + 1))
    return features


def _vectorize(text: str, dimension: int, idf: dict[str, float]) -> dict[int, float]:
    counts: dict[int, int] = {}
    for token in _tokens(text):
        bucket = _bucket(token, dimension)
        counts[bucket] = counts.get(bucket, 0) + 1
    vector = {
        bucket: (1.0 + math.log(count)) * idf.get(str(bucket), 1.0)
        for bucket, count in counts.items()
    }
    norm = math.sqrt(sum(value * value for value in vector.values()))
    if norm:
        vector = {bucket: value / norm for bucket, value in vector.items()}
    return vector


def _cosine(left: dict[int, float], right: dict[int, float]) -> float:
    if len(left) > len(right):
        left, right = right, left
    return sum(value * right.get(bucket, 0.0) for bucket, value in left.items())


def _normalize(vector: dict[int, float]) -> dict[int, float]:
    norm = math.sqrt(sum(value * value for value in vector.values()))
    return {bucket: value / norm for bucket, value in vector.items()} if norm else {}


def build_model(training: dict[str, Any]) -> dict[str, Any]:
    dimension = int(training.get("dimension", 2048))
    criteria = training["criteria"]
    documents: list[tuple[str, list[str]]] = []
    for criterion_id, payload in criteria.items():
        examples = [payload["title"], *payload["examples"]]
        documents.extend((criterion_id, _tokens(text)) for text in examples)

    doc_count = len(documents)
    frequency: dict[str, int] = {}
    for _, tokens in documents:
        for bucket in {str(_bucket(token, dimension)) for token in tokens}:
            frequency[bucket] = frequency.get(bucket, 0) + 1
    idf = {
        bucket: math.log((1.0 + doc_count) / (1.0 + count)) + 1.0
        for bucket, count in frequency.items()
    }

    sums: dict[str, dict[int, float]] = {}
    for criterion_id, tokens in documents:
        vector = _vectorize(" ".join(tokens), dimension, idf)
        # _vectorize tokenizes the joined string again; combine the original token list directly instead.
        counts: dict[int, int] = {}
        for token in tokens:
            bucket = _bucket(token, dimension)
            counts[bucket] = counts.get(bucket, 0) + 1
        vector = {
            bucket: (1.0 + math.log(count)) * idf.get(str(bucket), 1.0)
            for bucket, count in counts.items()
        }
        vector = _normalize(vector)
        aggregate = sums.setdefault(criterion_id, {})
        for bucket, value in vector.items():
            aggregate[bucket] = aggregate.get(bucket, 0.0) + value

    prototypes = {criterion_id: _normalize(vector) for criterion_id, vector in sums.items()}
    return {
        "schema_version": 1,
        "model_id": training.get("model_id", "ReproLens-SmallSemantic-v1"),
        "version": training.get("version", "1.0.0"),
        "license": training.get("license", "MIT"),
        "algorithm": "hashed-character-ngram-tfidf-centroid",
        "dimension": dimension,
        "min_similarity": float(training.get("min_similarity", 0.20)),
        "second_ratio": float(training.get("second_ratio", 0.90)),
        "idf": idf,
        "criteria": {
            criterion_id: {
                "title": criteria[criterion_id]["title"],
                "prototype": {str(bucket): round(value, 6) for bucket, value in prototypes[criterion_id].items()},
            }
            for criterion_id in criteria
        },
        "training_data_sha256": hashlib.sha256(
            json.dumps(training, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest(),
    }


def load_model(path: Path = MODEL_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def predict_claims(result: AuditResult, rules: list[dict], path: Path = MODEL_PATH) -> tuple[list[dict], dict[str, Any]]:
    model = load_model(path)
    dimension = int(model["dimension"])
    idf = {str(key): float(value) for key, value in model["idf"].items()}
    applicable = {item.id: item for item in result.criteria if item.applicable}
    prototypes = {
        criterion_id: {int(bucket): float(value) for bucket, value in payload["prototype"].items()}
        for criterion_id, payload in model["criteria"].items()
        if criterion_id in applicable
    }
    predictions: list[dict] = []
    for row in rules:
        claim = str(row.get("claim", "")).strip()
        if not claim:
            continue
        vector = _vectorize(claim, dimension, idf)
        ranked = sorted(
            ((criterion_id, _cosine(vector, prototype)) for criterion_id, prototype in prototypes.items()),
            key=lambda item: item[1],
            reverse=True,
        )
        if not ranked or ranked[0][1] < float(model["min_similarity"]):
            continue
        best_id, best_score = ranked[0]
        selected = [best_id]
        if len(ranked) > 1 and ranked[1][1] >= best_score * float(model["second_ratio"]):
            selected.append(ranked[1][0])
        confidence = "high" if best_score >= 0.45 else "medium" if best_score >= 0.28 else "low"
        predictions.append({
            "claim_id": row["claim_id"],
            "criterion_ids": selected,
            "confidence": confidence,
            "reason": f"本地语义模型匹配：{ranked[0][0]} 相似度 {best_score:.3f}；候选：" + ", ".join(
                f"{criterion_id}={score:.3f}" for criterion_id, score in ranked[:3]
            ),
        })
    return predictions, {
        "mode": "local-semantic",
        "enabled": True,
        "provider": "local",
        "model": model["model_id"],
        "model_version": model["version"],
        "license": model["license"],
        "algorithm": model["algorithm"],
        "claims_enhanced": 0,
        "validation": "criterion and evidence IDs are checked against repository evidence",
        "external_api": False,
    }
