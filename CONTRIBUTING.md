# Contributing to ReproLens

## Development setup

```powershell
cd repolens
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
python -m repolens audit examples/demo-llm-app --out-dir reports/demo-llm-app --explain --autofix
python -m repolens.web --open
```

## Pull requests

1. Keep the core deterministic and offline-capable.
2. Add or update tests for every rule, report, web, or AI-contract change.
3. Do not commit third-party repository source, `autofix/staging/`, API keys, or personal data.
4. Explain evidence sources and limitations in the PR description.
5. Preserve the rule that AI cannot invent evidence IDs or override deterministic scoring.

## Reporting issues

Please include the repository type, the affected criterion ID, the expected status, the actual status, and a minimal reproducible example without sensitive data.

## License

By contributing, you agree that your contribution is licensed under the repository MIT License.
