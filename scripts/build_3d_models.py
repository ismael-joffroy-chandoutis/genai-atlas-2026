import json, re
D = "2026-10-15"
ARENA = "https://huggingface.co/spaces/3d-arena/3d-arena"
ARENA_API = "https://3d-arena-3d-arena.hf.space/api/leaderboard"
def S(url, date=D, t="editeur"): return {"url": url, "date": date, "type": t}
def arena_src(): return S(ARENA_API + "?vote_type=render", D, "independant")
def arena_topo_src(): return S(ARENA_API + "?vote_type=topology", D, "independant")
def fal(ep): return S("https://fal.ai/models/" + ep, D, "independant")

def M(id, family, variant, vendor, country, task, released, ow, lic, api, app,
      inputs, outputs, blender, speed, price, local, pros, cons, sources,
      scores=None, scores_note=None, tasks_other=None, released_note=None, status_note=None):
    return {
        "id": id, "family": family, "variant": variant, "vendor": vendor, "country": country,
        "task": task, "tasks_other": tasks_other or [],
        "released": released, "released_note": released_note,
        "access": {"open_weights": ow, "license": lic, "api": api, "consumer_app": app},
        "scores": scores or {}, "scores_note": scores_note,
        "inputs": inputs, "outputs": outputs, "blender": blender, "speed": speed,
        "price": price, "local": local, "pros": pros, "cons": cons,
        "status_note": status_note, "sources": sources,
    }

def I(images=None, text=None, video=None, multiview=None, other=None):
    return {"images": images, "text": text, "video": video, "multiview": multiview, "other": other}
def O(mesh=None, pbr=None, splats=None, rig=None, formats=None, polygons=None, other=None):
    return {"mesh": mesh, "textures_pbr": pbr, "splats": splats, "rig": rig, "formats": formats or [], "polygons": polygons, "other": other}
def B(mode, note=None): return {"mode": mode, "note": note}
def P(unit=None, usd=None, platform=None, note=None): return {"unit": unit, "usd": usd, "platform": platform, "note": note}
def L(r5090=None, r4090=None, mac=None, tool=None, vram=None):
    return {"runs_on_rtx5090_32gb": r5090, "rtx4090_24gb": r4090, "mac_m5max_128gb": mac, "tool": tool, "vram_note": vram}
CLOUD = L(False, False, False, None, "Service en ligne, pas de poids publiés.")
TENCENT_LIC_NOTE = "ne s'applique pas dans l'Union européenne, au Royaume-Uni ni en Corée du Sud"

m = []

# ---------------- image_to_3d : Tencent Hunyuan3D ----------------
m.append(M("hunyuan3d-2-0", "Hunyuan3D", "2.0 (forme + Paint)", "Tencent", "CN", "image_to_3d", "2025-01-21",
  True, "Tencent Hunyuan 3D 2.0 Community License (" + TENCENT_LIC_NOTE + ")", True, False,
  I(True, False, False, False), O(True, False, False, False, ["GLB"], None, "Texture par Hunyuan3D-Paint 2.0 (couleur, pas PBR)"),
  B("addon", "Add-on Blender officiel (janvier 2025) : Blender appelle un serveur API Hunyuan3D lancé en local."),
  None, P("per_generation", None, "fal", "Endpoint fal-ai/hunyuan3d/v2 actif, prix non affiché sur la page le 15/10/2026."),
  L(True, True, True, "Dépôt officiel (gradio_app.py, mode low_vram), ComfyUI", "6 Go pour la forme, 16 Go forme + texture (README officiel). macOS, Windows et Linux annoncés."),
  ["1er au classement topologie de 3D Arena", "Tourne sur petite carte et sur Mac selon l'éditeur", "Add-on Blender officiel"],
  ["Licence inapplicable en France (UE exclue)", "Texture non PBR", "Remplacé par 2.1 côté éditeur"],
  [S("https://github.com/Tencent-Hunyuan/Hunyuan3D-2"), S("https://huggingface.co/tencent/Hunyuan3D-2"), arena_src(), arena_topo_src(), fal("fal-ai/hunyuan3d/v2")],
  {"3d_arena_rendu": 1284, "3d_arena_topologie": 1358}, "3D Arena lu le 15/10/2026 : rendu 8e (5245 votes), topologie 1er (853 votes)."))

m.append(M("hunyuan3d-2-1", "Hunyuan3D", "2.1 (forme + Paint PBR)", "Tencent", "CN", "image_to_3d", "2025-06-13",
  True, "Tencent Hunyuan 3D 2.1 Community License (" + TENCENT_LIC_NOTE + ")", False, False,
  I(True, False, False, False), O(True, True, False, False, ["GLB"], None, "Textures PBR (métal, rugosité) par Hunyuan3D-Paint 2.1"),
  B("import_direct", "GLB importable ; l'add-on Blender officiel vise la version 2.0."),
  None, P(None, None, "fal", "Endpoint fal-ai/hunyuan3d-v21 marqué « deprecated » le 15/10/2026."),
  L(True, False, None, "Dépôt officiel, ComfyUI", "10 Go pour la forme, 21 Go pour la texture, 29 Go pour les deux (README officiel) : la chaîne complète dépasse 24 Go."),
  ["Premier modèle ouvert de Tencent avec textures PBR", "4e au classement topologie de 3D Arena", "Code d'entraînement publié"],
  ["Licence inapplicable en France (UE exclue)", "29 Go pour forme + texture", "Plus d'API fal active"],
  [S("https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1"), S("https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2.1/main/LICENSE"), arena_src(), arena_topo_src()],
  {"3d_arena_rendu": 1272, "3d_arena_topologie": 1313}, "3D Arena lu le 15/10/2026 : rendu 10e (2208 votes), topologie 4e (823 votes)."))

m.append(M("hunyuan3d-2mv", "Hunyuan3D", "2mv (multivue)", "Tencent", "CN", "multiview_to_3d", None,
  True, "Tencent Hunyuan 3D 2.0 Community License (" + TENCENT_LIC_NOTE + ")", True, False,
  I(True, False, False, True), O(True, False, False, False, ["GLB"]),
  B("addon", "Même add-on Blender que la 2.0 (serveur local)."), None,
  P("per_generation", None, "fal", "Endpoint fal-ai/hunyuan3d/v2/multi-view actif, prix non affiché le 15/10/2026."),
  L(None, None, None, "Dépôt Hunyuan3D-2 (sous-dossier hunyuan3d-dit-v2-mv, version turbo)", None),
  ["Prend plusieurs vues d'un même objet (face, côté, dos)", "Version turbo disponible"],
  ["Licence inapplicable en France (UE exclue)", "Forme seule, texture par un second modèle"],
  [S("https://huggingface.co/tencent/Hunyuan3D-2mv"), S("https://github.com/Tencent-Hunyuan/Hunyuan3D-2"), fal("fal-ai/hunyuan3d/v2/multi-view")],
  released_note="Fiche Hugging Face créée le 12/03/2025."))

m.append(M("hunyuan3d-omni", "Hunyuan3D", "Omni (contrôlable)", "Tencent", "CN", "image_to_3d", None,
  True, "Licence Tencent « other » sur Hugging Face (texte non relu)", False, False,
  I(True, False, False, False, "Contrôles annoncés à vérifier sur la fiche"), O(True, None, False, False, []),
  B("import_direct"), None, P(), L(),
  ["Version ouverte annoncée en même temps que la 3.0"], ["Détails techniques non relus pour cet atlas"],
  [S("https://huggingface.co/tencent/Hunyuan3D-Omni"), S("https://www.notebookcheck.net/Tencent-s-new-Hunyuan-3D-3-0-brings-realistic-AI-model-generation-to-developers-and-creators.1116964.0.html", "2025-09-16", "independant")],
  released_note="Fiche Hugging Face créée le 23/09/2025."))

m.append(M("hunyuan3d-2-5", "Hunyuan3D", "2.5", "Tencent", "CN", "image_to_3d", "2025-04-23",
  False, None, True, True,
  I(True, True, False, None), O(True, True, False, None, [], None, "Textures 4K et PBR multivue selon la presse"),
  B("import_direct"), None, P("credits", None, "Tencent Cloud"), CLOUD,
  ["10 milliards de paramètres selon le rapport technique", "Textures PBR"],
  ["Aucun poids publié sur Hugging Face (dépôts Tencent vérifiés le 15/10/2026)", "Remplacé par 3.0 et 3.1"],
  [S("https://www.aibase.com/news/17448", "2025-04-23", "independant"), S("https://cgworld.jp/flashnews/01-202505-Hunyuan3D-25.html", "2025-05-01", "independant")]))

