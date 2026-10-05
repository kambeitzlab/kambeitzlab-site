"""Download all images referenced in the YAML exports from Wix's public CDN.

Usage:  pip install pyyaml requests && python download_images.py
Writes to ./images/<media-id>  (filenames match the ids in the YAML files)
"""
import pathlib
import requests
import yaml

CDN = "https://static.wixstatic.com/media/"
here = pathlib.Path(__file__).parent
out = here / "images"
out.mkdir(exist_ok=True)

ids = set()
for f in ["team.yaml", "alumni.yaml", "projects.yaml", "news.yaml"]:
    for item in yaml.safe_load((here / f).read_text(encoding="utf-8")):
        for key in ("photo", "image"):
            if item.get(key):
                ids.add(item[key])
        ids.update(item.get("gallery") or [])

for i, media_id in enumerate(sorted(ids), 1):
    target = out / media_id
    if target.exists():
        continue
    r = requests.get(CDN + media_id, timeout=60)
    r.raise_for_status()
    target.write_bytes(r.content)
    print(f"[{i}/{len(ids)}] {media_id} ({len(r.content) // 1024} kB)")

print(f"Done: {len(ids)} images in {out}")
