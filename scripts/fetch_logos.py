#!/usr/bin/env python3
"""Télécharge une fois l'icône publique de chaque site, en petit format, pour l'embarquer dans la page.

  python3 scripts/fetch_logos.py --config site/atlas.config.json --data site/atlas.data.json --out site/engine/logos

Une icône déjà présente n'est pas retéléchargée. Pas d'icône lisible : pas de fichier, la page affiche un monogramme.
"""
import argparse, json, pathlib, re, shutil, subprocess, tempfile, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15"
MAGIC = (b"\x89PNG", b"\x00\x00\x01\x00", b"\xff\xd8\xff", b"GIF8", b"RIFF")


def fetch(url, limit=600_000):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.read(limit), r.geturl()


def candidates(site):
    out = []
    try:
        page, final = fetch(site, 400_000)
        page = page.decode("utf-8", "ignore")
        for tag in re.findall(r"<link\b[^>]*>", page, re.I):
            rel = re.search(r'rel=["\']?([^"\'>]+)', tag, re.I)
            href = re.search(r'href=["\']?([^"\'> ]+)', tag, re.I)
            if not rel or not href or "icon" not in rel.group(1).lower():
                continue
            size = re.search(r'sizes=["\']?(\d+)', tag, re.I)
            score = (2 if "apple" in rel.group(1).lower() else 0) + (int(size.group(1)) / 100 if size else 0)
            out.append((score, urllib.parse.urljoin(final, href.group(1).replace("&amp;", "&"))))
        site = final
    except Exception:
        pass
    urls = [u for _, u in sorted(out, reverse=True) if not u.lower().split("?")[0].endswith(".svg") and not u.startswith("data:")]
    return urls + [urllib.parse.urljoin(site, "/apple-touch-icon.png"), urllib.parse.urljoin(site, "/favicon.ico")]


def one(key, site, dest, tmp):
    target = dest / f"{key}.png"
    if target.exists():
        return key, "déjà là", ""
    for u in candidates(site):
        try:
            data, _ = fetch(u)
        except Exception:
            continue
        if not data.startswith(MAGIC):
            continue
        base = re.sub(r"\W+", "_", key)
        raw, png = tmp / (base + "_raw"), tmp / (base + ".png")
        raw.write_bytes(data)
        r = subprocess.run(["sips", "-Z", "48", "-s", "format", "png", str(raw), "--out", str(png)], capture_output=True)
        if r.returncode or not png.exists():
            continue
        dims = subprocess.run(["sips", "-g", "pixelWidth", str(png)], capture_output=True, text=True).stdout
        m = re.search(r"pixelWidth: (\d+)", dims)
        if not m or int(m.group(1)) < 16 or png.stat().st_size > 30_000:
            continue
        shutil.copy(png, target)
        return key, "ok", u
    return key, "absent", ""


def wanted(cfg, data):
    out = {}
    for c in cfg["collections"]:
        logo = c.get("logo")
        if not logo:
            continue
        cur = data
        for k in c["path"].split("."):
            cur = cur[k]
        skip = logo.get("skip", [])
        for it in cur:
            v = it.get(logo["path"])
            if logo.get("rules"):
                for r in logo["rules"]:
                    if re.search(r["re"], str(v or ""), re.I):
                        out[r["host"]] = r.get("site") or f"https://{r['host']}/"
                        break
            elif v:
                m = re.match(r"(https?://(?:www\.)?([^/]+))", v)
                if m and m.group(2) not in skip:
                    out[m.group(2)] = m.group(1) + "/"
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", type=pathlib.Path, required=True)
    ap.add_argument("--data", type=pathlib.Path, required=True)
    ap.add_argument("--out", type=pathlib.Path, required=True)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    sites = wanted(json.loads(a.config.read_text()), json.loads(a.data.read_text()))
    with tempfile.TemporaryDirectory() as t, ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda kv: one(kv[0], kv[1], a.out, pathlib.Path(t)), sites.items()))
    for k, st, u in sorted(res):
        print(f"{st:8} {k} {u}")
    n = sum(1 for _, st, _ in res if st != "absent")
    size = sum(f.stat().st_size for f in a.out.glob("*.png"))
    print(f"{n} icônes sur {len(res)}, {size / 1024:.0f} Ko dans {a.out}")


if __name__ == "__main__":
    main()
