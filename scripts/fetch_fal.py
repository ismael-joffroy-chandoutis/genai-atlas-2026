#!/usr/bin/env python3
"""Relevé des modèles et prix fal.ai (lecture seule, aucune génération).

Sortie : data/raw/fal-<date>.json
Usage  : FAL_KEY=... python3 scripts/fetch_fal.py [--date 2026-10-15]
"""
import json, os, sys, time, urllib.request, urllib.parse, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATS = ["text-to-video", "image-to-video", "video-to-video", "text-to-image", "image-to-image"]
API = "https://api.fal.ai/v1"


def get(url, key):
    req = urllib.request.Request(url, headers={"Authorization": f"Key {key}", "Accept": "application/json"})
    for attempt in range(10):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code >= 500 and attempt >= 2:
                raise RuntimeError(f"{e.code} persistant sur {url}")
            if e.code == 429 or e.code >= 500:
                ra = e.headers.get("Retry-After")
                time.sleep(float(ra) if ra and ra.replace(".", "").isdigit() else min(60, 3 * 2 ** attempt))
                continue
            raise
    raise RuntimeError(f"429/5xx persistant sur {url}")


def main():
    date = sys.argv[sys.argv.index("--date") + 1] if "--date" in sys.argv else datetime.date.today().isoformat()
    key = os.environ.get("FAL_KEY")
    if not key:
        sys.exit("FAL_KEY absent")
    models = {}
    for cat in CATS:
        cursor = None
        while True:
            q = {"category": cat, "limit": 100}
            if cursor:
                q["cursor"] = cursor
            d = get(f"{API}/models?{urllib.parse.urlencode(q)}", key)
            for m in d.get("models", []):
                models[m["endpoint_id"]] = m
            cursor = d.get("next_cursor")
            if not d.get("has_more") or not cursor:
                break
    ids = sorted(models)
    print(f"{len(ids)} endpoints listés", flush=True)
    ckpt = ROOT / "data" / "raw" / f".fal-prices-{date}.ckpt.json"
    prices = json.loads(ckpt.read_text()) if ckpt.exists() else {}
    ids_todo = [e for e in ids if e not in prices]
    no_price = []
    errors = []
    for i in range(0, len(ids_todo), 10):
        chunk = ids_todo[i:i + 10]
        q = urllib.parse.urlencode([("endpoint_id", e) for e in chunk])
        try:
            d = get(f"{API}/models/pricing?{q}", key)
            plist = d.get("prices", [])
        except urllib.error.HTTPError as e:
            if e.code != 404 and e.code < 500:
                raise
            # un id sans prix fait échouer tout le lot : on repasse un par un
            plist = []
            for e1 in chunk:
                try:
                    plist += get(f"{API}/models/pricing?endpoint_id={urllib.parse.quote(e1)}", key).get("prices", [])
                except urllib.error.HTTPError as e2:
                    (no_price if e2.code == 404 else errors).append(e1)
                except RuntimeError:
                    errors.append(e1)
                time.sleep(1.0)
        except RuntimeError:
            plist = []
            errors.extend(chunk)
        for p in plist:
            prices[p["endpoint_id"]] = p
        for e1 in chunk:
            if e1 not in errors:
                prices.setdefault(e1, None)
        ckpt.write_text(json.dumps(prices))
        print(f"{min(i + 10, len(ids_todo))}/{len(ids_todo)}", flush=True)
        time.sleep(1.0)
    out = {
        "source": "fal", "retrieved_at": date, "no_price_404": no_price, "errors": errors,
        "endpoints": [{
            "endpoint_id": e,
            "category": models[e].get("metadata", {}).get("category"),
            "display_name": models[e].get("metadata", {}).get("display_name"),
            "status": models[e].get("metadata", {}).get("status"),
            "date": models[e].get("metadata", {}).get("date"),
            "model_url": models[e].get("metadata", {}).get("model_url"),
            "price": prices.get(e),
        } for e in ids],
    }
    path = ROOT / "data" / "raw" / f"fal-{date}.json"
    path.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"{len(ids)} endpoints, {len(prices)} prix -> {path}")


if __name__ == "__main__":
    main()
