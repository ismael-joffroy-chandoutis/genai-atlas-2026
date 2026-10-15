<title>Atlas génératif 2026</title>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,650&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout : en-tête, onglets (Choisir, Vidéo, Image, Audio, 3D, Plateformes, Prix, GPU), filtres, table triable sur grand écran et cartes sur téléphone, barre de comparaison en bas */
:root{
  --bg:#f2f3ef; --surface:#ffffff; --fg:#1b221e; --muted:#5b665f; --line:#d4dad5;
  --accent:#1f6f5c; --accent-soft:#e0eee8; --warn:#9c5418; --warn-soft:#f6e8da; --bad:#a3322e; --bad-soft:#f7e1df;
  --display:"Fraunces", Georgia, serif; --body:"IBM Plex Sans", system-ui, sans-serif; --mono:"IBM Plex Mono", ui-monospace, monospace;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --bg:#131816; --surface:#1b2220; --fg:#e3e8e4; --muted:#98a49d; --line:#323e38;
  --accent:#6cc3a8; --accent-soft:#1e3a32; --warn:#e3a26a; --warn-soft:#3a2b1e; --bad:#ef8a83; --bad-soft:#3d2321; color-scheme:dark } }
:root[data-theme="dark"]{
  --bg:#131816; --surface:#1b2220; --fg:#e3e8e4; --muted:#98a49d; --line:#323e38;
  --accent:#6cc3a8; --accent-soft:#1e3a32; --warn:#e3a26a; --warn-soft:#3a2b1e; --bad:#ef8a83; --bad-soft:#3d2321; color-scheme:dark }
body{background:var(--bg);color:var(--fg);font-family:var(--body);font-size:14px;line-height:1.45}
.wrap{max-width:1500px;margin:0 auto;padding-block:20px 90px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:flex;flex-direction:column;gap:16px}
h1{font-family:var(--display);font-weight:650;font-size:clamp(26px,4vw,40px);margin:0;line-height:1.1}
h2{font-family:var(--display);font-weight:500;font-size:20px;margin:0}
.lede{color:var(--muted);max-width:80ch;margin:6px 0 0}
.meta{font-family:var(--mono);font-size:12px;color:var(--muted)}
.tabs{display:flex;gap:6px;overflow-x:auto;padding-bottom:2px;scrollbar-width:none}
.tabs button{flex:0 0 auto;font:500 13px var(--body);padding:7px 14px;border:1px solid var(--line);background:var(--surface);color:var(--fg);border-radius:999px;cursor:pointer}
.tabs button[aria-selected="true"]{background:var(--accent);border-color:var(--accent);color:var(--surface)}
.filters{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;font-size:13px}
.filters input[type=search],.filters input[type=number],.filters select{font:inherit;padding:6px 10px;border:1px solid var(--line);border-radius:6px;background:var(--surface);color:var(--fg)}
.filters input[type=search]{min-width:200px;flex:1 1 200px;max-width:340px}
.filters input[type=number]{width:90px}
.filters label{display:flex;gap:5px;align-items:center;cursor:pointer}
.count{font-family:var(--mono);font-size:12px;color:var(--muted)}
.scroll{overflow:auto;max-height:78vh;border:1px solid var(--line);border-radius:6px;background:var(--surface)}
table{border-collapse:collapse;font-size:12.5px;min-width:100%}
th,td{padding:6px 8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top;white-space:nowrap}
thead th{position:sticky;top:0;background:var(--surface);z-index:2;font:500 11px var(--mono);letter-spacing:.04em;text-transform:uppercase;color:var(--muted);cursor:pointer;user-select:none}
thead th.sorted{color:var(--accent)}
tbody td:first-child,thead th:first-child{position:sticky;left:0;background:var(--surface);z-index:1;border-right:1px solid var(--line)}
thead th:first-child{z-index:3}
td.n{font-family:var(--mono);font-variant-numeric:tabular-nums;text-align:right}
td.wrap{white-space:normal;min-width:220px;max-width:340px}
.y{color:var(--accent);font-weight:600}.no{color:var(--muted)}.q{color:var(--warn)}
.fam{font-weight:600}.var{color:var(--muted);font-size:12px}
tr.row{cursor:pointer} tr.row:hover td{background:var(--accent-soft)}
tr.detail td{white-space:normal;background:var(--bg)}
.det{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;padding:6px 2px}
.det h4{margin:0 0 4px;font:500 11px var(--mono);text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}
.det ul{margin:0;padding-left:16px}.det p{margin:0 0 6px}
.det a{color:var(--accent);word-break:break-all}
.pill{display:inline-block;padding:0 7px;border-radius:999px;font:500 11px var(--mono);white-space:nowrap}
.open{background:var(--accent-soft);color:var(--accent)}.api{background:var(--warn-soft);color:var(--warn)}
.v-fiable{background:var(--accent-soft);color:var(--accent)}.v-tester{background:var(--warn-soft);color:var(--warn)}.v-eviter{background:var(--bad-soft);color:var(--bad)}
.cmp{font:500 12px var(--mono);border:1px solid var(--line);background:var(--surface);color:var(--fg);border-radius:6px;padding:2px 7px;cursor:pointer}
.cmp[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:var(--surface)}
.note{color:var(--muted);font-size:12.5px;max-width:95ch}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:10px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:12px;display:flex;flex-direction:column;gap:6px;min-width:0}
.card .top{display:flex;justify-content:space-between;gap:8px;align-items:flex-start}
.card .name{font-weight:600}.card .sub{color:var(--muted);font-size:12px}
.chips{display:flex;flex-wrap:wrap;gap:4px}
.chip{font:500 11px var(--mono);padding:1px 6px;border-radius:4px;background:var(--bg);color:var(--fg);border:1px solid var(--line)}
.chip.good{background:var(--accent-soft);border-color:transparent;color:var(--accent)}
.chip.bad{background:var(--bad-soft);border-color:transparent;color:var(--bad)}
.card .more{font:500 12px var(--body);color:var(--accent);background:none;border:0;padding:0;cursor:pointer;text-align:left}
.choose{display:grid;grid-template-columns:minmax(240px,320px) 1fr;gap:16px;align-items:start}
.panel{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:14px;display:flex;flex-direction:column;gap:10px;font-size:13px}
.panel fieldset{border:0;margin:0;padding:0;display:flex;flex-direction:column;gap:6px}
.panel legend{font:500 11px var(--mono);text-transform:uppercase;letter-spacing:.05em;color:var(--muted);margin-bottom:4px}
.panel select,.panel input[type=number]{font:inherit;padding:5px 8px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg)}
.panel label{display:flex;gap:6px;align-items:center}
.cmpbar{position:fixed;left:0;right:0;bottom:0;background:var(--surface);border-top:1px solid var(--line);padding:10px max(16px,env(safe-area-inset-right,0px)) calc(10px + env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-left,0px));display:flex;gap:10px;align-items:center;z-index:10;flex-wrap:wrap}
.cmpbar button{font:500 13px var(--body);padding:7px 14px;border-radius:6px;border:1px solid var(--accent);background:var(--accent);color:var(--surface);cursor:pointer}
.cmpbar button.ghost{background:transparent;color:var(--accent)}
.cmptable td{white-space:normal;min-width:180px;max-width:300px}
.cmptable th[scope=row]{font:500 11px var(--mono);text-transform:uppercase;color:var(--muted);white-space:nowrap}
@media (max-width:760px){ .choose{grid-template-columns:1fr} .filters input[type=search]{max-width:none} }
button:focus-visible,input:focus-visible,select:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
</style>