m.append(M("hunyuan3d-3-0", "Hunyuan3D", "3.0", "Tencent", "CN", "image_to_3d", "2025-09-16",
  False, None, True, True,
  I(True, True, False, True, "Croquis (sketch-to-3D)"), O(True, True, False, False, ["GLB"], None, "Modes Normal, LowPoly, Geometry"),
  B("import_direct", "Export GLB ; ComfyUI Partner Nodes."), None,
  P("per_generation", 0.375, "fal", "Normal 0,375 $, LowPoly 0,45 $, géométrie seule 0,225 $ ; PBR +0,15 $, multivue +0,15 $, nombre de faces imposé +0,15 $."),
  CLOUD,
  ["Résolution annoncée 1536³", "20 générations gratuites par jour sur le site Tencent (2025)", "Croquis vers 3D"],
  ["Pas de poids publiés", "Prix fal élevé dès qu'on ajoute PBR et multivue"],
  [S("https://cgworld.jp/flashnews/01-202509-Hunyuan3D-30.html", "2025-09-16", "independant"), fal("fal-ai/hunyuan3d-v3/image-to-3d"), fal("fal-ai/hunyuan3d-v3/sketch-to-3d")],
  tasks_other=["text_to_3d", "multiview_to_3d"]))

m.append(M("hunyuan3d-3-1-pro", "Hunyuan3D", "3.1 Pro", "Tencent", "CN", "image_to_3d", None,
  False, None, True, True,
  I(True, True, False, True), O(True, True, False, False, ["GLB"], "Nombre de faces réglable (jusqu'à 1,5 M selon des revendeurs)"),
  B("import_direct"), None,
  P("per_generation", 0.375, "fal", "0,375 $ ; PBR +0,15 $, multivue +0,15 $, faces imposées +0,15 $. Tencent Cloud : 25 crédits (Normal), 30 (LowPoly), 15 (géométrie), crédit à 0,02 $ en postpayé."),
  CLOUD,
  ["Même prix que la 3.0 chez Tencent (choix 3.0 ou 3.1 sans surcoût)", "Outils annexes : découpe en parties, retopologie, dépliage UV, rigging automatique"],
  ["Pas de poids publiés", "Date de sortie officielle non trouvée"],
  [fal("fal-ai/hunyuan-3d/v3.1/pro/image-to-3d"), S("https://www.tencentcloud.com/document/product/1284/75281", "2026-05-08")],
  tasks_other=["text_to_3d", "multiview_to_3d"], released_note="Sur fal depuis le 27/01/2026."))

m.append(M("hunyuan3d-3-1-rapid", "Hunyuan3D", "3.1 Rapid", "Tencent", "CN", "image_to_3d", None,
  False, None, True, True, I(True, True, False, False), O(True, True, False, False, ["GLB"]),
  B("import_direct"), None,
  P("per_generation", 0.225, "fal", "0,225 $ ; PBR +0,15 $. Tencent Cloud édition Express : 15 crédits, PBR +10."),
  CLOUD, ["Le moins cher de la famille 3.x", "Texte ou image"], ["Qualité inférieure à Pro (positionnement éditeur)", "Pas de poids publiés"],
  [fal("fal-ai/hunyuan-3d/v3.1/rapid/image-to-3d"), S("https://www.tencentcloud.com/document/product/1284/75281", "2026-05-08")],
  tasks_other=["text_to_3d"], released_note="Sur fal depuis le 27/01/2026."))

# ---------------- TRELLIS ----------------
m.append(M("trellis-image-large", "TRELLIS", "TRELLIS image-large (1re génération)", "Microsoft", "US", "image_to_3d", None,
  True, "MIT", True, False, I(True, False, False, True), O(True, False, True, False, ["GLB", "PLY (Gaussiennes)"], None, "Maillage, Gaussiennes ou champ de radiance"),
  B("import_direct", "GLB natif ; PLY de Gaussiennes via un add-on de splats."), None,
  P("per_generation", None, "fal", "fal-ai/trellis et fal-ai/trellis/multi actifs, prix non affiché le 15/10/2026."),
  L(True, True, False, "Dépôt officiel (Linux), ComfyUI", "GPU NVIDIA d'au moins 16 Go ; testé seulement sous Linux (README)."),
  ["2e au rendu de 3D Arena en sortie Gaussiennes", "2e en topologie", "Licence MIT"],
  ["Linux et NVIDIA uniquement", "Textures non PBR"],
  [S("https://github.com/microsoft/TRELLIS"), S("https://huggingface.co/microsoft/TRELLIS-image-large"), arena_src(), arena_topo_src(), fal("fal-ai/trellis")],
  {"3d_arena_rendu_maillage": 1304, "3d_arena_rendu_3dgs": 1398, "3d_arena_topologie": 1328},
  "3D Arena lu le 15/10/2026 : « TRELLIS-3DGS » 2e (4834 votes), « TRELLIS » 6e (5780 votes), topologie 2e (853 votes).",
  tasks_other=["multiview_to_3d"], released_note="Fiche Hugging Face créée le 02/12/2024."))

m.append(M("trellis-2-4b", "TRELLIS", "TRELLIS.2 4B", "Microsoft", "US", "image_to_3d", None,
  True, "MIT (dépendances nvdiffrast et nvdiffrec sous licence NVIDIA propre)", True, False,
  I(True, False, False, False), O(True, True, False, False, ["GLB"], None, "PBR : couleur, rugosité, métal, opacité ; transparence à rebrancher à la main"),
  B("import_direct", "GLB opaque par défaut, brancher l'alpha dans Blender."),
  "Sur H100 : environ 3 s en 512³, 17 s en 1024³, 60 s en 1536³ (éditeur).",
  P("per_generation", 0.25, "fal", "0,25 $ en 512, 0,30 $ en 1024, 0,35 $ en 1536 ; LoRA sur fal au même tarif."),
  L(True, True, False, "Dépôt officiel (Linux, CUDA 12.4), ComfyUI", "GPU NVIDIA d'au moins 24 Go, Linux seulement (README) : 4090 à la limite."),
  ["Textures PBR complètes", "Licence MIT", "Inférence LoRA proposée par fal"],
  ["Classé derrière TRELLIS 1 sur 3D Arena (18e au rendu)", "Linux et 24 Go minimum", "Dépendances NVIDIA sous licence à part"],
  [S("https://github.com/microsoft/TRELLIS.2"), S("https://huggingface.co/microsoft/TRELLIS.2-4B"), arena_src(), arena_topo_src(), fal("fal-ai/trellis-2"), fal("fal-ai/trellis-2-lora")],
  {"3d_arena_rendu": 1126, "3d_arena_topologie": 1144}, "3D Arena lu le 15/10/2026 : rendu 18e (1426 votes), topologie 11e (740 votes).",
  released_note="Fiche Hugging Face créée le 01/12/2025, sur fal depuis le 17/12/2025."))

m.append(M("trellis-2-retexture", "TRELLIS", "TRELLIS.2 retexture", "Microsoft", "US", "texturing", None,
  True, "MIT", True, False, I(True, False, False, False, "Maillage existant + image"), O(True, True, False, False, ["GLB"]),
  B("import_direct"), None, P("per_generation", 0.20, "fal", "0,20 $ en 512, 0,24 $ en 1024 et plus."),
  L(True, True, False, "Dépôt TRELLIS.2 (génération de textures PBR sur forme existante)", "Même besoin que TRELLIS.2 : 24 Go, Linux."),
  ["Texture PBR sur un maillage fait à la main ou scanné"], ["Linux et 24 Go en local"],
  [S("https://github.com/microsoft/TRELLIS.2"), fal("fal-ai/trellis-2/retexture")], released_note="Sur fal depuis le 02/03/2026."))

