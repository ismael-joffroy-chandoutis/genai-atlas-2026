#!/usr/bin/env python3
"""Fusionne les relevés bruts data/raw/*-<date>.json en data/prices.json (schéma « prices » de SCHEMA.md).

- fal, openrouter : relevés API (verified = api_live), normalisés ici.
- autres sources : fichiers déjà au format {"rows": [...]} (pages officielles ou tiers), repris tels quels
  après normalisation de l'id.
Écrit aussi data/model-ids.txt (ids utilisés, triés).

Usage : python3 scripts/merge-prices.py [--date 2026-10-15]
"""
import json, re, sys, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
DATE = sys.argv[sys.argv.index("--date") + 1] if "--date" in sys.argv else "2026-10-15"

# Résolutions 16:9 utilisées pour convertir les prix au token Seedance en $/s.
# Formule ByteDance : tokens = largeur x hauteur x 24 (fps) x durée / 1024.
RES_WH = {"480p": (864, 480), "720p": (1280, 720), "1080p": (1920, 1080)}
COLS = {"480p": "price_usd_480p_s", "720p": "price_usd_720p_s", "1080p": "price_usd_1080p_s"}

# ---------------------------------------------------------------- ids
VERSION_RE = re.compile(r"(\d+)\.(\d+)")


def kebab(s):
    s = s.lower().replace("_", "-").replace(" ", "-")
    s = VERSION_RE.sub(lambda m: f"{m.group(1)}-{m.group(2)}", s)
    s = VERSION_RE.sub(lambda m: f"{m.group(1)}-{m.group(2)}", s)
    s = re.sub(r"[^a-z0-9-]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")


VENDOR_PREFIX = {
    "x-ai": "xai", "xai": "xai", "kwaivgi": "kling", "kling": "kling", "black-forest-labs": "bfl", "bfl": "bfl",
    "bytedance-seed": "bytedance", "bytedance": "bytedance", "google": "google", "openai": "openai",
    "alibaba": "alibaba", "qwen": "alibaba", "minimax": "minimax", "runway": "runway", "heygen": "heygen",
    "recraft": "recraft", "krea": "krea", "microsoft": "microsoft", "meta": "meta", "tencent": "tencent",
    "sourceful": "sourceful", "lightricks": "ltx", "ltx": "ltx", "wan": "alibaba", "ideogram": "ideogram",
}

# Corrections explicites (après kebab) : forme brute -> id canonique
ALIASES = {
    "minimax-hailuo-3-max": "minimax-h3-max",
    "minimax-hailuo-3": "minimax-h3",
    "kling-v3-0-pro": "kling-3-0-pro",
    "kling-v3-0-std": "kling-3-0-std",
    "kling-video-o1": "kling-o1",
    "bytedance-seedance-1-5-pro": "bytedance-seedance-1-5-pro",
    "bytedance-seedream-5-0-flash": "bytedance-seedream-5-0-flash",
    "google-gemini-nano-banana-2-1": "google-nano-banana-2-1",
    "google-gemini-2-5-flash-image": "google-nano-banana",
    "google-gemini-3-pro-image-preview": "google-gemini-3-pro-image",
    "google-gemini-3-1-flash-image-preview": "google-gemini-3-1-flash-image",
    "bfl-flux-2-klein-4b": "bfl-flux-2-klein-4b",
    "alibaba-qwen-image-3": "alibaba-qwen-image-3",
}


def canon(raw_id):
    """'x-ai/grok-imagine-video-1.5' -> 'xai-grok-imagine-video-1-5'."""
    parts = raw_id.split("/")
    vendor = VENDOR_PREFIX.get(parts[0], parts[0])
    rest = kebab("-".join(parts[1:])) if len(parts) > 1 else ""
    # retirer un doublon de vendeur en tête du nom
    for pre in (vendor + "-", parts[0] + "-"):
        if rest.startswith(pre):
            rest = rest[len(pre):]
    cid = kebab(f"{vendor}-{rest}") if rest else kebab(vendor)
    return ALIASES.get(cid, cid)


