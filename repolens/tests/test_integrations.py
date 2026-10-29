import json
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from repolens.integrations import compact_score, main, notification_payload, post_json, render_summary, sign_dingtalk_url


class IntegrationTests(unittest.TestCase):
    def test_compact_score_contains_external_contract(self):
        data = {
            "repo_path": "example",
            "total_score": 78.8,
            "readiness": "Partially Ready",
            "evidence_coverage": {"covered": 15, "total": 16, "percent": 93.8},
            "claim_matrix": [
                {"claim_id": "C-001", "status": "verified", "gaps": []},
                {"claim_id": "C-002", "status": "partially_verified", "gaps": ["LLM-03"]},
            ],
            "findings": [{"criterion_id": "ENV-02", "severity": "high", "title": "是否锁定依赖版本"}],
        }
        summary = compact_score(data)
        self.assertEqual(summary["score"], 78.8)
        self.assertEqual(summary["claim_counts"]["verified"], 1)
        self.assertEqual(summary["top_findings"][0]["criterion_id"], "ENV-02")

    def test_rendered_summary_shows_gate_result_and_webhook(self):
        summary = compact_score({"total_score": 49.1, "readiness": "At Risk", "claim_matrix": []})
        text = render_summary(summary, 60.0, False, 204)
        self.assertIn("FAILED", text)
        self.assertIn("delivered (204)", text)

    def test_feishu_payload_uses_text_message_envelope(self):
        summary = compact_score({"total_score": 78.8, "readiness": "Partially Ready", "claim_matrix": []})
        payload = notification_payload(summary, 70, True, "feishu")
        self.assertEqual(payload["msg_type"], "text")
        self.assertIn("ReproLens", payload["content"]["text"])
        self.assertIn("质量门禁：通过", payload["content"]["text"])

    def test_dingtalk_payload_uses_markdown_envelope(self):
        summary = compact_score({"total_score": 49.1, "readiness": "At Risk", "claim_matrix": []})
        payload = notification_payload(summary, 60, False, "dingtalk")
        self.assertEqual(payload["msgtype"], "markdown")
        self.assertIn("ReproLens", payload["markdown"]["title"])
        self.assertIn("质量门禁：未通过", payload["markdown"]["text"])

    def test_dingtalk_signing_adds_timestamp_and_signature(self):
        signed = sign_dingtalk_url("https://example.test/hook", "secret", timestamp="123456")
        self.assertIn("timestamp=123456", signed)
        self.assertIn("sign=", signed)

    def test_post_json_sends_payload(self):
        received = {}

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                length = int(self.headers["Content-Length"])
                received.update(json.loads(self.rfile.read(length)))
                self.send_response(204)
                self.end_headers()

            def log_message(self, fmt, *args):
                return

        server = HTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.handle_request, daemon=True)
        thread.start()
        try:
            status = post_json(f"http://127.0.0.1:{server.server_port}/hook", {"score": 78.8})
        finally:
            thread.join(timeout=3)
            server.server_close()
        self.assertEqual(status, 204)
        self.assertEqual(received["score"], 78.8)

    def test_post_json_rejects_platform_error_response(self):
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"errcode": 310000, "errmsg": "keyword not matched"}')

            def log_message(self, fmt, *args):
                return

        server = HTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.handle_request, daemon=True)
        thread.start()
        try:
            with self.assertRaises(RuntimeError):
                post_json(f"http://127.0.0.1:{server.server_port}/hook", {"score": 78.8})
        finally:
            thread.join(timeout=3)
            server.server_close()

    def test_main_returns_failure_below_threshold(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "score.json"
            path.write_text(json.dumps({"total_score": 49.1, "readiness": "At Risk", "claim_matrix": []}), encoding="utf-8")
            self.assertEqual(main([str(path), "--min-score", "60"]), 1)


if __name__ == "__main__":
    unittest.main()
