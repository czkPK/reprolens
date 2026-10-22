# ReproLens Benchmark

- Labeled exact status accuracy: **14/14 (100.0%)**
- Detection precision: **1.000**
- Detection recall: **1.000**
- Detection F1: **1.000**

## Labeled Cases

| Case | Score | Exact | TP | FP | FN |
|---|---:|---:|---:|---:|---:|
| demo-llm-app | 49.1 | 10/10 | 6 | 0 | 0 |
| demo-ai-repo | 54.2 | 4/4 | 2 | 0 | 0 |

## Unlabeled Scanned Repositories

| Case | Score | Note |
|---|---:|---|
| mem0 | 81.9 | Missing manual labels |
| openai-python | 70.3 | Missing manual labels |
| smolagents | 70.0 | Missing manual labels |

## Case Details

### demo-llm-app

| Criterion | Expected | Actual | Match |
|---|---|---|---|
| ENV-01 | pass | pass | YES |
| DATA-02 | missing | missing | YES |
| LLM-01 | pass | pass | YES |
| LLM-02 | partial | partial | YES |
| LLM-03 | pass | pass | YES |
| LLM-04 | partial | partial | YES |
| LLM-05 | pass | pass | YES |
| LLM-06 | partial | partial | YES |
| LLM-07 | missing | missing | YES |
| LLM-08 | partial | partial | YES |

### demo-ai-repo

| Criterion | Expected | Actual | Match |
|---|---|---|---|
| ENV-01 | pass | pass | YES |
| EXP-03 | missing | missing | YES |
| MODEL-02 | missing | missing | YES |
| LLM-01 | not_applicable | not_applicable | YES |