# ---------------------------------------------------------------- lignes
def row(model_id, platform, endpoint, unit, raw, url, verified, modality, **cols):
    r = {"model_id": model_id, "platform": platform, "endpoint": endpoint, "unit": unit,
         "price_usd_480p_s": None, "price_usd_720p_s": None, "price_usd_1080p_s": None,
         "price_usd_per_image": None, "raw": raw, "retrieved_at": DATE, "source_url": url,
         "verified": verified, "modality": modality}
    for k, v in cols.items():
        r[k] = None if v is None else round(float(v), 6)
    return r


# ---------------------------------------------------------------- OpenRouter
OR_TOKENS_PER_IMAGE = {
    # BFL facture au mégapixel ; OpenRouter exprime 1 MP = 4096 tokens (0,03 $/MP FLUX.2 pro = 7,32421875e-6 $/token).
    "Other-bfl": 4096,
    # Autres modèles au tokenizer Media/Other : 4175 tokens = 1 image. Facteur déduit : il reproduit exactement les prix
    # officiels Recraft V4 (0,04 $), Recraft V4 Pro (0,25 $), Seedream 4.5 (0,04 $).
    "default": 4175,
}


def or_video(m, url):
    sk = {k: float(v) for k, v in (m.get("pricing_skus") or {}).items()}
    sup = m.get("supported_resolutions")
    cols, notes = {}, []
    is_tok = any(k.startswith("video_tokens") for k in sk)
    for res in ("480p", "720p", "1080p"):
        allowed = sup is None or res in sup or (res == "720p" and "768p" in sup)
        v = None
        if is_tok:
            p = sk.get(f"video_tokens_{res}") or sk.get("video_tokens_without_audio") or sk.get("video_tokens")
            if p and (sup is None or res in sup):
                w, h = RES_WH[res]
                v = p * w * h * 24 / 1024
                notes.append(f"{res}: {p} $/token x {w}x{h}x24/1024 = {v:.4f} $/s")
        else:
            for k in (f"duration_seconds_without_audio_{res}", f"duration_seconds_{res}",
                      f"text_to_video_duration_seconds_{res}"):
                if k in sk:
                    v = sk[k]; break
            if v is None:
                for k in (f"cents_per_video_output_second_{res}", f"cents_per_second_output_{res}"):
                    if k in sk:
                        v = sk[k] / 100; break
            if v is None and res == "720p" and "duration_seconds_768p" in sk:
                v = sk["duration_seconds_768p"]; notes.append("768p mis en colonne 720p")
            if v is None and allowed:
                for k in ("duration_seconds_without_audio", "duration_seconds"):
                    if k in sk:
                        v = sk[k]; break
                if v is None and "cents_per_second_output" in sk:
                    v = sk["cents_per_second_output"] / 100
        if v is not None:
            cols[COLS[res]] = v
    raw = f"pricing_skus={json.dumps(m.get('pricing_skus'))}; résolutions={sup}"
    if notes:
        raw += "; conversion: " + "; ".join(notes)
    if any(k for k in sk if "audio" in k):
        raw += "; colonnes = prix sans audio quand les deux existent"
    unit = "per_token" if is_tok else "per_second"
    return row(canon(m["id"]), "openrouter", m["id"], unit, raw, url, "api_live", "video", **cols)


def or_image(m, url):
    pr = {k: float(v) for k, v in (m.get("pricing") or {}).items() if v not in (None, "")}
    tok = m.get("architecture", {}).get("tokenizer")
    raw = f"pricing={json.dumps(m.get('pricing'))}; tokenizer={tok}"
    per_image = None
    out = pr.get("image_output")
    if out and out > 0 and tok in ("Media", "Other"):
        n = OR_TOKENS_PER_IMAGE["Other-bfl"] if m["id"].startswith("black-forest-labs/") else OR_TOKENS_PER_IMAGE["default"]
        per_image = out * n
        raw += f"; conversion: {out} $/token x {n} tokens = {per_image:.4f} $/image" + (" (1 MP)" if n == 4096 else "")
    elif out:
        raw += "; $/image non calculé (nombre de tokens par image dépend de la qualité/résolution chez ce fournisseur)"
    return row(canon(m["id"]), "openrouter", m["id"], "per_token", raw, url, "api_live", "image", price_usd_per_image=per_image)


