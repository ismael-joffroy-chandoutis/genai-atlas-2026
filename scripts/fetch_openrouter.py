#!/usr/bin/env python3
"""Relevé public des modèles vidéo et image d'OpenRouter (aucune clé, aucune génération).

Sortie : data/raw/openrouter-<date>.json
"""
import json, sys, datetime, pathlib, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent


def get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "genai-atlas/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def main():
    date = sys.argv[sys.argv.index("--date") + 1] if "--date" in sys.argv else datetime.date.today().isoformat()
    video = get("https://openrouter.ai/api/v1/videos/models").get("data", [])
    allm = get("https://openrouter.ai/api/v1/models?output_modalities=image").get("data", [])
    image = [m for m in allm if "image" in (m.get("architecture", {}).get("output_modalities") or [])]
    out = {"source": "openrouter", "retrieved_at": date, "video_models": video, "image_models": image}
    path = ROOT / "data" / "raw" / f"openrouter-{date}.json"
    path.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"{len(video)} vidéo, {len(image)} image -> {path}")


if __name__ == "__main__":
    main()
