#!/usr/bin/env python3
"""Écarts de prix : même modèle, plateformes différentes (lignes à l'usage, hors abonnements).

Pour chaque model_id et chaque colonne, prend le prix le plus bas par plateforme, puis signale
les modèles où max/min >= SEUIL. Usage : python3 scripts/compare-prices.py [seuil=1.5]
"""
import json, sys, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
SEUIL = float(sys.argv[1]) if len(sys.argv) > 1 else 1.5
COLS = ["price_usd_720p_s", "price_usd_1080p_s", "price_usd_480p_s", "price_usd_per_image"]

rows = json.loads((ROOT / "data" / "prices.json").read_text())
by = collections.defaultdict(lambda: collections.defaultdict(dict))
for r in rows:
    if r["unit"] == "subscription":
        continue
    for c in COLS:
        v = r.get(c)
        if v:
            cur = by[(r["model_id"], c)][r["platform"]]
            if not cur or v < cur[0]:
                by[(r["model_id"], c)][r["platform"]] = (v, r["verified"])
out = []
for (mid, c), plats in by.items():
    if len(plats) < 2:
        continue
    lo = min(plats.items(), key=lambda x: x[1][0])
    hi = max(plats.items(), key=lambda x: x[1][0])
    ratio = hi[1][0] / lo[1][0]
    if ratio >= SEUIL:
        out.append((ratio, mid, c, lo, hi, len(plats)))
for ratio, mid, c, lo, hi, n in sorted(out, reverse=True):
    print(f"x{ratio:4.1f}  {mid:38s} {c:20s} min {lo[0]}={lo[1][0]:.4f}  max {hi[0]}={hi[1][0]:.4f}  ({n} plateformes)")
