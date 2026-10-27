# ReproLens 评分 JSON 外部接入演示

> 日期：2026-10-27
> 目的：证明 `score.json` 不只是可下载文件，而是能被外部 CI 门禁和 Webhook 实际消费。

## 一、使用方式

终端 A 启动 Webhook 接收端：

```powershell
cd D:\CODEX\ReproLens\repolens
$env:PYTHONPATH = "src"
python scripts\webhook_receiver_demo.py --port 8770 --output reports\latest\webhook-received.json
```

终端 B 读取评分 JSON、执行门禁并发送 Webhook：

```powershell
cd D:\CODEX\ReproLens\repolens
$env:PYTHONPATH = "src"
python -m repolens.integrations reports\latest\score.json --min-score 40 --webhook-url http://127.0.0.1:8770/hook
```

## 二、实际门禁输出

```text
# ReproLens Score Gate

- Project: D:\CODEX\ReproLens\repolens\examples\demo-llm-app
- Commit: -
- Score: 49.1 / 100
- Readiness: At Risk
- Evidence coverage: 16/25 (64.0%)
- Claims: total=2, verified=2, partial=0
- Gate: PASSED (minimum 40.0)
- Webhook: delivered (204)
```

如果阈值改为 60 分，同一份评分会显示 `FAILED`，进程返回非零退出码，可直接用于阻止低质量变更合并。

## 三、Webhook 实际收到的数据

接收端返回 HTTP 204，并保存了 974 字节：

```json
{
  "schema_version": 1,
  "project": "D:\\CODEX\\ReproLens\\repolens\\examples\\demo-llm-app",
  "source_commit": null,
  "score": 49.1,
  "readiness": "At Risk",
  "evidence_coverage": {"covered": 16, "total": 25, "percent": 64.0},
  "claim_counts": {"total": 2, "verified": 2, "partially_verified": 0, "unverified": 0},
  "claims": [
    {"claim_id": "C-001", "status": "verified", "gaps": []},
    {"claim_id": "C-002", "status": "verified", "gaps": []}
  ],
  "top_findings": [
    {"criterion_id": "ENV-02", "severity": "medium", "title": "是否锁定依赖版本或提供容器化配置"},
    {"criterion_id": "DATA-01", "severity": "high", "title": "是否说明数据来源和获取方式"}
  ]
}
```

完整接收文件：`repolens/reports/latest/webhook-received.json`。

## 四、这说明了什么

1. `score.json` 可以被独立程序读取；
2. 外部系统可以按最低分数执行通过/失败门禁；
3. Webhook 可以接收标准化的精简审计结果；
4. GitHub Actions、CI、Slack/飞书机器人或内部质量平台都可以复用同一份 JSON。

## 五、测试覆盖

外部接入模块当前包含以下自动化测试：

- 评分 JSON 是否生成稳定的外部契约；
- 门禁通过/失败状态；
- HTTP Webhook 是否收到正确数据；
- 低于阈值时是否返回失败退出码。
