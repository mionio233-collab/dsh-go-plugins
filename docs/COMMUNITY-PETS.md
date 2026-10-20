# 社区宠物 Android 适配（2026-10-20）

商城新增两个独立可安装包，并移除 `go.sample.cat` 陪伴小猫。升级读取插件存储时只移除来源为 `builtin` 的旧示例记录；同 ID 的用户本地包不删除。两只宠物沿用现有互斥规则，启用一只会停用另一只。

| 原项目 | 固定提交 | 手机端支持 |
| --- | --- | --- |
| [dsh-pet](https://github.com/zhu1090093659/dsh-pet) | `a03fb5c8fbd5ecd3d09a97f227e3a8dd5b723787` | 原版鲸鱼娘精灵图、按原始时长播放待机/工作/点击挥手、拖动与位置记忆 |
| [DeepSeek Balance Whale Widget](https://github.com/MeteorNOX/DeepSeek-Balance-Whale-Widget) | `5247dd6813d6e4430728f39ccc63d43cda046022` | 原版角色图、点击弹性反馈、左右贴边与左侧镜像、位置记忆、官方 API 余额 |

这是原生 Android 适配，不运行上游 JavaScript 或桌面宿主。dsh-pet 的 Live2D、工坊、喂食与亲密度，以及小鲸鱼的桌面账本、逐轮费用、音效和泡泡编辑器尚未移植，商城描述已明确列出。

## 余额

启用前展示能力说明。App 仅选择本机 ID 为 `deepseek`、地址为 `https://api.deepseek.com` 或其 `/v1` 路径的服务商密钥，并只向固定官方 `https://api.deepseek.com/user/balance` 发请求，不跟随重定向。插件仅声明 `pet.showDeepSeekBalance`，无法获得密钥或指定 URL。

前台显示挂件时每 60 秒刷新，点按也可刷新；离开挂件或 App 进入后台后停止轮询。预览不会请求余额。无密钥或请求失败显示提示，金额保留原币种与十进制精度，不伪造余额或消费统计。未使用真实账号执行余额请求。

接口依据：[DeepSeek Get User Balance](https://api-docs.deepseek.com/api/get-user-balance/)。

## 素材与复现

图片字节原样打包，没有裁切、重绘或重新编码。包内 `sourceUrl` 与 `licenseNotice` 可在详情查看并随导出保留。特别保留小鲸鱼的 PROVENANCE：美术不属于代码 MIT 授权范围，仅用于运行该插件，不授予再许可。dsh-pet 的原图清单标注 BSD-3-Clause，而仓库根 LICENSE 为 Apache-2.0；包内分别保留该声明和上游完整许可证，不改写为统一授权。

在 `.artifacts/upstream-dsh-pet`、`.artifacts/upstream-whale` 准备对应提交后执行：

```powershell
python scripts/adapt-community-pets.py
python scripts/publish-go-plugins.py --bundle --output app/src/main/assets/go-marketplace/catalog.json
```

`pet.spriteSheet` 是可导出的通用数据能力，包含 `columns`、`rows`（1–16）及 `idle`、`working`、`tapped`，每条轨道含 `row`（从 0 开始）和 `durations`（每帧 40–5000 毫秒，长度不超过列数）。使用同一 `pet.imageBase64` 图片，图片尺寸必须整除网格。原图片大小和格式限制保持不变。这些新增字段需要本轮 App，适配包标注 `minAppVersion: 10008`，旧版会拒绝安装。

本仓库分发 Android 数据包；不是原作者官方 Android 发行版。