<div class="wrap">
<header>
  <div class="meta" id="built"></div>
  <h1>Atlas génératif 2026</h1>
  <p class="lede">Modèles vidéo, image, audio et 3D, variante par variante : entrées, sorties, classements indépendants, local (RTX 5090, RTX 4090, Mac 128 Go) et prix plateforme par plateforme, avec la fiabilité et la permissivité des plateformes. « ? » = non documenté. Le bouton « + » ajoute un modèle à la comparaison.</p>
</header>
<nav class="tabs" role="tablist" id="tabs">
  <button role="tab" data-tab="choose" aria-selected="true">Choisir</button>
  <button role="tab" data-tab="video" aria-selected="false">Vidéo</button>
  <button role="tab" data-tab="image" aria-selected="false">Image</button>
  <button role="tab" data-tab="audio" aria-selected="false">Audio</button>
  <button role="tab" data-tab="threed" aria-selected="false">3D</button>
  <button role="tab" data-tab="platforms" aria-selected="false">Plateformes</button>
  <button role="tab" data-tab="prices" aria-selected="false">Tous les prix</button>
  <button role="tab" data-tab="gpu" aria-selected="false">GPU à l'heure</button>
</nav>
<div id="view"></div>
<p class="note" id="foot"></p>
</div>
<div class="cmpbar" id="cmpbar" hidden>
  <span id="cmpcount" class="count"></span>
  <button id="cmpgo">Comparer</button>
  <button id="cmpclear" class="ghost">Vider</button>
</div>

<script>
const DATA = /*__DATA__*/null;
const $ = s => document.querySelector(s);
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const g = (o, p) => p.split(".").reduce((a, k) => a == null ? a : a[k], o);
const b = v => v === true ? '<span class="y">oui</span>' : v === false ? '<span class="no">non</span>' : '<span class="q">?</span>';
const n = v => v === null || v === undefined || v === "" ? '<span class="q">?</span>' : esc(typeof v === "object" ? JSON.stringify(v) : v);
const money = v => v == null ? '' : (v < 0.1 ? (+v).toFixed(3) : (+v).toFixed(2));
const isMobile = () => matchMedia("(max-width: 760px)").matches;
const ALL = () => [...DATA.video, ...DATA.image, ...DATA.audio, ...DATA.threed];
const byId = id => ALL().find(m => m.id === id);
const modality = m => DATA.video.includes(m) ? "video" : DATA.image.includes(m) ? "image" : DATA.audio.includes(m) ? "audio" : "threed";
const acc = m => g(m,"access.open_weights") ? '<span class="pill open">ouvert</span>' : (g(m,"access.api") ? '<span class="pill api">API</span>' : n(null));
const name = m => `<span class="fam">${esc(m.family)}</span><br><span class="var">${esc(m.variant)}</span>`;
const loc = (m, k) => { const L = m._local || {}; if (k === "5090") return g(m,"local.runs_on_rtx5090_32gb") ?? L.rtx5090; if (k === "4090") return L.rtx4090_24gb ?? g(m,"local.rtx4090_24gb"); return L.mac_m5max_128gb ?? g(m,"local.mac_m5max_128gb"); };
const scoreList = m => { const S = Object.assign({}, m._scores || {}, m.scores || {}); const r = m.ranking || {};
  [["aa_text_to_video","aa_t2v"],["aa_image_to_video","aa_i2v"],["aa_text_to_image","aa_t2i"],["aa_image_edit","aa_image_edit"]].forEach(([k,c]) => { if (r[k] != null && !Object.keys(S).some(x => x.startsWith(c))) S[c] = {elo:r[k]}; });
  return Object.entries(S).map(([k,v]) => [k, typeof v === "object" ? (v.elo ?? v.score ?? v.wer ?? null) : v]).filter(x => x[1] != null); };
const bestScore = m => { const l = scoreList(m).filter(x => typeof x[1] === "number" && x[1] > 200); return l.length ? Math.max(...l.map(x => x[1])) : null; };
const scoreCell = m => { const l = scoreList(m); if (!l.length) return n(null); const top = l.slice().sort((a,c) => (+c[1]||0)-(+a[1]||0))[0]; return `${esc(top[1])} <span class="var">${esc(top[0])}</span>${l.length>1?` <span class="var">+${l.length-1}</span>`:""}`; };
const intCount = m => (m._int||{}).count || 0;
const intList = m => { const i=m._int||{}; const L=[]; if((i.comfyui_local||[]).length) L.push("ComfyUI"); if((i.wan2gp||[]).length) L.push("Wan2GP"); (i.pinokio||[]).forEach(p=>L.push("Pinokio · "+p)); if(i.drawthings===true) L.push("Draw Things"); if(i.maestro===true) L.push("Maestro"); if(i.phosphene===true) L.push("Phosphene"); return L; };
const intCell = m => { const L=intList(m); const api=((m._int||{}).comfyui_api||[]).length; return L.length ? `<b>${L.length}</b> <span class="var">${esc(L.map(x=>x.split(" · ")[0]).filter((x,i,a)=>a.indexOf(x)===i).join(", "))}</span>` : (api?'<span class="var">nœud API ComfyUI</span>':'<span class="no">–</span>'); };
const best = (m, k) => (m._best || {})[k];
let compare = new Set(); try { compare = new Set(JSON.parse(localStorage.getItem("atlas-compare") || "[]")); } catch(e) {}
const saveCmp = () => { try { localStorage.setItem("atlas-compare", JSON.stringify([...compare])); } catch(e) {} };
const cmpBtn = m => `<button class="cmp" data-cmp="${esc(m.id)}" aria-pressed="${compare.has(m.id)}" title="Ajouter à la comparaison">${compare.has(m.id)?"✓":"+"}</button>`;

