#!/usr/bin/env python3
"""Construit atlas.html (page autonome, données embarquées) depuis data/*.json.
Usage : python3 scripts/build_atlas.py [--out site/index.html]"""
import json, sys, pathlib, datetime, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / "data"

def load(name, default):
    p = D / name
    return json.loads(p.read_text()) if p.exists() else default

video = load("video-models.json", [])
image = load("image-models.json", [])
prices = load("prices.json", [])
gpu = load("gpu-hour.json", [])
alias = load("model-id-aliases.json", {})  # id des prix -> id des modeles
local = load("local-runs.json", {})  # id -> Mac M5 Max 128 Go, RTX 4090
audio = load("audio-models.json", [])
threed = load("3d-models.json", [])
platforms = load("platforms.json", [])
rank = load("rankings.json", {})
integ = load("integrations.json", {}).get("by_id", {})

by_model = {}
for p in prices:
    mid = alias.get(p.get("model_id"), p.get("model_id"))
    by_model.setdefault(mid, []).append(p)

for m in audio + threed:
    m["_int"] = integ.get(m["id"], {})
for m in video + image:
    m["_int"] = integ.get(m["id"], {})
    m["_scores"] = rank.get("scores", {}).get(m["id"], {})
    m["_local"] = local.get(m["id"], {})
    ps = by_model.get(m["id"], [])
    m["_prices"] = ps
    def best(key):
        vals = [p[key] for p in ps if p.get("unit") != "subscription" and isinstance(p.get(key), (int, float)) and p[key] > 0]
        return min(vals) if vals else None
    m["_best"] = {k: best(k) for k in ("price_usd_480p_s", "price_usd_720p_s", "price_usd_1080p_s", "price_usd_per_image")}

data = {"video": video, "image": image, "audio": audio, "threed": threed, "platforms": platforms, "rank_sources": rank.get("sources", {}), "gpu": gpu, "prices": [dict(p, atlas_id=alias.get(p.get("model_id"), p.get("model_id"))) for p in prices],
        "orphans": sorted({p.get("model_id") for p in prices} - {m["id"] for m in video + image} - set(alias)),
        "built": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}

tpl = (ROOT / "scripts" / "atlas_template.tpl").read_text()
out = pathlib.Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else ROOT / "site" / "index.html"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(tpl.replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")))
print(f"{out} : {len(video)} video, {len(image)} image, {len(prices)} prix, {len(data['orphans'])} prix sans modele")
