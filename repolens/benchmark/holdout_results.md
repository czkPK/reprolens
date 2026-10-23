# ReproLens Holdout Set

- Labeled exact status accuracy: **19/42 (45.2%)**
- Detection precision: **0.368**
- Detection recall: **0.500**
- Detection F1: **0.424**

## Labeled Cases

| Case | Score | Exact | TP | FP | FN |
|---|---:|---:|---:|---:|---:|
| browser-use | 85.1 | 8/14 | 0 | 0 | 5 |
| aider | 74.8 | 6/14 | 3 | 4 | 2 |
| chat-ui | 44.1 | 5/14 | 4 | 8 | 0 |

## Case Details

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