const COLS = {
 video: [
  ["Modèle", m => `${cmpBtn(m)} ${name(m)}`, m => (m.family+" "+m.variant).toLowerCase()],
  ["Éditeur", m => `${esc(m.vendor)} <span class="var">${esc(m.country||"")}</span>`, m => m.vendor||""],
  ["Accès", acc, m => g(m,"access.open_weights") ? 0 : 1],
  ["Meilleur score", scoreCell, m => -(bestScore(m)||0), 1],
  ["Durée", m => { const a=g(m,"outputs.min_s"), c=g(m,"outputs.max_s"); return a==null&&c==null?n(null):`${a??"?"}–${c??"?"} s`; }, m => -(g(m,"outputs.max_s")||0)],
  ["Rés. max", m => n(g(m,"outputs.max_resolution")), m => g(m,"outputs.max_resolution")||""],
  ["Son", m => b(g(m,"outputs.native_audio")), m => g(m,"outputs.native_audio")?0:1],
  ["Lip-sync", m => b(g(m,"outputs.lip_sync")), m => g(m,"outputs.lip_sync")?0:1],
  ["Img réf.", m => n(g(m,"inputs.image_refs_max")), m => -(g(m,"inputs.image_refs_max")||0), 1],
  ["Vid réf.", m => { const v=g(m,"inputs.video_refs_max"), s=g(m,"inputs.video_refs_total_s"); return v==null?n(null):esc(v)+(s?` <span class="var">(${s} s)</span>`:""); }, m => -(g(m,"inputs.video_refs_max")||0), 1],
  ["Son réf.", m => { const v=g(m,"inputs.audio_refs_max"), s=g(m,"inputs.audio_refs_total_s"); return v==null?n(null):esc(v)+(s?` <span class="var">(${s} s)</span>`:""); }, m => -(g(m,"inputs.audio_refs_max")||0), 1],
  ["1re / dern.", m => `${b(g(m,"inputs.first_frame"))} / ${b(g(m,"inputs.last_frame"))}`, m => (g(m,"inputs.first_frame")?0:1)+(g(m,"inputs.last_frame")?0:1)],
  ["Img-clés", m => n(g(m,"inputs.keyframes_max")), m => -(g(m,"inputs.keyframes_max")||0), 1],
  ["V2V", m => b(g(m,"inputs.video_to_video")), m => g(m,"inputs.video_to_video")?0:1],
  ["Contrôle", m => esc((g(m,"inputs.control")||[]).join(", ")) || '<span class="no">–</span>', m => -((g(m,"inputs.control")||[]).length)],
  ["3D", m => b(g(m,"inputs.input_3d")), m => g(m,"inputs.input_3d")?0:1],
  ["LoRA", m => b(g(m,"inputs.lora_inference")), m => g(m,"inputs.lora_inference")?0:1],
  ["5090", m => b(loc(m,"5090")), m => loc(m,"5090")?0:1],
  ["4090", m => b(loc(m,"4090")), m => loc(m,"4090")?0:1],
  ["Mac 128 Go", m => b(loc(m,"mac")), m => loc(m,"mac")?0:1],
  ["Intégré dans", intCell, m => -intCount(m), 1],
  ["Visages réels", m => n(g(m,"moderation.real_faces")), m => g(m,"moderation.real_faces")||""],
  ["$/s 480p", m => money(best(m,"price_usd_480p_s")), m => best(m,"price_usd_480p_s") ?? 1e9, 1],
  ["$/s 720p", m => money(best(m,"price_usd_720p_s")), m => best(m,"price_usd_720p_s") ?? 1e9, 1],
  ["$/s 1080p", m => money(best(m,"price_usd_1080p_s")), m => best(m,"price_usd_1080p_s") ?? 1e9, 1],
 ],
 image: [
  ["Modèle", m => `${cmpBtn(m)} ${name(m)}`, m => (m.family+" "+m.variant).toLowerCase()],
  ["Éditeur", m => `${esc(m.vendor)} <span class="var">${esc(m.country||"")}</span>`, m => m.vendor||""],
  ["Accès", acc, m => g(m,"access.open_weights") ? 0 : 1],
  ["Licence", m => n(g(m,"access.license")), m => g(m,"access.license")||""],
  ["Meilleur score", scoreCell, m => -(bestScore(m)||0), 1],
  ["Rés. max", m => n(g(m,"outputs.max_resolution")), m => g(m,"outputs.max_resolution")||""],
  ["Img réf.", m => n(g(m,"inputs.image_refs_max")), m => -(g(m,"inputs.image_refs_max")||0), 1],
  ["Édition", m => b(g(m,"inputs.image_edit")), m => g(m,"inputs.image_edit")?0:1],
  ["Multi-édition", m => n(g(m,"inputs.multi_image_edit_max")), m => -(g(m,"inputs.multi_image_edit_max")||0), 1],
  ["Texte typo", m => n(g(m,"outputs.text_rendering")), m => g(m,"outputs.text_rendering")||""],
  ["LoRA", m => b(g(m,"inputs.lora_inference")), m => g(m,"inputs.lora_inference")?0:1],
  ["5090", m => b(loc(m,"5090")), m => loc(m,"5090")?0:1],
  ["4090", m => b(loc(m,"4090")), m => loc(m,"4090")?0:1],
  ["Mac 128 Go", m => b(loc(m,"mac")), m => loc(m,"mac")?0:1],
  ["Intégré dans", intCell, m => -intCount(m), 1],
  ["Visages réels", m => n(g(m,"moderation.real_faces")), m => g(m,"moderation.real_faces")||""],
  ["$/image", m => money(best(m,"price_usd_per_image")), m => best(m,"price_usd_per_image") ?? 1e9, 1],
 ],
 audio: [
  ["Modèle", m => `${cmpBtn(m)} ${name(m)}`, m => (m.family+" "+m.variant).toLowerCase()],
  ["Tâche", m => n(m.task), m => m.task||""],
  ["Éditeur", m => `${esc(m.vendor)} <span class="var">${esc(m.country||"")}</span>`, m => m.vendor||""],
  ["Accès", acc, m => g(m,"access.open_weights") ? 0 : 1],
  ["Licence", m => n(g(m,"access.license")), m => g(m,"access.license")||""],
  ["Meilleur score", scoreCell, m => -(bestScore(m)||0), 1],
  ["Français", m => n(m.french_quality), m => m.french_quality||""],
  ["Clonage", m => { const c=m.clone||{}; return c.seconds_needed==null&&c.zero_shot==null?n(null):`${c.zero_shot?"zéro-shot":""} ${c.seconds_needed!=null?esc(c.seconds_needed)+" s":""}`; }, m => (m.clone||{}).seconds_needed ?? 1e9, 1],
  ["Contrôle consentement", m => n((m.clone||{}).consent_check), m => (m.clone||{}).consent_check||""],
  ["Latence ms", m => n(m.realtime_latency_ms), m => m.realtime_latency_ms ?? 1e9, 1],
  ["Prix", m => { const p=m.price||{}; const v=p.usd_per_1k_chars??p.usd_per_min??p.usd_per_track??p.usd; return v==null?n(null):`${money(v)} $ <span class="var">${esc(p.unit||"")} ${esc(p.platform||"")}</span>`; }, m => { const p=m.price||{}; return p.usd_per_1k_chars??p.usd_per_min??p.usd_per_track??p.usd??1e9; }, 1],
  ["5090", m => b(loc(m,"5090")), m => loc(m,"5090")?0:1],
  ["4090", m => b(loc(m,"4090")), m => loc(m,"4090")?0:1],
  ["Mac 128 Go", m => b(loc(m,"mac")), m => loc(m,"mac")?0:1],
  ["Intégré dans", intCell, m => -intCount(m), 1],
 ],
 threed: [
  ["Modèle", m => `${cmpBtn(m)} ${name(m)}`, m => (m.family+" "+m.variant).toLowerCase()],
  ["Tâche", m => n(m.task), m => m.task||""],
  ["Éditeur", m => `${esc(m.vendor)} <span class="var">${esc(m.country||"")}</span>`, m => m.vendor||""],
  ["Accès", acc, m => g(m,"access.open_weights") ? 0 : 1],
  ["Meilleur score", scoreCell, m => -(bestScore(m)||0), 1],
  ["Entrées", m => n(Array.isArray(m.inputs)?m.inputs.join(", "):m.inputs), m => ""],
  ["Sorties", m => `<span class="var">${esc(Array.isArray(m.outputs)?m.outputs.join(", "):(typeof m.outputs==="object"?JSON.stringify(m.outputs):m.outputs||"?"))}</span>`, m => ""],
  ["Blender", m => n(m.blender), m => m.blender?0:1],
  ["Prix", m => { const p=m.price||{}; return p.usd==null?n(null):`${money(p.usd)} $ <span class="var">${esc(p.unit||"")}</span>`; }, m => (m.price||{}).usd ?? 1e9, 1],
  ["5090", m => b(loc(m,"5090")), m => loc(m,"5090")?0:1],
  ["4090", m => b(loc(m,"4090")), m => loc(m,"4090")?0:1],
  ["Mac 128 Go", m => b(loc(m,"mac")), m => loc(m,"mac")?0:1],
  ["Intégré dans", intCell, m => -intCount(m), 1],
 ],
 platforms: [
  ["Plateforme", p => `<span class="fam">${esc(p.name)}</span><br><span class="var">${esc(p.type||"")}</span>`, p => (p.name||"").toLowerCase()],
  ["Verdict", p => p.verdict ? `<span class="pill v-${esc(p.verdict)}">${esc({fiable:"fiable",tester:"à tester",eviter:"à éviter"}[p.verdict]||p.verdict)}</span>` : n(null), p => ({fiable:0,tester:1,eviter:2}[p.verdict] ?? 3)],
  ["Pays", p => n(p.country), p => p.country||""],
  ["Seedance $/s 480p", p => money(g(p,"seedance.usd_480p_s")), p => g(p,"seedance.usd_480p_s") ?? 1e9, 1],
  ["720p", p => money(g(p,"seedance.usd_720p_s")), p => g(p,"seedance.usd_720p_s") ?? 1e9, 1],
  ["1080p", p => money(g(p,"seedance.usd_1080p_s")), p => g(p,"seedance.usd_1080p_s") ?? 1e9, 1],
  ["Visages réels", p => n(g(p,"moderation.real_faces")), p => g(p,"moderation.real_faces")||""],
  ["Refus facturé", p => n(p.refusal_billed), p => p.refusal_billed||""],
  ["Paiement", p => n((p.payment||[]).join(", ")), p => (p.payment||[]).join()],
  ["LoRA", p => n(p.lora_hosting), p => p.lora_hosting?0:1],
  ["Avis des usagers", p => `<span class="var">${esc(((p.user_feedback||{}).summary||"").slice(0,140))}${((p.user_feedback||{}).summary||"").length>140?"…":""}</span>`, p => "", 0, "wrap"],
  ["Pourquoi", p => `<span class="var">${esc(p.verdict_reason||"")}</span>`, p => "", 0, "wrap"],
 ],
};
const DETAIL_KEYS = {video:["inputs.incompatible_combinations","local.vram_note","moderation.notes"], image:["outputs.text_rendering","local.vram_note","moderation.notes"]};

