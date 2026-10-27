# ReproLens Audit Report

- Repository: `https://github.com/WeChatCV/Wan-Alpha @ 9e5d0533da2d`
- Generated at: `2026-10-27T15:05:32.760299+00:00`
- Semantic claim mapping: **rules-fallback**
- Source: [https://github.com/WeChatCV/Wan-Alpha](https://github.com/WeChatCV/Wan-Alpha)
- Source commit: `9e5d0533da2dea390bbb0e50c59adfebe5613323`
- Files scanned: **407**
- Overall score: **65.7 / 100**
- Readiness: **Partially Ready**
- Evidence coverage: **19/23 (82.6%)**
- README claims audited: **4**

## Dimension Scores

| Dimension | Points | Max | Percent |
|---|---:|---:|---:|
| 环境可复现 | 21.0 | 25.0 | 84.0% |
| 数据可复现 | 11.0 | 22.0 | 50.0% |
| 模型可复现 | 19.0 | 22.0 | 86.4% |
| 实验可复现 | 23.0 | 33.0 | 69.7% |
| 文档可复现 | 11.0 | 17.0 | 64.7% |
| LLM 特有风险 | 13.5 | 31.0 | 43.5% |

## Top 3 Priority Actions

1. **固定并记录随机种子、框架确定性和硬件差异** — expected gain **+6.0**; 降低结果不可重复的随机性。
2. **说明评测集、数据划分和污染/泄漏风险** — expected gain **+6.0**; 让指标具有可比性，避免高估效果。
3. **添加测试、CI 或一键复现脚本** — expected gain **+6.0**; 把复现变成持续可验证的工程流程。

## Criteria

| 检查项编号 | 所属维度 | 检查要求 | 状态 | 证据强度 | 得分 | 证据编号 | 证据说明 |
|---|---|---|---|---|---:|---|---|

**读表说明：** PASS = 满足要求；PARTIAL = 只有部分证据；MISSING = 应有但没有找到；N/A = 当前项目类型不适用。Confidence 表示证据支持强度，不代表项目整体质量。

| ENV-01 | 环境可复现 | 是否存在依赖清单 | PASS | MEDIUM | 10.0/10.0 | E-002 | 支持证据：E-002（requirements.txt:1）：“torch>=2.4.0”。 |
| ENV-02 | 环境可复现 | 是否锁定依赖版本或提供容器化配置 | PARTIAL | MEDIUM | 4.0/8.0 | E-002 | 部分证据：E-002（requirements.txt:1）：“torch>=2.4.0”；现有证据不足以完全满足该项。 |
| ENV-03 | 环境可复现 | 是否提供安装步骤 | PASS | MEDIUM | 7.0/7.0 | E-006 | 支持证据：E-006（readme.md:78）：“# Create and activate Conda environment”。 |
| DATA-01 | 数据可复现 | 是否说明数据来源和获取方式 | PARTIAL | MEDIUM | 4.0/8.0 | E-008 | 部分证据：E-008（readme.md:11）：“[![arXiv](https://img.shields.io/badge/arXiv-2509.24979-red)](https://arxiv.org/pdf/250...”；现有证据不足以完全满足该项。 |
| DATA-02 | 数据可复现 | 是否提供数据下载或预处理脚本 | PARTIAL | MEDIUM | 4.0/8.0 | E-008 | 部分证据：E-008（readme.md:11）：“[![arXiv](https://img.shields.io/badge/arXiv-2509.24979-red)](https://arxiv.org/pdf/250...”；现有证据不足以完全满足该项。 |
| DATA-03 | 数据可复现 | 是否提供数据集卡或数据许可说明 | PARTIAL | MEDIUM | 3.0/6.0 | E-003, E-008 | 部分证据：E-003（LICENSE:1）：“MIT License”；E-008（readme.md:11）：“[![arXiv](https://img.shields.io/badge/arXiv-2509.24979-red)](https://arxiv.org/pdf/250...”；现有证据不足以完全满足该项。 |
| MODEL-01 | 模型可复现 | 是否提供模型权重、API 或获取方式 | PASS | HIGH | 8.0/8.0 | E-013, E-011, E-014 | 支持证据：E-013（readme.md:13）：“[![🤗 HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97%20HuggingFace-Model_v1.0-or...”；E-011（readme.md:13）：“[![🤗 HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97%20HuggingFace-Model_v1.0-or...”；E-014（readme.md:148）：“--model_id_with_origin_paths "Wan2.1-T2V-1.3B:diffusion_pytorch_model*.safetensors" \”。 |
| MODEL-02 | 模型可复现 | 是否提供模型卡或版本说明 | PASS | HIGH | 8.0/8.0 | E-011, E-014 | 支持证据：E-011（readme.md:13）：“[![🤗 HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97%20HuggingFace-Model_v1.0-or...”；E-014（readme.md:148）：“--model_id_with_origin_paths "Wan2.1-T2V-1.3B:diffusion_pytorch_model*.safetensors" \”。 |
| MODEL-03 | 模型可复现 | 是否说明模型许可和来源 | PARTIAL | MEDIUM | 3.0/6.0 | E-003 | 部分证据：E-003（LICENSE:1）：“MIT License”；现有证据不足以完全满足该项。 |
| EXP-01 | 实验可复现 | 是否提供训练或主运行脚本 | PASS | HIGH | 7.0/7.0 | E-004, E-007 | 支持证据：E-004（Wan-Alpha-VAE-train/train_vae.py:1）：“import os”；E-007（readme.md:135）：“CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python3 train_vae.py \”。 |
| EXP-02 | 实验可复现 | 是否提供评测脚本或评测命令 | PARTIAL | MEDIUM | 4.0/8.0 | E-009 | 部分证据：E-009（readme.md:89）：“Download [Lightx2v-T2V-14B](https://huggingface.co/Kijai/WanVideo_comfy/blob/main/Light...”；现有证据不足以完全满足该项。 |
| EXP-03 | 实验可复现 | 是否设置并说明随机种子 | MISSING | LOW | 0.0/6.0 | - | 未找到可引用证据，因此该项不能判定为通过。 |
| EXP-04 | 实验可复现 | 是否说明硬件或 API 环境要求 | PASS | HIGH | 5.0/5.0 | E-010, E-013 | 支持证据：E-010（readme.md:135）：“CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python3 train_vae.py \”；E-013（readme.md:13）：“[![🤗 HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97%20HuggingFace-Model_v1.0-or...”。 |
| EXP-05 | 实验可复现 | 是否给出预期结果和指标 | PASS | MEDIUM | 7.0/7.0 | E-009 | 支持证据：E-009（readme.md:89）：“Download [Lightx2v-T2V-14B](https://huggingface.co/Kijai/WanVideo_comfy/blob/main/Light...”。 |
| DOC-01 | 文档可复现 | 是否存在 README | PASS | MEDIUM | 5.0/5.0 | E-001 | 支持证据：E-001（readme.md:1）：“<div align="center">”。 |
| DOC-02 | 文档可复现 | 是否提供快速开始和运行示例 | PASS | HIGH | 6.0/6.0 | E-006, E-007 | 支持证据：E-006（readme.md:78）：“# Create and activate Conda environment”；E-007（readme.md:135）：“CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python3 train_vae.py \”。 |
| DOC-03 | 文档可复现 | 是否提供测试、CI 或一键复现脚本 | MISSING | LOW | 0.0/6.0 | - | 未找到可引用证据，因此该项不能判定为通过。 |
| LLM-01 | LLM 特有风险 | 是否记录模型/API 版本 | PASS | HIGH | 6.0/6.0 | E-013, E-011, E-014 | 支持证据：E-013（readme.md:13）：“[![🤗 HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97%20HuggingFace-Model_v1.0-or...”；E-011（readme.md:13）：“[![🤗 HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97%20HuggingFace-Model_v1.0-or...”；E-014（readme.md:148）：“--model_id_with_origin_paths "Wan2.1-T2V-1.3B:diffusion_pytorch_model*.safetensors" \”。 |
| LLM-02 | LLM 特有风险 | 是否对 prompt/template 进行版本记录 | PARTIAL | MEDIUM | 3.0/6.0 | E-012 | 部分证据：E-012（readme.md:55）：“<!-- \| Prompt \| Preview Video \| Alpha Video \|”；现有证据不足以完全满足该项。 |
| LLM-03 | LLM 特有风险 | 是否记录采样参数 | PARTIAL | MEDIUM | 2.5/5.0 | E-005 | 部分证据：E-005（Wan-Alpha-train/configs/accelerate_config/accelerate_wxg.yaml:1）：“compute_environment: LOCAL_MACHINE”；现有证据不足以完全满足该项。 |
| LLM-04 | LLM 特有风险 | 是否记录 tokenizer/上下文窗口 | MISSING | LOW | 0.0/4.0 | - | 未找到可引用证据，因此该项不能判定为通过。 |
| LLM-05 | LLM 特有风险 | 是否记录 RAG 索引/知识库版本 | N/A | N/A | 0.0/5.0 | - | 这是一个机器学习项目，不具备该检查项对应的项目产物，因此这项检查不适用。 |
| LLM-06 | LLM 特有风险 | 是否记录 Agent 工具调用轨迹 | N/A | N/A | 0.0/5.0 | - | 这是一个机器学习项目，不具备该检查项对应的项目产物，因此这项检查不适用。 |
| LLM-07 | LLM 特有风险 | 是否说明评测集、数据划分和污染风险 | MISSING | LOW | 0.0/6.0 | - | 未找到可引用证据，因此该项不能判定为通过。 |
| LLM-08 | LLM 特有风险 | 是否说明推理成本或延迟 | PARTIAL | MEDIUM | 2.0/4.0 | E-010, E-013 | 部分证据：E-010（readme.md:135）：“CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python3 train_vae.py \”；E-013（readme.md:13）：“[![🤗 HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97%20HuggingFace-Model_v1.0-or...”；现有证据不足以完全满足该项。 |

## Claim-Evidence Matrix

**读表方法：** 每一行先看 README 说了什么，再看验证状态、检查依据、缺口和支持证据。括号内是内部编号对应的中文含义。

| 声明编号 | README 声明 | 验证状态 | 检查依据（需要检查的项） | 还缺什么（缺口） | 支持证据 | 验证说明 |
|---|---|---|---|---|---|---|
| C-001 | [2026.03.10] Released Wan-Alpha v2.0 and Wan-Alpha VAE training codes and training datasets. | 未验证 | DOC-02（是否提供快速开始和运行示例）；DOC-03（是否提供测试、CI 或一键复现脚本）；EXP-02（是否提供评测脚本或评测命令） | DOC-03（是否提供测试、CI 或一键复现脚本）；EXP-02（是否提供评测脚本或评测命令） | `E-006` readme.md:78：# Create and activate Conda environment<br>`E-007` readme.md:135：CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python3 train_vae.py \<br>`E-009` readme.md:89：Download [Lightx2v-T2V-14B](https://huggingface.co/Kijai/WanVideo_comfy/blob/main/Light... | 缺少关键证据，当前声明不能视为已验证；缺口：DOC-03（是否提供测试、CI 或一键复现脚本）；EXP-02（是否提供评测脚本或评测命令）。 |
| C-002 | [x] Dataset: Open-source the VAE and T2V training dataset. | 未验证 | DOC-02（是否提供快速开始和运行示例）；DOC-03（是否提供测试、CI 或一键复现脚本）；EXP-02（是否提供评测脚本或评测命令） | DOC-03（是否提供测试、CI 或一键复现脚本）；EXP-02（是否提供评测脚本或评测命令） | `E-006` readme.md:78：# Create and activate Conda environment<br>`E-007` readme.md:135：CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python3 train_vae.py \<br>`E-009` readme.md:89：Download [Lightx2v-T2V-14B](https://huggingface.co/Kijai/WanVideo_comfy/blob/main/Light... | 缺少关键证据，当前声明不能视为已验证；缺口：DOC-03（是否提供测试、CI 或一键复现脚本）；EXP-02（是否提供评测脚本或评测命令）。 |
| C-003 | For the VAE training dataset, please refer to Section 3.3 of our paper for preparation details. | 未验证 | DOC-02（是否提供快速开始和运行示例）；DOC-03（是否提供测试、CI 或一键复现脚本）；EXP-02（是否提供评测脚本或评测命令） | DOC-03（是否提供测试、CI 或一键复现脚本）；EXP-02（是否提供评测脚本或评测命令） | `E-006` readme.md:78：# Create and activate Conda environment<br>`E-007` readme.md:135：CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python3 train_vae.py \<br>`E-009` readme.md:89：Download [Lightx2v-T2V-14B](https://huggingface.co/Kijai/WanVideo_comfy/blob/main/Light... | 缺少关键证据，当前声明不能视为已验证；缺口：DOC-03（是否提供测试、CI 或一键复现脚本）；EXP-02（是否提供评测脚本或评测命令）。 |
| C-004 | You can download the training dataset from Google Drive or Hugging Face. | 未验证 | DOC-02（是否提供快速开始和运行示例）；DOC-03（是否提供测试、CI 或一键复现脚本）；EXP-02（是否提供评测脚本或评测命令） | DOC-03（是否提供测试、CI 或一键复现脚本）；EXP-02（是否提供评测脚本或评测命令） | `E-006` readme.md:78：# Create and activate Conda environment<br>`E-007` readme.md:135：CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python3 train_vae.py \<br>`E-009` readme.md:89：Download [Lightx2v-T2V-14B](https://huggingface.co/Kijai/WanVideo_comfy/blob/main/Light... | 缺少关键证据，当前声明不能视为已验证；缺口：DOC-03（是否提供测试、CI 或一键复现脚本）；EXP-02（是否提供评测脚本或评测命令）。 |

## Findings

### F-001 [MEDIUM] 是否锁定依赖版本或提供容器化配置

- Criterion: `ENV-02`
- Message: 有依赖清单，但没有锁定文件或容器配置。
- Evidence: `E-002`

### F-002 [MEDIUM] 是否说明数据来源和获取方式

- Criterion: `DATA-01`
- Message: 提到了数据，但缺少可执行的获取或处理说明。
- Evidence: `E-008`

### F-003 [MEDIUM] 是否提供数据下载或预处理脚本

- Criterion: `DATA-02`
- Message: 有数据说明，但没有下载/预处理脚本。
- Evidence: `E-008`

### F-004 [MEDIUM] 是否提供数据集卡或数据许可说明

- Criterion: `DATA-03`
- Message: 有许可证和数据说明，但没有独立数据集卡。
- Evidence: `E-003`, `E-008`

### F-005 [MEDIUM] 是否说明模型许可和来源

- Criterion: `MODEL-03`
- Message: 有许可证或模型卡，但模型专用许可和来源仍需补充。
- Evidence: `E-003`

### F-006 [MEDIUM] 是否提供评测脚本或评测命令

- Criterion: `EXP-02`
- Message: 有指标描述，但没有评测脚本。
- Evidence: `E-009`

### F-007 [MEDIUM] 是否设置并说明随机种子

- Criterion: `EXP-03`
- Message: 没有随机种子或确定性设置。
- Evidence: none

### F-008 [MEDIUM] 是否提供测试、CI 或一键复现脚本

- Criterion: `DOC-03`
- Message: 没有测试、CI 或一键复现脚本。
- Evidence: none

### F-009 [MEDIUM] 是否对 prompt/template 进行版本记录

- Criterion: `LLM-02`
- Message: 有 prompt 文件或描述，但没有可核验的版本信息。
- Evidence: `E-012`

### F-010 [MEDIUM] 是否记录采样参数

- Criterion: `LLM-03`
- Message: 有采样参数或配置线索，但仍需补充可核验值。
- Evidence: `E-005`

### F-011 [MEDIUM] 是否记录 tokenizer/上下文窗口

- Criterion: `LLM-04`
- Message: 没有记录 tokenizer 或上下文窗口。
- Evidence: none

### F-012 [MEDIUM] 是否说明评测集、数据划分和污染风险

- Criterion: `LLM-07`
- Message: 没有说明评测集、数据划分或污染风险。
- Evidence: none

### F-013 [MEDIUM] 是否说明推理成本或延迟

- Criterion: `LLM-08`
- Message: 有成本/硬件线索，但仍需量化数据。
- Evidence: `E-010`, `E-013`

## Execution Evidence

| Probe | Status | Return code | Duration | Command |
|---|---|---:|---:|---|
| python-syntax | PASS | 0 | 0.492s | `C:\Program Files\Python313\python.exe -c import ast, pathlib, sys ignore={'.git','.venv','venv','node_modules','__pycache__','.mypy_cache','.pytest_cache','dist','build'} bad=[] fo` |

## Minimal Remediation Plan

### F-007 - 固定并记录随机种子、框架确定性和硬件差异

- Rationale: 降低结果不可重复的随机性。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+6.0**
- Evidence: none

### F-012 - 说明评测集、数据划分和污染/泄漏风险

- Rationale: 让指标具有可比性，避免高估效果。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+6.0**
- Evidence: none

### F-008 - 添加测试、CI 或一键复现脚本

- Rationale: 把复现变成持续可验证的工程流程。
- Cost: **medium**
- Impact: **medium**
- Estimated score gain: **+6.0**
- Evidence: none

### F-002 - 补充数据来源、获取方式和数据许可说明

- Rationale: 让读者知道数据从哪里来、能否使用。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+4.0**
- Evidence: `E-008`

### F-011 - 记录 tokenizer、上下文窗口和截断策略

- Rationale: 避免输入长度和分词差异导致结果变化。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+4.0**
- Evidence: none

### F-001 - 添加锁文件或 Dockerfile，固定 Python、CUDA 和依赖版本

- Rationale: 消除环境版本漂移，提升跨机器复现概率。
- Cost: **medium**
- Impact: **high**
- Estimated score gain: **+4.0**
- Evidence: `E-002`

### F-003 - 添加数据下载或预处理脚本

- Rationale: 把数据准备从手工步骤变成可执行流程。
- Cost: **medium**
- Impact: **high**
- Estimated score gain: **+4.0**
- Evidence: `E-008`

### F-006 - 添加评测脚本、评测命令和指标计算方式

- Rationale: 让结果可以被独立验证。
- Cost: **medium**
- Impact: **high**
- Estimated score gain: **+4.0**
- Evidence: `E-009`

### F-004 - 添加数据集卡或数据许可说明

- Rationale: 明确数据边界和再分发条件。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+3.0**
- Evidence: `E-003`, `E-008`

### F-005 - 在模型卡中说明模型许可和来源

- Rationale: 避免模型使用和再分发风险。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+3.0**
- Evidence: `E-003`

### F-009 - 将 prompt/template 版本化并记录在配置或模型卡中

- Rationale: 避免 prompt 漂移导致结果不可复现。
- Cost: **low**
- Impact: **high**
- Estimated score gain: **+3.0**
- Evidence: `E-012`

### F-010 - 记录 temperature、top_p、max_tokens 等采样参数

- Rationale: 让生成行为可以复现和比较。
- Cost: **low**
- Impact: **medium**
- Estimated score gain: **+2.5**
- Evidence: `E-005`

### F-013 - 说明推理成本、延迟和 token 消耗

- Rationale: 让读者评估复现成本。
- Cost: **low**
- Impact: **low**
- Estimated score gain: **+2.0**
- Evidence: `E-010`, `E-013`

## Evidence Appendix

- `E-001` [readme] `readme.md:1` — <div align="center">
- `E-002` [dependency-manifest] `requirements.txt:1` — torch>=2.4.0
- `E-003` [license] `LICENSE:1` — MIT License
- `E-004` [script] `Wan-Alpha-VAE-train/train_vae.py:1` — import os
- `E-005` [config] `Wan-Alpha-train/configs/accelerate_config/accelerate_wxg.yaml:1` — compute_environment: LOCAL_MACHINE
- `E-006` [instruction] `readme.md:78` — # Create and activate Conda environment
- `E-007` [instruction] `readme.md:135` — CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python3 train_vae.py \
- `E-008` [data] `readme.md:11` — [![arXiv](https://img.shields.io/badge/arXiv-2509.24979-red)](https://arxiv.org/pdf/2509.24979)
- `E-009` [metric] `readme.md:89` — Download [Lightx2v-T2V-14B](https://huggingface.co/Kijai/WanVideo_comfy/blob/main/Lightx2v/lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors)
- `E-010` [hardware] `readme.md:135` — CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python3 train_vae.py \
- `E-011` [model] `readme.md:13` — [![🤗 HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97%20HuggingFace-Model_v1.0-orange)](https://huggingface.co/htdong/Wan-Alpha)
- `E-012` [prompt] `readme.md:55` — <!-- | Prompt | Preview Video | Alpha Video |
- `E-013` [llm-provider] `readme.md:13` — [![🤗 HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97%20HuggingFace-Model_v1.0-orange)](https://huggingface.co/htdong/Wan-Alpha)
- `E-014` [model] `readme.md:148` — --model_id_with_origin_paths "Wan2.1-T2V-1.3B:diffusion_pytorch_model*.safetensors" \
- `E-015` [claim] `readme.md:30` — [2026.03.10] Released Wan-Alpha v2.0 and Wan-Alpha VAE training codes and training datasets.
- `E-016` [claim] `readme.md:44` — [x] Dataset: Open-source the VAE and T2V training dataset.
- `E-017` [claim] `readme.md:128` — For the VAE training dataset, please refer to Section 3.3 of our paper for preparation details.
- `E-018` [claim] `readme.md:157` — You can download the training dataset from Google Drive or Hugging Face.

## Scope and Limitations

- This is static reproduction readiness analysis, not proof that the project reproduces successfully.
- No untrusted repository code is executed by default.
- Execution probes are optional and require explicit --execute; GitHub Action integration is available in the repository.
- AI-generated explanations must be reviewed by the team before submission or release.
