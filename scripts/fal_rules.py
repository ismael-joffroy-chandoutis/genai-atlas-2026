"""Règles de normalisation des endpoints fal vers les ids canoniques et les colonnes du schéma.

L'API fal /v1/models/pricing ne rend qu'un prix unitaire (unit_price + unit) par endpoint, sans résolution.
- unit "seconds" / "second" : prix par seconde ; la résolution n'est pas donnée par l'API, donc les colonnes
  restent null sauf si l'endpoint porte la résolution dans son nom. Le prix est toujours dans raw et dans
  le champ additionnel price_usd_unit.
- unit "1000 tokens" (Seedance) : converti en $/s par tokens = l x h x 24 x durée / 1024.
- unit "images" / "image" : $/image. "megapixels" : $/image pour 1 MP (1024x1024), noté dans raw.
"""
import re

TASKS = {"text-to-video", "image-to-video", "reference-to-video", "video-to-video", "text-to-image",
         "image-to-image", "edit", "first-last-frame-to-video", "start-end-to-video", "multi-image-to-video",
         "extend", "extend-video", "video-edit", "i2v", "t2v", "edit-image", "image-edit", "remix",
         "reference", "references", "elements", "multi-reference", "keyframes", "lipsync", "audio-to-video",
         "multiconditioning", "effects", "inpaint", "outpaint", "text-to-video-with-audio", "frames-to-video"}
VARIANTS = {"standard": "std", "std": "std", "pro": "pro", "master": "master", "fast": "fast", "turbo": "turbo",
            "lite": "lite", "max": "max", "ultra": "ultra", "flex": "flex", "dev": "dev", "schnell": "schnell"}
RES_WH = {"480p": (864, 480), "720p": (1280, 720), "1080p": (1920, 1080)}
TOKEN_RES = {  # résolutions proposées par modèle (d'après la liste OpenRouter du même jour)
    "bytedance-seedance-2-5": ("480p", "720p"),
    "bytedance-seedance-2-0-fast": ("480p", "720p"),
    "bytedance-seedance-2-0-mini": ("480p", "720p"),
    "bytedance-seedance-2-0": ("480p", "720p", "1080p"),
    "bytedance-seedance-1-5-pro": ("480p", "720p", "1080p"),
}
VENDORS = {"fal-ai": None, "bytedance": "bytedance", "minimax": "minimax", "google": "google", "openai": "openai",
           "alibaba": "alibaba", "xai": "xai", "x-ai": "xai", "kling-video": "kling", "kwaivgi": "kling",
           "black-forest-labs": "bfl",
           "bfl": "bfl", "recraft": "recraft", "ideogram": "ideogram", "runway": "runway", "pixverse": "pixverse",
           "luma-dream-machine": "luma", "decart": "decart", "heygen": "heygen", "krea": "krea",
           "blackforestlabs": "bfl", "lightricks": "ltx", "vidu": "vidu"}


def _v(s):
    s = s.lower()
    s = re.sub(r"(\d+)\.(\d+)", r"\1-\2", s)
    s = re.sub(r"(\d+)\.(\d+)", r"\1-\2", s)
    s = re.sub(r"^v(\d)", r"\1", s)
    return s


def endpoint_to_id(ep):
    parts = [p for p in ep.split("/") if p]
    if parts and parts[0] == "fal-ai":
        parts = parts[1:]
    res = None
    keep = [parts[0]]
    for p in parts[1:]:
        if re.fullmatch(r"\d{3,4}p", p):
            res = p
        elif p in TASKS or p in ("us", "eu"):
            continue
        else:
            keep.append(p)
    parts = keep
    head = parts[0]
    vendor = VENDORS.get(head)
    if head.startswith("kling"):
        vendor = "kling"
    elif head.startswith("veo"):
        vendor = "google"
    elif head.startswith("wan"):
        vendor = "alibaba"
    elif head.startswith("flux"):
        vendor = "bfl"
    elif head.startswith(("ltx",)):
        vendor = "ltx"
    elif head.startswith(("seedance", "seedream")):
        vendor = "bytedance"
    elif head.startswith(("minimax", "hailuo")):
        vendor = "minimax"
    elif head.startswith(("nano-banana", "gemini", "imagen")):
        vendor = "google"
    elif head.startswith(("gpt-image", "sora")):
        vendor = "openai"
    elif head.startswith("qwen"):
        vendor = "alibaba"
    elif head.startswith("grok"):
        vendor = "xai"
    if vendor and head in VENDORS and len(parts) > 1:
        parts = parts[1:]
    name = "-".join(_v(p) for p in parts)
    name = re.sub(r"^kling-video-", "", name)
    name = re.sub(r"^(minimax-|bytedance-|google-|openai-|alibaba-|xai-)", "", name)
    name = name.replace("standard", "std")
    name = re.sub(r"-v(\d)", r"-\1", name)
    mid = f"{vendor}-{name}" if vendor and not name.startswith(vendor) else name
    if vendor == "kling":
        mid = re.sub(r"^kling-kling-", "kling-", mid)
    mid = re.sub(r"-+", "-", mid).strip("-")
    for pat, rep in FIXES:
        mid = re.sub(pat, rep, mid)
    return mid, res