def load_openrouter():
    p = RAW / f"openrouter-{DATE}.json"
    if not p.exists():
        return []
    d = json.loads(p.read_text())
    rows = [or_video(m, "https://openrouter.ai/api/v1/videos/models") for m in d["video_models"]]
    rows += [or_image(m, "https://openrouter.ai/api/v1/models?output_modalities=image")
             for m in d["image_models"] if not m["id"].startswith("openrouter/")]
    return rows


# ---------------------------------------------------------------- fal
RES_A = re.compile(r"(\d{3,4})p([^$]{0,80}?)\$(\d*\.?\d+)")
RES_B = re.compile(r"\$(\d*\.?\d+)\s*(?:per second\s*)?(?:at\s*|for\s*)?(\d{3,4})p")
RES_COL = {"480": "price_usd_480p_s", "720": "price_usd_720p_s", "768": "price_usd_720p_s", "1080": "price_usd_1080p_s"}


def parse_fal_page(text):
    """Extrait des $/s par résolution du texte de prix d'une page fal. Première occurrence par résolution.
    Ordre « prix puis résolution » si le premier $ précède la première résolution, sinon l'inverse."""
    cols = {}
    if not text or not re.search(r"per second|every second|/second|second of|per-second|/s\b", text):
        return cols  # prix par vidéo (« 5 second video ») : pas de conversion ici
    first_d, m_res = text.find("$"), re.search(r"\d{3,4}p", text)
    if first_d == -1 or not m_res:
        return cols
    if first_d < m_res.start():
        for m in RES_B.finditer(text):
            c = RES_COL.get(m.group(2))
            if c and c not in cols and "token" not in text[m.end():m.end() + 15]:
                cols[c] = float(m.group(1))
    else:
        for m in RES_A.finditer(text):
            c = RES_COL.get(m.group(1))
            after = text[m.end():m.end() + 15]
            if c and c not in cols and ("second" in m.group(2) or "second" in after) \
                    and "token" not in m.group(2) and "token" not in after:
                cols[c] = float(m.group(3))
    return cols


def load_fal():
    p = RAW / f"fal-{DATE}.json"
    if not p.exists():
        return []
    d = json.loads(p.read_text())
    pp = RAW / f"fal-pages-{DATE}.json"
    pages = json.loads(pp.read_text()) if pp.exists() else {}
    rows = []
    for e in d["endpoints"]:
        pr = e.get("price")
        if not pr:
            continue
        mid, unit, cols = fal_rules(e)
        if mid is None:
            continue
        unit_price = cols.pop("_unit_price")
        rows.append(row(mid, "fal", e["endpoint_id"], unit,
                        f"unit_price={pr['unit_price']} {pr['currency']} / {pr['unit']}; catégorie={e['category']}; "
                        + cols.pop("_note", ""),
                        f"https://api.fal.ai/v1/models/pricing?endpoint_id={e['endpoint_id']}", "api_live",
                        "video" if "video" in (e["category"] or "") else "image", **cols))
        rows[-1]["price_usd_unit"] = unit_price
        rows[-1]["unit_api"] = pr["unit"]
        txt = pages.get(e["endpoint_id"])
        if txt:
            r = rows[-1]
            r["raw"] += " | page fal.ai : " + " ".join(txt.split())
            pc = parse_fal_page(txt) if r["modality"] == "video" else {}
            if pc:
                for k in COLS.values():
                    r[k] = round(pc[k], 6) if k in pc else None
                r["raw"] += " | colonnes = prix par seconde lus sur la page (première valeur citée par résolution ; 768p en colonne 720p)"
                r["verified"] = "page"
                r["source_url"] = f"https://fal.ai/models/{e['endpoint_id']}"
    return rows


# règles fal définies dans fal_rules.py pour garder ce fichier lisible
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from fal_rules import fal_rules  # noqa: E402

# ---------------------------------------------------------------- sources « rows »
KNOWN = {"model_name", "model_id", "platform", "endpoint", "modality", "unit", "raw", "source_url", "verified",
         "price_usd_480p_s", "price_usd_720p_s", "price_usd_1080p_s", "price_usd_per_image"}
