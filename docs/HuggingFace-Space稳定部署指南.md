# ReproLens 稳定公网部署指南（Hugging Face Space）

临时隧道只适合本机测试。最终作品应部署到固定公网地址。

## 为什么选择 Hugging Face Space

- 免费 CPU Basic 实例可长期运行；
- 创建后网址固定，不会像临时隧道一样变化；
- 支持 Docker，可直接运行 ReproLens 的 Python 服务；
- 国内网络通常可以访问；
- 后续修改代码后可在 Space 中重新构建。

## 一次性部署步骤

### 1. 登录

打开：

<https://huggingface.co/new-space>

使用 GitHub 账号或 Hugging Face 账号登录。

### 2. 创建 Space

填写：

- Owner：你的账号；
- Space name：`reprolens`；
- License：MIT；
- SDK：**Docker**；
- Docker template：**Blank**；
- Hardware：**CPU basic（免费）**；
- Visibility：**Public**。

点击 **Create Space**。

### 3. 上传部署文件

进入 Space 的 **Files** 页面，点击 **Add file → Upload files**，上传以下两个文件：

```text
D:\CODEX\ReproLens\deploy\huggingface-space\Dockerfile
D:\CODEX\ReproLens\deploy\huggingface-space\README.md
```

上传后点击提交，等待 Space 自动构建。

### 4. 获取固定地址

构建成功后，网页地址通常是：

```text
https://huggingface.co/spaces/你的用户名/reprolens
```

应用地址通常是：

```text
https://你的用户名-reprolens.hf.space
```

以后正式提交和演示使用 `hf.space` 这个固定地址。

## 验证

1. 打开固定应用地址；
2. 输入 `https://github.com/huggingface/smolagents`；
3. 等待分析完成；
4. 检查完整报告、声明矩阵、AutoFix 验证和评分 JSON；
5. 再输入 GitHub Pages 地址验证自动识别。

## 注意事项

- 免费 Space 长时间无人访问会休眠，首次打开可能需要几十秒唤醒，但网址不会改变。
- 报告文件保存在临时目录，Space 重启后旧报告链接可能失效；重新分析即可生成新报告。
- 公网主页和核心应用地址是稳定的。
- 免费实例不保证永久 SLA，但比临时隧道可靠得多。
- Space 构建时会从 GitHub 拉取 `czkPK/reprolens` 的最新 `main` 分支。更新作品后，在 Space 中选择 **Factory rebuild** 即可重新部署。
