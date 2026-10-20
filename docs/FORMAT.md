# DSH Go 手机插件与开放发布

DSH Go 的插件页包含商城、社区发布、已安装、创作、技能五个入口。本机 API 和连接电脑两种模式都可使用。桌面 DSH 插件仍在“已安装 → 查看连接电脑的 DSH 插件”中查看。

## 用户使用

1. 打开“插件 → 商城”，预览 DSH Pet 鲸鱼娘、小鲸鱼余额挂件、背景或主题并安装。
2. 在“已安装”中启用。同一时间使用一套主题、一个背景和一只宠物；冲突插件会停用，界面有提示。
3. 宠物可拖动、点击互动，聊天生成中显示工作状态。宠物只出现在 App 聊天内。余额挂件启用时会说明密钥使用范围。
4. 在“创作”填写名称、作者、唯一 ID，生成模板，可导入自己的 PNG/JPEG/WebP 图片，或编辑 AI 生成的 JSON。
5. 预览后安装，或导出 `.dshgo.json` 文件。另一台手机可在“已安装 → 从文件安装插件”导入。
6. 可暂停所有插件、卸载、检查同来源更新或回退上一版本。更新及回退后需要重新启用。

App 内 AI 可生成 `.dshgo.json`，使用已获授权的 `write_file` 保存后，聊天文件卡片和本机文件页会提供预览安装入口。生成文件不等于安装或发布；用户仍需安装并启用。

## 开发者开放发布：GitHub Topic

社区入口：https://github.com/topics/dsh-go-plugin

这采用 GitHub 原生的 Topic 收录机制，无需向 App 作者申请上传账号。开发者在自己的**公开仓库**发布，代码与发行权由开发者保留。

1. 将插件文件放在仓库 `plugins/` 目录，例如 `plugins/my-cat.dshgo.json`。
2. 从本项目复制 `scripts/publish-go-plugins.py`。执行以下命令，`OWNER/REPO` 与 `COMMIT_SHA` 替换为真实仓库和已提交的插件版本：

   ```sh
   python scripts/publish-go-plugins.py --source plugins --base-url https://raw.githubusercontent.com/OWNER/REPO/COMMIT_SHA/plugins --output dsh-go-catalog.json
   ```

3. 将生成的 `dsh-go-catalog.json` 提交到默认分支根目录。目录指向固定 commit 的文件，避免目录与下载内容在更新时不一致。
4. 在 GitHub 仓库首页 About → Topics 添加 `dsh-go-plugin`。同时支持桌面 DSH 时可以再添加 `dsh-plugin`，但不要把仅桌面可用的包声明成手机插件。
5. 等待 GitHub 搜索索引更新。手机端“社区发布”按更新时间分页发现仓库，读取默认分支根目录中的目录文件，再显示可安装插件。
6. 更新时递增插件 `version`，重新生成并发布目录。手机端从安装时记录的同一个来源检查更新。

可将 [自动发布工作流模板](../.github/workflows/publish.yml) 复制为自己仓库的 `.github/workflows/publish.yml`。它只生成并提交目录，不执行插件包里的代码。仓库需要允许 Actions 写入内容。

Topic 自动生成，不是可上传任意文件的托管商店。**添加标签不代表官方审核、作者认证或安装兼容性。** App 显示仓库/目录来源，下载后核验 SHA-256、包身份及协议。哈希保证与当前目录一致，不是作者数字签名。GitHub 断网、限流或尚未收录时，可在商城填写目录 HTTPS 直链，也可离线导入文件。

本仓库是公开发布入口，Topic 收录仍取决于 GitHub 搜索索引。

## 插件协议 v1

包是一个 UTF-8 JSON 文件，推荐后缀 `.dshgo.json`。**数据声明式格式，不执行 JavaScript、DEX、npm、HTML 或安装脚本。** 不支持的字段会被拒绝。插件不能申请任意文件、网络、无障碍或系统悬浮权限。可选余额能力仅由 App 调用固定 DeepSeek 官方接口，并在启用前单独说明。

