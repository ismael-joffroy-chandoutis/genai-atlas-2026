#!/usr/bin/env python3
"""Construit un atlas interactif en un seul fichier HTML, sans dépendance.

  python3 scripts/build_site.py merge    # data/*.json -> site/atlas.data.json
  python3 scripts/build_site.py check    # contrôle : aucune entrée perdue ni modifiée
  python3 scripts/build_site.py render   # site/atlas.config.json + données -> site/index.html
  python3 scripts/build_site.py scan     # cherche ce qui ne doit pas sortir : fichiers internes, chemins, machines

Le gabarit (site/engine/atlas.template.tpl) ne connaît aucun champ : tout passe par
la configuration. Autre atlas, même commande :

  python3 scripts/build_site.py render --config c.json --data d.json --out a.html
"""
import argparse, base64, datetime, json, pathlib, re, shutil, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / "data"
SITE = ROOT / "site"
TEMPLATE = SITE / "engine" / "atlas.template.tpl"

COLLECTIONS = {
    "video": "video-models.json", "image": "image-models.json", "audio": "audio-models.json",
    "threed": "3d-models.json", "platforms": "platforms.json", "prices": "prices.json", "gpu": "gpu-hour.json",
}
ANNEXES = {
    "rankings": "rankings.json", "stages": "stages.json", "status": "status.json",
    "integrations": "integrations.json", "local_runs": "local-runs.json",
    "local_runs_extra": "local-runs-extra.json", "aliases": "model-id-aliases.json",
}
# Dans le dépôt mais hors de ce JSON : ce ne sont pas des entrées de données.
NOT_DATA = ["TABLES.md (tableaux dérivés)", "guides/ (textes)", "lab/focal-test/ (mesures et images)", "README, licences, bannières"]

STAGE_RE = [
    ("effets", r"visage|lip|recast|remplac|swap|avatar|doublage|dubit|motion control|mouvement d.une vidéo|animation d.un personnage|personnage|inpainting|plaque propre|alpha|retouche|suppression de fond|baguette"),
    ("montage", r"prolong|extend|multi-plans|multi-clips|insert|reprise|retake|continuation|recadrage|reframe|transition|interpolation|boucle|outpainting"),
    ("etalonnage", r"relight|hdr|étalonn|couleur|recolor"),
    ("agrandissement", r"super-résolution|upscal|restauration|défloutage|détails affinés|seedvr|topaz|starlight"),
    ("storyboard", r"storyboard|3d-to-video|viewport|brouillon|draft|\b(?:fast|mini|lite|turbo|flash|preview)\b"),
]


def load(name):
    return json.loads((D / name).read_text())


def stages_for(m, kind, stages):
    """Même rangement par étape que scripts/build_atlas.py."""
    txt = " ".join((m.get("edit_functions") or []) + [m.get("variant") or "", m.get("family") or ""]).lower()
    s = set()
    if kind == "video":
        s.add("tournage")
        if (m.get("outputs") or {}).get("lip_sync"):
            s.add("effets")
        if (m.get("outputs") or {}).get("native_audio") or re.search(r"texte vers audio|musique|doublage", txt):
            s.add("son")
        if (m.get("inputs") or {}).get("input_3d"):
            s.add("storyboard")
        for st, rx in STAGE_RE:
            if re.search(rx, txt):
                s.add(st)
    elif kind == "image":
        s.add("storyboard")
        if (m.get("inputs") or {}).get("image_edit"):
            s.add("effets")
        for st, rx in STAGE_RE:
            if st in ("effets", "etalonnage", "agrandissement") and re.search(rx, txt):
                s.add(st)
    elif kind == "audio":
        s.add("son")
        t = m.get("task") or ""
        if t == "stt":
            s |= {"ecriture", "montage"}
        if t in ("lip_sync", "dubbing"):
            s.add("effets")
    elif kind == "threed":
        s.add("storyboard")
        if (m.get("task") or "") in ("depth_and_camera", "scene_reconstruction"):
            s.add("effets")
    ov = stages.get("model_overrides", {})
    s |= set(ov.get("add", {}).get(m["id"], []))
    s -= set(ov.get("remove", {}).get(m["id"], []))
    return [x["id"] for x in stages.get("stages", []) if x["id"] in s]


