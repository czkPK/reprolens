# ReproLens Fresh Holdout Set

- Labeled exact status accuracy: **26/28 (92.9%)**
- Detection precision: **1.000**
- Detection recall: **0.818**
- Detection F1: **0.900**

## Labeled Cases

| Case | Score | Exact | TP | FP | FN |
|---|---:|---:|---:|---:|---:|
| anything-llm | 71.2 | 14/14 | 5 | 0 | 0 |
| open-webui | 86.1 | 12/14 | 4 | 0 | 2 |

## Case Details

### anything-llm

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
| LLM-03 | not_applicable | not_applicable | YES |
| LLM-05 | partial | partial | YES |
| LLM-06 | partial | partial | YES |
| LLM-07 | missing | missing | YES |
| LLM-08 | partial | partial | YES |

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

