import unittest

from repolens.web import parse_github_url


class WebTests(unittest.TestCase):
    def test_parse_github_url_normalizes_git_suffix(self):
        self.assertEqual(
            parse_github_url("https://github.com/openai/openai-python.git"),
            "https://github.com/openai/openai-python",
        )

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


if __name__ == "__main__":
    unittest.main()
