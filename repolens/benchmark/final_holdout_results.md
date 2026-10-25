# FinalHoldout基准结果

- Labeled exact status accuracy: **28/28 (100.0%)**
- Detection precision: **1.000**
- Detection recall: **1.000**
- Detection F1: **1.000**

## Labeled Cases

| Case | Score | Exact | TP | FP | FN |
|---|---:|---:|---:|---:|---:|
| flowise | 71.2 | 14/14 | 4 | 0 | 0 |
| agentgpt | 75.9 | 14/14 | 4 | 0 | 0 |

## Case Details

### flowise

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
| LLM-03 | missing | missing | YES |
| LLM-05 | not_applicable | not_applicable | YES |
| LLM-06 | not_applicable | not_applicable | YES |
| LLM-07 | missing | missing | YES |
| LLM-08 | partial | partial | YES |

### agentgpt

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
| LLM-05 | not_applicable | not_applicable | YES |
| LLM-06 | partial | partial | YES |
| LLM-07 | partial | partial | YES |
| LLM-08 | partial | partial | YES |