```json
{
  "schemaVersion": 1,
  "id": "yourname.cat",
  "name": "我的小猫",
  "version": 1,
  "author": "你的名字",
  "description": "可拖动的小猫",
  "minAppVersion": 10007,
  "pet": {
    "idle": ["🐱", "😺"],
    "working": ["🐱", "💭"],
    "tapped": ["😻", "💕"],
    "sizeDp": 64,
    "frameMillis": 900
  }
}
```

| 字段 | 规则 |
| --- | --- |
| `schemaVersion` | 当前为 1 |
| `id` | 必填，最长 100 字符，小写域名式标识，如 `yourname.cat`；更新保持 ID 不变 |
| `name` / `author` | 必填，非空，分别最长 80 / 100 字符；作者为自述信息 |
| `version` | 正整数，更新时递增；默认 1 |
| `minAppVersion` | App versionCode；默认 10007，要求高于当前 App 时拒绝安装 |
| `description` | 最长 2000 字符 |
| `theme` | `lightAccent` 和 `darkAccent`，均为 `#RRGGBB`；替换客户端强调色，保留基础文字和控件配色 |
| `background` | `lightColor`、`darkColor`、`opacity`（0–0.4）、可选 `imageBase64`；只改变聊天背景 |
| `pet` | `idle`、`working`、`tapped` 各 1–16 个短文字/emoji 帧，每帧最长 16 个 UTF-16 单元；`sizeDp` 40–120、`frameMillis` 200–5000；可选 `imageBase64` |
| `instructions` | 非空文本，最长 12000 字符；启用时单独确认，注入本机模型及本机定时任务，不注入远程电脑会话；不能新增工具权限 |

至少声明一种扩展能力。可以组合，组合包启用时会停用任何有视觉功能冲突的其他包。多个技能包可共同启用，注入总量限制 24000 字符。

`imageBase64` 是 PNG、JPEG 或 WebP 文件的裸 Base64，不带 `data:` 前缀，不支持 URL。编码最多 3 MB，图片每边不超过 4096 且总像素不超过 4,194,304。插件包最多 4 MB，最多安装 48 个包，安装数据与回退版本共用 32 MB 配额。静态图片与文字状态帧受支持。App 10008 起支持 pet.spriteSheet 精灵图以及 pet.showDeepSeekBalance；详见 [社区宠物适配](COMMUNITY-PETS.md)。GIF 与任意脚本不受支持。

## 商城目录 v1

文件名必须为默认分支根目录 `dsh-go-catalog.json`，自定义目录不限路径：

```json
{
  "schemaVersion": 1,
  "plugins": [{
    "id": "yourname.cat",
    "name": "我的小猫",
    "version": 1,
    "author": "你的名字",
    "description": "可拖动的小猫",
    "url": "https://raw.githubusercontent.com/OWNER/REPO/COMMIT_SHA/plugins/my-cat.dshgo.json",
    "sha256": "替换为插件文件原始字节的64位十六进制SHA256"
  }]
}
```

目录最多 512 KB / 500 项，不能出现重复 ID。下载地址必须为无账号信息、无片段的 HTTPS 直链，不接受重定向；`id`、`name`、`author`、`version` 必须与下载包相符。生成脚本对数据字段做预检查；手机安装器还会校验图片尺寸、当前 App 兼容版本等。

## 维护与边界

- 内置示例也通过同一目录、包协议和安装器安装，无特权路径。重新生成：`python scripts/publish-go-plugins.py --bundle --output app/src/main/assets/go-marketplace/catalog.json`。
- 安装、启用、停用、回退以原子文件提交，更新保留上一版本和来源。读取失败时不加载任何插件且保留损坏文件，不自动覆盖。
- “暂停所有插件”保留安装记录和启用选择，关闭后恢复；卸载会删除插件及回退数据。
- 当前是手机声明式插件 v1，不兼容任意桌面 DSH 插件，不提供任意网页面板、脚本工具或原生模块热加载。后续增加扩展点需升级协议与 App。
- 独立商城后端账号、审核、评分、收费及作者签名不在此版本中；目前开放发布依托 GitHub 仓库及 Topic，自定义目录支持自托管。