let tab = "choose", sortCol = null, sortDir = 1, open = new Set(), q = "", flt = {};

function priceRows(m){
  const ps = m._prices || [];
  if(!ps.length) return "<p class='note'>Aucun prix relevé pour cette variante.</p>";
  return "<ul>" + ps.slice().sort((a,c)=>(a.price_usd_720p_s??a.price_usd_per_image??9)-(c.price_usd_720p_s??c.price_usd_per_image??9)).map(p => {
    const parts = [["480p",p.price_usd_480p_s],["720p",p.price_usd_720p_s],["1080p",p.price_usd_1080p_s]].filter(x=>x[1]!=null).map(x=>`${x[0]} ${money(x[1])} $/s`);
    if(p.price_usd_per_image!=null) parts.push(`${money(p.price_usd_per_image)} $/image`);
    return `<li><b>${esc(p.platform)}</b>${p.unit==="subscription"?" (abonnement)":""} · ${parts.join(" · ") || esc((p.raw||"").slice(0,120))} <span class="var">(${esc(p.verified)}${p.source_url?`, <a href="${esc(p.source_url)}" target="_blank" rel="noopener">source</a>`:""})</span></li>`;
  }).join("") + "</ul>";
}
function detail(m){
  const li = a => (a&&a.length) ? "<ul>"+a.map(x=>`<li>${esc(x)}</li>`).join("")+"</ul>" : "<p class='note'>–</p>";
  const src = (m.sources||[]).map(s=>`<li>${s.url?`<a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.url)}</a>`:"(sans lien)"} <span class="var">${esc(s.date||"")} ${esc(s.type||"")}</span></li>`).join("");
  const sc = scoreList(m).map(([k,v]) => `<li>${esc(k)} : <b>${esc(v)}</b></li>`).join("");
  const L = m._local || {};
  const extra = [];
  if (g(m,"inputs.incompatible_combinations")) extra.push(`<h4>Ne se combine pas</h4><p>${esc(g(m,"inputs.incompatible_combinations"))}</p>`);
  if (g(m,"local.vram_note")) extra.push(`<h4>Local</h4><p>${esc(g(m,"local.vram_note"))}</p>`);
  if (L.rtx4090_note) extra.push(`<h4>RTX 4090</h4><p>${esc(L.rtx4090_note)}</p>`);
  if (L.mac_tool || L.mac_note) extra.push(`<h4>Mac M5 Max 128 Go</h4><p>${esc([L.mac_tool,L.mac_note].filter(Boolean).join(" · "))}</p>`);
  const mod = [g(m,"moderation.public_figures"), g(m,"moderation.notes"), g(m,"moderation.voix_celebrites")].filter(Boolean).join(" · ");
  if (mod) extra.push(`<h4>Modération</h4><p>${esc(mod)}</p>`);
  if (g(m,"ranking.aa_note")) extra.push(`<h4>Note</h4><p>${esc(g(m,"ranking.aa_note"))}</p>`);
  { const i=m._int||{}; const parts=[]; if((i.comfyui_local||[]).length) parts.push(`ComfyUI, templates officiels : ${i.comfyui_local.join(", ")}${i.comfyui_usage?` (usage ${i.comfyui_usage})`:""}`); if((i.comfyui_api||[]).length) parts.push(`ComfyUI, nœuds API : ${i.comfyui_api.length}`); if((i.wan2gp||[]).length) parts.push(`Wan2GP : ${i.wan2gp.join(", ")}`); if((i.pinokio||[]).length) parts.push(`Pinokio : ${i.pinokio.join(", ")}`); ["drawthings","maestro","phosphene"].forEach(k=>{ if(i[k]===true) parts.push({drawthings:"Draw Things",maestro:"Maestro",phosphene:"Phosphene"}[k]); }); if(i.notes) parts.push(i.notes); if(parts.length) extra.push(`<h4>Intégré dans</h4><p>${parts.map(esc).join("<br>")}</p>`); }
  return `<div class="det">
    <div><h4>Points forts</h4>${li(m.pros)}<h4>Faiblesses</h4>${li(m.cons)}</div>
    <div><h4>Scores</h4>${sc?`<ul>${sc}</ul>`:"<p class='note'>Aucun classement.</p>"}<h4>Prix par plateforme</h4>${priceRows(m)}</div>
    <div><h4>Fonctions d'édition</h4>${li(m.edit_functions)}${extra.join("")}</div>
    <div><h4>Sources</h4><ul>${src||"<li>–</li>"}</ul></div></div>`;
}
function platformDetail(p){
  const src = (p.sources||[]).map(s=>`<li>${s.url?`<a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.url)}</a>`:"(témoignage direct)"} <span class="var">${esc(s.date||"")} ${esc(s.type||"")}</span></li>`).join("");
  const txt = v => { if (v == null) return ""; if (typeof v !== "object") return esc(v);
    if (Array.isArray(v)) return v.map(x => typeof x === "object" ? esc([x.text, x.ends ? "jusqu'au " + x.ends : "", x.source ? "" : ""].filter(Boolean).join(" · ")) + (x.source ? ` <a href="${esc(x.source)}" target="_blank" rel="noopener">source</a>` : "") : esc(x)).join("<br>");
    const parts = [v.summary, v.verdict, v.calc, v.clip && v.usd_per_clip_sub != null ? `Clip ${v.clip} : ${v.usd_per_clip_sub} $ par abonnement (${v.plan||""}), ${v.best_api ? v.best_api.usd_per_clip + " $ chez " + v.best_api.platform : "?"} en API` : null, v.breakeven || v.volume].filter(Boolean);
    return parts.length ? parts.map(esc).join("<br>") : esc(JSON.stringify(v)); };
  const row = (t,v) => (v && (typeof v !== "object" || Object.keys(v).length)) ? `<h4>${t}</h4><p>${txt(v)}</p>` : "";
  return `<div class="det"><div>${row("Pourquoi ce verdict",p.verdict_reason)}${row("Modèles",(p.models||[]).join(", "))}${row("Seedance",g(p,"seedance.note"))}${row("Promotions",p.promotions)}</div>
   <div>${row("Modération",[g(p,"moderation.notes"),g(p,"moderation.public_figures"),g(p,"moderation.violence")].filter(Boolean).join(" · "))}${row("Refus facturé",p.refusal_billed)}${row("Conditions",p.terms)}</div>
   <div>${row("Fiabilité",p.reliability)}${row("Retours d'usagers",p.user_feedback)}${row("Abonnement ou API",p.api_vs_subscription)}</div>
   <div><h4>Sources</h4><ul>${src||"<li>–</li>"}</ul></div></div>`;
}
function filtersHtml(kind){
  const loc3 = `<label><input type="checkbox" data-f="open"> poids ouverts</label><label><input type="checkbox" data-f="l5090"> RTX 5090</label><label><input type="checkbox" data-f="l4090"> RTX 4090</label><label><input type="checkbox" data-f="lmac"> Mac 128 Go</label>`;
  const extra = kind==="video" ? `<label><input type="checkbox" data-f="audio"> son natif</label><label><input type="checkbox" data-f="ff"> 1re / dernière image</label><label><input type="checkbox" data-f="ref"> références image</label><label><input type="checkbox" data-f="lora"> LoRA</label><label><input type="checkbox" data-f="price"> avec prix</label>`
    : kind==="image" ? `<label><input type="checkbox" data-f="edit"> édition</label><label><input type="checkbox" data-f="lora"> LoRA</label><label><input type="checkbox" data-f="price"> avec prix</label>` : "";
  return `<div class="filters"><input type="search" id="q" placeholder="Filtrer : nom, éditeur, fonction…" aria-label="Filtrer" value="${esc(q)}">${kind!=="platforms"&&kind!=="prices"?loc3:""}${extra}<span class="count" id="count"></span></div>`;
}
function passes(m, kind){
  if(q && !JSON.stringify([m.family,m.variant,m.vendor,m.name,m.task,m.edit_functions,g(m,"inputs.control"),m.models]).toLowerCase().includes(q)) return false;
  if(flt.open && !g(m,"access.open_weights")) return false;
  if(flt.l5090 && !loc(m,"5090")) return false;
  if(flt.l4090 && !loc(m,"4090")) return false;
  if(flt.lmac && !loc(m,"mac")) return false;
  if(flt.lora && !g(m,"inputs.lora_inference")) return false;
  if(flt.price && !(m._prices||[]).length) return false;
  if(flt.audio && !g(m,"outputs.native_audio")) return false;
  if(flt.ff && !g(m,"inputs.first_frame")) return false;
  if(flt.ref && !(g(m,"inputs.image_refs_max")>0)) return false;
  if(flt.edit && !g(m,"inputs.image_edit")) return false;
  return true;
}
function card(m, kind, reason){
  const chips = [];
  const s = bestScore(m); if (s) chips.push(`<span class="chip">score ${s}</span>`);
  if (kind==="video"){ const mx=g(m,"outputs.max_s"); if(mx) chips.push(`<span class="chip">≤ ${mx} s</span>`); if(g(m,"outputs.native_audio")) chips.push('<span class="chip good">son</span>'); if(g(m,"inputs.first_frame")) chips.push('<span class="chip">1re img</span>'); if(g(m,"inputs.image_refs_max")) chips.push(`<span class="chip">${g(m,"inputs.image_refs_max")} réf.</span>`); const p=best(m,"price_usd_720p_s"); if(p!=null) chips.push(`<span class="chip good">${money(p)} $/s 720p</span>`); }
  if (kind==="image"){ if(g(m,"inputs.image_edit")) chips.push('<span class="chip">édition</span>'); const r=g(m,"inputs.image_refs_max"); if(r) chips.push(`<span class="chip">${r} réf.</span>`); const p=best(m,"price_usd_per_image"); if(p!=null) chips.push(`<span class="chip good">${money(p)} $/image</span>`); }
  if (kind==="audio" && m.task) chips.push(`<span class="chip">${esc(m.task)}</span>`);
  if (kind==="threed" && m.task) chips.push(`<span class="chip">${esc(m.task)}</span>`);
  if (g(m,"access.open_weights")) chips.push('<span class="chip good">ouvert</span>');
  ["5090","4090","mac"].forEach(k => { if (loc(m,k)) chips.push(`<span class="chip">${k==="mac"?"Mac":k}</span>`); });
  if (intCount(m)) chips.push(`<span class="chip good">intégré dans ${intCount(m)} outil${intCount(m)>1?"s":""} locaux</span>`);
  return `<article class="card"><div class="top"><div><div class="name">${esc(m.family)} · ${esc(m.variant)}</div><div class="sub">${esc(m.vendor||"")}</div></div>${cmpBtn(m)}</div>
    ${reason?`<div class="var">${reason}</div>`:""}<div class="chips">${chips.join("")}</div>
    <button class="more" data-open="${esc(m.id)}">${open.has(m.id)?"Masquer le détail":"Voir le détail"}</button>${open.has(m.id)?detail(m):""}</article>`;
}
function renderModels(kind){
  const cols = COLS[kind]; let rows = DATA[kind].filter(m => passes(m, kind));
  if(sortCol!==null && cols[sortCol]){ const f = cols[sortCol][2]; rows = rows.slice().sort((a,c)=>{const x=f(a),y=f(c);return (x>y?1:x<y?-1:0)*sortDir;}); }
  let body;
  if (!DATA[kind].length) body = `<p class="note">Données en cours de collecte pour cet onglet.</p>`;
  else if (isMobile() && kind!=="platforms") body = `<div class="cards">${rows.map(m => card(m, kind)).join("")}</div>`;
  else if (isMobile()) body = `<div class="cards">${rows.map(p => `<article class="card"><div class="top"><div><div class="name">${esc(p.name)}</div><div class="sub">${esc(p.type||"")} ${esc(p.country||"")}</div></div>${p.verdict?`<span class="pill v-${esc(p.verdict)}">${esc({fiable:"fiable",tester:"à tester",eviter:"à éviter"}[p.verdict]||p.verdict)}</span>`:""}</div><div class="var">${esc(p.verdict_reason||"")}</div><button class="more" data-open="${esc(p.id)}">${open.has(p.id)?"Masquer le détail":"Voir le détail"}</button>${open.has(p.id)?platformDetail(p):""}</article>`).join("")}</div>`;
  else body = `<div class="scroll"><table><thead><tr>${cols.map((c,i)=>`<th data-i="${i}" class="${i===sortCol?"sorted":""}">${esc(c[0])}${i===sortCol?(sortDir>0?" ↑":" ↓"):""}</th>`).join("")}</tr></thead><tbody>${
      rows.map(m => `<tr class="row" data-id="${esc(m.id)}">`+cols.map((c,i)=>`<td class="${c[4]||""} ${c[3]?"n":""}">${c[1](m)}</td>`).join("")+"</tr>"+(open.has(m.id)?`<tr class="detail"><td colspan="${cols.length}">${kind==="platforms"?platformDetail(m):detail(m)}</td></tr>`:"")).join("")}</tbody></table></div>`;
  $("#view").innerHTML = filtersHtml(kind) + body;
  const c = $("#count"); if (c) c.textContent = `${rows.length} / ${DATA[kind].length}`;
}
function renderPrices(){
  const PC = [["Modèle",p=>esc(p.model_id),p=>p.model_id],["Plateforme",p=>esc(p.platform),p=>p.platform],["Unité",p=>esc(p.unit),p=>p.unit||""],
    ["$/s 480p",p=>money(p.price_usd_480p_s),p=>p.price_usd_480p_s??1e9,1],["$/s 720p",p=>money(p.price_usd_720p_s),p=>p.price_usd_720p_s??1e9,1],
    ["$/s 1080p",p=>money(p.price_usd_1080p_s),p=>p.price_usd_1080p_s??1e9,1],["$/image",p=>money(p.price_usd_per_image),p=>p.price_usd_per_image??1e9,1],
    ["Relevé",p=>esc(p.verified),p=>p.verified||""],["Détail",p=>`<span class="var">${esc((p.raw||"").slice(0,90))}</span>`,p=>""],
    ["Source",p=>p.source_url?`<a href="${esc(p.source_url)}" target="_blank" rel="noopener">lien</a>`:"",p=>""]];
  let rows = DATA.prices.filter(p => !q || JSON.stringify(p).toLowerCase().includes(q));
  if(sortCol!==null && PC[sortCol]){ const f=PC[sortCol][2]; rows=rows.slice().sort((a,c)=>{const x=f(a),y=f(c);return (x>y?1:x<y?-1:0)*sortDir;}); }
  $("#view").innerHTML = filtersHtml("prices") + `<div class="scroll"><table><thead><tr>${PC.map((c,i)=>`<th data-i="${i}" class="${i===sortCol?"sorted":""}">${esc(c[0])}</th>`).join("")}</tr></thead><tbody>${rows.map(p=>"<tr>"+PC.map(c=>`<td class="${c[3]?"n":""}">${c[1](p)}</td>`).join("")+"</tr>").join("")}</tbody></table></div>`;
  $("#count").textContent = `${rows.length} / ${DATA.prices.length} prix`;
}
function renderGpu(){
  const rows = DATA.gpu||[], keys = rows.length ? Object.keys(rows[0]).filter(k=>k!=="sources") : [];
  $("#view").innerHTML = `<div class="scroll"><table><thead><tr>${keys.map(k=>`<th>${esc(k)}</th>`).join("")}</tr></thead><tbody>${rows.map(r=>"<tr>"+keys.map(k=>`<td>${typeof r[k]==="object"?esc(JSON.stringify(r[k])):esc(r[k])}</td>`).join("")+"</tr>").join("")}</tbody></table></div>`;
}
let need = {integ:0, kind:"video", audio:false, lipsync:false, ff:false, lf:false, refs:0, vrefs:false, lora:false, open:false, machine:"", maxprice:"", mindur:"", edit:false, task:"", french:false, clone:false};
function renderChoose(){
  const k = need.kind;
  const vid = `<fieldset><legend>La vidéo doit</legend>
      <label><input type="checkbox" data-n="audio" ${need.audio?"checked":""}> avoir le son natif</label>
      <label><input type="checkbox" data-n="lipsync" ${need.lipsync?"checked":""}> synchroniser les lèvres</label>
      <label><input type="checkbox" data-n="ff" ${need.ff?"checked":""}> partir d'une première image</label>
      <label><input type="checkbox" data-n="lf" ${need.lf?"checked":""}> finir sur une dernière image</label>
      <label><input type="checkbox" data-n="vrefs" ${need.vrefs?"checked":""}> accepter des vidéos de référence</label>
      <label>au moins <input type="number" min="0" max="50" data-n="refs" value="${need.refs||""}" placeholder="0"> images de référence</label>
      <label>plans d'au moins <input type="number" min="0" max="60" data-n="mindur" value="${need.mindur}" placeholder="s"> s</label>
      <label>au plus <input type="number" step="0.01" min="0" data-n="maxprice" value="${need.maxprice}" placeholder="$/s"> $/s en 720p</label></fieldset>`;
  const img = `<fieldset><legend>L'image doit</legend>
      <label><input type="checkbox" data-n="edit" ${need.edit?"checked":""}> éditer une image existante</label>
      <label>au moins <input type="number" min="0" max="20" data-n="refs" value="${need.refs||""}" placeholder="0"> images de référence</label>
      <label>au plus <input type="number" step="0.01" min="0" data-n="maxprice" value="${need.maxprice}" placeholder="$"> $ par image</label></fieldset>`;
  const tasks = [...new Set(DATA.audio.map(m=>m.task).filter(Boolean))];
  const aud = `<fieldset><legend>L'audio doit</legend>
      <label>tâche <select data-n="task"><option value="">toutes</option>${tasks.map(t=>`<option ${need.task===t?"selected":""}>${esc(t)}</option>`).join("")}</select></label>
      <label><input type="checkbox" data-n="french" ${need.french?"checked":""}> bien parler français</label>
      <label><input type="checkbox" data-n="clone" ${need.clone?"checked":""}> cloner une voix</label></fieldset>`;
  const common = `<fieldset><legend>Contraintes</legend>
      <label><input type="checkbox" data-n="lora" ${need.lora?"checked":""}> accepter ma LoRA</label>
      <label><input type="checkbox" data-n="open" ${need.open?"checked":""}> poids ouverts</label>
      <label>intégré dans au moins <select data-n="integ"><option value="0" ${!need.integ?"selected":""}>0</option><option value="1" ${need.integ==1?"selected":""}>1</option><option value="2" ${need.integ==2?"selected":""}>2</option><option value="3" ${need.integ==3?"selected":""}>3</option></select> outils locaux (ComfyUI, Wan2GP, Pinokio, Draw Things, Maestro, Phosphene)</label>
      <label>tourner sur <select data-n="machine"><option value="">peu importe</option><option value="5090" ${need.machine==="5090"?"selected":""}>RTX 5090</option><option value="4090" ${need.machine==="4090"?"selected":""}>RTX 4090</option><option value="mac" ${need.machine==="mac"?"selected":""}>Mac 128 Go</option></select></label></fieldset>`;
  const pool = DATA[k] || [];
  const ok = pool.filter(m => {
    if (need.open && !g(m,"access.open_weights")) return false;
    if (need.lora && !g(m,"inputs.lora_inference")) return false;
    if (need.machine && !loc(m, need.machine)) return false;
    if (+need.integ && intCount(m) < +need.integ) return false;
    if (k==="video"){
      if (need.audio && !g(m,"outputs.native_audio")) return false;
      if (need.lipsync && !g(m,"outputs.lip_sync")) return false;
      if (need.ff && !g(m,"inputs.first_frame")) return false;
      if (need.lf && !g(m,"inputs.last_frame")) return false;
      if (need.vrefs && !(g(m,"inputs.video_refs_max")>0)) return false;
      if (need.refs && !(g(m,"inputs.image_refs_max")>=need.refs)) return false;
      if (need.mindur && !(g(m,"outputs.max_s")>=+need.mindur)) return false;
      if (need.maxprice !== "" && !(best(m,"price_usd_720p_s")!=null && best(m,"price_usd_720p_s")<=+need.maxprice)) return false;
    }
    if (k==="image"){
      if (need.edit && !g(m,"inputs.image_edit")) return false;
      if (need.refs && !(g(m,"inputs.image_refs_max")>=need.refs)) return false;
      if (need.maxprice !== "" && !(best(m,"price_usd_per_image")!=null && best(m,"price_usd_per_image")<=+need.maxprice)) return false;
    }
    if (k==="audio"){
      if (need.task && m.task!==need.task) return false;
      if (need.french && !["bonne"].includes(m.french_quality)) return false;
      if (need.clone && !(m.clone && (m.clone.zero_shot || m.clone.seconds_needed!=null))) return false;
    }
    return true;
  }).sort((a,c) => (bestScore(c)||0)-(bestScore(a)||0) || ((best(a,"price_usd_720p_s")??best(a,"price_usd_per_image")??9)-(best(c,"price_usd_720p_s")??best(c,"price_usd_per_image")??9)));
  $("#view").innerHTML = `<div class="choose"><form class="panel" id="needs" onsubmit="return false">
      <fieldset><legend>Je cherche</legend><label><select data-n="kind"><option value="video" ${k==="video"?"selected":""}>une vidéo</option><option value="image" ${k==="image"?"selected":""}>une image</option><option value="audio" ${k==="audio"?"selected":""}>de l'audio</option><option value="threed" ${k==="threed"?"selected":""}>de la 3D</option></select></label></fieldset>
      ${k==="video"?vid:k==="image"?img:k==="audio"?aud:""}${common}
      <p class="note">Classement : meilleur score indépendant d'abord, puis prix le plus bas. Une case « ? » dans les données exclut le modèle d'un critère coché : vérifiez aussi l'onglet complet.</p></form>
    <section><h2>${ok.length} modèle${ok.length>1?"s":""} répond${ok.length>1?"ent":""}</h2><div class="cards" style="margin-top:10px">${ok.slice(0,60).map(m => card(m,k)).join("") || "<p class='note'>Aucun modèle ne remplit tous ces critères. Décochez un critère.</p>"}</div></section></div>`;
}
const CMP_ROWS = [
  ["Éditeur", m => esc(m.vendor||"?")],["Accès", acc],["Licence", m => n(g(m,"access.license"))],["Scores", m => scoreList(m).map(([k,v])=>`${esc(k)} ${esc(v)}`).join("<br>") || n(null)],
  ["Durée", m => g(m,"outputs.max_s")!=null?`${g(m,"outputs.min_s")??"?"}–${g(m,"outputs.max_s")} s`:n(null)],["Résolution max", m => n(g(m,"outputs.max_resolution"))],
  ["Son natif", m => b(g(m,"outputs.native_audio"))],["Lip-sync", m => b(g(m,"outputs.lip_sync"))],
  ["Images de réf.", m => n(g(m,"inputs.image_refs_max"))],["Vidéos de réf.", m => n(g(m,"inputs.video_refs_max"))],["Sons de réf.", m => n(g(m,"inputs.audio_refs_max"))],
  ["1re / dernière image", m => `${b(g(m,"inputs.first_frame"))} / ${b(g(m,"inputs.last_frame"))}`],["Images-clés", m => n(g(m,"inputs.keyframes_max"))],
  ["Ne se combine pas", m => n(g(m,"inputs.incompatible_combinations"))],["Contrôle", m => n((g(m,"inputs.control")||[]).join(", "))],["LoRA", m => b(g(m,"inputs.lora_inference"))],
  ["Édition", m => n((m.edit_functions||[]).join(", "))],["Tâche", m => n(m.task)],["Français", m => n(m.french_quality)],
  ["Intégré dans", m => esc(intList(m).join(", ")) || n(null)],
  ["RTX 5090 / 4090 / Mac", m => `${b(loc(m,"5090"))} / ${b(loc(m,"4090"))} / ${b(loc(m,"mac"))}`],
  ["Visages réels", m => n(g(m,"moderation.real_faces"))],
  ["Meilleur prix", m => { const p=[["480p",best(m,"price_usd_480p_s")],["720p",best(m,"price_usd_720p_s")],["1080p",best(m,"price_usd_1080p_s")]].filter(x=>x[1]!=null).map(x=>`${x[0]} ${money(x[1])} $/s`); if(best(m,"price_usd_per_image")!=null) p.push(`${money(best(m,"price_usd_per_image"))} $/image`); return p.join("<br>")||n(null); }],
  ["Points forts", m => esc((m.pros||[]).join(" · "))],["Faiblesses", m => esc((m.cons||[]).join(" · "))],
];
function renderCompare(){
  const ms = [...compare].map(byId).filter(Boolean);
  $("#view").innerHTML = `<div style="display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap"><h2>Comparaison de ${ms.length} modèle${ms.length>1?"s":""}</h2><button class="cmp" id="back">Retour</button></div>
    <div class="scroll" style="margin-top:10px"><table class="cmptable"><thead><tr><th></th>${ms.map(m=>`<th>${esc(m.family)}<br><span class="var">${esc(m.variant)}</span> ${cmpBtn(m)}</th>`).join("")}</tr></thead>
    <tbody>${CMP_ROWS.map(([t,f])=>`<tr><th scope="row">${esc(t)}</th>${ms.map(m=>`<td>${f(m)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
}
function render(){
  if (tab==="compare") renderCompare();
  else if (tab==="choose") renderChoose();
  else if (tab==="prices") renderPrices();
  else if (tab==="gpu") renderGpu();
  else renderModels(tab);
  $("#cmpbar").hidden = compare.size === 0;
  $("#cmpcount").textContent = `${compare.size} modèle${compare.size>1?"s":""} à comparer`;
}
$("#tabs").addEventListener("click", e => { const t = e.target.closest("button"); if(!t) return;
  document.querySelectorAll("#tabs button").forEach(x=>x.setAttribute("aria-selected", x===t)); tab = t.dataset.tab; sortCol=null; render(); });
$("#view").addEventListener("click", e => {
  const c = e.target.closest("[data-cmp]"); if (c){ const id=c.dataset.cmp; compare.has(id)?compare.delete(id):compare.add(id); saveCmp(); e.stopPropagation(); render(); return; }
  if (e.target.id === "back"){ tab = "video"; document.querySelectorAll("#tabs button").forEach(x=>x.setAttribute("aria-selected", x.dataset.tab===tab)); render(); return; }
  const o = e.target.closest("[data-open]"); if (o){ const id=o.dataset.open; open.has(id)?open.delete(id):open.add(id); render(); return; }
  const th = e.target.closest("th[data-i]"); if(th){ const i=+th.dataset.i; sortDir = sortCol===i ? -sortDir : 1; sortCol=i; render(); return; }
  if(e.target.closest("a")) return;
  const tr = e.target.closest("tr.row"); if(tr){ const id=tr.dataset.id; open.has(id)?open.delete(id):open.add(id); render(); }
});
$("#view").addEventListener("input", e => {
  if (e.target.id === "q"){ q = e.target.value.trim().toLowerCase(); const pos = e.target.selectionStart; render(); const el=$("#q"); if(el){ el.focus(); el.setSelectionRange(pos,pos); } return; }
  if (e.target.dataset.f){ flt[e.target.dataset.f] = e.target.checked; render(); return; }
  const k = e.target.dataset.n; if (!k) return;
  need[k] = e.target.type==="checkbox" ? e.target.checked : (e.target.type==="number" ? (e.target.value===""?"":(k==="refs"?+e.target.value:e.target.value)) : e.target.value);
  if (k==="kind"){ need.refs=0; need.maxprice=""; }
  if (e.target.type==="number"){ const pos=e.target.selectionStart; const sel=`[data-n="${k}"]`; render(); const el=$(sel); if(el){ el.focus(); try{el.setSelectionRange(pos,pos);}catch(_){} } } else render();
});
$("#cmpgo").addEventListener("click", () => { tab="compare"; document.querySelectorAll("#tabs button").forEach(x=>x.setAttribute("aria-selected","false")); render(); window.scrollTo(0,0); });
$("#cmpclear").addEventListener("click", () => { compare.clear(); saveCmp(); if (tab==="compare") tab="choose"; render(); });
matchMedia("(max-width: 760px)").addEventListener("change", render);
$("#built").textContent = `Données relevées le 15/10/2026 · page construite le ${DATA.built} · ${DATA.video.length} vidéo, ${DATA.image.length} image, ${DATA.audio.length} audio, ${DATA.threed.length} 3D, ${DATA.platforms.length} plateformes, ${DATA.prices.length} prix`;
$("#foot").textContent = DATA.orphans.length ? `${DATA.orphans.length} modèles ont des prix mais pas de fiche (anciens modèles, abonnements) : ils sont dans l'onglet « Tous les prix ».` : "";
render();
</script>
