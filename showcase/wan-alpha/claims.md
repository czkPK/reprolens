# ReproLens 声明—证据—缺口矩阵

- Repository: `https://github.com/WeChatCV/Wan-Alpha @ 9e5d0533da2d`
- Generated at: `2026-10-27T15:05:32.760299+00:00`
- Evidence coverage: **19/23 (82.6%)**
- Claims extracted: **4**

## Matrix

| 声明编号 | README 声明 | 验证状态 | 检查依据（需要检查的项） | 还缺什么（缺口） | 支持证据 | 验证说明 |
|---|---|---|---|---|---|---|
| C-001 | [2026.03.10] Released Wan-Alpha v2.0 and Wan-Alpha VAE training codes and training datasets. | 未验证 | DOC-02（是否提供快速开始和运行示例）；DOC-03（是否提供测试、CI 或一键复现脚本）；EXP-02（是否提供评测脚本或评测命令） | DOC-03（是否提供测试、CI 或一键复现脚本）；EXP-02（是否提供评测脚本或评测命令） | `E-006` readme.md:78：# Create and activate Conda environment<br>`E-007` readme.md:135：CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python3 train_vae.py \<br>`E-009` readme.md:89：Download [Lightx2v-T2V-14B](https://huggingface.co/Kijai/WanVideo_comfy/blob/main/Light... | 缺少关键证据，当前声明不能视为已验证；缺口：DOC-03（是否提供测试、CI 或一键复现脚本）；EXP-02（是否提供评测脚本或评测命令）。 |
| C-002 | [x] Dataset: Open-source the VAE and T2V training dataset. | 未验证 | DOC-02（是否提供快速开始和运行示例）；DOC-03（是否提供测试、CI 或一键复现脚本）；EXP-02（是否提供评测脚本或评测命令） | DOC-03（是否提供测试、CI 或一键复现脚本）；EXP-02（是否提供评测脚本或评测命令） | `E-006` readme.md:78：# Create and activate Conda environment<br>`E-007` readme.md:135：CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python3 train_vae.py \<br>`E-009` readme.md:89：Download [Lightx2v-T2V-14B](https://huggingface.co/Kijai/WanVideo_comfy/blob/main/Light... | 缺少关键证据，当前声明不能视为已验证；缺口：DOC-03（是否提供测试、CI 或一键复现脚本）；EXP-02（是否提供评测脚本或评测命令）。 |
| C-003 | For the VAE training dataset, please refer to Section 3.3 of our paper for preparation details. | 未验证 | DOC-02（是否提供快速开始和运行示例）；DOC-03（是否提供测试、CI 或一键复现脚本）；EXP-02（是否提供评测脚本或评测命令） | DOC-03（是否提供测试、CI 或一键复现脚本）；EXP-02（是否提供评测脚本或评测命令） | `E-006` readme.md:78：# Create and activate Conda environment<br>`E-007` readme.md:135：CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python3 train_vae.py \<br>`E-009` readme.md:89：Download [Lightx2v-T2V-14B](https://huggingface.co/Kijai/WanVideo_comfy/blob/main/Light... | 缺少关键证据，当前声明不能视为已验证；缺口：DOC-03（是否提供测试、CI 或一键复现脚本）；EXP-02（是否提供评测脚本或评测命令）。 |
| C-004 | You can download the training dataset from Google Drive or Hugging Face. | 未验证 | DOC-02（是否提供快速开始和运行示例）；DOC-03（是否提供测试、CI 或一键复现脚本）；EXP-02（是否提供评测脚本或评测命令） | DOC-03（是否提供测试、CI 或一键复现脚本）；EXP-02（是否提供评测脚本或评测命令） | `E-006` readme.md:78：# Create and activate Conda environment<br>`E-007` readme.md:135：CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python3 train_vae.py \<br>`E-009` readme.md:89：Download [Lightx2v-T2V-14B](https://huggingface.co/Kijai/WanVideo_comfy/blob/main/Light... | 缺少关键证据，当前声明不能视为已验证；缺口：DOC-03（是否提供测试、CI 或一键复现脚本）；EXP-02（是否提供评测脚本或评测命令）。 |

## Status Definitions

- **已验证**：相关检查项全部通过，并且有证据支持。
- **部分验证**：找到部分证据，但仍有缺口。
- **未验证**：关键证据缺失，当前声明不能视为已验证。
- **不适用**：相关检查项不适用于当前项目类型。

读表方法：Claim 是 README 原句；Required criteria 是验证这句话需要检查的项；Gaps 是仍未满足的检查项；Evidence 是支持证据编号。该矩阵不执行第三方代码，也不保证语义完全正确。
