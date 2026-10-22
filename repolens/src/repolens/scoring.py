from __future__ import annotations

from collections import OrderedDict

from .models import CriterionResult, DimensionScore


DIMENSION_ORDER = [
    "环境可复现",
    "数据可复现",
    "模型可复现",
    "实验可复现",
    "文档可复现",
    "LLM 特有风险",
]


def score_dimensions(criteria: list[CriterionResult]) -> list[DimensionScore]:
    grouped: dict[str, list[CriterionResult]] = OrderedDict((name, []) for name in DIMENSION_ORDER)
    for item in criteria:
        grouped.setdefault(item.dimension, []).append(item)

    dimensions: list[DimensionScore] = []
    for name, items in grouped.items():
        applicable = [item for item in items if item.applicable]
        max_points = sum(item.max_points for item in applicable)
        points = sum(item.points for item in applicable)
        percent = round(points / max_points * 100, 1) if max_points else 100.0
        dimensions.append(
            DimensionScore(name=name, points=round(points, 1), max_points=round(max_points, 1), percent=percent)
        )
    return dimensions


def total_score(criteria: list[CriterionResult]) -> float:
    applicable = [item for item in criteria if item.applicable]
    max_points = sum(item.max_points for item in applicable)
    points = sum(item.points for item in applicable)
    return round(points / max_points * 100, 1) if max_points else 0.0


def readiness_label(score: float) -> str:
    if score >= 85:
        return "Ready"
    if score >= 65:
        return "Partially Ready"
    if score >= 40:
        return "At Risk"
    return "Not Ready"

