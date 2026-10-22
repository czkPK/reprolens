from __future__ import annotations

from .models import Finding, Remediation


def plan_remediations(findings: list[Finding]) -> list[Remediation]:
    remediations: list[Remediation] = []
    for finding in findings:
        if finding.rule in {"network-copyleft", "distribution-copyleft", "project-license-conflict"}:
            remediations.extend(
                [
                    Remediation(
                        finding_id=finding.id,
                        action=f"替换 {finding.package} 为 Apache-2.0/MIT 等更宽松许可的等价依赖",
                        rationale="从源头消除 copyleft 兼容性风险，通常是最稳定的整改方式。",
                        cost="medium",
                        impact="high",
                        evidence=finding.evidence,
                    ),
                    Remediation(
                        finding_id=finding.id,
                        action=f"将 {finding.package} 隔离为独立服务或独立进程，并评估其对外分发方式",
                        rationale="通过架构隔离降低衍生作品边界的不确定性，但需要法律与工程联合复核。",
                        cost="medium",
                        impact="medium",
                        evidence=finding.evidence + ["architecture:isolation"],
                    ),
                    Remediation(
                        finding_id=finding.id,
                        action=f"联系 {finding.package} 的版权方，确认商业许可或书面例外",
                        rationale="在无法替换依赖时，取得明确授权可以消除许可证不确定性。",
                        cost="high",
                        impact="high",
                        evidence=finding.evidence + ["process:commercial-license"],
                    ),
                ]
            )
        elif finding.rule == "unknown-or-proprietary-license":
            remediations.extend(
                [
                    Remediation(
                        finding_id=finding.id,
                        action=f"补充 {finding.package} 的原始 LICENSE、版本和来源证据",
                        rationale="未知许可证不能直接判定为可用，必须先完成证据核验。",
                        cost="low",
                        impact="high",
                        evidence=finding.evidence,
                    ),
                    Remediation(
                        finding_id=finding.id,
                        action=f"为 {finding.package} 寻找许可证明确的替代依赖",
                        rationale="当上游无法提供明确授权时，替换依赖比承担未知风险更可控。",
                        cost="medium",
                        impact="high",
                        evidence=finding.evidence,
                    ),
                ]
            )
        elif finding.rule == "notice-required":
            remediations.append(
                Remediation(
                    finding_id=finding.id,
                    action=f"将 {finding.package} 的版权与许可证信息加入 NOTICE/第三方声明",
                    rationale="满足署名和许可证保留义务，降低分发合规风险。",
                    cost="low",
                    impact="medium",
                    evidence=finding.evidence,
                )
            )
    return remediations