# ---------------- VAST / Tripo ----------------
m.append(M("triposg-1-5b", "TripoSG", "TripoSG 1.5B", "VAST (Tripo)", "CN", "image_to_3d", None,
  True, "MIT", False, False, I(True, False, False, False), O(True, False, False, False, ["GLB"], "Nombre de faces limitable (--faces)"),
  B("import_direct"), None, P(),
  L(True, True, False, "Dépôt officiel, ComfyUI", "GPU CUDA d'au moins 8 Go (README)."),
  ["8 Go suffisent", "8e en topologie sur 3D Arena", "Variante croquis + texte (TripoSG-scribble)"],
  ["Forme seule, pas de texture", "Pas d'API officielle pour ce modèle ouvert"],
  [S("https://github.com/VAST-AI-Research/TripoSG"), S("https://huggingface.co/VAST-AI/TripoSG"), arena_topo_src()],
  {"3d_arena_topologie": 1222}, "3D Arena topologie lu le 15/10/2026 : 8e (814 votes).", released_note="Publié en mars 2025 (README)."))

m.append(M("triposplat", "TripoSplat", "TripoSplat", "VAST (Tripo)", "CN", "image_to_3d", None,
  True, "MIT", True, False, I(True, False, False, False), O(False, False, True, False, ["PLY (Gaussiennes)"]),
  B("addon", "Gaussiennes : add-on de splats nécessaire dans Blender."), None,
  P("per_generation", None, "fal", "tripo3d/triposplat actif, prix non affiché le 15/10/2026."), L(),
  ["Image vers Gaussiennes, poids ouverts"], ["Pas de maillage", "Peu de mesures publiques"],
  [S("https://huggingface.co/VAST-AI/TripoSplat"), fal("tripo3d/triposplat")], released_note="Fiche Hugging Face créée le 31/05/2026."))

TRIPO_BL = B("addon", "Tripo DCC Bridge pour Blender 4.1 et plus : envoie le modèle du site vers Blender, animations comprises.")
m.append(M("tripo-v3-0", "Tripo", "v3.0 (Ultra)", "VAST (Tripo)", "CN", "image_to_3d", None,
  False, None, True, True, I(True, True, False, True), O(True, True, False, None, []), TRIPO_BL, None,
  P("credits", None, "Tripo"), CLOUD,
  ["Mode Ultra pour le détail"], ["Prix API par modèle non publié en clair", "Site tripo3d.ai inaccessible aux robots (403) le 15/10/2026"],
  [S("https://pasqualepillitteri.it/en/news/7811/tripo-ai-review-3d-model-generator", D, "independant"), S("https://www.tripo3d.ai/blog/tripo-dcc-bridge-for-blender")],
  released_note="Septembre 2025 selon une revue indépendante, non confirmé par l'éditeur."))

m.append(M("tripo-h3-1", "Tripo", "H3.1", "VAST (Tripo)", "CN", "image_to_3d", None,
  False, None, True, True, I(True, True, False, True), O(True, True, False, None, ["GLB"], "Option maillage quad"),
  TRIPO_BL, None,
  P("per_generation", 0.20, "fal", "Image : 0,20 $ sans texture, 0,30 $ texture standard, 0,40 $ HD ; géométrie détaillée +0,20 $, quad +0,05 $. Texte : 0,10 à 0,30 $."),
  CLOUD,
  ["Modèle haut de gamme de Tripo en 2026", "Quads en option", "Pont Blender officiel"],
  ["Pas de poids publiés", "Classement communautaire indépendant non trouvé pour ce nom exact"],
  [S("https://www.newsfilecorp.com/release/289194", "2026-03-20"), fal("tripo3d/h3.1/image-to-3d"), fal("tripo3d/h3.1/text-to-3d"), S("https://www.sloyd.ai/blog/ai-3d-model-generator-rankings", "2026-08-03", "independant")],
  scores_note="Un classement « Top 3D AI » cité par Sloyd (concurrent) met « Tripo AI v3.1 » 1er à 1042 (03/08/2026) ; correspondance avec H3.1 non vérifiée.",
  tasks_other=["text_to_3d", "multiview_to_3d"], released_note="Annoncé avec P1.0 en mars 2026 (communiqué du 20/03/2026) ; sur fal depuis le 07/04/2026."))

m.append(M("tripo-p1", "Tripo", "Smart Mesh P1.0", "VAST (Tripo)", "CN", "image_to_3d", "2026-03-20",
  False, None, True, True, I(True, True, False, False), O(True, True, False, None, [], "Low poly"), TRIPO_BL,
  "Annoncé « en deux secondes » par l'éditeur.",
  P("per_generation", 0.40, "fal", "0,40 $ sans texture, 0,50 $ avec texture."), CLOUD,
  ["Low poly propre et rapide, utile pour du blocage"], ["Peu de détail par construction"],
  [S("https://www.newsfilecorp.com/release/289194", "2026-03-20"), fal("tripo3d/p1/image-to-3d")], tasks_other=["text_to_3d"]))

m.append(M("tripo-p2", "Tripo", "P2", "VAST (Tripo)", "CN", "image_to_3d", None,
  False, None, True, True, I(True, True, False, False), O(True, True, False, None, ["GLB"], "Nombre de faces réglable, triangles ou quads"), TRIPO_BL, None,
  P("per_generation", 1.00, "fal", "1,00 $ sans texture, 1,10 $ texture rapide ou standard, 1,20 $ détaillée, 1,30 $ extrême ; quads sans surcoût."),
  CLOUD, ["Topologie quad sans surcoût", "Faces réglables"], ["Le plus cher de Tripo sur fal", "Annonce éditeur non trouvée"],
  [fal("tripo3d/p2/image-to-3d"), fal("tripo3d/p2/text-to-3d")], tasks_other=["text_to_3d"], released_note="Sur fal depuis le 20/09/2026."))

m.append(M("tripo-h3-1-multiview", "Tripo", "H3.1 multivue", "VAST (Tripo)", "CN", "multiview_to_3d", None,
  False, None, True, True, I(True, False, False, True), O(True, True, False, None, ["GLB"]), TRIPO_BL, None,
  P("per_generation", 0.20, "fal", "Même grille que H3.1 image : 0,20 à 0,40 $ plus options."), CLOUD,
  ["Plusieurs vues d'un objet ou d'un personnage"], ["Pas de poids publiés"], [fal("tripo3d/h3.1/multiview-to-3d")],
  released_note="Sur fal depuis le 07/04/2026."))

m.append(M("tripo-h3-1-text", "Tripo", "H3.1 texte", "VAST (Tripo)", "CN", "text_to_3d", None,
  False, None, True, True, I(False, True, False, False), O(True, True, False, None, ["GLB"]), TRIPO_BL, None,
  P("per_generation", 0.10, "fal", "0,10 $ sans texture, 0,20 $ standard, 0,30 $ HD ; géométrie détaillée +0,20 $, quad +0,05 $."), CLOUD,
  ["Texte vers 3D le moins cher relevé sur fal"], ["Pas de poids publiés"], [fal("tripo3d/h3.1/text-to-3d")],
  released_note="Sur fal depuis le 07/04/2026."))

m.append(M("unirig", "UniRig", "UniRig", "VAST (Tripo)", "CN", "rigging_animation", None,
  True, "MIT", False, False, I(False, False, False, False, "Maillage OBJ, FBX, GLB ou VRM"), O(True, False, False, True, ["FBX", "GLB"], None, "Squelette puis poids de peau, fusion avec le modèle d'origine"),
  B("addon", "Add-on Blender fourni (dérivé de VRM-Addon-for-Blender) pour importer et exporter les .vrm ; FBX et GLB s'importent directement."), None,
  P(), L(True, True, None, "Dépôt officiel", "GPU CUDA d'au moins 8 Go pour l'inférence (README)."),
  ["Rigging automatique de n'importe quel modèle, humain, animal ou objet", "Squelette modifiable avant le calcul des poids", "Licence MIT"],
  ["Squelettes manquants dégradent la peau (README)", "Attributs physiques des os pas encore publiés"],
  [S("https://github.com/VAST-AI-Research/UniRig"), S("https://huggingface.co/VAST-AI/UniRig")], released_note="SIGGRAPH 2025 ; fiche Hugging Face créée le 09/04/2025."))

m.append(M("geosam2", "GeoSAM2", "GeoSAM2", "VAST, HKU, Tsinghua", "CN", "part_segmentation", None,
  True, "Apache-2.0 (fiche Hugging Face)", False, False, I(False, False, False, False, "Maillage sans texture + clics ou boîtes 2D"), O(True, False, False, False, [], None, "Découpe du maillage en parties"),
  B("import_direct"), None, P(), L(None, None, None, "Dépôt officiel VAST-AI-Research/GeoSAM2", None),
  ["Découpe un maillage en parties avec de simples clics", "Base SAM 2.1 (environ 154 M paramètres)"],
  ["Évalué seulement sur des objets sans texture", "Catégorie hors liste : segmentation en parties"],
  [S("https://huggingface.co/VAST-AI/GeoSAM2"), S("https://arxiv.org/abs/2508.14036v2", D, "independant")],
  released_note="CVPR 2026 ; fiche Hugging Face créée le 20/04/2026."))

