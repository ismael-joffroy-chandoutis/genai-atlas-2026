<title>Atlas génératif 2026</title>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,650&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout : en-tête, onglets vidéo / image / GPU, filtres, une grande table triable par onglet avec détail dépliable */
:root{
  --bg:#f2f3ef; --surface:#ffffff; --fg:#1b221e; --muted:#5b665f; --line:#d4dad5;
  --accent:#1f6f5c; --accent-soft:#e0eee8; --warn:#9c5418; --warn-soft:#f6e8da; --bad:#a3322e;
  --display:"Fraunces", Georgia, serif; --body:"IBM Plex Sans", system-ui, sans-serif; --mono:"IBM Plex Mono", ui-monospace, monospace;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --bg:#131816; --surface:#1b2220; --fg:#e3e8e4; --muted:#98a49d; --line:#323e38;
  --accent:#6cc3a8; --accent-soft:#1e3a32; --warn:#e3a26a; --warn-soft:#3a2b1e; --bad:#ef8a83; color-scheme:dark } }
:root[data-theme="dark"]{
  --bg:#131816; --surface:#1b2220; --fg:#e3e8e4; --muted:#98a49d; --line:#323e38;
  --accent:#6cc3a8; --accent-soft:#1e3a32; --warn:#e3a26a; --warn-soft:#3a2b1e; --bad:#ef8a83; color-scheme:dark }
body{background:var(--bg);color:var(--fg);font-family:var(--body);font-size:14px;line-height:1.45}
.wrap{max-width:1500px;margin:0 auto;padding-block:24px 60px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:flex;flex-direction:column;gap:18px}
h1{font-family:var(--display);font-weight:650;font-size:clamp(28px,4vw,40px);margin:0;line-height:1.1}
.lede{color:var(--muted);max-width:80ch;margin:6px 0 0}
.meta{font-family:var(--mono);font-size:12px;color:var(--muted)}
.tabs{display:flex;gap:6px;flex-wrap:wrap}
.tabs button{font:500 13px var(--body);padding:7px 14px;border:1px solid var(--line);background:var(--surface);color:var(--fg);border-radius:999px;cursor:pointer}
.tabs button[aria-selected="true"]{background:var(--accent);border-color:var(--accent);color:var(--surface)}
.filters{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;font-size:13px}
.filters input[type=search]{font:inherit;padding:6px 10px;border:1px solid var(--line);border-radius:6px;background:var(--surface);color:var(--fg);min-width:220px}
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
.y{color:var(--accent);font-weight:600}.no{color:var(--muted)}.q{color:var(--warn)}
.fam{font-weight:600}.var{color:var(--muted);font-size:12px}
tr.row{cursor:pointer} tr.row:hover td{background:var(--accent-soft)}
tr.detail td{white-space:normal;background:var(--bg)}
.det{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px;padding:6px 2px;max-width:1300px}
.det h4{margin:0 0 4px;font:500 11px var(--mono);text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}
.det ul{margin:0;padding-left:16px}
.det a{color:var(--accent);word-break:break-all}
.pill{display:inline-block;padding:0 6px;border-radius:999px;font:500 11px var(--mono)}
.open{background:var(--accent-soft);color:var(--accent)}.api{background:var(--warn-soft);color:var(--warn)}
.note{color:var(--muted);font-size:12.5px;max-width:95ch}
</style>

<div class="wrap">
<header>
  <div class="meta" id="built"></div>
  <h1>Atlas génératif 2026</h1>
  <p class="lede">Modèles vidéo et image, variante par variante : ce qu'ils acceptent en entrée (texte, images, vidéos, sons, 3D), ce qu'ils sortent, leurs fonctions, leur classement indépendant et leur prix plateforme par plateforme. Cliquer une ligne pour le détail, les prix complets et les sources. « ? » = non documenté.</p>
</header>
<div class="tabs" role="tablist">
  <button role="tab" data-tab="video" aria-selected="true">Vidéo</button>
  <button role="tab" data-tab="image" aria-selected="false">Image</button>
  <button role="tab" data-tab="prices" aria-selected="false">Tous les prix</button>
  <button role="tab" data-tab="gpu" aria-selected="false">GPU à l'heure</button>
</div>
<div class="filters" id="filters">
  <input type="search" id="q" placeholder="Filtrer : nom, éditeur, fonction…" aria-label="Filtrer">
  <label><input type="checkbox" id="f-open"> poids ouverts</label>
  <label><input type="checkbox" id="f-local"> RTX 5090</label>
  <label><input type="checkbox" id="f-4090"> RTX 4090</label>
  <label><input type="checkbox" id="f-mac"> Mac M5 Max 128 Go</label>
  <label class="vonly"><input type="checkbox" id="f-audio"> audio natif</label>
  <label class="vonly"><input type="checkbox" id="f-ff"> 1re / dernière image</label>
  <label class="vonly"><input type="checkbox" id="f-ref"> références image</label>
  <label><input type="checkbox" id="f-lora"> LoRA</label>
  <label><input type="checkbox" id="f-price"> avec prix</label>
  <span class="count" id="count"></span>
</div>
<div class="scroll"><table id="t"><thead></thead><tbody></tbody></table></div>
<p class="note" id="foot"></p>
</div>

<script>
const DATA = /*__DATA__*/null;
const $ = s => document.querySelector(s);
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const b = v => v === true ? '<span class="y">oui</span>' : v === false ? '<span class="no">non</span>' : '<span class="q">?</span>';
const n = v => v === null || v === undefined ? '<span class="q">?</span>' : esc(v);
const money = v => v == null ? '' : (v < 0.1 ? v.toFixed(3) : v.toFixed(2));
const g = (o, p) => p.split(".").reduce((a, k) => a == null ? a : a[k], o);
const dur = m => { const a = g(m,"outputs.min_s"), c = g(m,"outputs.max_s"); return a==null && c==null ? n(null) : `${a ?? "?"}–${c ?? "?"} s`; };
const acc = m => g(m,"access.open_weights") ? '<span class="pill open">ouvert</span>' : (g(m,"access.api") ? '<span class="pill api">API</span>' : n(null));

const COLS = {
 video: [
  ["Modèle", m => `<span class="fam">${esc(m.family)}</span><br><span class="var">${esc(m.variant)}</span>`, m => (m.family+" "+m.variant).toLowerCase()],
  ["Éditeur", m => `${esc(m.vendor)} <span class="var">${esc(m.country||"")}</span>`, m => m.vendor||""],
  ["Accès", acc, m => g(m,"access.open_weights") ? 0 : 1],
  ["Elo T2V", m => n(g(m,"ranking.aa_text_to_video")), m => -(g(m,"ranking.aa_text_to_video")||0), 1],
  ["Elo I2V", m => n(g(m,"ranking.aa_image_to_video")), m => -(g(m,"ranking.aa_image_to_video")||0), 1],
  ["Durée", dur, m => -(g(m,"outputs.max_s")||0)],
  ["Rés. max", m => n(g(m,"outputs.max_resolution")), m => g(m,"outputs.max_resolution")||""],
  ["Audio", m => b(g(m,"outputs.native_audio")), m => g(m,"outputs.native_audio") ? 0 : 1],
  ["Lip-sync", m => b(g(m,"outputs.lip_sync")), m => g(m,"outputs.lip_sync") ? 0 : 1],
  ["Img réf.", m => n(g(m,"inputs.image_refs_max")), m => -(g(m,"inputs.image_refs_max")||0), 1],
  ["Vid réf.", m => { const v=g(m,"inputs.video_refs_max"), s=g(m,"inputs.video_refs_total_s"); return v==null?n(null):esc(v)+(s?` <span class="var">(${s} s)</span>`:""); }, m => -(g(m,"inputs.video_refs_max")||0), 1],
  ["Son réf.", m => { const v=g(m,"inputs.audio_refs_max"), s=g(m,"inputs.audio_refs_total_s"); return v==null?n(null):esc(v)+(s?` <span class="var">(${s} s)</span>`:""); }, m => -(g(m,"inputs.audio_refs_max")||0), 1],
  ["1re img", m => b(g(m,"inputs.first_frame")), m => g(m,"inputs.first_frame") ? 0 : 1],
  ["Dern. img", m => b(g(m,"inputs.last_frame")), m => g(m,"inputs.last_frame") ? 0 : 1],
  ["Img-clés", m => n(g(m,"inputs.keyframes_max")), m => -(g(m,"inputs.keyframes_max")||0), 1],
  ["V2V", m => b(g(m,"inputs.video_to_video")), m => g(m,"inputs.video_to_video") ? 0 : 1],
  ["Contrôle", m => esc((g(m,"inputs.control")||[]).join(", ")) || '<span class="no">–</span>', m => -((g(m,"inputs.control")||[]).length)],
  ["Caméra", m => b(g(m,"inputs.camera_control")), m => g(m,"inputs.camera_control") ? 0 : 1],
  ["3D", m => b(g(m,"inputs.input_3d")), m => g(m,"inputs.input_3d") ? 0 : 1],
  ["LoRA", m => b(g(m,"inputs.lora_inference")), m => g(m,"inputs.lora_inference") ? 0 : 1],
  ["5090", m => b(g(m,"local.runs_on_rtx5090_32gb")), m => g(m,"local.runs_on_rtx5090_32gb") ? 0 : 1],
  ["4090", m => b(m._local.rtx4090_24gb), m => m._local.rtx4090_24gb ? 0 : 1],
  ["Mac 128 Go", m => b(m._local.mac_m5max_128gb), m => m._local.mac_m5max_128gb ? 0 : 1],
  ["Visages réels", m => n(g(m,"moderation.real_faces")), m => g(m,"moderation.real_faces")||""],
  ["$/s 480p", m => money(m._best.price_usd_480p_s), m => m._best.price_usd_480p_s ?? 1e9, 1],
  ["$/s 720p", m => money(m._best.price_usd_720p_s), m => m._best.price_usd_720p_s ?? 1e9, 1],
  ["$/s 1080p", m => money(m._best.price_usd_1080p_s), m => m._best.price_usd_1080p_s ?? 1e9, 1],
 ],
 image: [
  ["Modèle", m => `<span class="fam">${esc(m.family)}</span><br><span class="var">${esc(m.variant)}</span>`, m => (m.family+" "+m.variant).toLowerCase()],
  ["Éditeur", m => `${esc(m.vendor)} <span class="var">${esc(m.country||"")}</span>`, m => m.vendor||""],
  ["Accès", acc, m => g(m,"access.open_weights") ? 0 : 1],
  ["Licence", m => n(g(m,"access.license")), m => g(m,"access.license")||""],
  ["Elo T2I", m => n(g(m,"ranking.aa_text_to_image")), m => -(g(m,"ranking.aa_text_to_image")||0), 1],
  ["Elo édition", m => n(g(m,"ranking.aa_image_edit")), m => -(g(m,"ranking.aa_image_edit")||0), 1],
  ["Rés. max", m => n(g(m,"outputs.max_resolution")), m => g(m,"outputs.max_resolution")||""],
  ["Img réf.", m => n(g(m,"inputs.image_refs_max")), m => -(g(m,"inputs.image_refs_max")||0), 1],
  ["Édition", m => b(g(m,"inputs.image_edit")), m => g(m,"inputs.image_edit") ? 0 : 1],
  ["Multi-édition", m => n(g(m,"inputs.multi_image_edit_max")), m => -(g(m,"inputs.multi_image_edit_max")||0), 1],
  ["Contrôle", m => esc((g(m,"inputs.control")||[]).join(", ")) || '<span class="no">–</span>', m => -((g(m,"inputs.control")||[]).length)],
  ["Texte typo", m => n(g(m,"outputs.text_rendering")), m => g(m,"outputs.text_rendering")||""],
  ["LoRA", m => b(g(m,"inputs.lora_inference")), m => g(m,"inputs.lora_inference") ? 0 : 1],
  ["5090", m => b(g(m,"local.runs_on_rtx5090_32gb")), m => g(m,"local.runs_on_rtx5090_32gb") ? 0 : 1],
  ["4090", m => b(m._local.rtx4090_24gb), m => m._local.rtx4090_24gb ? 0 : 1],
  ["Mac 128 Go", m => b(m._local.mac_m5max_128gb), m => m._local.mac_m5max_128gb ? 0 : 1],
  ["Visages réels", m => n(g(m,"moderation.real_faces")), m => g(m,"moderation.real_faces")||""],
  ["$/image", m => money(m._best.price_usd_per_image), m => m._best.price_usd_per_image ?? 1e9, 1],
 ],
};

let tab = "video", sortCol = null, sortDir = 1, open = new Set();

function priceRows(m){
  if(!m._prices.length) return "<p class='note'>Aucun prix relevé pour cette variante.</p>";
  return "<ul>" + m._prices.map(p => {
    const parts = [["480p",p.price_usd_480p_s],["720p",p.price_usd_720p_s],["1080p",p.price_usd_1080p_s]].filter(x=>x[1]!=null).map(x=>`${x[0]} ${money(x[1])} $/s`);
    if(p.price_usd_per_image!=null) parts.push(`${money(p.price_usd_per_image)} $/image`);
    return `<li><b>${esc(p.platform)}</b> · ${parts.join(" · ") || esc(p.raw)} <span class="var">(${esc(p.verified)}${p.source_url?`, <a href="${esc(p.source_url)}" target="_blank" rel="noopener">source</a>`:""})</span></li>`;
  }).join("") + "</ul>";
}
function detail(m){
  const li = a => (a&&a.length) ? "<ul>"+a.map(x=>`<li>${esc(x)}</li>`).join("")+"</ul>" : "<p class='note'>–</p>";
  const src = (m.sources||[]).map(s=>`<li><a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.url)}</a> <span class="var">${esc(s.date||"")} ${esc(s.type||"")}</span></li>`).join("");
  const inc = g(m,"inputs.incompatible_combinations");
  return `<div class="det">
    <div><h4>Points forts</h4>${li(m.pros)}<h4>Faiblesses</h4>${li(m.cons)}</div>
    <div><h4>Prix par plateforme</h4>${priceRows(m)}</div>
    <div><h4>Fonctions d'édition</h4>${li(m.edit_functions)}${inc?`<h4>Ne se combine pas</h4><p>${esc(inc)}</p>`:""}
      <h4>Local</h4><p>${esc(g(m,"local.vram_note")||"–")}</p>
      ${m._local.rtx4090_note?`<h4>RTX 4090</h4><p>${esc(m._local.rtx4090_note)}</p>`:""}
      ${(m._local.mac_tool||m._local.mac_note)?`<h4>Mac M5 Max 128 Go</h4><p>${esc([m._local.mac_tool,m._local.mac_note].filter(Boolean).join(" · "))}</p>`:""}
      <h4>Modération</h4><p>${esc([g(m,"moderation.public_figures"), g(m,"moderation.notes")].filter(Boolean).join(" · ")||"–")}</p>
      ${g(m,"ranking.aa_note")?`<h4>Note</h4><p>${esc(g(m,"ranking.aa_note"))}</p>`:""}</div>
    <div><h4>Sources</h4><ul>${src||"<li>–</li>"}</ul></div></div>`;
}
function filtered(){
  const q = $("#q").value.trim().toLowerCase();
  return DATA[tab].filter(m => {
    if(q && !JSON.stringify([m.family,m.variant,m.vendor,m.edit_functions,g(m,"inputs.control")]).toLowerCase().includes(q)) return false;
    if($("#f-open").checked && !g(m,"access.open_weights")) return false;
    if($("#f-local").checked && !g(m,"local.runs_on_rtx5090_32gb")) return false;
    if($("#f-4090").checked && !m._local.rtx4090_24gb) return false;
    if($("#f-mac").checked && !m._local.mac_m5max_128gb) return false;
    if($("#f-lora").checked && !g(m,"inputs.lora_inference")) return false;
    if($("#f-price").checked && !m._prices.length) return false;
    if(tab==="video"){
      if($("#f-audio").checked && !g(m,"outputs.native_audio")) return false;
      if($("#f-ff").checked && !g(m,"inputs.first_frame")) return false;
      if($("#f-ref").checked && !(g(m,"inputs.image_refs_max")>0)) return false;
    }
    return true;
  });
}
function render(){
  const T = $("#t");
  if(tab==="prices"){
    $("#filters").hidden = false; document.querySelectorAll(".vonly, #filters label").forEach(e => e.hidden = true);
    const q = $("#q").value.trim().toLowerCase();
    const PC = [["Modèle",p=>esc(p.model_id),p=>p.model_id],["Plateforme",p=>esc(p.platform),p=>p.platform],["Unité",p=>esc(p.unit),p=>p.unit||""],
      ["$/s 480p",p=>money(p.price_usd_480p_s),p=>p.price_usd_480p_s??1e9,1],["$/s 720p",p=>money(p.price_usd_720p_s),p=>p.price_usd_720p_s??1e9,1],
      ["$/s 1080p",p=>money(p.price_usd_1080p_s),p=>p.price_usd_1080p_s??1e9,1],["$/image",p=>money(p.price_usd_per_image),p=>p.price_usd_per_image??1e9,1],
      ["Relevé",p=>esc(p.verified),p=>p.verified||""],["Détail",p=>`<span class="var">${esc((p.raw||"").slice(0,90))}</span>`,p=>""],
      ["Source",p=>p.source_url?`<a href="${esc(p.source_url)}" target="_blank" rel="noopener">lien</a>`:"",p=>""]];
    let rows = DATA.prices.filter(p => !q || JSON.stringify(p).toLowerCase().includes(q));
    if(sortCol!==null && PC[sortCol]){ const f=PC[sortCol][2]; rows=rows.slice().sort((a,c)=>{const x=f(a),y=f(c);return (x>y?1:x<y?-1:0)*sortDir;}); }
    T.tHead.innerHTML = "<tr>"+PC.map((c,i)=>`<th data-i="${i}" class="${i===sortCol?"sorted":""}">${esc(c[0])}</th>`).join("")+"</tr>";
    T.tBodies[0].innerHTML = rows.map(p=>"<tr>"+PC.map(c=>`<td class="${c[3]?"n":""}">${c[1](p)}</td>`).join("")+"</tr>").join("");
    $("#count").textContent = `${rows.length} / ${DATA.prices.length} prix`; return;
  }
  document.querySelectorAll("#filters label").forEach(e => e.hidden = false);
  if(tab==="gpu"){
    $("#filters").hidden = true;
    const rows = DATA.gpu||[], keys = rows.length ? Object.keys(rows[0]).filter(k=>k!=="sources") : [];
    T.tHead.innerHTML = "<tr>"+keys.map(k=>`<th>${esc(k)}</th>`).join("")+"</tr>";
    T.tBodies[0].innerHTML = rows.map(r=>"<tr>"+keys.map(k=>`<td>${typeof r[k]==="object"?esc(JSON.stringify(r[k])):esc(r[k])}</td>`).join("")+"</tr>").join("");
    $("#count").textContent = ""; return;
  }
  $("#filters").hidden = false;
  document.querySelectorAll(".vonly").forEach(e => e.hidden = tab!=="video");
  const cols = COLS[tab]; let rows = filtered();
  if(sortCol!==null){ const f = cols[sortCol][2]; rows = rows.slice().sort((a,c)=>{const x=f(a),y=f(c);return (x>y?1:x<y?-1:0)*sortDir;}); }
  T.tHead.innerHTML = "<tr>"+cols.map((c,i)=>`<th data-i="${i}" class="${i===sortCol?"sorted":""}">${esc(c[0])}${i===sortCol?(sortDir>0?" ↑":" ↓"):""}</th>`).join("")+"</tr>";
  T.tBodies[0].innerHTML = rows.map(m => `<tr class="row" data-id="${esc(m.id)}">`+cols.map((c,i)=>`<td class="${c[3]||i>=cols.length-3?"n":""}">${c[1](m)}</td>`).join("")+"</tr>"+(open.has(m.id)?`<tr class="detail"><td colspan="${cols.length}">${detail(m)}</td></tr>`:"")).join("");
  $("#count").textContent = `${rows.length} / ${DATA[tab].length} variantes`;
}
document.querySelector(".tabs").addEventListener("click", e => { const t = e.target.closest("button"); if(!t) return;
  document.querySelectorAll(".tabs button").forEach(x=>x.setAttribute("aria-selected", x===t)); tab = t.dataset.tab; sortCol=null; render(); });
$("#t").addEventListener("click", e => {
  if(tab==="gpu") return;
  const th = e.target.closest("th[data-i]"); if(th){ const i=+th.dataset.i; sortDir = sortCol===i ? -sortDir : 1; sortCol=i; render(); return; }
  if(e.target.closest("a")) return;
  const tr = e.target.closest("tr.row"); if(tr){ const id=tr.dataset.id; open.has(id)?open.delete(id):open.add(id); render(); }
});
document.querySelectorAll("#filters input").forEach(i => i.addEventListener("input", render));
$("#built").textContent = `Données relevées le 15/10/2026 · page construite le ${DATA.built} · ${DATA.video.length} variantes vidéo, ${DATA.image.length} variantes image`;
$("#foot").textContent = DATA.orphans.length ? `${DATA.orphans.length} modèles ont des prix mais pas de fiche (anciens modèles, abonnements) : ils sont dans l'onglet « Tous les prix ».` : "";
render();
</script>
