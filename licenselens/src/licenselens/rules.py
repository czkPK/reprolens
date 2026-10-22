from __future__ import annotations

from .catalog import get_license
from .models import DISTRIBUTION_MODES, Dependency, Finding, UsageMode


_COPYLEFT_PROJECT_LICENSES = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause"}


def analyze_dependencies(
    dependencies: list[Dependency],
    usage_mode: UsageMode,
    project_license: str | None,
) -> list[Finding]:
    findings: list[Finding] = []
    seen: set[tuple[str, str]] = set()

    def add(package: str, spdx: str, rule: str, severity: str, message: str, evidence: list[str]) -> None:
        key = (package.lower(), rule)
        if key in seen:
            return
        seen.add(key)
        findings.append(
            Finding(
                id=f"F-{len(findings) + 1:03d}",
                severity=severity,
                package=package,
                license_spdx=spdx,
                rule=rule,
                message=message,
                evidence=evidence,
            )
        )

    for dep in dependencies:
        info = get_license(dep.license_spdx)
        base_evidence = list(dep.evidence) + [f"license:{info.spdx}"]
        if info.unknown:
            add(
                dep.name,
                info.spdx,
                "unknown-or-proprietary-license",
                "high",
                f"{dep.name} 的许可证无法可靠识别，需要人工核验原始 LICENSE 和依赖条款。",
                base_evidence,
            )
            continue

        if usage_mode == UsageMode.SAAS and info.network_copyleft:
            add(
                dep.name,
                info.spdx,
                "network-copyleft",
                "high",
                f"{dep.name} 使用 {info.spdx}，在对外提供 SaaS 服务时可能触发网络 copyleft 义务，需要隔离或替换。",
                base_evidence + ["obligation:network-copyleft"],
            )

        if usage_mode in DISTRIBUTION_MODES and info.source_disclosure:
            add(
                dep.name,
                info.spdx,
                "distribution-copyleft",
                "high",
                f"{dep.name} 使用 {info.spdx}，在分发场景下可能要求提供相应源代码并遵守 copyleft 条款。",
                base_evidence + ["obligation:provide-source"],
            )

        if usage_mode != UsageMode.INTERNAL and info.notice_required:
            add(
                dep.name,
                info.spdx,
                "notice-required",
                "info",
                f"{dep.name} 使用 {info.spdx}，分发或对外服务时应保留版权、许可证和 NOTICE 信息。",
                base_evidence + ["obligation:include-notice"],
            )

        if (
            project_license in _COPYLEFT_PROJECT_LICENSES
            and info.source_disclosure
            and usage_mode in DISTRIBUTION_MODES
        ):
            add(
                dep.name,
                info.spdx,
                "project-license-conflict",
                "high",
                f"项目声明许可证为 {project_license}，而依赖 {dep.name} 为 {info.spdx}，分发时可能存在许可证兼容性冲突。",
                base_evidence + [f"project-license:{project_license}"],
            )

    return findings