# ---------------- Meshy ----------------
MESHY_BL = B("addon", "Plugin Blender officiel Meshy ; USDZ en mètres depuis le 12/10/2026.")
MESHY_FMT = ["GLB", "FBX", "OBJ", "USDZ"]
m.append(M("meshy-6", "Meshy", "Meshy 6", "Meshy", "US", "image_to_3d", None,
  False, None, True, True, I(True, True, False, True), O(True, True, False, None, MESHY_FMT), MESHY_BL, None,
  P("per_generation", 1.20, "fal", "Meshy 6 Preview sur fal : 0,80 $ sans texture, 1,20 $ texturé ; rigging +0,20 $, animation +0,12 $. API Meshy : 20 crédits (Pro à 19 €/mois pour 1000 crédits)."),
  CLOUD,
  ["3e au rendu et 3e en topologie de 3D Arena, 1er des modèles payants classés", "Rigging et animation dans la même API"],
  ["Pas de poids publiés", "Assets API supprimés après 3 jours hors offre Entreprise"],
  [S("https://docs.meshy.ai/en/api/changelog"), S("https://www.meshy.ai/api"), arena_src(), arena_topo_src(), fal("fal-ai/meshy/v6-preview/image-to-3d")],
  {"3d_arena_rendu": 1356, "3d_arena_topologie": 1327}, "3D Arena lu le 15/10/2026 : rendu 3e (1013 votes), topologie 3e (565 votes).",
  tasks_other=["text_to_3d", "multiview_to_3d"], released_note="Meshy 6 Preview dans l'API le 16/09/2025 (image) et le 23/09/2025 (texte)."))

m.append(M("meshy-7", "Meshy", "Meshy 7", "Meshy", "US", "image_to_3d", "2026-08-13",
  False, None, True, True, I(True, True, False, True), O(True, True, False, None, MESHY_FMT, "Smart Topology à nombre de polygones visé"), MESHY_BL, None,
  P("per_generation", 1.20, "fal", "0,80 $ sans texture, 1,20 $ texturé, 1,40 $ en mode ultra ; API Meshy : 20 à 35 crédits."),
  CLOUD, ["Géométrie plus fidèle que Meshy 6 (éditeur)", "Topologie « jeu vidéo » à budget de polygones"],
  ["Classé sous Meshy 6 sur 3D Arena (peu de votes)", "Déprécié au profit de 7.1"],
  [S("https://docs.meshy.ai/en/api/changelog"), arena_src(), arena_topo_src(), fal("meshy/v7/image-to-3d")],
  {"3d_arena_rendu": 1306, "3d_arena_topologie": 1276}, "3D Arena lu le 15/10/2026 : rendu 5e (199 votes), topologie 5e (167 votes).",
  tasks_other=["text_to_3d", "multiview_to_3d"]))

m.append(M("meshy-7-1", "Meshy", "Meshy 7.1", "Meshy", "US", "image_to_3d", "2026-09-18",
  False, None, True, True, I(True, True, False, True), O(True, True, False, None, MESHY_FMT, "Modes standard, low poly, Smart Topology ; géométrie standard, 2k ou 4k"), MESHY_BL, None,
  P("per_generation", 1.20, "fal", "0,80 $ sans texture, 1,20 $ texturé, rigging +0,20 $, animation +0,12 $ ; API Meshy : même coût que Meshy 7, géométrie 2k ou 4k +5 crédits."),
  CLOUD, ["Modèle par défaut (« latest ») de Meshy", "Géométrie 4k", "Chaîne complète : texture, rig, animation, export Blender"],
  ["Pas encore classé sur 3D Arena", "4k indisponible en multivue"],
  [S("https://docs.meshy.ai/en/api/changelog"), fal("meshy/v7.1/image-to-3d"), fal("meshy/v7.1/text-to-3d"), fal("meshy/v7.1/multi-image-to-3d")],
  tasks_other=["text_to_3d", "multiview_to_3d"]))

m.append(M("meshy-6-lite-retexture", "Meshy", "Meshy 6 Lite (retexture)", "Meshy", "US", "texturing", None,
  False, None, True, True, I(True, True, False, False, "Maillage existant + texte ou image de style"), O(True, True, False, None, MESHY_FMT),
  MESHY_BL, None, P("per_generation", 0.30, "fal", "0,30 $ par modèle, PBR inclus ; API Meshy : 10 crédits (2K ou 4K), 15 en 8K pour la texture."),
  CLOUD, ["Retexture un modèle importé (GLB, glTF, OBJ, FBX, STL)", "PBR inclus"], ["Pas de poids publiés"],
  [fal("meshy/v6-lite/retexture"), S("https://docs.meshy.ai/en/api/changelog"), S("https://www.meshy.ai/api")], released_note="Sur fal depuis le 06/10/2026."))

m.append(M("meshy-rigging-animation", "Meshy", "Auto-rigging + animation", "Meshy", "US", "rigging_animation", None,
  False, None, True, True, I(False, False, False, False, "Personnage humanoïde en GLB"), O(True, None, False, True, ["GLB", "FBX"]),
  MESHY_BL, None, P("per_request", 0.20, "fal", "Rigging 0,20 $, +0,12 $ par clip d'animation ; API Meshy : rigging 5 crédits, animation 3 crédits."),
  CLOUD, ["Rig et bibliothèque de mouvements en un appel", "Accepte un mouvement généré par texte"], ["Humanoïdes seulement"],
  [fal("fal-ai/meshy/rigging"), fal("fal-ai/meshy/rigging/multi-animation"), S("https://www.meshy.ai/api")]))

m.append(M("meshy-text-to-motion", "Meshy", "Text to Motion", "Meshy", "US", "rigging_animation", "2026-08-21",
  False, None, True, True, I(False, True, False, False), O(False, False, False, True, ["FBX", "BVH"], None, "Clip de mouvement de 2 à 10 s"),
  B("import_direct", "FBX et BVH s'importent dans Blender."), None,
  P("credits", None, "Meshy", "Mode prime 10 crédits (FBX), mode swift 3 crédits (BVH)."), CLOUD,
  ["Mouvement décrit en texte, applicable ensuite à un personnage riggé"], ["Bipèdes", "Pas de poids publiés"],
  [S("https://docs.meshy.ai/en/api/changelog")]))

# ---------------- Hyper3D Rodin ----------------
RODIN_BL = B("addon", "Add-on Blender Hyper3D listé parmi les plug-ins officiels.")
m.append(M("rodin-gen-2", "Rodin (Hyper3D)", "Gen-2", "Deemos Tech", "CN", "image_to_3d", "2025-10-01",
  False, None, True, True, I(True, True, False, True), O(True, True, False, None, []), RODIN_BL, None,
  P("per_generation", None, "fal", "fal-ai/hyper3d/rodin/v2 actif, prix non affiché le 15/10/2026. Hyper3D : Creator 30 $/mois, Business 120 $/mois avec API."),
  CLOUD, ["10 milliards de paramètres annoncés", "Édition de modèle par texte (Gen-2 Edit, mars 2026)"], ["API réservée à l'offre Business"],
  [S("https://markets.financialcontent.com/pennwell.pennenergy/article/pressadvantage-2025-10-1-deemos-tech-launches-hyper3d-rodin-gen-2-next-generation-3d-model-generator", "2025-10-01"), S("https://hyper3d.ai/pricing"), fal("fal-ai/hyper3d/rodin/v2")],
  tasks_other=["text_to_3d", "multiview_to_3d"]))

m.append(M("rodin-gen-2-5", "Rodin (Hyper3D)", "Gen-2.5", "Deemos Tech", "CN", "image_to_3d", None,
  False, None, True, True, I(True, True, False, True), O(True, True, False, None, []), RODIN_BL, None,
  P("per_generation", 0.40, "fal", "0,40 $, option HighPack +0,80 $ ; version Fast 0,10 $ ; WaveSpeed annonce dès 0,48 $."),
  CLOUD, ["Version Fast à 0,10 $ pour le blocage", "Niveaux de qualité réglables"], ["Annonce éditeur non trouvée", "Pas de poids publiés"],
  [fal("fal-ai/hyper3d/rodin/v2.5"), fal("fal-ai/hyper3d/rodin/v2.5/fast"), S("https://wavespeed.ai/hyper-3d-studio", D, "independant"), S("https://www.sloyd.ai/blog/ai-3d-model-generator-rankings", "2026-08-03", "independant")],
  scores_note="Classement « Top 3D AI » cité par Sloyd (concurrent) : Rodin Gen 2.5 6e à 1009 (03/08/2026).",
  tasks_other=["text_to_3d"], released_note="Sur fal depuis le 28/05/2026."))

