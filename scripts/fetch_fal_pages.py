#!/usr/bin/env python3
"""Lit le texte de prix (« pricingInfoOverride ») des pages modèles fal.ai pour les endpoints retenus.

Pourquoi : l'API /v1/models/pricing rend un seul prix unitaire, sans résolution ni audio, et il diffère
parfois du texte de la page (ex. Kling 3.0 standard : API 0,14 $/s, page 0,084 $/s sans audio, 0,126 avec).
Entrée : les endpoints fal présents dans data/prices.json (lancer merge-prices.py d'abord).
Sortie : data/raw/fal-pages-<date>.json  {endpoint_id: texte | null}
"""
import json, re, sys, time, datetime, pathlib, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503):
                time.sleep(5 * (attempt + 1)); continue
            return None
        except Exception:
            time.sleep(3)
    return None


def extract(page, ep):
    # Le JSON de la page est échappé (\") ; on cherche l'objet du bon endpoint puis son pricingInfoOverride.
    key = f'\\"id\\":\\"{ep}\\"'
    i = page.find(key)
    while i != -1:
        j = page.find('pricingInfoOverride', i)
        nxt = page.find('\\"id\\":\\"', i + len(key))
        if j != -1 and (nxt == -1 or j < nxt + 2000):
            m = re.match(r'pricingInfoOverride\\":\\"(.*?)\\",\\"', page[j:j + 3000], re.S)
            if m:
                return m.group(1).replace("\\\\n", "\n").replace("\\n", "\n").replace("**", "")
        i = page.find(key, i + 1)
    return None


def main():
    date = sys.argv[sys.argv.index("--date") + 1] if "--date" in sys.argv else datetime.date.today().isoformat()
    out_path = ROOT / "data" / "raw" / f"fal-pages-{date}.json"
    done = json.loads(out_path.read_text()) if out_path.exists() else {}
    eps = sorted({r["endpoint"] for r in json.loads((ROOT / "data" / "prices.json").read_text())
                  if r["platform"] == "fal"})
    todo = [e for e in eps if e not in done]
    for n, ep in enumerate(todo, 1):
        page = fetch(f"https://fal.ai/models/{ep}")
        done[ep] = extract(page, ep) if page else None
        if n % 25 == 0:
            out_path.write_text(json.dumps(done, indent=1, ensure_ascii=False))
            print(f"{n}/{len(todo)}", flush=True)
        time.sleep(0.4)
    out_path.write_text(json.dumps(done, indent=1, ensure_ascii=False))
    print(f"{sum(1 for v in done.values() if v)}/{len(done)} textes de prix -> {out_path}")


if __name__ == "__main__":
    main()
