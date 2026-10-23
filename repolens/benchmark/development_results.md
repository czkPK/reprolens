# ReproLens Development Set

- Labeled exact status accuracy: **56/56 (100.0%)**
- Detection precision: **1.000**
- Detection recall: **1.000**
- Detection F1: **1.000**

## Labeled Cases

| Case | Score | Exact | TP | FP | FN |
|---|---:|---:|---:|---:|---:|
| demo-llm-app | 49.1 | 10/10 | 6 | 0 | 0 |
| demo-ai-repo | 54.2 | 4/4 | 2 | 0 | 0 |
| mem0 | 84.8 | 14/14 | 5 | 0 | 0 |
| openai-python | 94.9 | 14/14 | 0 | 0 | 0 |
| smolagents | 78.8 | 14/14 | 6 | 0 | 0 |

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

### mem0

| Criterion | Expected | Actual | Match |
|---|---|---|---|
| ENV-01 | pass | pass | YES |
| ENV-02 | pass | pass | YES |
| DATA-02 | not_applicable | not_applicable | YES |
| MODEL-02 | not_applicable | not_applicable | YES |
| MODEL-03 | not_applicable | not_applicable | YES |
| EXP-02 | pass | pass | YES |
| EXP-03 | not_applicable | not_applicable | YES |
| DOC-03 | pass | pass | YES |
| LLM-02 | partial | partial | YES |
| LLM-03 | partial | partial | YES |
| LLM-05 | partial | partial | YES |
| LLM-06 | not_applicable | not_applicable | YES |
| LLM-07 | partial | partial | YES |
| LLM-08 | partial | partial | YES |

### openai-python

| Criterion | Expected | Actual | Match |
|---|---|---|---|
| ENV-01 | pass | pass | YES |
| ENV-02 | pass | pass | YES |
| DATA-02 | not_applicable | not_applicable | YES |
| MODEL-02 | not_applicable | not_applicable | YES |
| MODEL-03 | not_applicable | not_applicable | YES |
| EXP-02 | pass | pass | YES |
| EXP-03 | not_applicable | not_applicable | YES |
| DOC-03 | pass | pass | YES |
| LLM-02 | not_applicable | not_applicable | YES |
| LLM-03 | not_applicable | not_applicable | YES |
| LLM-05 | not_applicable | not_applicable | YES |
| LLM-06 | not_applicable | not_applicable | YES |
| LLM-07 | not_applicable | not_applicable | YES |
| LLM-08 | not_applicable | not_applicable | YES |

### smolagents

| Criterion | Expected | Actual | Match |
|---|---|---|---|
| ENV-01 | pass | pass | YES |
| ENV-02 | partial | partial | YES |
| DATA-02 | not_applicable | not_applicable | YES |
| MODEL-02 | not_applicable | not_applicable | YES |
| MODEL-03 | not_applicable | not_applicable | YES |
| EXP-02 | pass | pass | YES |
| EXP-03 | not_applicable | not_applicable | YES |
| DOC-03 | pass | pass | YES |
| LLM-02 | partial | partial | YES |
| LLM-03 | partial | partial | YES |
| LLM-05 | not_applicable | not_applicable | YES |
| LLM-06 | partial | partial | YES |
| LLM-07 | partial | partial | YES |
| LLM-08 | partial | partial | YES |