# ---------------- Autres image vers 3D ----------------
m.append(M("csm-cube", "CSM Cube", "Cube", "Common Sense Machines", "US", "image_to_3d", None,
  False, None, None, None, I(True, True, None, None), O(None, None, None, None, []), B(None), None, P(), CLOUD,
  [], ["Site csm.ai injoignable le 15/10/2026 (nom de domaine sans réponse web) ; aucune actualité 2026 trouvée"],
  [S("https://csm.ai/academy/what-is-cube-by-csm", D, "editeur")],
  status_note="Statut non confirmé : site injoignable au relevé, ne pas conclure à un arrêt sans source."))

m.append(M("luma-genie", "Luma Genie", "Genie", "Luma AI", "US", "text_to_3d", None,
  False, None, None, None, I(None, True, None, None), O(True, None, None, None, []), B(None), "Moins de 10 s annoncées au lancement.", P(), CLOUD,
  [], ["lumalabs.ai/genie redirige vers l'accueil le 15/10/2026 : produit plus mis en avant", "Luma concentré sur la vidéo (Ray)"],
  [S("https://lumalabs.ai/genie", D, "editeur")],
  status_note="Page produit retirée au relevé du 15/10/2026 ; disponibilité non confirmée."))

m.append(M("stable-fast-3d", "Stability 3D", "Stable Fast 3D (SF3D)", "Stability AI", "GB", "image_to_3d", None,
  True, "Stability AI Community License (gratuit sous 1 M$ de revenu annuel)", True, False, I(True, False, False, False), O(True, None, False, False, ["GLB"], None, "Maillage UV déplié texturé"),
  B("import_direct"), None, P(), L(None, None, None, "Dépôt officiel, ComfyUI", None),
  ["Licence commerciale gratuite sous 1 M$ de revenu annuel", "Maillage UV déplié"], ["15e au rendu, 16e en topologie sur 3D Arena", "Accès Hugging Face soumis à acceptation"],
  [S("https://huggingface.co/stabilityai/stable-fast-3d"), arena_src(), arena_topo_src()],
  {"3d_arena_rendu": 1175, "3d_arena_topologie": 1061}, "3D Arena lu le 15/10/2026 : rendu 15e (8035 votes), topologie 16e (839 votes).",
  released_note="Fiche Hugging Face créée le 17/07/2024."))

m.append(M("spar3d", "Stability 3D", "SPAR3D", "Stability AI", "GB", "image_to_3d", "2025-01-08",
  True, "Stability AI Community License (gratuit sous 1 M$ de revenu annuel)", True, False, I(True, False, False, False, "Nuage de points éditable"), O(True, True, False, False, ["GLB"], None, "Maillage UV texturé, rugosité et métal par objet"),
  B("import_direct"), "Moins d'une seconde par objet (éditeur).", P(), L(None, None, None, "Dépôt officiel", None),
  ["Moins d'une seconde", "Dos de l'objet corrigeable via le nuage de points"], ["Qualité dépassée (19e au rendu sur 3D Arena)"],
  [S("https://huggingface.co/stabilityai/stable-point-aware-3d"), arena_src(), arena_topo_src()],
  {"3d_arena_rendu": 1113, "3d_arena_topologie": 1159}, "3D Arena lu le 15/10/2026 : rendu 19e (4928 votes), topologie 10e (854 votes)."))

m.append(M("partcrafter", "PartCrafter", "PartCrafter", None, None, "image_to_3d", "2025-07-13",
  True, "MIT", False, False, I(True, False, False, False), O(True, False, False, False, [], None, "Plusieurs maillages par parties en une passe, objet ou scène"),
  B("import_direct"), None, P(), L(True, True, None, "Dépôt officiel", "GPU CUDA d'au moins 8 Go (README)."),
  ["Pièces séparées dès la génération (utile pour animer un accessoire)", "NeurIPS 2025, licence MIT"], ["Pas de texture documentée", "Format de sortie non précisé"],
  [S("https://github.com/wgsxm/PartCrafter"), S("https://huggingface.co/wgsxm/PartCrafter")]))

m.append(M("step1x-3d", "Step1X-3D", "Step1X-3D (géométrie 1,3B + texture 3,5B)", "StepFun", "CN", "image_to_3d", "2025-05-13",
  True, "Apache-2.0", False, False, I(True, False, False, False), O(True, None, False, False, ["GLB"]),
  B("import_direct"), "152 s pour 50 pas (éditeur).", P(),
  L(True, False, None, "Dépôt officiel", "27 à 29 Go pour géométrie + texture (README) : au-delà d'une 4090."),
  ["Apache-2.0, usage commercial libre", "Code d'entraînement publié"], ["Plus de mise à jour depuis juin 2025", "PBR non confirmé"],
  [S("https://github.com/stepfun-ai/Step1X-3D")]))

m.append(M("sparc3d", "Sparc3D", "Sparc3D (recherche)", "Math Magic, NTU, Imperial College", "CN", "image_to_3d", None,
  False, None, False, False, I(True, False, False, False), O(True, None, False, False, []), B(None), None, P(), CLOUD,
  ["Géométrie très haute résolution (base de Hitem3D)"], ["Code annoncé mais jamais publié ; exploité commercialement via Hitem3D"],
  [S("https://www.gamebusiness.jp/article/2025/06/27/24512.html", "2025-06-27", "independant"), S("https://blog.hitem3d.ai/blog/sparc3d/")],
  released_note="Annoncé le 13/06/2025."))

m.append(M("hi3d-v3-0", "Hitem3D (Hi3D)", "Hi3D V3.0", "Math Magic", "CN", "image_to_3d", None,
  False, None, True, True, I(True, False, False, True), O(True, True, False, None, ["GLB", "OBJ"], "Géométrie jusqu'à 2048³"), B("import_direct"), None,
  P("per_generation", 2.10, "fal", "2,10 $ en qualité 2048³, 9,10 $ en master ; crédit à 0,02 $."), CLOUD,
  ["Géométrie la plus fine annoncée (2048³)", "Outils de découpe en parties et de texture"], ["Cher en mode master", "Pas de poids publiés"],
  [fal("hitem3d/hi3d/v3.0/image-to-3d"), S("https://www.thailand-business-news.com/pr-news/math-magic-closes-series-a-raising-nearly-50-million-across-two-rounds-in-six-months", "2026-08-20", "independant")],
  tasks_other=["multiview_to_3d"], released_note="Vers le 19/08/2026 selon le communiqué ; sur fal depuis le 19/08/2026."))

m.append(M("direct3d-s2", "Direct3D-S2", "Direct3D-S2 v1.1", "DreamTech", "CN", "image_to_3d", "2025-05-30",
  True, "MIT", False, False, I(True, False, False, False), O(True, False, False, False, ["OBJ"], "Résolution 1024³"),
  B("import_direct"), "Environ 2 fois plus rapide que la v1.0 (éditeur).", P(),
  L(True, None, None, "Dépôt officiel", "Au moins 10 Go en 512, environ 24 Go en 1024 (README)."),
  ["Géométrie fine en 1024³", "Licence MIT"], ["Forme seule", "La 1024 frôle les 24 Go"],
  [S("https://github.com/DreamTechAI/Direct3D-S2")]))

m.append(M("pixal3d", "Pixal3D", "Pixal3D (base TRELLIS.2)", "Tencent ARC et Tsinghua", "CN", "image_to_3d", None,
  True, "MIT (composants tiers sous leurs licences)", True, False, I(True, False, False, False), O(True, True, False, False, []), B("import_direct"), None,
  P("per_generation", 0.30, "fal", "0,30 $ en 1024, 0,42 $ en 1536."), L(None, None, None, "Dépôt officiel, nœuds ComfyUI communautaires", None),
  ["Licence MIT, contrairement aux autres modèles Tencent", "13e au rendu et 9e en topologie sur 3D Arena"], ["Licence MIT relevée via des sources secondaires et la fiche HF"],
  [S("https://huggingface.co/TencentARC/Pixal3D"), arena_src(), arena_topo_src(), fal("fal-ai/pixal3d")],
  {"3d_arena_rendu": 1265, "3d_arena_topologie": 1221}, "3D Arena lu le 15/10/2026 : rendu 13e (321 votes), topologie 9e (251 votes).",
  released_note="Mai 2026 (fiche Hugging Face) ; sur fal depuis le 13/05/2026."))

