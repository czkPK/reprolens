# ReproLens 稳定公网部署指南（Koyeb）

当 Hugging Face 登录被拦截时，使用 Koyeb 部署固定公网地址。

## 部署前确认

- GitHub 仓库：<https://github.com/czkPK/reprolens>
- 根目录已有 `Dockerfile`
- 服务端口通过环境变量 `PORT` 设置
- 健康检查地址：`/`

## 一次性部署步骤

### 1. 登录

打开：

<https://app.koyeb.com/auth/signup>

选择 **Continue with GitHub**，使用能访问 `czkPK/reprolens` 的 GitHub 账号登录。

### 2. 创建 Web Service

进入 **Create Service → Web Service → GitHub**。

如果看不到仓库，安装 Koyeb GitHub App，并只授权：

```text
czkPK/reprolens
```

### 3. 填写部署配置

- Repository：`czkPK/reprolens`
- Branch：`main`
- Builder：`Dockerfile`
- Dockerfile path：`Dockerfile`
- Service name：`reprolens`
- Region：`Singapore`（或其他可用亚洲区域）
- Instance type：Free / Nano（以界面实际免费选项为准）
- Port：`8000`
- Health check path：`/`

在环境变量中增加：

```text
PORT=8000
```

### 4. 部署

点击 **Deploy**，等待构建和健康检查完成。

成功后 Koyeb 会提供固定地址，类似：

```text
https://reprolens-你的组织名.koyeb.app
```

这个地址不会像临时隧道一样频繁变化。

## 部署后验证

依次测试：

1. 首页能打开；
2. 输入 `https://github.com/huggingface/smolagents`；
3. 输入 `https://donghaotian123.github.io/Wan-Alpha/`；
4. 确认自动识别为 `WeChatCV/Wan-Alpha`；
5. 检查完整报告、声明矩阵、AutoFix 验证、评分 JSON。

## 注意事项

- Koyeb 免费实例可能缩容到零，首次打开可能需要等待唤醒，但网址保持稳定。
- 报告保存在容器临时目录，实例重启后旧报告可能失效；重新分析即可。
- 不要在公开服务中配置 GitHub 私有令牌。
- 若 Koyeb 要求付费验证或免费实例不可用，可改用 ModelScope 创空间或其他支持 Docker 的云服务。

## 更新作品

GitHub `main` 分支更新后，在 Koyeb 中重新部署服务即可使用最新代码。