def last_checked(o):
    found = []

    def walk(x):
        if isinstance(x, dict):
            d = x.get("date")
            if isinstance(d, str) and x.get("type") and re.match(r"^\d{4}-\d{2}(-\d{2})?$", d):
                found.append(d)
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(o)
    return max(found) if found else None


def derive(cols, ann):
    """Valeurs calculées, rangées à part : les objets sources restent intacts."""
    alias = ann["aliases"]
    stages = ann["stages"]
    status = ann["status"]
    by_model = {}
    for p in cols["prices"]:
        by_model.setdefault(alias.get(p.get("model_id"), p.get("model_id")), []).append(p)
    keys = ("price_usd_480p_s", "price_usd_720p_s", "price_usd_1080p_s", "price_usd_per_image")
    out = {}
    for kind in ("video", "image", "audio", "threed"):
        out[kind] = {}
        for m in cols[kind]:
            ps = by_model.get(m["id"], [])
            best = {}
            for k in keys:
                vals = [p[k] for p in ps if p.get("unit") != "subscription" and isinstance(p.get(k), (int, float)) and p[k] > 0]
                best[k] = min(vals) if vals else None
            entry = status.get("models", {}).get(m["id"])
            st = {"value": "actif", "presumed": True} if not entry else {k: entry.get(k) for k in ("value", "date", "note")}
            out[kind][m["id"]] = {"stages": stages_for(m, kind, stages), "status": st, "checked": last_checked(m),
                                  "best": best, "n_prices": len(ps)}
    out["platforms"] = {}
    for p in cols["platforms"]:
        entry = status.get("platforms", {}).get(p["id"])
        st = {"value": "actif", "presumed": True} if not entry else {k: entry.get(k) for k in ("value", "date", "note")}
        out["platforms"][p["id"]] = {
            "stages": [s["id"] for s in stages.get("stages", []) if p["id"] in stages.get("platforms", {}).get(s["id"], [])],
            "status": st, "checked": last_checked(p), "why": stages.get("platform_why", {}).get(p["id"]),
        }
    return out


def merge(args):
    cols = {k: load(f) for k, f in COLLECTIONS.items()}
    ann = {k: load(f) for k, f in ANNEXES.items()}
    m = re.search(r"^## (v[0-9.]+)", (ROOT / "CHANGELOG.md").read_text(), re.M)
    derived = derive(cols, ann)
    dates = [p.get("retrieved_at") for p in cols["prices"] if p.get("retrieved_at")]
    meta = {
        "title": "Atlas génératif 2026", "version": m.group(1) if m else None,
        "data_date": ann["rankings"].get("generated"), "last_source_date": max(dates) if dates else None,
        "counts": {k: len(v) for k, v in cols.items()},
        "licence": {"donnees": "CC BY-SA 4.0", "code": "MIT"},
    }
    out = {"meta": meta, "collections": cols, "annexes": ann, "derived": derived}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
    print(f"{args.out.relative_to(ROOT)} : {args.out.stat().st_size / 1e6:.2f} Mo, {meta['counts']}")


def stale_signals(cols, ann, today):
    """Dates dépassées et chiffres divergents : signalés, jamais corrigés."""
    sig = []
    for p in cols["platforms"]:
        for x in p.get("promotions") or []:
            if isinstance(x, dict) and x.get("ends") and x["ends"] < today:
                sig.append(f"promotion expirée : {p['id']}, fin {x['ends']}")
    for mid, s in ann["status"].get("models", {}).items():
        if s.get("value") == "pas_sorti":
            sig.append(f"statut « pas encore sorti » à revérifier : {mid}, noté le {s.get('date') or 'sans date'}")
        if s.get("value") == "a_verifier":
            sig.append(f"statut « à vérifier » : {mid}")
    readme = (ROOT / "README.fr.md").read_text()
    for label, pat, n in (("vidéo", r"(\d+) variantes vidéo", len(cols["video"])), ("image", r"(\d+) variantes image", len(cols["image"])),
                          ("plateformes", r"(\d+) plateformes :", len(cols["platforms"])), ("prix", r"(\d+) prix pour", len(cols["prices"]))):
        m = re.search(pat, readme)
        if m and int(m.group(1)) != n:
            sig.append(f"README.fr.md annonce {m.group(1)} ({label}), le JSON en contient {n}")
    return sig


