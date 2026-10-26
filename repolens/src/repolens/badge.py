from __future__ import annotations

from html import escape

from .models import AuditResult


def badge_color(score: float) -> str:
    if score >= 85:
        return "#0f8a5f"
    if score >= 65:
        return "#2457d6"
    if score >= 40:
        return "#b66a06"
    return "#b42336"


def badge_payload(result: AuditResult) -> dict:
    return {
        "schemaVersion": 1,
        "label": "ReproLens",
        "message": f"{result.total_score:.1f}/100 {result.readiness}",
        "color": badge_color(result.total_score),
        "score": result.total_score,
        "readiness": result.readiness,
        "evidence_coverage": result.evidence_coverage,
        "source_url": result.source_url,
        "source_commit": result.source_commit,
        "generated_at": result.generated_at,
    }


def render_badge_svg(result: AuditResult) -> str:
    payload = badge_payload(result)
    label_width = 105
    message_width = 205
    width = label_width + message_width
    label = escape(payload["label"])
    message = escape(payload["message"])
    color = payload["color"]
    aria = escape(f"ReproLens: {payload['message']}")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="28" role="img" aria-label="{aria}">
  <linearGradient id="s" x2="0" y2="100%">
    <stop offset="0" stop-color="#ffffff" stop-opacity=".18"/>
    <stop offset="1" stop-color="#000000" stop-opacity=".08"/>
  </linearGradient>
  <rect width="{width}" height="28" rx="6" fill="#1f2937"/>
  <rect x="{label_width}" width="{message_width}" height="28" rx="6" fill="{color}"/>
  <rect width="{width}" height="28" rx="6" fill="url(#s)"/>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,DejaVu Sans,sans-serif" font-size="11">
    <text x="{label_width / 2:.1f}" y="18" font-weight="700">{label}</text>
    <text x="{label_width + message_width / 2:.1f}" y="18" font-weight="700">{message}</text>
  </g>
</svg>
'''
