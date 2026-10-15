#!/usr/bin/env python3
"""Builds data/integrations.json: in which local tools each atlas model is integrated.
Reads data/raw/integrations/comfy-index.json (ComfyUI official templates index),
data/raw/integrations/wan2gp/*.json (Wan2GP model definitions) and, if present,
data/raw/integrations/web.json (Pinokio, Draw Things, Maestro, Phosphene)."""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "integrations"
ids = set()
for f in ("video-models.json", "image-models.json", "audio-models.json", "3d-models.json"):
    p = ROOT / "data" / f
    if p.exists():
        ids |= {m["id"] for m in json.loads(p.read_text())}

# ComfyUI template title (regex) -> atlas ids. Ordered from specific to general; first match wins per template.
COMFY = [
    (r"FastH3", ["minimax-fasth3-v2-8-etapes"]),
    (r"H3 Max Turbo|H3 Turbo", ["minimax-h3-max-turbo"]),
    (r"H3 Max", ["minimax-h3-max"]),
    (r"H3 Fun ControlNet", ["minimax-h3-fun-controlnet-union"]),
    (r"MiniMax H3.*(Reference|Multiframe)", ["minimax-h3-ref2va-33b", "minimax-h3-pruned-20b-ref2va"]),
    (r"MiniMax H3|^Image to Video\s*$", ["minimax-h3-fl2va-33b", "minimax-h3-pruned-20b-fl2va"]),
    (r"Seedance ?2\.5", ["seedance-2-5"]), (r"Seedance ?2\.0 ?Mini|Seedance 2 Mini", ["seedance-2-0-mini"]),
    (r"Seedance ?2\.0 ?Fast", ["seedance-2-0-fast"]), (r"Seedance ?2\.0|Seedance 2:", ["seedance-2-0"]),
    (r"LTX-?2\.5.*Layout", ["ltx-2-5-ic-lora-layout-to-render"]), (r"LTX-?2\.5", ["ltx-2-5-dev", "ltx-2-5-distilled"]),
    (r"LTX-?2\.3", ["ltx-2-3-open-weights"]),
    (r"Wan ?2\.2.*(Animate)", ["wan-2-2-animate-2"]), (r"Wan ?2\.2.*S2V", ["wan-2-2-s2v-14b"]), (r"Wan ?2\.2.*(5B|TI2V)", ["wan-2-2-ti2v-5b"]),
    (r"Wan ?2\.2.*(VACE|Fun)", ["wan-2-2-vace-fun-a14b"]), (r"Wan ?2\.2", ["wan-2-2-a14b"]),
    (r"Wan ?3\.0 Prime", ["wan-3-0-prime"]), (r"Wan ?3\.0|Wan3", ["wan-3-0"]), (r"Wan ?2\.7", ["wan-2-7"]), (r"Wan ?2\.6", ["wan-2-6"]),
    (r"Kling O3|Kling 3\.0 Omni", ["kling-3-0-omni-pro", "kling-3-0-omni-std"]), (r"Kling 3\.0.*Motion", ["kling-3-0-motion-control"]),
    (r"Kling 3\.0", ["kling-3-0-pro", "kling-3-0-std"]), (r"Kling O1", ["kling-o1-pro"]), (r"Kling 2\.6", ["kling-2-6-pro", "kling-2-6-std"]),
    (r"Kling 2\.5", ["kling-2-5-turbo-pro"]), (r"Kling 4", ["kling-4-0"]),
    (r"Omni 1\.1 Flash|Omni Flash 1\.1", ["google-gemini-omni-flash-1-1"]), (r"Omni Flash|Gemini Omni", ["google-gemini-omni-flash-1-0"]),
    (r"Veo ?3\.1 Fast", ["google-veo-3-1-fast"]), (r"Veo ?3\.1 Lite", ["google-veo-3-1-lite"]), (r"Veo ?3\.1", ["google-veo-3-1"]),
    (r"Vidu Q3", ["vidu-q3-pro"]), (r"Vidu Q2", ["vidu-q2-pro"]), (r"Vidu Q4", ["vidu-q4-preview"]),
    (r"HappyHorse", ["happyhorse-1-0"]), (r"Hunyuan ?Video ?1\.5|HunyuanVideo 1\.5", ["hunyuanvideo-1-5"]),
    (r"Grok Imagine.*Image", ["xai-grok-imagine-image"]), (r"Grok", ["xai-grok-imagine-1-5"]),
    (r"Luma Ray ?3\.2|Ray3\.2", ["luma-ray-3-2"]), (r"Ray ?3", ["luma-ray-3"]),
    (r"FLUX ?3.*Video|Flux 3.*Video", ["bfl-flux-3-video"]),
    (r"Nano Banana Pro|Gemini 3 Pro Image|Gemini3 Pro Image", ["google-nano-banana-pro"]), (r"Nano Banana 2", ["google-nano-banana-2"]), (r"Nano Banana", ["google-nano-banana"]),
    (r"Z-Image.*Base", ["alibaba-z-image-base"]), (r"Z-Image", ["alibaba-z-image-turbo"]),
    (r"Flux\.?2.*Klein|FLUX\.2.*klein", ["bfl-flux-2-klein-4b", "bfl-flux-2-klein-9b"]), (r"Flux\.?2.*Dev|FLUX\.2 \[dev\]", ["bfl-flux-2-dev"]),
    (r"Flux\.?2.*Pro|FLUX\.2 \[pro\]", ["bfl-flux-2-pro"]), (r"Kontext.*Dev|Kontext \[dev\]", ["bfl-flux-1-kontext-dev"]), (r"Kontext", ["bfl-flux-1-kontext-pro"]),
    (r"Flux\.?1 Krea|FLUX\.1 Krea", ["bfl-flux-1-krea-dev"]), (r"FLUX ?3|Flux 3", ["bfl-flux-3-image"]),
    (r"Qwen-Image.*2512", ["alibaba-qwen-image-2512"]), (r"Qwen-Image.*2\.1|Qwen Image 2\.1", ["alibaba-qwen-image-2-1"]),
    (r"Qwen-Image-Edit|Qwen Image Edit", ["alibaba-qwen-image-edit-2511"]),
    (r"Krea 2", ["krea-2-turbo", "krea-2-medium", "krea-2-large"]),
    (r"GPT[- ]Image 2\.5", ["openai-gpt-image-2-5-flare", "openai-gpt-image-2-5-sunburst"]), (r"GPT[- ]Image 2", ["openai-gpt-image-2"]), (r"GPT[- ]Image 1\.5", ["openai-gpt-image-1-5"]),
    (r"Seedream 5\.0 Pro|Seedream 5 Pro", ["bytedance-seedream-5-0-pro"]), (r"Seedream 5", ["bytedance-seedream-5-0-lite"]), (r"Seedream 4\.5", ["bytedance-seedream-4-5"]), (r"Seedream 4", ["bytedance-seedream-4-0"]),
    (r"Mai Image 2\.6|MAI-Image-2\.6", ["microsoft-mai-image-2-6"]), (r"Ideogram 4|Ideogram V4", ["ideogram-4-0"]), (r"Ideogram 3|Ideogram V3", ["ideogram-3-0"]),
    (r"HiDream", ["hidream-o1-image", "hidream-o1-image-dev"]), (r"SDXL", ["stability-sdxl-1-0"]), (r"SD ?3\.5", ["stability-sd-3-5-large"]),
    (r"Hunyuan ?Image ?3|HunyuanImage 3", ["tencent-hunyuanimage-3-0"]), (r"Recraft", ["recraft-v4-1-utility"]),
]
WAN = [  # Wan2GP definition file name (regex) -> atlas ids
    (r"^minimax_h3_fl2va$", ["minimax-h3-fl2va-33b"]), (r"^minimax_h3_ref2va$", ["minimax-h3-ref2va-33b"]),
    (r"^minimax_h3_fl2va_pruned$", ["minimax-h3-pruned-20b-fl2va"]), (r"^minimax_h3_ref2va_pruned$", ["minimax-h3-pruned-20b-ref2va"]),
    (r"^minimax_h3_.*_pdd$", ["minimax-h3-pdd-8-etapes"]), (r"^minimax_h3_.*_veda$", ["minimax-h3-veda-sparse"]),
    (r"^minimax_h3_control", ["minimax-h3-fun-controlnet-union"]), (r"^minimax_h3_fl2va$", ["minimax-h3-turbo-lora"]),
    (r"^ltx2_25_22B$", ["ltx-2-5-dev"]), (r"^ltx2_25_22B_distilled$", ["ltx-2-5-distilled"]), (r"^ltx2_25_22B_distilled_nvfp4$", ["ltx-2-5-nvfp4-int8"]),
    (r"^ltx2_25_22B_layout_to_render$", ["ltx-2-5-ic-lora-layout-to-render"]), (r"^ltx2_22B", ["ltx-2-3-open-weights"]),
    (r"^(t2v|i2v)_2_2", ["wan-2-2-a14b"]), (r"^ti2v_2_2", ["wan-2-2-ti2v-5b"]), (r"^vace_fun_14B_2_2", ["wan-2-2-vace-fun-a14b"]), (r"^animate2", ["wan-2-2-animate-2"]),
    (r"^hunyuan_1_5", ["hunyuanvideo-1-5"]),
    (r"^flux2_dev", ["bfl-flux-2-dev"]), (r"^flux2_klein_4b", ["bfl-flux-2-klein-4b"]), (r"^flux2_klein_9b", ["bfl-flux-2-klein-9b"]),
    (r"^flux_krea$", ["bfl-flux-1-krea-dev"]), (r"^flux_dev_kontext$", ["bfl-flux-1-kontext-dev"]),
    (r"^qwen_image_21", ["alibaba-qwen-image-2-1"]), (r"^qwen_image_2512", ["alibaba-qwen-image-2512"]),
    (r"^z_image$", ["alibaba-z-image-turbo"]), (r"^z_image_base", ["alibaba-z-image-base"]),
    (r"^krea2_turbo", ["krea-2-turbo"]), (r"^ideogram4", ["ideogram-4-0"]), (r"^hidream_o1$", ["hidream-o1-image"]), (r"^hidream_o1_dev", ["hidream-o1-image-dev"]),
]

