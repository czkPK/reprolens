# FreshHoldout基准结果

> 初次独立评估为 26/28（92.9%，F1 0.900）。本文件是后续证据门槛修复后的当前代码复跑结果，不能替代初次独立结果。

- Labeled exact status accuracy: **27/28 (96.4%)**
- Detection precision: **1.000**
- Detection recall: **1.000**
- Detection F1: **1.000**

## Labeled Cases

| Case | Score | Exact | TP | FP | FN |
|---|---:|---:|---:|---:|---:|
| anything-llm | 71.2 | 14/14 | 5 | 0 | 0 |
| open-webui | 78.8 | 13/14 | 6 | 0 | 0 |

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
| LLM-03 | partial | missing | NO |
| LLM-05 | partial | partial | YES |
| LLM-06 | partial | partial | YES |
| LLM-07 | partial | partial | YES |
| LLM-08 | partial | partial | YES |

