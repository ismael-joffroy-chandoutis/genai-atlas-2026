#!/usr/bin/env python3
"""Writes TABLES.md (readable on GitHub) from data/*.json.
Usage: python3 scripts/export_tables.py"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / "data"
load = lambda n, d: json.loads((D / n).read_text()) if (D / n).exists() else d
video, image = load("video-models.json", []), load("image-models.json", [])
prices, alias, local = load("prices.json", []), load("model-id-aliases.json", {}), load("local-runs.json", {})
integ = load("integrations.json", {}).get("by_id", {})
def ints(mid):
    i = integ.get(mid, {}); L = []
    if i.get("comfyui_local"): L.append("ComfyUI")
    if i.get("wan2gp"): L.append("Wan2GP")
    if i.get("pinokio"): L.append("Pinokio")
    for k, nm in (("drawthings", "Draw Things"), ("maestro", "Maestro"), ("phosphene", "Phosphene")):
        if i.get(k) is True: L.append(nm)
    return ", ".join(L) or "–"

import re
_cl = ROOT / "CHANGELOG.md"
_vm = re.search(r"^## (v[0-9.]+) · (\d{2})/(\d{2})/(\d{4})", _cl.read_text(), re.M) if _cl.exists() else None
MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]
asof = f"Version {_vm.group(1)}, data as of {int(_vm.group(2))} {MONTHS[int(_vm.group(3))-1]} {_vm.group(4)}." if _vm else "Data as of 15 October 2026."
best = {}
for p in prices:
    if p.get("unit") == "subscription":
        continue
    mid = alias.get(p.get("model_id"), p.get("model_id"))
    for k in ("price_usd_480p_s", "price_usd_720p_s", "price_usd_1080p_s", "price_usd_per_image"):
        v = p.get(k)
        if isinstance(v, (int, float)) and v > 0:
            cur = best.setdefault(mid, {}).get(k)
            if cur is None or v < cur[0]:
                best[mid][k] = (v, p.get("platform"))

g = lambda o, path: __import__("functools").reduce(lambda a, k: a.get(k) if isinstance(a, dict) else None, path.split("."), o)
def yn(v): return "yes" if v is True else ("no" if v is False else "?")
def num(v): return "?" if v is None else str(v)
def money(mid, k):
    b = best.get(mid, {}).get(k)
    return "" if not b else f"{b[0]:.3f} ({b[1]})"
def dur(m):
    a, b = g(m, "outputs.min_s"), g(m, "outputs.max_s")
    return "?" if a is None and b is None else f"{num(a)}–{num(b)} s"
def refs(m, n, s):
    v, t = g(m, n), g(m, s)
    return "?" if v is None else (f"{v} ({t} s)" if t else str(v))

out = ["# Tables", "", "Generated from `data/*.json` by `scripts/export_tables.py`. " + asof + " "
       "`?` = not documented. Prices: cheapest pay-per-use price found, in USD per second of video or per image, with the platform. "
       "Local columns: RTX 5090 32 GB, RTX 4090 24 GB, Mac M5 Max 128 GB. \"Integrated in\" = the model ships in the official ComfyUI templates (local, not API nodes), in Wan2GP, Pinokio, Draw Things, Maestro or Phosphene. Notes inside the JSON files are in French.", ""]
out += ["## Video", "", "| Model | Vendor | Open weights | Duration | Max res | Audio | Image refs | Video refs | Audio refs | First / last frame | Keyframes | LoRA | 5090 | 4090 | Mac 128 GB | AA T2V | AA I2V | Integrated in | Cheapest 720p $/s |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
for m in sorted(video, key=lambda m: (m["family"], m["variant"])):
    L = local.get(m["id"], {})
    out.append("| " + " | ".join([
        f"{m['family']} · {m['variant']}", m.get("vendor") or "?", yn(g(m, "access.open_weights")), dur(m),
        num(g(m, "outputs.max_resolution")), yn(g(m, "outputs.native_audio")),
        num(g(m, "inputs.image_refs_max")), refs(m, "inputs.video_refs_max", "inputs.video_refs_total_s"),
        refs(m, "inputs.audio_refs_max", "inputs.audio_refs_total_s"),
        f"{yn(g(m, 'inputs.first_frame'))} / {yn(g(m, 'inputs.last_frame'))}", num(g(m, "inputs.keyframes_max")),
        yn(g(m, "inputs.lora_inference")), yn(g(m, "local.runs_on_rtx5090_32gb")), yn(L.get("rtx4090_24gb")), yn(L.get("mac_m5max_128gb")),
        num(g(m, "ranking.aa_text_to_video")), num(g(m, "ranking.aa_image_to_video")), ints(m["id"]), money(m["id"], "price_usd_720p_s"),
    ]).replace("\n", " ") + " |")
out += ["", "## Image", "", "| Model | Vendor | Open weights | License | Max res | Image refs | Edit | LoRA | 5090 | 4090 | Mac 128 GB | AA T2I | AA edit | Integrated in | Cheapest $/image |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
for m in sorted(image, key=lambda m: (m["family"], m["variant"])):
    L = local.get(m["id"], {})
    out.append("| " + " | ".join([
        f"{m['family']} · {m['variant']}", m.get("vendor") or "?", yn(g(m, "access.open_weights")),
        (g(m, "access.license") or "?").replace("|", "/"), num(g(m, "outputs.max_resolution")),
        num(g(m, "inputs.image_refs_max")), yn(g(m, "inputs.image_edit")), yn(g(m, "inputs.lora_inference")),
        yn(g(m, "local.runs_on_rtx5090_32gb")), yn(L.get("rtx4090_24gb")), yn(L.get("mac_m5max_128gb")),
        num(g(m, "ranking.aa_text_to_image")), num(g(m, "ranking.aa_image_edit")), ints(m["id"]), money(m["id"], "price_usd_per_image"),
    ]).replace("\n", " ") + " |")
(ROOT / "TABLES.md").write_text("\n".join(out) + "\n")
print("TABLES.md :", len(video), "video,", len(image), "image")