def check(args):
    merged = json.loads(args.data.read_text())
    ok = True
    print(f"{'fichier source':28} {'avant':>6} {'après':>6}  identique")
    for group, mapping in (("collections", COLLECTIONS), ("annexes", ANNEXES)):
        for k, f in mapping.items():
            src, dst = load(f), merged[group].get(k)
            same = src == dst and json.dumps(src, sort_keys=True) == json.dumps(dst, sort_keys=True)
            ok &= same
            print(f"{f:28} {len(src):>6} {len(dst or []):>6}  {'oui' if same else 'NON'}")
    cols, ann = merged["collections"], merged["annexes"]
    ids = {m["id"] for k in ("video", "image", "audio", "threed") for m in cols[k]}
    orphans = sorted({p["model_id"] for p in cols["prices"]} - ids - set(ann["aliases"]))
    extra = sorted(set(ann["local_runs_extra"]) - ids)
    print("\nNon rattachable à une fiche, conservé tel quel et consultable :")
    print(f"  {len(orphans)} identifiants de modèle présents seulement dans les prix (onglet Prix)")
    print(f"  {len(ann['rankings'].get('unmatched', []))} scores de classement sans fiche (annexes.rankings.unmatched)")
    print(f"  clés de local-runs-extra sans modèle : {extra}")
    print("Hors du JSON, car ce ne sont pas des entrées : " + " ; ".join(NOT_DATA))
    sig = stale_signals(cols, ann, args.today)
    print(f"\nPérimé ou divergent, signalé au {args.today}, rien de corrigé ({len(sig)}) :")
    for s in sig:
        print("  " + s)
    print("\nContrôle : " + ("aucune entrée perdue ni modifiée" if ok else "ÉCHEC"))
    disp_ok = True
    if args.config.exists():
        print()
        disp_ok = display_report(json.loads(args.config.read_text()), merged)[0]
    sys.exit(0 if ok and disp_ok else 1)


# Ce qui ne doit jamais apparaître dans une page publiée. Les termes propres à un poste de
# travail vivent hors du dépôt, dans .scan-terms (une ligne : « libellé<TAB>expression »).
LEAKS = [("nom de fichier interne", r"(?<![\w/.-])[\w-]+\.(?:md|py|tpl|sh|jsonl?|html)\b")]
TERMS = ROOT / ".scan-terms"
if TERMS.exists():
    LEAKS += [tuple(l.split("\t", 1)) for l in TERMS.read_text().splitlines() if "\t" in l and not l.startswith("#")]
else:
    print("scan : pas de fichier .scan-terms, seuls les noms de fichiers sont cherchés", file=sys.stderr)


def leaves(o, path=""):
    """Toutes les chaînes d'un objet, avec leur chemin."""
    if isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, f"{path}.{k}" if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, f"{path}.{i}")
    elif isinstance(o, str):
        yield path, o


def apply_display(o, rules, keep, path=""):
    """Copie de l'objet avec les règles d'affichage appliquées. Les sources ne sont pas touchées."""
    if isinstance(o, dict):
        return {k: apply_display(v, rules, keep, f"{path}.{k}" if path else k) for k, v in o.items()}
    if isinstance(o, list):
        return [apply_display(v, rules, keep, f"{path}.{i}") for i, v in enumerate(o)]
    if isinstance(o, str) and not re.search(keep, path):
        before = o
        for rx, to in rules:
            o = rx.sub(to, o)
        return re.sub(r"\s{2,}", " ", o).strip() if o != before else o
    return o


