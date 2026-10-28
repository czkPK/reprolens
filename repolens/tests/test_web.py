import json
import re
import tempfile
import threading
import time
import unittest
import urllib.request
from pathlib import Path
from unittest.mock import patch

from repolens.web import WEBHOOK_DEMO_HTML, ReproLensHTTPServer, _run_git, parse_github_url, resolve_github_source


class WebTests(unittest.TestCase):
    def test_webhook_demo_explains_technical_titles(self):
        for text in (
            "Webhook（回调通知）",
            "JSON（结构化数据）",
            "HTTP POST（提交数据）",
            "接收状态（服务是否在线）",
            "最近一次 HTTP POST 内容",
        ):
            self.assertIn(text, WEBHOOK_DEMO_HTML)

    def test_parse_github_url_normalizes_git_suffix(self):
        self.assertEqual(
            parse_github_url("https://github.com/openai/openai-python.git"),
            "https://github.com/openai/openai-python",
        )

    def test_parse_github_pages_url_maps_to_repository(self):
        self.assertEqual(
            parse_github_url("https://donghaotian123.github.io/Wan-Alpha/"),
            "https://github.com/donghaotian123/Wan-Alpha",
        )
        self.assertEqual(
            parse_github_url("https://donghaotian123.github.io/Wan-Alpha/docs/index.html"),
            "https://github.com/donghaotian123/Wan-Alpha",
        )
        self.assertEqual(
            parse_github_url("https://donghaotian123.github.io/"),
            "https://github.com/donghaotian123/donghaotian123.github.io",
        )

    def test_parse_github_url_cleans_pasted_whitespace_and_missing_scheme(self):
        expected = "https://github.com/YangQiWei3/HiHR"
        for value in (
            " https: //github.com/YangQiWei3/HiHR ",
            "https：//github.com/YangQiWei3/HiHR",
            "github.com/YangQiWei3/HiHR",
            "https://www.github.com/YangQiWei3/HiHR",
        ):
            with self.subTest(value=value):
                self.assertEqual(parse_github_url(value), expected)

    def test_parse_github_url_rejects_non_repository_links(self):
        for value in (
            "http://github.com/openai/openai-python",
            "https://example.com/openai/openai-python",
            "https://github.com/openai/openai-python/issues/1",
            "https://github.com/openai",
            "",
        ):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    parse_github_url(value)

    def test_github_pages_resolver_prefers_linked_upstream_repository(self):
        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def read(self, limit):
                return (
                    b'<a href="https://github.com/donghaotian123/Wan-Alpha">page</a>'
                    b'<a href="https://github.com/WeChatCV/Wan-Alpha">source</a>'
                )

        with patch("repolens.web.urllib.request.urlopen", return_value=FakeResponse()):
            self.assertEqual(
                resolve_github_source("https://donghaotian123.github.io/Wan-Alpha/"),
                "https://github.com/WeChatCV/Wan-Alpha",
            )

    def test_missing_git_uses_fallback_exit_code(self):
        with patch("repolens.web.subprocess.run", side_effect=FileNotFoundError):
            result = _run_git(["clone", "https://github.com/openai/openai-python"])
        self.assertEqual(result.returncode, 127)
        self.assertIn("archive fallback", result.stderr)

    def test_async_audit_job_can_be_polled_to_completion(self):
        summary = {
            "run_id": "test-run",
            "score": 88.0,
            "readiness": "Ready",
            "report_url": "/reports/test-run/report.html",
        }

        def fake_audit(source_url, runs_dir, autofix=True):
            time.sleep(0.08)
            return summary

        with tempfile.TemporaryDirectory() as tmp:
            runs_dir = Path(tmp)
            proposal_file = runs_dir / "test-run" / "autofix" / "proposal" / "Dockerfile"
            proposal_file.parent.mkdir(parents=True)
            proposal_file.write_text("FROM python:3.11-slim\n", encoding="utf-8")
            server = ReproLensHTTPServer(("127.0.0.1", 0), runs_dir)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            base = f"http://127.0.0.1:{server.server_port}"
            try:
                with patch("repolens.web.run_remote_audit", side_effect=fake_audit):
                    request = urllib.request.Request(
                        f"{base}/api/jobs",
                        data=json.dumps({"url": "https://github.com/openai/openai-python"}).encode("utf-8"),
                        headers={"Content-Type": "application/json"},
                        method="POST",
                    )
                    with urllib.request.urlopen(request, timeout=5) as response:
                        self.assertEqual(response.status, 202)
                        job = json.loads(response.read().decode("utf-8"))
                    self.assertRegex(job["job_id"], re.compile(r"^[a-f0-9]{32}$"))
                    self.assertIn(job["status"], {"queued", "running"})

                    result = None
                    for _ in range(50):
                        with urllib.request.urlopen(f"{base}/api/jobs/{job['job_id']}", timeout=5) as response:
                            state = json.loads(response.read().decode("utf-8"))
                        if state["status"] == "done":
                            result = state["result"]
                            break
                        self.assertNotEqual(state["status"], "error")
                        time.sleep(0.03)
                    self.assertEqual(result, summary)
                    with urllib.request.urlopen(f"{base}/reports/test-run/autofix/proposal/Dockerfile", timeout=5) as response:
                        self.assertEqual(response.status, 200)
                        self.assertIn(b"FROM python:3.11-slim", response.read())
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
