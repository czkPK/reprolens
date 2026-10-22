# Benchmark Harness

This harness compares ReproLens status predictions against manually specified expectations.

Run:

```powershell
$env:PYTHONPATH = "src"
python -m repolens.benchmark
```

Outputs:

- `results.json`
- `results.md`

The initial cases are demonstration fixtures. Expand the `CASES` list in `src/repolens/benchmark.py` to 20-30 real LLM/RAG/Agent repositories with manually verified expected statuses.
