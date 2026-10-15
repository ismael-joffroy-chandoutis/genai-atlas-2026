#!/usr/bin/env python3
"""Releve des prix GPU a l'heure : RunPod (API GraphQL), Vast.ai (API offres), Modal (page).
stdlib seulement. Aucune cle, aucune location. Sorties :
  data/raw/gpu-hour-<date>.json  (brut)   data/gpu-hour.json (normalise)
"""
import json, os, statistics, sys, urllib.request
from datetime import date

TODAY = "2026-10-15"
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RAW = os.path.join(BASE, "data", "raw", f"gpu-hour-{TODAY}.json")
OUT = os.path.join(BASE, "data", "gpu-hour.json")
# Vast.ai (Cloudflare) renvoie 403 au UA Mozilla et au UA Python-urllib par defaut : UA curl accepte.
UA = {"User-Agent": "curl/8.7.1", "Content-Type": "application/json", "Accept": "*/*"}

# --- RunPod : displayName (API) -> libelle normalise
RUNPOD_GPUS = {"RTX 5090": "RTX 5090", "RTX 4090": "RTX 4090", "L40S": "L40S",
               "H100 SXM": "H100 SXM", "H100 PCIe": "H100 PCIe", "H100 NVL": "H100 NVL",
               "H200 SXM": "H200", "B200": "B200"}
# --- Vast : gpu_name (API) -> libelle normalise
VAST_GPUS = {"RTX 5090": "RTX 5090", "RTX 4090": "RTX 4090", "L40S": "L40S",
             "H100 SXM": "H100 SXM", "H100 PCIE": "H100 PCIe", "H100 NVL": "H100 NVL",
             "H200": "H200", "B200": "B200"}

# --- Modal : valeurs relevees A LA MAIN sur https://modal.com/pricing le 2026-10-15.
# La page affiche des $/seconde (la colonne "par heure" repete a tort la valeur par seconde).
# Heure = seconde x 3600. Modal n'affiche ni RTX 5090 ni RTX 4090.
# gpu: (prix_par_seconde_usd, vram_gb)  VRAM = specs constructeur, pas affichee sur la page.
PAGE_VALUES = {
    "modal": {
        "source_url": "https://modal.com/pricing", "date": "2026-10-15",
        "gpus": {
            "B300": (0.001972, 288), "B200": (0.001736, 180), "H200": (0.001261, 141),
            "H100 SXM": (0.001097, 80), "RTX PRO 6000": (0.000842, 96),
            "A100 80GB": (0.000694, 80), "A100 40GB": (0.000583, 40),
            "L40S": (0.000542, 48), "A10": (0.000306, 24), "L4": (0.000222, 24), "T4": (0.000164, 16),
        },
    }
}

def post(url, payload):
    req = urllib.request.Request(url, json.dumps(payload).encode(), UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def runpod(rows, raw):
    url = "https://api.runpod.io/graphql"
    q = "query { gpuTypes { id displayName memoryInGb securePrice communityPrice } }"
    try:
        d = post(url, {"query": q})["data"]["gpuTypes"]
    except Exception as e:
        raw["runpod_error"] = repr(e); print("RunPod KO", e, file=sys.stderr); return
    raw["runpod"] = d
    for g in d:
        name = RUNPOD_GPUS.get(g["displayName"])
        if not name: continue
        for tier, key in (("secure", "securePrice"), ("community", "communityPrice")):
            p = g.get(key)
            if p:  # 0 ou null = non propose
                rows.append(dict(provider="runpod", gpu=name, vram_gb=g["memoryInGb"], tier=tier,
                    price_usd_hour=p, n_offers=None, raw=f"{g['id']} {key}={p}",
                    retrieved_at=TODAY, source_url=url, verified="api_live"))

def vast(rows, raw):
    url = "https://console.vast.ai/api/v0/bundles/"
    raw["vast"] = {}
    for gname, name in VAST_GPUS.items():
        try:
            offers = post(url, {"gpu_name": {"eq": gname}, "rentable": {"eq": True},
                                "num_gpus": {"eq": 1}, "limit": 1000}).get("offers", [])
        except Exception as e:
            raw["vast"][gname] = {"error": repr(e)}; print("Vast KO", gname, e, file=sys.stderr); continue
        prices = sorted(o["dph_total"] for o in offers if o.get("dph_total"))
        raw["vast"][gname] = {"n": len(prices), "prices": prices}
        if not prices: continue
        vram = round(statistics.median(o["gpu_ram"] for o in offers if o.get("gpu_ram")) / 1024)
        for tier, v in (("marketplace-min", prices[0]), ("marketplace-median", statistics.median(prices))):
            rows.append(dict(provider="vast", gpu=name, vram_gb=vram, tier=tier,
                price_usd_hour=round(v, 4), n_offers=len(prices),
                raw=f"{tier} of dph_total over {len(prices)} rentable 1-GPU offers (gpu_name={gname}, limit 1000)",
                retrieved_at=TODAY, source_url=url, verified="api_live"))

def modal(rows):
    m = PAGE_VALUES["modal"]
    for name, (ps, vram) in m["gpus"].items():
        rows.append(dict(provider="modal", gpu=name, vram_gb=vram, tier="serverless",
            price_usd_hour=round(ps * 3600, 4), n_offers=None,
            raw=f"{ps}/s x 3600 (page {m['date']})", retrieved_at=TODAY,
            source_url=m["source_url"], verified="page"))

def main():
    rows, raw = [], {"retrieved_at": TODAY}
    runpod(rows, raw); vast(rows, raw); modal(rows)
    os.makedirs(os.path.dirname(RAW), exist_ok=True)
    json.dump(raw, open(RAW, "w"), indent=1)
    # garder les machines completes (kind=machine) ajoutees a la main, sinon un refetch les efface
    try:
        rows += [r for r in json.load(open(OUT)) if r.get("kind") == "machine"]
    except (OSError, ValueError):
        pass
    json.dump(rows, open(OUT, "w"), indent=1, ensure_ascii=False)
    print(len(rows), "lignes")

if __name__ == "__main__":
    main()
