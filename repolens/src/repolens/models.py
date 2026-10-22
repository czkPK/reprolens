from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Evidence:
    id: str
    kind: str
    path: str
    line: int | None
    excerpt: str


@dataclass
class CriterionResult:
    id: str
    dimension: str
    title: str
    status: str
    points: float
    max_points: float
    applicable: bool
    note: str
    evidence_ids: list[str] = field(default_factory=list)


@dataclass
class Finding:
    id: str
    severity: str
    criterion_id: str
    title: str
    message: str
    evidence_ids: list[str] = field(default_factory=list)


@dataclass
class Remediation:
    finding_id: str
    action: str
    rationale: str
    cost: str
    impact: str
    estimated_score_gain: float
    evidence_ids: list[str] = field(default_factory=list)


@dataclass
class DimensionScore:
    name: str
    points: float
    max_points: float
    percent: float


@dataclass
class ProbeResult:
    name: str
    command: str
    status: str
    returncode: int | None
    duration_seconds: float
    stdout: str
    stderr: str


@dataclass
class AuditResult:
    repo_path: str
    generated_at: str
    total_score: float
    readiness: str
    dimensions: list[DimensionScore]
    criteria: list[CriterionResult]
    findings: list[Finding]
    remediations: list[Remediation]
    evidence: list[Evidence]
    files_scanned: int
    probes: list[ProbeResult] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

