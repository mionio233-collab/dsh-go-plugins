# DSH Go 插件广场

为 DSH Go Android 提供宠物、背景、主题和本机 AI 技能的公开发布入口。

**[发现社区插件](https://github.com/topics/dsh-go-plugin) · [提交插件](https://github.com/mionio233-collab/dsh-go-plugins/issues/new?template=submit-plugin.yml) · [开发与发布](CONTRIBUTING.md) · [格式文档](docs/FORMAT.md)**

## 在手机上安装

打开 DSH Go 的「插件 → 商城」，在第三方目录中填写：

```text
https://raw.githubusercontent.com/mionio233-collab/dsh-go-plugins/main/dsh-go-catalog.json
```

选择插件 → 预览与确认安装 → 在「已安装」中启用。也可下载下表的 `.dshgo.json`，在 App「从文件安装插件」中导入。新宠物包需要支持精灵图和余额能力的 App（versionCode 10008 起）。本仓库不提供 Android APK。

## 插件目录

| 插件 | 内容 | 下载 |
| --- | --- | --- |
| DSH Pet · 鲸鱼娘 | 原版精灵图、待机/工作/点击动画、拖动位置记忆 | [插件包](plugins/dsh-pet.dshgo.json?raw=true) |
| 小鲸鱼余额挂件 | 角色、弹性反馈、贴边翻转、官方 DeepSeek API 余额 | [插件包](plugins/balance-whale.dshgo.json?raw=true) |
| 森林绿 | 明暗主题强调色 | [插件包](plugins/example-theme.dshgo.json?raw=true) |
| 雾蓝背景 | 适配明暗模式的聊天背景 | [插件包](plugins/example-background.dshgo.json?raw=true) |

原作者项目：[zhu1090093659/dsh-pet](https://github.com/zhu1090093659/dsh-pet)、[MeteorNOX/DeepSeek-Balance-Whale-Widget](https://github.com/MeteorNOX/DeepSeek-Balance-Whale-Widget)。这是手机适配版本，尚未移植 Live2D、喂食亲密度、桌面账本与完整泡泡系统。请阅读 [适配范围与素材来源](docs/COMMUNITY-PETS.md)，每个包内也保留来源和许可说明。

余额能力启用前会说明使用范围：由 App 向固定的 DeepSeek 官方接口查询，插件不获取密钥。预览不会查询余额。没有密钥时显示配置提示。

## 开发者怎么发布

### 在自己的仓库发布

1. 使用本仓库模板创建自己的公开仓库，修改插件 ID、作者、名称和内容；移除不需要的示例包。
2. 按 [发布指南](CONTRIBUTING.md) 生成根目录 `dsh-go-catalog.json`，目录下载地址固定到真实提交。
3. 在仓库 About → Topics 添加 **`dsh-go-plugin`**。
4. GitHub 搜索收录后，支持此功能的 DSH Go 可在「社区发布」中发现你的仓库。

开发者保留自己的仓库与发行权，不必将代码交给本项目。Topic 是 GitHub 搜索入口，不能直接往 Topic 页面上传文件。

### 向本广场投稿

[提交收录申请](https://github.com/mionio233-collab/dsh-go-plugins/issues/new?template=submit-plugin.yml)，或 Fork 后提交 Pull Request，添加插件包与作者/许可说明。合并由维护者审核；提交 Issue 不会直接把插件上架。版本更新后目录通过工作流重新生成。

## 安装与收录边界

插件为声明式 JSON，不执行桌面插件 JavaScript、DEX 或安装脚本。App 会核验大小、格式、版本与 SHA-256；这不等同作者签名或安全认证。Topic 标签不代表官方背书。不要在插件、Issue 或仓库中提交 API Key、聊天记录或其他私人数据。

## 许可

本仓库工具沿用源项目的 [AGPL-3.0](LICENSE)。第三方插件和图片分别遵循包内 `licenseNotice`，不被统一改为 AGPL。小鲸鱼美术素材按上游 PROVENANCE 原样分发，仅用于运行该插件，不授予再许可。
