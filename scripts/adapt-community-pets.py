"""Package the two pinned upstream pets without changing their artwork or executing upstream code."""
import base64
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(repo, path):
    return (ROOT / '.artifacts' / repo / path).read_text(encoding='utf-8')

def image(repo, path):
    return base64.b64encode((ROOT / '.artifacts' / repo / path).read_bytes()).decode('ascii')

def package(repo, commit, name, plugin):
    folder = ROOT / '.artifacts' / repo
    actual = subprocess.check_output(['git', '-C', str(folder), 'rev-parse', 'HEAD'], text=True).strip()
    assert actual == commit, f'Expected {commit}; got {actual}'
    plugin.update(schemaVersion=1, version=1, minAppVersion=10008)
    (ROOT / 'plugins' / name).write_text(json.dumps(plugin, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

pet_repo = 'upstream-dsh-pet'
manifest = json.loads(read(pet_repo, 'assets/whale/pet.json'))
tracks = manifest['sprite2d']['tracks']
package(pet_repo, 'a03fb5c8fbd5ecd3d09a97f227e3a8dd5b723787', 'dsh-pet.dshgo.json', {
    'id': 'community.dsh.pet', 'name': 'DSH Pet · 鲸鱼娘', 'author': 'zhu1090093659 / dsh-pet contributors',
    'sourceUrl': 'https://github.com/zhu1090093659/dsh-pet',
    'description': 'dsh-pet 手机适配版。保留原版鲸鱼娘精灵图与帧时长，支持待机、工作、点击挥手及拖动记忆。当前未移植 Live2D、宠物工坊、喂食与亲密度系统。',
    'licenseNotice': '来源：zhu1090093659/dsh-pet @ a03fb5c8fbd5ecd3d09a97f227e3a8dd5b723787\n'
        'Android 适配：以原始精灵图及清单数据驱动原生绘制；图片字节未修改。非原作者官方 Android 发行版。\n'
        '上游 assets/whale/pet.json 将该图声明为 BSD-3-Clause，上游根 LICENSE 当前为 Apache-2.0，保留原始声明及许可证如下，不将素材重新许可。\n\n'
        + read(pet_repo, 'LICENSE') + '\n原始素材清单：\n' + read(pet_repo, 'assets/whale/pet.json'),
    'pet': {'idle': ['🐋'], 'working': ['💭'], 'tapped': ['💕'], 'sizeDp': 104,
        'imageBase64': image(pet_repo, 'assets/whale/spritesheet.webp'),
        'spriteSheet': {'columns': 8, 'rows': 9,
            'idle': {'row': 0, 'durations': tracks['idle']['durations']},
            'working': {'row': 7, 'durations': tracks['running']['durations']},
            'tapped': {'row': 3, 'durations': tracks['waving']['durations']}}}
})
whale_repo = 'upstream-whale'
package(whale_repo, '5247dd6813d6e4430728f39ccc63d43cda046022', 'balance-whale.dshgo.json', {
    'id': 'community.balance.whale', 'name': '小鲸鱼余额挂件', 'author': 'MeteorNOX / contributors',
    'sourceUrl': 'https://github.com/MeteorNOX/DeepSeek-Balance-Whale-Widget',
    'description': 'DeepSeek Balance Whale Widget 手机适配版。原版鲸鱼娘、点击弹性反馈、拖动贴边与左侧翻转；读取手机配置的官方 DeepSeek API 余额，前台每分钟刷新。未移植桌面账本、逐轮费用、音效及自定义泡泡编辑器。',
    'licenseNotice': '来源：MeteorNOX/DeepSeek-Balance-Whale-Widget @ 5247dd6813d6e4430728f39ccc63d43cda046022\n'
        'Android 适配：原生界面及余额接口替代桌面宿主。DSniang1.png 字节未修改，仅用于运行此插件，不授予素材再许可。非原作者官方 Android 发行版。\n\n'
        + read(whale_repo, 'LICENSE') + '\n' + read(whale_repo, 'PROVENANCE.md'),
    'pet': {'idle': ['🐋'], 'working': ['💭'], 'tapped': ['💕'], 'sizeDp': 104,
        'imageBase64': image(whale_repo, 'assets/DSniang1.png'), 'showDeepSeekBalance': True}
})
print('Generated two pinned Android adaptations; upstream artwork preserved byte-for-byte.')