m.append(M("picgen3d", "PicGen3D", "PicGen3D", None, None, "image_to_3d", None,
  False, None, None, None, I(True, None, None, None), O(None, None, None, None, []), B(None), None, P(), L(),
  ["1er au rendu de 3D Arena au 15/10/2026"], ["Éditeur, accès et prix introuvables"],
  [arena_src()], {"3d_arena_rendu": 1416}, "3D Arena lu le 15/10/2026 : rendu 1er (4373 votes), marqué non open source.",
  status_note="Présent seulement dans le classement ; aucune page produit trouvée."))

m.append(M("404-gen", "404-GEN", "404-GEN (Bittensor sous-réseau 17)", "404 (Bittensor SN17)", None, "image_to_3d", None,
  False, None, None, True, I(True, None, None, None), O(None, None, None, None, []), B(None), None, P(), L(),
  ["4e au rendu de 3D Arena"], ["Réseau décentralisé à jeton, informations surtout issues de réseaux sociaux"],
  [arena_src(), S("https://404-gen-readme.static.hf.space/README.md", "2025-04-14")],
  {"3d_arena_rendu": 1334}, "3D Arena lu le 15/10/2026 : rendu 4e (1449 votes), marqué non open source."))

m.append(M("sam-3d-objects", "SAM 3D", "SAM 3D Objects", "Meta", "US", "image_to_3d", "2025-11-19",
  True, "SAM License (accès sur demande)", True, False, I(True, False, False, False, "Image + masque de l'objet, plusieurs objets"), O(None, None, True, False, ["PLY (Gaussiennes)"], None, "Forme, texture, pose et place dans la scène"),
  B("addon", "Gaussiennes : add-on de splats nécessaire."), None,
  P("per_unit", 0.02, "fal", "0,02 $ par unité."), L(None, None, None, "Dépôt officiel", None),
  ["Objets tirés d'une vraie photo, à leur place dans la scène", "12e au rendu de 3D Arena"], ["Sortie Gaussiennes dans l'exemple officiel", "Poids sur demande"],
  [S("https://github.com/facebookresearch/sam-3d-objects"), arena_src(), fal("fal-ai/sam-3/3d-objects")],
  {"3d_arena_rendu_3dgs": 1267}, "3D Arena lu le 15/10/2026 : « SAM-3D-Objects-3DGS » 12e (1406 votes)."))

m.append(M("sam-3d-body", "SAM 3D", "SAM 3D Body", "Meta", "US", "image_to_3d", None,
  None, None, True, False, I(True, False, False, False), O(True, False, False, None, [], None, "Forme et position du corps humain"),
  B("import_direct"), None, P("per_unit", 0.02, "fal", "0,02 $ par unité."), L(),
  ["Pose d'un acteur depuis une seule image, utile pour bloquer une scène"], ["Licence non relue (fiche HF fermée)"],
  [fal("fal-ai/sam-3/3d-body")], released_note="Sur fal depuis le 02/12/2025."))

# ---------------- Mondes ----------------
MARBLE_BL = B("addon", "Splats via add-on Gaussian Splatting (doc officielle Blender) ; maillage GLB en import direct.")
MARBLE_OUT = O(True, False, True, False, ["SPZ", "PLY", "GLB (collision)", "GLB texturé (Pro)", "panorama 360"], "Maillage haute qualité vers 600 k triangles texturé ou 1 M en couleurs de sommets")
MARBLE_SRC = [S("https://docs.worldlabs.ai/marble/models"), S("https://docs.worldlabs.ai/marble/release-notes"), S("https://docs.worldlabs.ai/api/pricing"), S("https://docs.worldlabs.ai/marble/export/mesh"), S("https://docs.worldlabs.ai/marble/support/account-billing")]
MARBLE_IN = I(True, True, True, True, "Panorama, maquette 3D grossière (Chisel)")
m.append(M("marble-1-1", "Marble (World Labs)", "Marble 1.1", "World Labs", "US", "image_to_world", "2026-04-02",
  False, None, True, True, MARBLE_IN, MARBLE_OUT, MARBLE_BL, "Maillage haute qualité : jusqu'à 1 h de calcul (doc).",
  P("per_generation", 1.20, "World Labs API", "1500 crédits par génération, crédits API à 1 $ les 1250. Application : offres Free, Standard, Pro (export GLB texturé et droits commerciaux), Max."),
  CLOUD, ["Monde persistant exportable en splats et en maillage", "Blocage 3D grossier transformé en décor (Chisel)", "Caméras et vidéos de survol (Record)"],
  ["Maillage moins propre que les splats (doc)", "Export impossible en offre gratuite", "Crédits app et API séparés"],
  MARBLE_SRC, tasks_other=["scene_reconstruction"]))
m.append(M("marble-1-1-plus", "Marble (World Labs)", "Marble 1.1 Plus", "World Labs", "US", "image_to_world", "2026-04-02",
  False, None, True, True, MARBLE_IN, MARBLE_OUT, MARBLE_BL, None,
  P("per_generation", 1.20, "World Labs API", "1500 crédits de base + 0 à 1500 variables, soit 1,20 à 2,40 $ via l'API."),
  CLOUD, ["Mondes les plus grands de la gamme"], ["Coût variable"], MARBLE_SRC))
m.append(M("marble-1-0-draft", "Marble (World Labs)", "Marble 1.0 Draft", "World Labs", "US", "image_to_world", None,
  False, None, True, True, MARBLE_IN, MARBLE_OUT, MARBLE_BL, "Modèle le plus rapide de la gamme (doc).",
  P("per_generation", 0.12, "World Labs API", "150 crédits par génération."), CLOUD,
  ["Dix fois moins cher, pour tester des cadrages"], ["Qualité brouillon"], MARBLE_SRC))

m.append(M("genie-3", "Genie (Google DeepMind)", "Genie 3 (Project Genie)", "Google DeepMind", "US", "image_to_world", "2025-08-05",
  False, None, False, True, I(True, True, False, False), O(False, False, False, False, ["vidéo"], None, "Monde explorable en temps réel, 720p, 20 à 24 images/s"),
  B("none", "Aucun export 3D : seules les vidéos se téléchargent."), "Temps réel ; sessions de 60 s.",
  P("subscription", 250, "Google AI Ultra", "Inclus dans Google AI Ultra (environ 250 $/mois selon la presse)."), CLOUD,
  ["Exploration interactive en première ou troisième personne", "Mémoire de plusieurs minutes"],
  ["États-Unis seulement, 18 ans et plus (janvier 2026)", "Pas de géométrie exportable"],
  [S("https://deepmind.google/models/genie/"), S("https://blog.google/innovation-and-ai/models-and-research/google-deepmind/project-genie/", "2026-01-29"), S("https://startupintros.com/news/2026-01-29-google-project-genie", "2026-01-29", "independant")],
  released_note="Annoncé le 05/08/2025 ; Project Genie ouvert le 29/01/2026."))

HYW_LIC = "Tencent HY-WORLD 2.0 Community License (" + TENCENT_LIC_NOTE + ")"
m.append(M("hy-world-2-0", "HunyuanWorld", "HY-World 2.0", "Tencent", "CN", "image_to_world", "2026-04-15",
  True, HYW_LIC, False, True, I(True, True, True, True), O(True, False, True, False, ["PLY (Gaussiennes)", "panorama 360"], None, "Maillage, 3DGS, nuage de points, caméras"),
  B("import_direct", "Import Blender, Unity, Unreal annoncé, sans procédure détaillée."), None, P(),
  L(None, None, None, "Dépôt officiel (CUDA 12.8)", "HY-Pano-2 environ 80 milliards de paramètres, WorldStereo-2 environ 17 milliards : poids lourds pour une carte grand public."),
  ["Chaîne ouverte complète texte ou image vers monde navigable", "Collision physique"], ["Licence inapplicable en France (UE exclue)", "Très gros modèles"],
  [S("https://github.com/Tencent-Hunyuan/HY-World-2.0"), S("https://raw.githubusercontent.com/Tencent-Hunyuan/HY-World-2.0/main/License.txt")],
  tasks_other=["scene_reconstruction"]))
