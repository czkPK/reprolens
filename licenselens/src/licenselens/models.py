from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class UsageMode(str, Enum):
    INTERNAL = "internal"
    SAAS = "saas"
    BINARY_DISTRIBUTION = "binary-distribution"
    SOURCE_DISTRIBUTION = "source-distribution"
    MODEL_REDISTRIBUTION = "model-redistribution"


DISTRIBUTION_MODES = {
    UsageMode.BINARY_DISTRIBUTION,
    UsageMode.SOURCE_DISTRIBUTION,
    UsageMode.MODEL_REDISTRIBUTION,
}


@dataclass(frozen=True)
class LicenseInfo:
    spdx: str
    name: str
    obligations: tuple[str, ...] = ()
    source_disclosure: bool = False
    network_copyleft: bool = False
    notice_required: bool = False
    unknown: bool = False
    proprietary: bool = False


@dataclass
class Dependency:
    name: str
    version: str | None
    license_spdx: str
    source: str
    confidence: float = 1.0
    evidence: list[str] = field(default_factory=list)


@dataclass
class Finding:
    id: str
    severity: str
    package: str
    license_spdx: str
    rule: str
    message: str
    evidence: list[str] = field(default_factory=list)


@dataclass
class Remediation:
    finding_id: str
    action: str
    rationale: str
    cost: str
    impact: str
    evidence: list[str] = field(default_factory=list)


@dataclass
class AnalysisResult:
    project_root: str
    usage_mode: str
    project_license: str | None
    dependencies: list[Dependency]
    findings: list[Finding]
    remediations: list[Remediation]
    generated_at: str
    tool_version: str = "0.1.0"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
