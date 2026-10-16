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

extra = load("local-runs-extra.json", {})
for m in audio + threed:
    m["_int"] = integ.get(m["id"], {})
    m["_local"] = extra.get(m["id"], {})
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

stages = load("stages.json", {"stages": [], "model_overrides": {}, "platforms": {}})
STAGE_RE = [  # (étape, motif cherché dans les fonctions d'édition et le nom de la variante)
    ("effets", r"visage|lip|recast|remplac|swap|avatar|doublage|dubit|motion control|mouvement d.une vidéo|animation d.un personnage|personnage|inpainting|plaque propre|alpha|retouche|suppression de fond|baguette"),
    ("montage", r"prolong|extend|multi-plans|multi-clips|insert|reprise|retake|continuation|recadrage|reframe|transition|interpolation|boucle|outpainting"),
    ("etalonnage", r"relight|hdr|étalonn|couleur|recolor"),
    ("agrandissement", r"super-résolution|upscal|restauration|défloutage|détails affinés|seedvr|topaz|starlight"),
    ("storyboard", r"storyboard|3d-to-video|viewport|brouillon|draft|\b(?:fast|mini|lite|turbo|flash|preview)\b"),
]
def stages_for(m, kind):
    import re
    txt = " ".join((m.get("edit_functions") or []) + [m.get("variant") or "", m.get("family") or ""]).lower()
    S = set()
    if kind == "video":
        S.add("tournage")
        if (m.get("outputs") or {}).get("lip_sync"): S.add("effets")
        if (m.get("outputs") or {}).get("native_audio") or re.search(r"texte vers audio|musique|doublage", txt): S.add("son")
        if (m.get("inputs") or {}).get("input_3d"): S.add("storyboard")
        for st, rx in STAGE_RE:
            if re.search(rx, txt): S.add(st)
    elif kind == "image":
        S.add("storyboard")
        if (m.get("inputs") or {}).get("image_edit"): S.add("effets")
        for st, rx in STAGE_RE:
            if st in ("effets", "etalonnage", "agrandissement") and re.search(rx, txt): S.add(st)
    elif kind == "audio":
        S.add("son")
        t = m.get("task") or ""
        if t == "stt": S |= {"ecriture", "montage"}
        if t in ("lip_sync", "dubbing"): S.add("effets")
    elif kind == "threed":
        S.add("storyboard")
        if (m.get("task") or "") in ("depth_and_camera", "scene_reconstruction"): S.add("effets")
    ov = stages.get("model_overrides", {})
    S |= set(ov.get("add", {}).get(m["id"], []))
    S -= set(ov.get("remove", {}).get(m["id"], []))
    order = [s["id"] for s in stages.get("stages", [])]
    return [s for s in order if s in S]
for kind, L in (("video", video), ("image", image), ("audio", audio), ("threed", threed)):
    for m in L:
        m["_stages"] = stages_for(m, kind)
pids = {p["id"] for p in platforms}
for st, L in stages.get("platforms", {}).items():
    for pid in L:
        if pid not in pids:
            print(f"étape {st} : plateforme inconnue {pid}, ignorée")
TYPE_BILLING = {"abonnement": "abonnement", "editeur (abonnement)": "abonnement", "agregateur": "paiement à l'usage",
                "revendeur": "paiement à l'usage", "inference": "paiement à l'usage", "gpu-cloud": "location de GPU à l'heure"}
for p in platforms:
    if not p.get("offer") and TYPE_BILLING.get(p.get("type")):
        p["_offer"] = {"billing": TYPE_BILLING[p["type"]], "derived": True}
    else:
        p["_offer"] = p.get("offer") or {}
for p in platforms:
    p["_stages"] = [s["id"] for s in stages.get("stages", []) if p["id"] in stages.get("platforms", {}).get(s["id"], [])]

data = {"stages": stages, "video": video, "image": image, "audio": audio, "threed": threed, "platforms": platforms, "rank_sources": rank.get("sources", {}), "gpu": gpu, "prices": [dict(p, atlas_id=alias.get(p.get("model_id"), p.get("model_id"))) for p in prices],
        "orphans": sorted({p.get("model_id") for p in prices} - {m["id"] for m in video + image} - set(alias)),
        "built": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}

tpl = (ROOT / "scripts" / "atlas_template.tpl").read_text()
out = pathlib.Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else ROOT / "site" / "index.html"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(tpl.replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")))
print(f"{out} : {len(video)} video, {len(image)} image, {len(prices)} prix, {len(data['orphans'])} prix sans modele")