m.append(M("hy-world-2-1", "HunyuanWorld", "HY World 2.1", "Tencent", "CN", "image_to_world", None,
  False, None, None, True, I(True, None, None, None), O(None, None, None, None, []), B(None), None, P(), CLOUD,
  ["Mise à jour accessible sur le site Tencent (sceneTo3D)"], ["Aucun détail technique publié"],
  [S("https://github.com/Tencent-Hunyuan/HY-World-2.0")], released_note="Juillet 2026 (README)."))
m.append(M("hunyuanworld-1-0", "HunyuanWorld", "HunyuanWorld 1.0", "Tencent", "CN", "image_to_world", "2025-07-27",
  True, "Tencent HunyuanWorld-1.0 Community License (" + TENCENT_LIC_NOTE + ")", True, False, I(True, True, False, False), O(True, None, None, False, ["panorama"], None, "Panorama ou monde 3D en couches"),
  B("import_direct"), None, P("per_generation", None, "fal", "fal-ai/hunyuan_world/image-to-world actif, prix non affiché."), L(),
  ["Premier monde 3D ouvert de Tencent"], ["Licence inapplicable en France", "Dépassé par la 2.0"],
  [S("https://raw.githubusercontent.com/Tencent-Hunyuan/HunyuanWorld-1.0/main/LICENSE"), fal("fal-ai/hunyuan_world/image-to-world")]))

# ---------------- Reconstruction de scène ----------------
m.append(M("worldmirror-2-0", "HunyuanWorld", "WorldMirror 2.0", "Tencent", "CN", "scene_reconstruction", "2026-04-16",
  True, HYW_LIC, False, False, I(True, False, True, True, "A priori caméra, profondeur, intrinsèques"), O(None, False, True, False, ["PLY (Gaussiennes)", "COLMAP"], None, "Profondeur, normales, caméras, nuage de points, 3DGS"),
  B("import_direct", "Caméras COLMAP et nuage de points importables via add-ons Blender."), None, P(),
  L(None, None, None, "Dépôt HY-World-2.0", "Environ 1,2 milliard de paramètres ; 50 k à 500 k pixels par image."),
  ["Photos ou vidéo vers caméras et splats en une passe", "Accepte des caméras connues"], ["Licence inapplicable en France (UE exclue)", "VRAM non publiée"],
  [S("https://github.com/Tencent-Hunyuan/HY-World-2.0"), S("https://github.com/Tencent-Hunyuan/HunyuanWorld-Mirror")]))
m.append(M("worldmirror-1-0", "HunyuanWorld", "WorldMirror 1.0", "Tencent", "CN", "scene_reconstruction", "2025-10-22",
  True, "Tencent HunyuanWorld-Mirror Community License (" + TENCENT_LIC_NOTE + ")", False, False, I(True, False, True, True, "A priori caméra, profondeur, intrinsèques"), O(None, False, True, False, ["COLMAP", "PLY (Gaussiennes)"]),
  B("import_direct"), None, P(), L(),
  ["Export COLMAP direct"], ["Remplacé par 2.0", "Licence inapplicable en France"],
  [S("https://github.com/Tencent-Hunyuan/HunyuanWorld-Mirror"), S("https://raw.githubusercontent.com/Tencent-Hunyuan/HunyuanWorld-Mirror/main/License.txt")]))

MA_IN = I(True, False, False, True, "Intrinsèques, poses, profondeur optionnelles")
MA_OUT = O(None, False, False, False, ["COLMAP", "GLB", "PLY"], None, "Géométrie métrique et caméras ; entraînement gsplat ensuite")
m.append(M("mapanything-apache", "MapAnything", "map-anything-apache", "Meta", "US", "scene_reconstruction", None,
  True, "Apache-2.0", False, False, MA_IN, MA_OUT, B("import_direct", "GLB direct ; COLMAP via add-on."), None, P(),
  L(None, None, None, "Dépôt officiel", "Mode économe : jusqu'à 2000 vues sur 140 Go (README)."),
  ["Variante utilisable commercialement", "Prend des caméras ou profondeurs connues"], ["Pas de tableau de VRAM publié"],
  [S("https://github.com/facebookresearch/map-anything"), S("https://huggingface.co/facebook/map-anything-apache")], released_note="Version V1, septembre 2025 (README)."))
m.append(M("mapanything-nc", "MapAnything", "map-anything (CC-BY-NC)", "Meta", "US", "scene_reconstruction", None,
  True, "CC-BY-NC 4.0", False, False, MA_IN, MA_OUT, B("import_direct"), None, P(), L(),
  ["Recommandée pour la recherche"], ["Non commercial"],
  [S("https://github.com/facebookresearch/map-anything"), S("https://huggingface.co/facebook/map-anything")], released_note="Septembre 2025 (README)."))

VG_OUT = O(None, False, False, False, ["COLMAP"], None, "Caméras, profondeur, cartes de points, suivi de points")
m.append(M("vggt-1b-commercial", "VGGT", "VGGT-1B-Commercial", "Meta et Oxford VGG", "US", "scene_reconstruction", None,
  True, "Licence VGGT (usage commercial permis hors militaire, accès sur formulaire)", False, False, I(True, False, False, True), VG_OUT,
  B("import_direct", "COLMAP puis gsplat."), "Moins d'une seconde par scène en général (README).", P(), L(),
  ["Seul checkpoint VGGT utilisable commercialement", "Sortie COLMAP directe"], ["Accès sur demande"],
  [S("https://github.com/facebookresearch/vggt"), S("https://huggingface.co/facebook/VGGT-1B-Commercial")], released_note="Fiche Hugging Face créée le 21/07/2025."))
m.append(M("vggt-1b", "VGGT", "VGGT-1B", "Meta et Oxford VGG", "US", "scene_reconstruction", None,
  True, "CC-BY-NC 4.0", False, False, I(True, False, False, True), VG_OUT, B("import_direct"), "Moins d'une seconde par scène en général (README).", P(), L(),
  ["Référence de la reconstruction en une passe (CVPR 2025)"], ["Non commercial"],
  [S("https://github.com/facebookresearch/vggt"), S("https://huggingface.co/facebook/VGGT-1B")], released_note="Fiche Hugging Face créée le 11/03/2025."))
m.append(M("vggt-omega", "VGGT", "VGGT-Omega", "Meta et Oxford VGG", "US", "scene_reconstruction", None,
  True, None, False, False, I(True, False, False, True), VG_OUT, B(None), None, P(), L(),
  ["Successeur de VGGT (CVPR 2026 oral)"], ["Accès sur demande, refus signalés", "Licence non lue"],
  [S("https://github.com/facebookresearch/vggt"), S("https://huggingface.co/facebook/VGGT-Omega", D, "editeur")], released_note="Annoncé dans le dépôt VGGT le 18/05/2026."))

DA3_SRC = [S("https://github.com/ByteDance-Seed/Depth-Anything-3")]
DA3_OUT = O(None, False, True, False, ["GLB", "PLY", "NPZ"], None, "Profondeur, poses caméra, Gaussiennes")
DA3_BL = B("addon", "Add-on communautaire DA3-blender ; nœuds ComfyUI.")
for vid, var, p, lic, ow_note in [
  ("da3-nested-giant-large-1-1", "DA3NESTED-GIANT-LARGE-1.1", "1,40 milliard", "CC-BY-NC 4.0", "Version la plus complète, métrique"),
  ("da3-giant-1-1", "DA3-GIANT-1.1", "1,15 milliard", "CC-BY-NC 4.0", "Toutes vues"),
  ("da3-large-1-1", "DA3-LARGE-1.1", "0,35 milliard", "CC-BY-NC 4.0", "Toutes vues"),
  ("da3-base", "DA3-BASE", "0,12 milliard", "Apache-2.0", "Toutes vues, commercial"),
  ("da3-small", "DA3-SMALL", "0,08 milliard", "Apache-2.0", "Toutes vues, commercial")]:
  m.append(M(vid, "Depth Anything 3", var, "ByteDance Seed", "CN", "scene_reconstruction", "2025-11-14",
    True, lic, False, False, I(True, False, True, True, "Poses caméra optionnelles"), DA3_OUT, DA3_BL, None, P(),
    L(None, None, None, "Dépôt officiel, ComfyUI-DepthAnythingV3", "DA3-Streaming : moins de 12 Go pour les très longues vidéos (README)."),
    [ow_note + " (" + p + " de paramètres)", "Vidéo vers profondeur cohérente et caméras"],
    (["Non commercial"] if "NC" in lic else ["Moins précis que les grandes variantes"]) + ["Préférer les versions « 1.1 » (bug d'entraînement corrigé)"] if "1-1" in vid else (["Non commercial"] if "NC" in lic else ["Moins précis que les grandes variantes"]),
    DA3_SRC, tasks_other=["depth_and_camera"]))