API_REDIRECT = {"minimax-h3-fl2va-33b": "minimax-h3-api", "minimax-h3-ref2va-33b": "minimax-h3-api", "minimax-h3-pruned-20b-fl2va": None,
    "minimax-h3-pruned-20b-ref2va": None, "ltx-2-5-dev": "ltx-2-5-pro-api", "ltx-2-5-distilled": "ltx-2-5-fast-api", "ltx-2-3-open-weights": "ltx-2-3-pro-api",
    "wan-2-2-a14b": None, "alibaba-qwen-image-2-1": None}
out = {i: {"comfyui_local": [], "comfyui_api": [], "comfyui_usage": 0, "wan2gp": [], "pinokio": [], "drawthings": None, "maestro": None, "phosphene": None} for i in ids}
idx = json.loads((RAW / "comfy-index.json").read_text())
for cat in idx:
    for t in cat.get("templates", []):
        text = t.get("title", "") + " | " + " ".join(t.get("models") or [])
        for rx, targets in COMFY:
            if re.search(rx, t.get("title", ""), re.I) or re.search(rx, " ".join(t.get("models") or []), re.I):
                for tid in targets:
                    if not t.get("openSource") and tid in API_REDIRECT:
                        tid = API_REDIRECT[tid]
                    if tid in out:
                        out[tid]["comfyui_local" if t.get("openSource") else "comfyui_api"].append(t["name"])
                        out[tid]["comfyui_usage"] += t.get("usage") or 0
                break
