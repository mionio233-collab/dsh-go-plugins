# 发布与投稿

## 自己发布（无需等待本仓库审核）

1. 使用本仓库模板或 Fork，清理示例，在 `plugins/` 放置自己的 `.dshgo.json`。每个插件的 ID 要唯一，作者与许可必须真实，更新时递增 version。
2. 提交插件文件并记录提交 SHA。使用 Python 3.12 执行：

```sh
python scripts/publish-go-plugins.py --source plugins --base-url https://raw.githubusercontent.com/OWNER/REPO/COMMIT_SHA/plugins --output dsh-go-catalog.json
```

将 OWNER、REPO、COMMIT_SHA 替换为真实值，再提交目录文件。不要用不存在的提交或需要登录的地址。

3. About → Topics 添加 `dsh-go-plugin`。手机端可直接粘贴目录 URL，不必等待 Topic 搜索索引。
4. 可启用本仓库附带的 GitHub Actions 发布工作流；它需要 contents:write 以提交目录。仓库规则不允许机器人直接提交时，按上面的命令手动生成并提交。

## 向本广场投稿

- 简单收录：使用「提交插件」Issue 表单，提供仓库、目录直链、功能和素材许可。
- 直接贡献：Fork → 在 `plugins/` 添加包 → 更新 README 目录 → Pull Request。不要提交密钥、二进制 APK、上游桌面执行脚本或完整模型文件。
- 投稿表示你有权分发所提交的内容；第三方图片必须附来源和原始许可，不能把代码许可套用于美术资源。
- 本仓库检查通过不代表自动合并；维护者确认格式、来源、能力说明后才会上架。

协议见 [FORMAT.md](docs/FORMAT.md)。商城更新应保留插件 ID，增加 version；安装或更新后由用户自行启用。

Windows 开发者请保持 JSON 文件为 LF 换行；本仓库的 .gitattributes 已固定 LF，避免提交时换行转换造成哈希不一致。