# ---------------- Profondeur et caméra ----------------
for vid, var, lic in [("da3-metric-large", "DA3METRIC-LARGE", "Apache-2.0"), ("da3-mono-large", "DA3MONO-LARGE", "Apache-2.0")]:
  m.append(M(vid, "Depth Anything 3", var, "ByteDance Seed", "CN", "depth_and_camera", "2025-11-14",
    True, lic, False, False, I(True, False, False, False), O(False, False, False, False, ["NPZ", "images de profondeur"], None, "Profondeur métrique" if "METRIC" in var else "Profondeur relative"),
    DA3_BL, None, P(), L(None, None, None, "Dépôt officiel, ComfyUI", None),
    ["Monoculaire, licence commerciale", "0,35 milliard de paramètres"], ["Une image à la fois"], DA3_SRC))

MOGE_SRC = [S("https://github.com/microsoft/MoGe")]
MOGE_OUT = O(None, False, False, False, ["GLB", "PLY"], None, "Carte de points métrique, profondeur, intrinsèques, normales")
for vid, var, p in [("moge-2-vitl-normal", "MoGe-2 ViT-L normal", "331 M"), ("moge-2-vitl", "MoGe-2 ViT-L", "326 M"), ("moge-2-vitb-normal", "MoGe-2 ViT-B normal", "104 M"), ("moge-2-vits-normal", "MoGe-2 ViT-S normal", "35 M")]:
  m.append(M(vid, "MoGe", var, "Microsoft", "US", "depth_and_camera", None,
    True, "MIT (code ; licence des poids non précisée hors fiche HF)", False, False, I(True, False, False, False, "Champ de vision connu optionnel"), MOGE_OUT,
    B("import_direct", "GLB texturé ou PLY en couleurs de sommets."), "60 ms par image annoncés (A100 ou RTX 3090, FP16, ViT-L), version non précisée.", P(),
    L(None, None, None, "moge infer --version v2", None),
    [p + " paramètres", "Échelle métrique et focale estimées d'une seule image"], ["Remplacé par MoGe-3 pour le détail fin"],
    MOGE_SRC + ([S("https://huggingface.co/Ruicheng/" + vid.replace("moge-2-", "moge-2-"))] if False else []), released_note="arXiv 2507.02546 (juillet 2025)."))
for vid, var, p in [("moge-3-vitg", "MoGe-3 ViT-G", "1,25 milliard"), ("moge-3-vitl", "MoGe-3 ViT-L", "370 M")]:
  m.append(M(vid, "MoGe", var, "Microsoft", "US", "depth_and_camera", "2026-08-18",
    True, "MIT (code ; licence des poids non précisée)", False, False, I(True, False, False, False), MOGE_OUT,
    B("import_direct"), None, P(), L(None, None, False, "moge infer (v3 par défaut)", "macOS non pris en charge (FlexGEMM sur Triton)."),
    [p + " paramètres", "Géométrie fine améliorée par raffinement"], ["Pas sur Mac"], MOGE_SRC))

m.append(M("depth-pro", "Depth Pro", "Depth Pro", "Apple", "US", "depth_and_camera", None,
  True, "Apple AMLR (licence de recherche Apple)", False, False, I(True, False, False, False), O(False, False, False, False, [], None, "Profondeur métrique en mètres et focale en pixels, 2,25 mégapixels"),
  B("none", "Carte de profondeur à convertir (displacement, nuage de points)."), "0,3 s pour une carte de 2,25 Mpx sur un GPU standard (éditeur).", P(), L(),
  ["Focale estimée sans métadonnées", "Bords nets"], ["Licence de recherche"],
  [S("https://github.com/apple/ml-depth-pro"), S("https://huggingface.co/apple/DepthPro")], released_note="ICLR 2025 ; fiche Hugging Face créée le 03/10/2024."))

m.append(M("geocalib", "GeoCalib", "GeoCalib (pinhole et distorted)", "ETH Zurich (CVG)", "CH", "depth_and_camera", None,
  True, "Code Apache-2.0, poids CC-BY-4.0", False, False, I(True, False, True, False, "Focale ou gravité connues optionnelles ; plusieurs images d'une même caméra"), O(False, False, False, False, [], None, "Focale, gravité (roulis, tangage), distorsion radiale ou fisheye"),
  B("none", "Valeurs à reporter dans la caméra Blender."), None, P(), L(None, None, None, "Dépôt officiel, démo webcam", None),
  ["Retrouve la focale et l'horizon d'un plan pour caler une caméra 3D", "Modèles fisheye"], ["Point principal fixé au centre"],
  [S("https://github.com/cvg/GeoCalib")], released_note="ECCV 2024."))

# ---------------- Animation ----------------
m.append(M("animateanymesh", "AnimateAnyMesh", "AnimateAnyMesh", "HUST et Alibaba DAMO", "CN", "rigging_animation", None,
  True, "Apache-2.0", False, False, I(False, True, False, False, "Maillage statique GLB"), O(True, False, False, False, ["FBX", "ABC"], None, "Animation de sommets sans squelette"),
  B("import_direct", "FBX ou Alembic dans Blender."), "Quelques secondes par maillage (README).", P(), L(None, None, None, "Dépôt officiel (CUDA 11.8+)", None),
  ["Anime n'importe quel maillage par texte, sans rig", "Apache-2.0"], ["GLB seul en entrée", "Pas de squelette éditable"],
  [S("https://github.com/JarrentWu1031/AnimateAnyMesh")], released_note="Poids publiés le 22/08/2025 ; ICCV 2025."))

m.append(M("hunyuan-motion", "Hunyuan Motion", "Hunyuan Motion 1B et 0,46B (fast)", "Tencent", "CN", "rigging_animation", None,
  None, None, True, False, I(False, True, False, False), O(False, False, False, True, [], None, "Mouvement humain 3D"),
  B(None), None, P("per_generation", None, "fal", "Prix non affiché sur fal le 15/10/2026."), L(),
  ["Mouvement humain par texte"], ["Licence et format non relus"],
  [fal("fal-ai/hunyuan-motion")], released_note="Sur fal depuis le 30/12/2025."))

# ---------------- Texture ----------------
m.append(M("hunyuan3d-paint-2-1", "Hunyuan3D", "Paint 2.1", "Tencent", "CN", "texturing", "2025-06-13",
  True, "Tencent Hunyuan 3D 2.1 Community License (" + TENCENT_LIC_NOTE + ")", False, False, I(True, False, False, False, "Maillage existant + image"), O(True, True, False, False, ["GLB"]),
  B("import_direct"), None, P(), L(True, True, None, "Dépôt Hunyuan3D-2.1", "Environ 21 Go pour la texture (README)."),
  ["Texture PBR sur un maillage existant, en local"], ["Licence inapplicable en France"],
  [S("https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1")]))
m.append(M("hi3d-texture", "Hitem3D (Hi3D)", "Hi3D Texture", "Math Magic", "CN", "texturing", None,
  False, None, True, True, I(True, False, False, False, "Maillage + image de référence"), O(True, True, False, None, []), B("import_direct"), None,
  P("credits", None, "fal", "0,02 $ le crédit ; texture 10 crédits et PBR 5 crédits dans la grille de génération."), CLOUD,
  ["Texture depuis une image de référence"], ["Pas de poids publiés"], [fal("hitem3d/hi3d/texture")], released_note="Sur fal depuis le 31/07/2026."))

for x in m:
  for k in ("pros", "cons"):
    x[k] = [s for s in x[k] if s]

ids = [x["id"] for x in m]
assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
txt = json.dumps(m, ensure_ascii=False, indent=1)
assert "—" not in txt and "–" not in txt
out = str(__import__("pathlib").Path(__file__).resolve().parent.parent / "data" / "3d-models.json")
open(out, "w").write(txt + "\n")
from collections import Counter
print(len(m), Counter(x["task"] for x in m))