# Harmonisation avec les ids des autres sources
FIXES = [
    (r"^ltx-ltx-", "ltx-"),
    (r"^bfl-flux-3$", "bfl-flux-3"),
    (r"^(kling-(?:image-)?)(\d)(?=-[a-z]|$)", r"\g<1>\2-0"),
    (r"^bytedance-seedream-(\d)(?=-[a-z]|$)", r"bytedance-seedream-\1-0"),
    (r"^ideogram-(\d)(?=-[a-z]|$)", r"ideogram-\1-0"),
    (r"^google-veo(\d)(-|$)", r"google-veo-\1\2"),
    (r"^alibaba-wan-(\d)(\d)(-|$)", r"alibaba-wan-\1-\2\3"),
    (r"^google-gemini-25-flash-image$", "google-nano-banana"),
    (r"^google-gemini-3-pro-image-preview$", "google-gemini-3-pro-image"),
    (r"^google-nano-banana-pro$", "google-gemini-3-pro-image"),
    (r"^google-gemini-3-1-flash-image-preview$", "google-gemini-3-1-flash-image"),
    (r"^google-gemini-omni-flash-1-1$", "google-gemini-omni-1-1-flash"),
    (r"^recraft-(\d)", r"recraft-v\1"),
    (r"^alibaba-happy-horse", "alibaba-happyhorse"),
    (r"^bfl-flux-pro-", "bfl-flux-"),
    (r"^pixverse-(\d)", r"pixverse-v\1"),
]

# Endpoints utilitaires exclus de prices.json (ils restent dans data/raw/fal-*.json)
UTILITY = re.compile(r"lora|upscal|avatar|lipsync|lip-sync|redux|inpaint|outpaint|remove|effects|motion-control|"
                     r"vectoriz|reframe|background|tryon|try-on|swap|sound|transition|enhanc|layer|depth|pose|canny|"
                     r"fill|trainer|segment|caption|matting|relight|recast|camera-controls|insert-video|styles|"
                     r"3d-to-video|vace|subject|pulid|srpo|template|action")


# Familles gardées même quand le modèle n'existe que chez fal (sinon : seulement les ids déjà vus ailleurs)
KEEP_FAL_ONLY = re.compile(r"^(kling-|minimax-|google-|openai-|bytedance-seedance|bytedance-seedream|alibaba-wan|"
                           r"alibaba-happyhorse|alibaba-qwen-image|bfl-flux|ltx-2|pixverse-v|vidu-q|xai-|runway-|luma-|"
                           r"krea-|ideogram-[234]|recraft-v4|hidream|z-image|moonvalley-marey|pika-2|tencent-|"
                           r"hunyuan-video-1-5|bria-fibo-gen|longcat-video|kandinsky6)")


def fal_rules(e):
    pr = e["price"]
    mid, res = endpoint_to_id(e["endpoint_id"])
    if UTILITY.search(e["endpoint_id"]):
        return None, None, None
    m3 = re.match(r"^bfl-flux-3(-draft)?$", mid)
    if m3:
        mid = "bfl-flux-3-" + ("video" if "video" in (e.get("category") or "") else "image") + (m3.group(1) or "")
    unit = (pr.get("unit") or "").lower()
    p = float(pr["unit_price"])
    cols = {"_note": ""}
    if unit in ("second", "seconds"):
        u = "per_second"
        if res in RES_WH:
            cols[f"price_usd_{res}_s"] = p
            cols["_note"] = f"résolution {res} portée par l'endpoint"
        else:
            cols["_note"] = "prix par seconde, résolution non précisée par l'API (colonnes null)"
    elif "token" in unit:
        u = "per_token"
        per_tok = p / (1_000_000 if unit.startswith("1m") else 1000 if unit.startswith("1000") else 1)
        notes = []
        for r in TOKEN_RES.get(mid, ()):
            w, h = RES_WH[r]
            v = per_tok * w * h * 24 / 1024
            cols[f"price_usd_{r}_s"] = v
            notes.append(f"{r}: {per_tok:g} $/token x {w}x{h}x24/1024 = {v:.4f} $/s")
        cols["_note"] = "conversion: " + "; ".join(notes) if notes else "prix au token, résolutions du modèle inconnues"
    elif unit in ("image", "images"):
        u = "per_image"
        cols["price_usd_per_image"] = p
    elif unit in ("megapixel", "megapixels", "processed megapixels") and "video" in (e.get("category") or ""):
        u = "per_second"
        cols["_note"] = "vidéo facturée au mégapixel traité : pas de conversion en $/s"
    elif unit in ("megapixel", "megapixels", "processed megapixels"):
        u = "per_image"
        cols["price_usd_per_image"] = p
        cols["_note"] = "facturé au mégapixel : colonne = image de 1 MP (1024x1024)"
    elif unit in ("video", "videos"):
        u = "per_second"
        cols["_note"] = "prix par vidéo, durée non donnée par l'API (colonnes null)"
    else:
        u = "per_second" if "video" in (e.get("category") or "") else "per_image"
        cols["_note"] = f"unité non convertie ({unit})"
    cols["_unit_price"] = p
    return mid, u, cols