def display_rules(cfg):
    disp = cfg.get("display") or {}
    rules = [(re.compile(r["re"]), r["to"]) for r in disp.get("rules", [])]
    return rules, disp.get("keep", r"(^|\.)(url|capture|id)$"), disp.get("allow", [])


def find_leaks(obj, allow, keep):
    out = []
    for path, s in leaves(obj):
        if re.search(keep, path):
            continue
        txt = s
        for a in allow:
            txt = txt.replace(a, "")
        for label, rx in LEAKS:
            for m in re.finditer(rx, txt):
                out.append((label, path, txt[max(0, m.start() - 45):m.end() + 35].replace("\n", " ")))
    return out


def _shape(o):
    if isinstance(o, dict):
        return {k: _shape(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_shape(v) for v in o]
    return "s" if isinstance(o, str) else o


def display_report(cfg, data, show=True):
    """Compare les données et ce que la page affichera : mêmes entrées, résidus éventuels, réécritures à reporter."""
    rules, keep, allow = display_rules(cfg)
    shown = apply_display(data, rules, keep)
    same_shape = _shape(data) == _shape(shown)
    changed = [(p, a, b) for (p, a), (_, b) in zip(leaves(data), leaves(shown)) if a != b]
    cfg_view = {k: v for k, v in cfg.items() if k != "display"}
    residue = find_leaks(shown, allow, keep) + find_leaks(cfg_view, allow, r"(^|\.)(url|src|re)$")
    if show:
        print(f"Affichage : {len(changed)} valeurs réécrites par le filtre, sources intactes, structure {'identique' if same_shape else 'DIFFÉRENTE'}.")
        print(f"Recherche de fichiers, chemins et machines : {len(residue)} résidu(s) après filtre.")
        for label, path, ctx in residue[:40]:
            print(f"  {label} : {path} : {ctx}")
    return same_shape and not residue, changed, shown


def scan(args):
    cfg = json.loads(args.config.read_text())
    data = json.loads(args.data.read_text())
    ok, changed, _ = display_report(cfg, data)
    if args.list:
        print("\nÀ réécrire dans les données plutôt que de filtrer :")
        for path, a, b in changed:
            print(f"- {path}\n    avant : {a[:220]}\n    après : {b[:220]}")
    print("Contrôle d'affichage : " + ("rien d'interne ne sort" if ok else "ÉCHEC"))
    sys.exit(0 if ok else 1)


def embed_logos(cfg, data, folder):
    """Petites icônes déjà téléchargées (scripts/fetch_logos.py), embarquées en base64. Jamais de chargement externe."""
    if not folder or not pathlib.Path(folder).is_dir():
        return {}
    hosts = set()
    for c in cfg["collections"]:
        logo = c.get("logo")
        if not logo:
            continue
        cur = data
        for k in c["path"].split("."):
            cur = cur[k]
        for it in cur:
            v = it.get(logo["path"])
            if logo.get("rules"):
                for r in logo["rules"]:
                    if re.search(r["re"], str(v or ""), re.I):
                        hosts.add(r["host"])
                        break
            elif v:
                m = re.match(r"https?://(?:www\.)?([^/]+)", v)
                if m:
                    hosts.add(m.group(1))
    out = {}
    for h in sorted(hosts):
        f = pathlib.Path(folder) / f"{h}.png"
        if f.exists():
            out[h] = "data:image/png;base64," + base64.b64encode(f.read_bytes()).decode()
    return out


def embed_images(cfg, data, data_path, width):
    """Vignettes JPEG en base64, pour que le fichier reste autonome. Ne change pas les données."""
    images, missing = {}, []
    sips = shutil.which("sips")
    tmp = pathlib.Path(tempfile.mkdtemp(dir=tempfile.gettempdir()))
    try:
        for c in cfg["collections"]:
            if not c.get("thumb"):
                continue
            cur = data
            for k in c["path"].split("."):
                cur = cur[k]
            for it in cur:
                rel = it.get(c["thumb"])
                if not rel:
                    continue
                src = data_path.parent / rel
                if not src.exists():
                    missing.append(rel)
                    continue
                out = tmp / (re.sub(r"\W+", "_", rel) + ".jpg")
                if sips:
                    subprocess.run([sips, "-Z", str(width), "-s", "format", "jpeg", "-s", "formatOptions", "60", str(src), "--out", str(out)],
                                   check=True, capture_output=True)
                else:
                    out = src
                mime = "image/jpeg" if out.suffix == ".jpg" else "image/png"
                images[rel] = f"data:{mime};base64," + base64.b64encode(out.read_bytes()).decode()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if missing:
        print(f"captures introuvables : {missing}")
    return images


def render(args):
    cfg = json.loads(args.config.read_text())
    data = json.loads(args.data.read_text())
    images = embed_images(cfg, data, args.data, args.thumb_width) if args.embed_images else {}
    logos = embed_logos(cfg, data, args.logos)
    ok, changed, shown = display_report(cfg, data, show=False)
    if not ok:
        display_report(cfg, data)
        sys.exit("Page non écrite : du texte interne sortirait. Voir scan.")
    data = shown
    cfg = {k: v for k, v in cfg.items() if k != "display"}
    if not cfg.get("dataDate") and cfg.get("dataDatePath"):
        cur = data
        for k in cfg["dataDatePath"].split("."):
            cur = cur.get(k) if isinstance(cur, dict) else None
        cfg["dataDate"] = cur
    if cfg.get("dataVersionPath"):
        cfg["dataVersion"] = (data.get("meta") or {}).get(cfg["dataVersionPath"].split(".")[-1])
    tojson = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    esc = lambda s: str(s or "").replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")
    html = TEMPLATE.read_text()
    html = html.replace("/*__TITLE__*/", esc(cfg.get("title"))).replace("/*__DESCRIPTION__*/", esc(cfg.get("description")))
    html = html.replace("/*__LANG__*/fr", cfg.get("lang", "fr"))
    html = html.replace("/*__CONFIG__*/null", tojson(cfg)).replace("/*__DATA__*/null", tojson(data)).replace("/*__IMAGES__*/{}", tojson(images)).replace("/*__LOGOS__*/{}", tojson(logos))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html)
    print(f"{args.out} : {args.out.stat().st_size / 1e6:.2f} Mo, {len(cfg['collections'])} collections, {len(images)} images et {len(logos)} logos embarqués, {len(changed)} valeurs filtrées à l'affichage")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("merge")
    a.add_argument("--out", type=pathlib.Path, default=SITE / "atlas.data.json")
    a = sub.add_parser("check")
    a.add_argument("--data", type=pathlib.Path, default=SITE / "atlas.data.json")
    a.add_argument("--today", default=datetime.date.today().isoformat())
    a.add_argument("--config", type=pathlib.Path, default=SITE / "atlas.config.json")
    a = sub.add_parser("scan")
    a.add_argument("--config", type=pathlib.Path, default=SITE / "atlas.config.json")
    a.add_argument("--data", type=pathlib.Path, default=SITE / "atlas.data.json")
    a.add_argument("--list", action="store_true", help="liste ce qui devrait être réécrit dans les données")
    a = sub.add_parser("render")
    a.add_argument("--config", type=pathlib.Path, default=SITE / "atlas.config.json")
    a.add_argument("--data", type=pathlib.Path, default=SITE / "atlas.data.json")
    a.add_argument("--out", type=pathlib.Path, default=SITE / "index.html")
    a.add_argument("--embed-images", action="store_true", help="embarque les captures en vignettes (champ thumb de la configuration)")
    a.add_argument("--thumb-width", type=int, default=720)
    a.add_argument("--logos", type=pathlib.Path, default=SITE / "engine" / "logos", help="dossier des icônes <hôte>.png")
    args = ap.parse_args()
    {"merge": merge, "check": check, "render": render, "scan": scan}[args.cmd](args)


if __name__ == "__main__":
    main()
