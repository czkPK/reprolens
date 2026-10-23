# ReproLens Benchmark

- Labeled exact status accuracy: **75/98 (76.5%)**
- Detection precision: **0.684**
- Detection recall: **0.788**
- Detection F1: **0.732**

## Labeled Cases

| Case | Score | Exact | TP | FP | FN |
|---|---:|---:|---:|---:|---:|
| demo-llm-app | 49.1 | 10/10 | 6 | 0 | 0 |
| demo-ai-repo | 54.2 | 4/4 | 2 | 0 | 0 |
| mem0 | 84.8 | 14/14 | 5 | 0 | 0 |
| browser-use | 85.1 | 8/14 | 0 | 0 | 5 |
| openai-python | 94.9 | 14/14 | 0 | 0 | 0 |
| smolagents | 78.8 | 14/14 | 6 | 0 | 0 |
| aider | 74.8 | 6/14 | 3 | 4 | 2 |
| chat-ui | 44.1 | 5/14 | 4 | 8 | 0 |

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

### browser-use

| Criterion | Expected | Actual | Match |
|---|---|---|---|
| ENV-01 | pass | pass | YES |
| ENV-02 | pass | pass | YES |
| DATA-02 | not_applicable | pass | NO |
| MODEL-02 | not_applicable | not_applicable | YES |
| MODEL-03 | not_applicable | not_applicable | YES |
| EXP-02 | pass | pass | YES |
| EXP-03 | not_applicable | not_applicable | YES |
| DOC-03 | pass | pass | YES |
| LLM-02 | partial | not_applicable | NO |
| LLM-03 | partial | not_applicable | NO |
| LLM-05 | not_applicable | not_applicable | YES |
| LLM-06 | partial | not_applicable | NO |
| LLM-07 | partial | not_applicable | NO |
| LLM-08 | partial | not_applicable | NO |

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

### aider

| Criterion | Expected | Actual | Match |
|---|---|---|---|
| ENV-01 | pass | pass | YES |
| ENV-02 | pass | pass | YES |
| DATA-02 | not_applicable | partial | NO |
| MODEL-02 | not_applicable | pass | NO |
| MODEL-03 | not_applicable | partial | NO |
| EXP-02 | pass | partial | NO |
| EXP-03 | not_applicable | missing | NO |
| DOC-03 | pass | pass | YES |
| LLM-02 | partial | partial | YES |
| LLM-03 | partial | missing | NO |
| LLM-05 | not_applicable | not_applicable | YES |
| LLM-06 | partial | pass | NO |
| LLM-07 | partial | partial | YES |
| LLM-08 | partial | pass | NO |

### chat-ui

| Criterion | Expected | Actual | Match |
|---|---|---|---|
| ENV-01 | pass | missing | NO |
| ENV-02 | pass | pass | YES |
| DATA-02 | not_applicable | partial | NO |
| MODEL-02 | not_applicable | pass | NO |
| MODEL-03 | not_applicable | partial | NO |
| EXP-02 | pass | missing | NO |
| EXP-03 | not_applicable | missing | NO |
| DOC-03 | pass | partial | NO |
| LLM-02 | partial | partial | YES |
| LLM-03 | not_applicable | missing | NO |
| LLM-05 | not_applicable | partial | NO |
| LLM-06 | partial | partial | YES |
| LLM-07 | missing | missing | YES |
| LLM-08 | partial | partial | YES |

