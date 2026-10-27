# ReproLens Vercel 稳定动态部署指南

这个方案保留完整在线分析能力：用户可以输入任意公开 GitHub 仓库或 GitHub Pages 地址，现场生成报告。

## 已准备好的配置

- `vercel_app/app.py`：FastAPI 应用和 `/api/audit` 在线分析接口；
- `vercel_app/requirements.txt`：Vercel Python 依赖；
- `vercel_app/vercel.json`：函数最长运行时间 300 秒；
- `vercel_app/.vercelignore`：排除不必要文件；
- `vercel_app/vercel_ui.py`：动态网页界面；
- `vercel_app/repolens/`：随函数部署的扫描器源码。

## 部署步骤

### 1. 登录

打开：

<https://vercel.com/new>

选择 **Continue with GitHub**，使用 `czkPK` 对应的 GitHub 账号登录。

### 2. 导入项目

在项目列表中导入：

```text
czkPK/reprolens
```

### 3. 保留默认配置

Vercel 会自动识别：

```text
Framework Preset: FastAPI
Root Directory: vercel_app
Build Command: automatic
Output Directory: automatic
```

不需要设置环境变量。

### 4. 点击 Deploy

首次部署通常需要几分钟。成功后 Vercel 会提供固定地址，格式类似：

```text
https://reprolens-xxxx.vercel.app
```

以后重新推送 GitHub `main` 分支，Vercel 会自动重新部署。

## 功能验证

打开固定网址后测试：

1. 输入 `https://github.com/huggingface/smolagents`；
2. 等待分析完成；
3. 查看完整报告、声明矩阵、AutoFix 验证和评分 JSON；
4. 输入 `https://donghaotian123.github.io/Wan-Alpha/`；
5. 确认自动识别为 `WeChatCV/Wan-Alpha`；
6. 刷新页面，确认浏览器会恢复上一次结果。

## 说明

- Vercel 固定主页地址长期存在；
- 分析结果保存在浏览器本地，不依赖临时服务器文件；
- 免费实例的函数最长运行时间配置为 300 秒；
- 超大仓库可能超过在线分析上限，但仍可使用本地版；
- 不执行第三方仓库代码。
