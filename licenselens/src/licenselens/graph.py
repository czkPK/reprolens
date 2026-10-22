from __future__ import annotations

from .models import AnalysisResult


def build_graph(result: AnalysisResult) -> dict:
    nodes = [
        {
            "id": "project",
            "type": "project",
            "label": result.project_root,
            "license": result.project_license or "UNKNOWN",
            "usage_mode": result.usage_mode,
        }
    ]
    edges = []
    for dep in result.dependencies:
        dep_id = f"dep:{dep.name.lower()}"
        license_id = f"license:{dep.license_spdx}"
        nodes.append(
            {
                "id": dep_id,
                "type": "dependency",
                "label": dep.name,
                "version": dep.version,
                "license": dep.license_spdx,
                "confidence": dep.confidence,
            }
        )
        nodes.append({"id": license_id, "type": "license", "label": dep.license_spdx})
        edges.append({"source": "project", "target": dep_id, "type": "uses"})
        edges.append({"source": dep_id, "target": license_id, "type": "licensed-under"})
        for finding in result.findings:
            if finding.package == dep.name:
                finding_id = f"finding:{finding.id}"
                nodes.append(
                    {
                        "id": finding_id,
                        "type": "finding",
                        "label": finding.rule,
                        "severity": finding.severity,
                    }
                )
                edges.append({"source": dep_id, "target": finding_id, "type": "triggers"})
    return {"nodes": nodes, "edges": edges}
