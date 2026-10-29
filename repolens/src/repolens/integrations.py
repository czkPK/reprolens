from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


def compact_score(data: dict[str, Any]) -> dict[str, Any]:
    claims = data.get("claim_matrix", [])
    project = data.get("source_url") or data.get("repo_path")
    github_repo = os.environ.get("GITHUB_REPOSITORY")
    if not data.get("source_url") and github_repo:
        server = os.environ.get("GITHUB_SERVER_URL", "https://github.com").rstrip("/")
        project = f"{server}/{github_repo}"
    source_commit = data.get("source_commit") or os.environ.get("GITHUB_SHA")
    return {
        "schema_version": 1,
        "project": project,
        "source_commit": source_commit,
        "score": data.get("total_score"),
        "readiness": data.get("readiness"),
        "evidence_coverage": data.get("evidence_coverage", {}),
        "claim_counts": {
            "total": len(claims),
            "verified": sum(1 for item in claims if item.get("status") == "verified"),
            "partially_verified": sum(1 for item in claims if item.get("status") == "partially_verified"),
            "unverified": sum(1 for item in claims if item.get("status") == "unverified"),
        },
        "claims": [
            {
                "claim_id": item.get("claim_id"),
                "status": item.get("status"),
                "gaps": item.get("gaps", []),
            }
            for item in claims
        ],
        "top_findings": [
            {
                "criterion_id": item.get("criterion_id"),
                "severity": item.get("severity"),
                "title": item.get("title"),
            }
            for item in data.get("findings", [])[:5]
        ],
    }


def post_json(url: str, payload: dict[str, Any], timeout: int = 10) -> int:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "ReproLens-Integration/0.1"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        status = response.status
        body = response.read()
        if body:
            try:
                data = json.loads(body.decode("utf-8"))
            except (ValueError, UnicodeDecodeError):
                return status
            if isinstance(data, dict):
                if data.get("code") not in (None, 0):
                    raise RuntimeError(f"webhook rejected: {data.get('msg') or data.get('code')}")
                if data.get("errcode") not in (None, 0):
                    raise RuntimeError(f"webhook rejected: {data.get('errmsg') or data.get('errcode')}")
        return status


def sign_dingtalk_url(url: str, secret: str, timestamp: str | None = None) -> str:
    timestamp = timestamp or str(round(time.time() * 1000))
    string_to_sign = f"{timestamp}\n{secret}".encode("utf-8")
    digest = hmac.new(secret.encode("utf-8"), string_to_sign, hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(digest))
    separator = "&" if "?" in url else "?"
    return f"{url}{separator}timestamp={timestamp}&sign={sign}"


def render_notification_text(summary: dict[str, Any], minimum: float, passed: bool) -> str:
    coverage = summary.get("evidence_coverage", {})
    claims = summary.get("claim_counts", {})
    lines = [
        "ReproLens 复现审计通知",
        f"项目：{summary.get('project')}",
        f"提交：{summary.get('source_commit') or '-'}",
        f"得分：{summary.get('score')} / 100",
        f"就绪度：{summary.get('readiness')}",
        f"证据覆盖率：{coverage.get('covered', 0)}/{coverage.get('total', 0)} ({coverage.get('percent', 0):.1f}%)",
        f"声明：总数 {claims.get('total', 0)}，已验证 {claims.get('verified', 0)}，部分验证 {claims.get('partially_verified', 0)}",
        f"质量门禁：{'通过' if passed else '未通过'}（最低 {minimum:.1f} 分）",
    ]
    findings = summary.get("top_findings", [])
    if findings:
        lines.append("主要发现：")
        lines.extend(
            f"- [{item.get('severity', '').upper()}] {item.get('title')} ({item.get('criterion_id')})"
            for item in findings
        )
    return "\n".join(lines)


def notification_payload(
    summary: dict[str, Any],
    minimum: float,
    passed: bool,
    payload_format: str,
) -> dict[str, Any]:
    if payload_format == "feishu":
        return {
            "msg_type": "text",
            "content": {"text": render_notification_text(summary, minimum, passed)},
        }
    if payload_format == "dingtalk":
        return {
            "msgtype": "markdown",
            "markdown": {
                "title": "ReproLens 复现审计通知",
                "text": render_notification_text(summary, minimum, passed),
            },
        }
    return summary


def render_summary(summary: dict[str, Any], minimum: float, passed: bool, webhook_status: int | None, webhook_error: str = "") -> str:
    coverage = summary.get("evidence_coverage", {})
    claims = summary.get("claim_counts", {})
    lines = [
        "# ReproLens Score Gate",
        "",
        f"- Project: {summary.get('project')}",
        f"- Commit: {summary.get('source_commit') or '-'}",
        f"- Score: **{summary.get('score'):.1f} / 100**" if isinstance(summary.get("score"), (int, float)) else f"- Score: {summary.get('score')}",
        f"- Readiness: **{summary.get('readiness')}**",
        f"- Evidence coverage: **{coverage.get('covered', 0)}/{coverage.get('total', 0)} ({coverage.get('percent', 0):.1f}%)**",
        f"- Claims: total={claims.get('total', 0)}, verified={claims.get('verified', 0)}, partial={claims.get('partially_verified', 0)}",
        f"- Gate: **{'PASSED' if passed else 'FAILED'}** (minimum {minimum:.1f})",
        f"- Webhook: **{'delivered (' + str(webhook_status) + ')' if webhook_status else ('failed: ' + webhook_error if webhook_error else 'not configured')}**",
    ]
    if summary.get("top_findings"):
        lines.extend(["", "## Top findings"])
        lines.extend(
            f"- [{item['severity'].upper()}] {item['title']} ({item['criterion_id']})"
            for item in summary["top_findings"]
        )
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="repolens.integrations", description="Consume ReproLens score.json in external automation.")
    parser.add_argument("score_json", help="Path to score.json produced by ReproLens.")
    parser.add_argument("--min-score", type=float, default=0.0, help="Minimum score required by the CI gate.")
    parser.add_argument("--webhook-url", help="Optional HTTP endpoint that receives the compact JSON summary.")
    parser.add_argument("--format", choices=("generic", "feishu", "dingtalk"), default="generic", help="Payload format for the webhook endpoint.")
    parser.add_argument("--webhook-secret", help="Optional DingTalk signing secret.")
    parser.add_argument("--timeout", type=int, default=10)
    args = parser.parse_args(argv)

    data = json.loads(Path(args.score_json).read_text(encoding="utf-8"))
    summary = compact_score(data)
    score = float(data.get("total_score", 0.0))
    passed = score >= args.min_score
    webhook_status = None
    webhook_error = ""
    if args.webhook_secret and args.format != "dingtalk":
        parser.error("--webhook-secret is only supported with --format dingtalk")
    payload = notification_payload(summary, args.min_score, passed, args.format)
    if args.webhook_url:
        try:
            webhook_url = args.webhook_url
            if args.format == "dingtalk" and args.webhook_secret:
                webhook_url = sign_dingtalk_url(webhook_url, args.webhook_secret)
            webhook_status = post_json(webhook_url, payload, args.timeout)
        except Exception as exc:
            webhook_error = str(exc) or type(exc).__name__
    print(render_summary(summary, args.min_score, passed, webhook_status, webhook_error), end="")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
