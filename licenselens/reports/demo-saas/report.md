# LicenseLens Analysis Report

- Project: `C:\Users\86199\Documents\ChatGPT\全球校园人工智能算法精英大赛\licenselens\examples\demo-saas`
- Usage mode: `saas`
- Project license: `MIT`
- Generated at: `2026-10-19T02:49:38.231287+00:00`

## Summary

- Dependencies: **3**
- Findings: **4**
- Remediation actions: **6**

## Dependencies

| Package | Version | License | Confidence | Evidence |
|---|---|---|---:|---|
| requests | 2.32.3 | Apache-2.0 | 0.75 | `manifest:requirements.txt`, `catalog:common-packages` |
| numpy | 2.1.0 | BSD-3-Clause | 0.95 | `manifest:requirements.txt`, `metadata:python-distribution` |
| some-agpl-lib | 1.0.0 | AGPL-3.0-only | 0.95 | `manifest:requirements.txt`, `override:licenses.json` |

## Findings

### F-001 [INFO] notice-required

- Package: `requests`
- License: `Apache-2.0`
- Message: requests 使用 Apache-2.0，分发或对外服务时应保留版权、许可证和 NOTICE 信息。
- Evidence: `manifest:requirements.txt`, `catalog:common-packages`, `license:Apache-2.0`, `obligation:include-notice`

### F-002 [INFO] notice-required

- Package: `numpy`
- License: `BSD-3-Clause`
- Message: numpy 使用 BSD-3-Clause，分发或对外服务时应保留版权、许可证和 NOTICE 信息。
- Evidence: `manifest:requirements.txt`, `metadata:python-distribution`, `license:BSD-3-Clause`, `obligation:include-notice`

### F-003 [HIGH] network-copyleft

- Package: `some-agpl-lib`
- License: `AGPL-3.0-only`
- Message: some-agpl-lib 使用 AGPL-3.0-only，在对外提供 SaaS 服务时可能触发网络 copyleft 义务，需要隔离或替换。
- Evidence: `manifest:requirements.txt`, `override:licenses.json`, `license:AGPL-3.0-only`, `obligation:network-copyleft`

### F-004 [INFO] notice-required

- Package: `some-agpl-lib`
- License: `AGPL-3.0-only`
- Message: some-agpl-lib 使用 AGPL-3.0-only，分发或对外服务时应保留版权、许可证和 NOTICE 信息。
- Evidence: `manifest:requirements.txt`, `override:licenses.json`, `license:AGPL-3.0-only`, `obligation:include-notice`

## Remediation Plan

### F-001 - 将 requests 的版权与许可证信息加入 NOTICE/第三方声明

- Rationale: 满足署名和许可证保留义务，降低分发合规风险。
- Cost: **low**
- Impact: **medium**
- Evidence: `manifest:requirements.txt`, `catalog:common-packages`, `license:Apache-2.0`, `obligation:include-notice`

### F-002 - 将 numpy 的版权与许可证信息加入 NOTICE/第三方声明

- Rationale: 满足署名和许可证保留义务，降低分发合规风险。
- Cost: **low**
- Impact: **medium**
- Evidence: `manifest:requirements.txt`, `metadata:python-distribution`, `license:BSD-3-Clause`, `obligation:include-notice`

### F-003 - 替换 some-agpl-lib 为 Apache-2.0/MIT 等更宽松许可的等价依赖

- Rationale: 从源头消除 copyleft 兼容性风险，通常是最稳定的整改方式。
- Cost: **medium**
- Impact: **high**
- Evidence: `manifest:requirements.txt`, `override:licenses.json`, `license:AGPL-3.0-only`, `obligation:network-copyleft`

### F-003 - 将 some-agpl-lib 隔离为独立服务或独立进程，并评估其对外分发方式

- Rationale: 通过架构隔离降低衍生作品边界的不确定性，但需要法律与工程联合复核。
- Cost: **medium**
- Impact: **medium**
- Evidence: `manifest:requirements.txt`, `override:licenses.json`, `license:AGPL-3.0-only`, `obligation:network-copyleft`, `architecture:isolation`

### F-003 - 联系 some-agpl-lib 的版权方，确认商业许可或书面例外

- Rationale: 在无法替换依赖时，取得明确授权可以消除许可证不确定性。
- Cost: **high**
- Impact: **high**
- Evidence: `manifest:requirements.txt`, `override:licenses.json`, `license:AGPL-3.0-only`, `obligation:network-copyleft`, `process:commercial-license`

### F-004 - 将 some-agpl-lib 的版权与许可证信息加入 NOTICE/第三方声明

- Rationale: 满足署名和许可证保留义务，降低分发合规风险。
- Cost: **low**
- Impact: **medium**
- Evidence: `manifest:requirements.txt`, `override:licenses.json`, `license:AGPL-3.0-only`, `obligation:include-notice`

## Scope and Limitations

- This is an engineering compliance check, not legal advice.
- Unknown or custom licenses require manual review of the original LICENSE and upstream terms.
- The current MVP focuses on Python/npm manifests and a defined set of usage modes.
- AI-generated explanations must be reviewed by the team before submission or release.
