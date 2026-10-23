# ReproLens Holdout Set

- Labeled exact status accuracy: **38/42 (90.5%)**
- Detection precision: **0.917**
- Detection recall: **0.786**
- Detection F1: **0.846**

## Labeled Cases

| Case | Score | Exact | TP | FP | FN |
|---|---:|---:|---:|---:|---:|
| browser-use | 72.4 | 13/14 | 4 | 0 | 1 |
| aider | 87.2 | 12/14 | 3 | 0 | 2 |
| chat-ui | 65.3 | 13/14 | 4 | 1 | 0 |

## Case Details

### browser-use

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
| LLM-03 | partial | not_applicable | NO |
| LLM-05 | not_applicable | not_applicable | YES |
| LLM-06 | partial | partial | YES |
| LLM-07 | partial | partial | YES |
| LLM-08 | partial | partial | YES |

### aider

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
| LLM-03 | partial | not_applicable | NO |
| LLM-05 | not_applicable | not_applicable | YES |
| LLM-06 | partial | pass | NO |
| LLM-07 | partial | partial | YES |
| LLM-08 | partial | partial | YES |

### chat-ui

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
| LLM-03 | not_applicable | partial | NO |
| LLM-05 | not_applicable | not_applicable | YES |
| LLM-06 | partial | partial | YES |
| LLM-07 | missing | missing | YES |
| LLM-08 | partial | partial | YES |

