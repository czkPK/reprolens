# ReproLens Fresh Holdout Set

- Labeled exact status accuracy: **20/28 (71.4%)**
- Detection precision: **0.692**
- Detection recall: **0.750**
- Detection F1: **0.720**

## Labeled Cases

| Case | Score | Exact | TP | FP | FN |
|---|---:|---:|---:|---:|---:|
| anything-llm | 62.8 | 8/14 | 5 | 4 | 1 |
| open-webui | 86.1 | 12/14 | 4 | 0 | 2 |

## Case Details

### anything-llm

| Criterion | Expected | Actual | Match |
|---|---|---|---|
| ENV-01 | pass | pass | YES |
| ENV-02 | pass | pass | YES |
| DATA-02 | not_applicable | partial | NO |
| MODEL-02 | not_applicable | pass | NO |
| MODEL-03 | not_applicable | partial | NO |
| EXP-02 | pass | pass | YES |
| EXP-03 | not_applicable | missing | NO |
| DOC-03 | pass | partial | NO |
| LLM-02 | partial | partial | YES |
| LLM-03 | missing | missing | YES |
| LLM-05 | partial | partial | YES |
| LLM-06 | partial | partial | YES |
| LLM-07 | missing | missing | YES |
| LLM-08 | partial | pass | NO |

### open-webui

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
| LLM-05 | partial | pass | NO |
| LLM-06 | partial | pass | NO |
| LLM-07 | partial | partial | YES |
| LLM-08 | partial | partial | YES |

