"""Build a GitHub-discoverable DSH Go catalogue, or the app's bundled examples.

No upload or network requests. Publish generated files using your normal Git workflow.
"""
import argparse
import base64
import hashlib
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse, quote


def validate(p):
    allowed = {"schemaVersion", "id", "name", "version", "author", "description", "minAppVersion", "theme", "background", "pet", "instructions", "sourceUrl", "licenseNotice"}
    if set(p) - allowed:
        raise ValueError("Unknown fields: " + str(set(p) - allowed))
    assert p.get("schemaVersion", 1) == 1, "Unsupported schema"
    assert re.fullmatch(r"[a-z][a-z0-9]*(?:[.-][a-z0-9]+)+", p["id"]) and len(p["id"]) <= 100, "Invalid ID"
    assert isinstance(p["name"], str) and 0 < len(p["name"].strip()) <= 80, "Invalid name"
    assert isinstance(p["author"], str) and 0 < len(p["author"].strip()) <= 100, "Invalid author"
    assert type(p.get("version", 1)) is int and p.get("version", 1) > 0, "Invalid version"
    assert type(p.get("minAppVersion", 10007)) is int and p.get("minAppVersion", 10007) > 0, "Invalid app version"
    assert len(p.get("description", "")) <= 2000
    assert len(p.get("licenseNotice") or "") <= 30000
    if p.get("sourceUrl"):
        u = urlparse(p["sourceUrl"])
        assert u.scheme == "https" and u.hostname and not u.username and len(p["sourceUrl"]) <= 500
    assert any(p.get(key) is not None for key in ("theme", "background", "pet", "instructions")), "No extension"
    for key, color_keys, allowed_keys in (
        ("theme", ("lightAccent", "darkAccent"), {"lightAccent", "darkAccent"}),
        ("background", ("lightColor", "darkColor"), {"lightColor", "darkColor", "imageBase64", "opacity"}),
        ("pet", (), {"idle", "working", "tapped", "imageBase64", "sizeDp", "frameMillis", "spriteSheet", "showDeepSeekBalance"}),
    ):
        part = p.get(key)
        if part is None:
            continue
        assert not set(part) - allowed_keys, f"Unknown {key} fields"
        for color in color_keys:
            if key == "theme" or color in part:
                assert re.fullmatch(r"#[0-9A-Fa-f]{6}", part[color]), "Expected #RRGGBB"
        if part.get("imageBase64") is not None:
            assert len(part["imageBase64"]) <= 3 * 1024 * 1024
            image = base64.b64decode(part["imageBase64"], validate=True)
            assert image.startswith((b"\x89PNG\r\n\x1a\n", b"\xff\xd8\xff")) or (image[:4] == b"RIFF" and image[8:12] == b"WEBP"), "Invalid raster image"
        if key == "background":
            assert 0 <= part.get("opacity", .15) <= .4
        if key == "pet":
            assert type(part.get("showDeepSeekBalance", False)) is bool
            sheet = part.get("spriteSheet")
            if sheet is not None:
                assert set(sheet) == {"columns", "rows", "idle", "working", "tapped"}
                assert part.get("imageBase64") and all(type(sheet[k]) is int and 1 <= sheet[k] <= 16 for k in ("columns", "rows"))
                for state in ("idle", "working", "tapped"):
                    t = sheet[state]
                    assert set(t) == {"row", "durations"} and type(t["row"]) is int and 0 <= t["row"] < sheet["rows"]
                    assert 1 <= len(t["durations"]) <= sheet["columns"] and all(type(d) is int and 40 <= d <= 5000 for d in t["durations"])
            assert type(part.get("sizeDp", 64)) is int and 40 <= part.get("sizeDp", 64) <= 120
            assert type(part.get("frameMillis", 700)) is int and 200 <= part.get("frameMillis", 700) <= 5000
            for state in ("idle", "working", "tapped"):
                frames = part.get(state, ["cat"])
                assert isinstance(frames, list) and 1 <= len(frames) <= 16
                assert all(isinstance(f, str) and f.strip() and len(f.encode("utf-16-le")) // 2 <= 16 and "\n" not in f for f in frames)
    if p.get("instructions") is not None:
        assert p["instructions"].strip() and len(p["instructions"]) <= 12000


def build(source, output, base_url=None, bundle=False):
    if not bundle:
        parsed = urlparse(base_url or "")
        if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ValueError("Use an HTTPS --base-url for the directory containing the packages")
    entries, ids = [], set()
    for path in sorted(source.glob("*.dshgo.json")):
        raw = path.read_bytes()
        if len(raw) > 4 * 1024 * 1024:
            raise ValueError(f"{path}: exceeds 4 MB")
        p = json.loads(raw)
        validate(p)
        if p["id"] in ids:
            raise ValueError("Duplicate ID: " + p["id"])
        ids.add(p["id"])
        name = p["id"] + ".json" if bundle else path.name
        entries.append({"id": p["id"], "name": p["name"], "version": p.get("version", 1), "author": p["author"],
                        "description": p.get("description", ""), "url": name if bundle else base_url.rstrip("/") + "/" + quote(name),
                        "sha256": hashlib.sha256(raw).hexdigest()})
        if bundle:
            output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, output.parent / name)
    if not entries:
        raise ValueError("No *.dshgo.json packages found")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"schemaVersion": 1, "plugins": entries}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return entries


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("plugins"))
    parser.add_argument("--output", type=Path, default=Path("dsh-go-catalog.json"))
    parser.add_argument("--base-url")
    parser.add_argument("--bundle", action="store_true", help="Copy verified examples beside the app's local catalogue")
    args = parser.parse_args()
    result = build(args.source, args.output, args.base_url, args.bundle)
    print(f"Validated {len(result)} plugins; wrote {args.output}. No files uploaded.")
