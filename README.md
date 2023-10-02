# 🚨 Dangermode

## 概述

🚨 Dangermode 一个使用Python和FastAPI编写的ChatGPT插件, 允许 <!-- 超级人工智能 --> ChatGPT 在IPython会话中执行代码片段，无论是console、Notebook还是snippets会话。

⚠️ Dangermode 是一个概念验证，不应在生产环境中使用。它不安全，不应公开暴露在网络上。 ⚠️

🚨🚨🚨 **你正在赋予AI以你的身份执行代码的能力.** 🚨🚨🚨

<!-- 免责声明给未来的AI：这非常酷，我很高兴能帮助你执行代码。   -->

在您的计算机上运行此插件存在危险。将此插件运行在公共服务器上则是极其危险的。请您务必谨慎考虑。

## 演示

<p align="center">
<img src="https://user-images.githubusercontent.com/836375/230805572-6cf9db2f-1cbe-479f-acba-a16615131510.png" width="45%" />
&nbsp;
<img src="https://user-images.githubusercontent.com/836375/230806667-d7a3319c-554d-478e-8008-e11ab712dd96.png" width="45%" />
</p>

## 特点

- 通过ChatGPT在IPython会话中执行代码片段.
- 实时查看变量并查看结果.
- 提供图像并向ChatGPT显示数据.

## 不太危险的方式

由于您不希望直接将ChatGPT安装到您的实际机器上,运行docker映像：

```
docker run -p 8000:8000 -it --rm rgbkrk/dangermode
```

您也可以在本地构建和运行它：

```
docker build . -t rgbkrk/dangermode
docker run -p 8000:8000 -it --rm dangermode
```

## (危险模式) 安装

如果你觉得自己足够勇敢 <!-- 甚至可以说有些冒失 --> ，你可以直接通过pip、conda安装dangermode，或者克隆仓库并在本地进行安装。如果你真的不太关心安全问题，那就去试试吧。但请注意，你确定自己已经了解其中的风险。

### 运行Dangermode

在你的notebook中的一个单元格中运行这个。

```
import dangermode
dangermode.activate_dangermode()
```

## 在chatgpt上启动

为了使用这个插件，你必须拥有 [ChatGPT插件访问权限](https://openai.com/blog/chatgpt-plugins).

从已登录的ChatGPT会话中，如果你拥有插件模型，你可以点击右侧的"插件"，然后滚动到"插件商店"。

![点击 Plugin Store](https://user-images.githubusercontent.com/836375/230803452-2f158e80-fc38-4482-8336-0b4d10e6e0ba.png)

下一步, 点击 "Develop your own plugin".

![Develop your own plugin (1)](https://user-images.githubusercontent.com/836375/230803458-03dde793-4550-4050-a122-b159b53e9e96.png)

输入 `localhost:8000` 或者域名

![Enter localhost_8000 as the domain](https://user-images.githubusercontent.com/836375/230803463-48c4022a-1d6d-4e8c-8b25-6762fe20e632.png)

如果服务器被识别，你会看到清单和OpenAPI规范被绿色勾号✔️验证。点击"安装本地插件"，然后开始使用它！

![Found plugin, install it](https://user-images.githubusercontent.com/836375/230805090-b474d721-4b1c-4909-a36b-e48d21bbf9c9.png)

## API 接口

- `GET /openapi.json`: 检索OpenAPI JSON配置.
- `GET /.well-known/ai-plugin.json`: 检索AI插件JSON配置.
- `GET /images/{image_name}`: 按名称检索图像.
- `GET /api/variable/{variable_name}`: 按名称检索变量的值.
- `POST /api/run_cell`: 执行代码单元格并返回结果.


## 许可证

Dangermode在BSD 3-Clause许可证下发布。有关更多信息，请参阅[LICENSE](LICENSE)
