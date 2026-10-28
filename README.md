# InceptionV1 Microscope

静态神经网络探索网站：网络概览、层、4×4 分组与神经元详情四级交互，支持 Feature Vis、Dataset、激活统计、正负稀疏归因关系和热图。

此仓库迁移自原 ChatGPT Sites 项目。网页运行不依赖 GPT API、ChatGPT 登录或原托管站；研究来源链接仅供访问者选择查看。

## 目录

- `dist/`：完整网页及所有运行所需的图片、JSON、压缩热图。
- `original-source/`：取得并保留的原始图片、热图、连接及审计记录；不发布到 Pages。
- `scripts/`：资源下载、转换和校验工具。
- `ops/`：独立服务器部署脚本与说明（如果原项目包含）。
- `.github/workflows/pages.yml`：验证数据后，仅将 `dist/` 发布到 GitHub Pages。

历史上的临时部署压缩包、平台身份配置和 Git 历史不属于本迁移的运行资源，不导入本仓库。

## 发布 GitHub Pages

将代码和数据推送至 `main` 后，在仓库 Settings → Pages → Build and deployment 中，将 Source 设置为 **GitHub Actions**，然后运行 Actions 中的部署工作流。

预期地址：`https://verdyc-mcdonald.github.io/InceptionV1-Microscope/`。该地址只有在 Pages 部署成功后才可访问，以 Actions 返回的实际部署地址为准。

页面使用相对资源路径，支持仓库名称形成的 URL 子目录。GitHub Pages 发布体积限制仅针对部署输出；原始备份不进入网页发布包。

## 本地运行与检查

```sh
python3 scripts/verify-pages.py
python3 -m http.server 8000 --directory dist
```

打开 `http://localhost:8000/`，不要通过双击 HTML 使用 `file://` 打开。

## 数据状态和后续替换

当前内容是从原研究站取得的实验数据，不是本项目自行复现的实验结论。图片隐藏标记、缺失状态和上下游不同的归因指标应保留。当前展示稀疏关系列表，不能据此还原完整连接矩阵。

当前仍是文件式数据接入，并无上传后台。替换实验数据时，应同步生成结构清单、各层统计、连接、图片索引及热图，并更新页面来源文案和默认样例。提交前运行校验，不用零值替代缺失统计。

网页当前使用 AVIF 展示副本；Feature Vis 保持原尺寸，Dataset 裁剪图为 64×64，原始下载文件保留在 `original-source/`。

## 来源

研究数据来源：<https://already-clean.goodfire.com/microscope/inceptionv1.html>，下载日期见数据元信息及审计记录。本项目是独立的研究展示实现，与原研究站无隶属关系。资源原有权利归属不因迁移而改变；此说明不授予第三方素材新的许可。