for f in sorted((RAW / "wan2gp").glob("*.json")):
    for rx, targets in WAN:
        if re.search(rx, f.stem):
            for tid in targets:
                if tid in out:
                    out[tid]["wan2gp"].append(f.stem)
web = json.loads((RAW / "web.json").read_text()) if (RAW / "web.json").exists() else {}
for tid, w in (web.get("by_id") or {}).items():
    if tid in out:
        out[tid]["pinokio"] = w.get("pinokio") or []
        for k in ("drawthings", "maestro", "phosphene"):
            out[tid][k] = w.get(k)
        if w.get("notes"):
            out[tid]["notes"] = w["notes"]
for v in out.values():
    v["count"] = sum([bool(v["comfyui_local"]), bool(v["wan2gp"]), bool(v["pinokio"]), v["drawthings"] is True, v["maestro"] is True, v["phosphene"] is True])
meta = {"comfyui": "ComfyUI official templates index (comfyui-workflow-templates, read on 2026-10-15)",
        "wan2gp": "Wan2GP v18 model definitions (defaults/, read on 2026-10-15)", "web": web.get("tools")}
(ROOT / "data" / "integrations.json").write_text(json.dumps({"sources": meta, "by_id": out}, ensure_ascii=False, indent=1))
print("integrations:", sum(1 for v in out.values() if v["count"]), "models in at least one local tool /", len(out))