API_SOURCES = {"fal", "openrouter", "gpu-hour"}


def load_row_sources():
    rows = []
    for p in sorted(RAW.glob(f"*-{DATE}.json")):
        src = p.name[: -len(f"-{DATE}.json")]
        if src in API_SOURCES:
            continue
        d = json.loads(p.read_text())
        for r in d.get("rows", []):
            mid = r.get("model_id") or canon(r.get("model_name", "inconnu"))
            mid = ALIASES.get(kebab(mid), kebab(mid))
            out = row(mid, r.get("platform") or src, r.get("endpoint"), r.get("unit") or "per_second",
                      (r.get("raw") or "") + "".join(f"; {k}={r[k]}" for k in r if k not in KNOWN and r[k] is not None), r.get("source_url") or (d.get("pages") or [None])[0],
                      r.get("verified") or "page", r.get("modality"),
                      **{k: r.get(k) for k in COLS.values()}, price_usd_per_image=r.get("price_usd_per_image"))
            rows.append(out)
    return rows


# Passe finale d'harmonisation des ids entre plateformes (la variante de tâche reste dans "endpoint").
CANON_RULES = [
    (r"^(alibaba-wan-[0-9-]+?)-(i2v|t2v|r2v)(-fast)?$", r"\1\3"),
    (r"-standard$", "-std"),
    (r"-standard-", "-std-"),
    (r"^ideogram-v(\d)$", r"ideogram-\1-0"),
    (r"^ideogram-v(\d)-", r"ideogram-\1-0-"),
    (r"^alibaba-qwen-image-2-0(-pro)?$", r"alibaba-qwen-image-2\1"),
    (r"^alibaba-image-3(-pro)?$", r"alibaba-qwen-image-3\1"),
    (r"^runway-aleph-2-0$", "runway-aleph-2"),
    (r"^xai-grok-imagine-image-2-0$", "xai-grok-imagine-image-2"),
    (r"^minimax-h3-ws-native$", "minimax-h3"),
    (r"^bfl-flux-1-1$", "bfl-flux-1-1-pro"),
    (r"^bfl-flux-1-1-ultra$", "bfl-flux-1-1-pro-ultra"),
    (r"^bfl-flux-kontext-max$", "bfl-flux-1-kontext-max"),
    (r"^bfl-flux-kontext$", "bfl-flux-1-kontext-pro"),
    (r"^kling-(3|o3)-4k$", lambda m: "kling-3-0-4k" if m.group(1) == "3" else "kling-o3-4k"),
]


def canon_final(mid):
    for pat, rep in CANON_RULES:
        mid = re.sub(pat, rep, mid)
    return mid


def main():
    other = load_openrouter() + load_row_sources()
    for r in other:
        r["model_id"] = canon_final(r["model_id"])
    seen_ids = {r["model_id"] for r in other}
    from fal_rules import KEEP_FAL_ONLY
    fal = []
    for r in load_fal():
        r["model_id"] = canon_final(r["model_id"])
        if r["model_id"] in seen_ids or (KEEP_FAL_ONLY.search(r["model_id"])
                                         and not re.search(r"ltx-2-3-quality-|retake|reference-video", r["model_id"])):
            fal.append(r)
    rows = fal + other
    seen, uniq = set(), []
    for r in rows:
        k = (r["model_id"], r["platform"], r["endpoint"], r["raw"])
        if k not in seen:
            seen.add(k); uniq.append(r)
    uniq.sort(key=lambda r: (r["modality"] or "", r["model_id"], r["platform"], r["endpoint"] or ""))
    (ROOT / "data" / "prices.json").write_text(json.dumps(uniq, indent=1, ensure_ascii=False))
    ids = sorted({r["model_id"] for r in uniq})
    (ROOT / "data" / "model-ids.txt").write_text("\n".join(ids) + "\n")
    c = collections.Counter(r["platform"] for r in uniq)
    print(f"{len(uniq)} lignes, {len(ids)} ids")
    for k, v in c.most_common():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
