import json, csv, sys, os
"""usage: python build2.py CHARTDIR OUT.html [--standalone]
--standalone writes a complete HTML document (for static hosting, e.g. a Jekyll/GitHub Pages folder)
with a back link to the site root and a CSV download link."""
STANDALONE = "--standalone" in sys.argv
from credits import CREDITS, SERVICES, key
CH = sys.argv[1]; out_html = sys.argv[2]
T = json.load(open(f"{CH}/targets.json"))
picks = {"NGC 891", "IC 342", "Maffei 1", "Maffei 2", "NGC 7331", "M74 Phantom", "NGC 2403", "M51 Whirlpool", "M64 Black Eye",
         "IC 1396A Elephant Trunk", "Barnard 361", "NGC 1333", "LDN 1551 / HL Tau", "Horsehead + NGC 2023", "Barnard 335",
         "W3 / IC 1795", "Cygnus Wall (NGC 7000)", "Barnard 92 / 93", "Eagle Pillars (M16)",
         "NGC 604 in M33", "NGC 7714 / 7715 (Arp 284)", "IC 1613", "NGC 1569", "NGC 2366 / Mrk 71", "M101 HII regions", "NGC 4449",
         "Centaurus A (NGC 5128)", "NGC 253 Sculptor", "Circinus galaxy", "NGC 1365", "30 Doradus / Tarantula", "NGC 346 in the SMC",
         "M83 Southern Pinwheel", "Carina Keyhole", "Thackeray's globules (IC 2944)", "NGC 3603", "CG 4 (God's Hand)",
         "R CrA / NGC 6729", "Barnard 68", "Galactic Centre field", "Cat's Paw NGC 6334"}
for t in T:
    t["pick"] = t["name"] in picks
    t["cred"] = sorted({key(l) for l in t["labels"] if key(l)}, key=list(CREDITS).index)
used = [k for k in CREDITS if any(k in t["cred"] for t in T)]
with open(os.path.join(os.path.dirname(out_html), "IMAGE_CREDITS.txt"), "w") as f:
    f.write("Image credits for the finding-chart previews (charts/*.jpg)\n\n")
    for k in used:
        n, h, a, r = CREDITS[k]
        f.write(f"{n}\n  HiPS: {h}\n  Reference: {r}\n  Acknowledgement: {a}\n\n")
    f.write("Services\n  " + SERVICES + "\n")
MON = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()

CSV = out_html.replace(".html", ".csv") if not STANDALONE else os.path.join(os.path.dirname(out_html), "targets.csv")
with open(CSV, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["type", "name", "ra_j2000", "dec_j2000", "ra_deg", "dec_deg", "gal_l", "gal_b", "size",
                *[f"maxalt_{s}" for s in T[0]["alt"]], *[f"N_hrs_{m}" for m in MON], *[f"S_hrs_{m}" for m in MON],
                "surveys_colour_u_g_r_i_z_Y", "notes"])
    for t in T:
        w.writerow([{"G": "galaxy", "D": "dust", "S": "star-forming"}[t["kind"]], t["name"], t["ra"], t["dec"], t["radeg"], t["decdeg"],
                    t["l"], t["b"], t["size"], *t["alt"].values(), *t["vis"]["N"], *t["vis"]["S"], " | ".join(t["labels"]), t["why"]])

page = r"""<title>Camera Showcase Targets</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: observing-log page. Sticky filter bar (type, hemisphere, months), overview table, then one card per field:
   large colour preview beside a 3x2 grid of u g r / i z Y, plus a 12-month dark-time strip for each hemisphere. */
:root{
  --bg:#f3f4f6; --panel:#ffffff; --fg:#151a22; --muted:#5b6474; --line:#d9dde4;
  --accent:#0b7f95; --accent-soft:#dff1f4; --warn:#946200; --warn-soft:#fbf0d6; --bad:#8a3a3a; --bad-soft:#f6e3e3;
  --dust:#7a4e1f; --dust-soft:#f3e8da; --sf:#5b3fa6; --sf-soft:#ece6f8; --vis:11,127,149; --cell:#e7eaee;
  --sans:"Archivo",system-ui,-apple-system,"Segoe UI",sans-serif; --mono:"IBM Plex Mono",ui-monospace,Menlo,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#0c0f14; --panel:#141922; --fg:#e6e9ef; --muted:#97a0b0; --line:#262d3a;
  --accent:#4cc3d8; --accent-soft:#12303a; --warn:#e5b54a; --warn-soft:#33290f; --bad:#e08a8a; --bad-soft:#341a1a;
  --dust:#e0a866; --dust-soft:#33240f; --sf:#b8a3f0; --sf-soft:#261d40; --vis:76,195,216; --cell:#1c222d; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#0c0f14; --panel:#141922; --fg:#e6e9ef; --muted:#97a0b0; --line:#262d3a;
  --accent:#4cc3d8; --accent-soft:#12303a; --warn:#e5b54a; --warn-soft:#33290f; --bad:#e08a8a; --bad-soft:#341a1a;
  --dust:#e0a866; --dust-soft:#33240f; --sf:#b8a3f0; --sf-soft:#261d40; --vis:76,195,216; --cell:#1c222d; color-scheme:dark}
body{background:var(--bg);color:var(--fg);font-family:var(--sans);font-size:15px;line-height:1.5}
.wrap{max-width:1180px;margin:0 auto;padding-block:28px 60px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:grid;gap:22px}
h1{font-size:30px;font-weight:700;letter-spacing:-.01em;margin:0;text-wrap:balance}
h2{font-size:19px;margin:0;font-weight:600;text-wrap:balance}
.lede{color:var(--muted);max-width:76ch;margin:6px 0 0}
.lede b{color:var(--fg);font-weight:600}
.legend{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px}
.legend div{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:10px 12px;font-size:13.5px;color:var(--muted);min-width:0}
.legend b{display:block;color:var(--fg);font-size:12px;letter-spacing:.06em;text-transform:uppercase;margin-bottom:2px}
.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);padding-block:10px;display:grid;gap:8px;border-bottom:1px solid var(--line)}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.lbl{font:600 11px var(--sans);letter-spacing:.06em;text-transform:uppercase;color:var(--muted);min-width:64px}
.seg{display:inline-flex;flex-wrap:wrap;border:1px solid var(--line);border-radius:6px;overflow:hidden}
.seg button,.chk{font:500 13px var(--sans);background:var(--panel);color:var(--fg);border:0;padding:6px 11px;cursor:pointer}
.seg button+button{border-left:1px solid var(--line)}
.seg button[aria-pressed="true"]{background:var(--accent);color:var(--bg)}
.months button{padding:6px 9px;font-family:var(--mono);font-size:12.5px}
.chk{border:1px solid var(--line);border-radius:6px;display:inline-flex;gap:6px;align-items:center}
.link{font:500 13px var(--sans);background:none;border:0;color:var(--accent);cursor:pointer;padding:4px}
button:focus-visible,.chk:focus-within,a:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.count{margin-left:auto;color:var(--muted);font:13px var(--mono)}
.tbl{overflow-x:auto;background:var(--panel);border:1px solid var(--line);border-radius:6px;max-height:460px;overflow-y:auto}
table{border-collapse:collapse;width:100%;font-size:13px;font-variant-numeric:tabular-nums}
th,td{text-align:left;padding:5px 10px;border-bottom:1px solid var(--line);white-space:nowrap}
th{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-weight:600;position:sticky;top:0;background:var(--panel)}
td.m{font-family:var(--mono)}
td a{color:var(--accent);text-decoration:none;font-weight:600}
.cards{display:grid;gap:18px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:16px;display:grid;gap:12px;scroll-margin-top:150px}
.head{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:baseline}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{font:600 11px var(--sans);letter-spacing:.05em;text-transform:uppercase;padding:2px 8px;border-radius:999px;background:var(--accent-soft);color:var(--accent)}
.chip.D{background:var(--dust-soft);color:var(--dust)}
.chip.S{background:var(--sf-soft);color:var(--sf)}
.chip.hemi{background:var(--cell);color:var(--fg)}
.chip.pick{background:var(--fg);color:var(--bg)}
.meta{display:flex;flex-wrap:wrap;gap:4px 18px;font:13px var(--mono);color:var(--muted)}
.meta b{color:var(--fg);font-weight:500}
.why{margin:0;max-width:80ch}
.body{display:grid;grid-template-columns:minmax(0,2fr) minmax(0,3fr);gap:6px}
.bands{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px;align-content:start}
.pan{width:100%;aspect-ratio:1;max-width:100%;border:0;padding:0;border-radius:3px;background-color:#000;background-repeat:no-repeat;background-size:700% 100%;cursor:zoom-in}
.vis{display:grid;grid-template-columns:auto repeat(12,minmax(0,1fr));gap:2px;font:11px var(--mono);color:var(--muted);align-items:center;max-width:520px}
.vis span.c{height:16px;border-radius:2px;background:var(--cell);position:relative}
.vis span.c i{position:absolute;inset:0;border-radius:2px;background:rgb(var(--vis))}
.vis span.c.sel{outline:1.5px solid var(--fg);outline-offset:0}
.vis .h{padding-right:6px}
.vis .ml{text-align:center}
.mini{display:inline-grid;grid-template-columns:repeat(12,7px);gap:1px;vertical-align:middle}
.mini span{height:10px;background:var(--cell);position:relative}
.mini span i{position:absolute;inset:0;background:rgb(var(--vis))}
.copy{font:500 12px var(--sans);border:1px solid var(--line);background:transparent;color:var(--muted);border-radius:5px;padding:2px 8px;cursor:pointer}
.foot{color:var(--muted);font-size:13px;max-width:84ch}
.back{display:inline-block;margin-bottom:10px;font-size:13px;color:var(--accent);text-decoration:none}
.lede a{color:var(--accent)}
.cred{font-size:12.5px;color:var(--muted)}
.cred b{color:var(--fg);font-weight:500}
.credits{display:grid;gap:10px}
.credits dl{margin:0;display:grid;gap:12px;background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:14px 16px}
.credits dt{font-weight:600}
.credits dd{margin:2px 0 0;font-size:13px;color:var(--muted);max-width:90ch}
.credits code{font:12px var(--mono);color:var(--fg)}
.empty{color:var(--muted);padding:24px;text-align:center;background:var(--panel);border:1px dashed var(--line);border-radius:8px}
.zoom{position:fixed;inset:0;background:rgba(0,0,0,.9);display:grid;place-items:center;z-index:20;padding:max(16px,env(safe-area-inset-top,0px)) max(16px,env(safe-area-inset-right,0px)) max(16px,env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-left,0px))}
.zbox{display:grid;gap:10px;justify-items:center}
.zimg{width:min(88vw,78vh,760px);aspect-ratio:1;background-repeat:no-repeat;background-size:700% 100%;background-color:#000;border-radius:4px}
.zctl{display:flex;flex-wrap:wrap;gap:6px;justify-content:center}
.zctl button{font:500 13px var(--sans);background:#1b212b;color:#e6e9ef;border:1px solid #333c4a;border-radius:5px;padding:6px 11px;cursor:pointer}
.zctl button[aria-pressed="true"]{background:#4cc3d8;color:#0c0f14}
.ztitle{color:#e6e9ef;font:600 15px var(--sans)}
@media (max-width:760px){.body{grid-template-columns:minmax(0,1fr)} h1{font-size:24px}}
@media (prefers-reduced-motion:no-preference){.pan{transition:opacity .15s}.pan:hover{opacity:.85}}
</style>

<div class="wrap">
  <header>
    <h1>Camera showcase targets: u to Y across both hemispheres</h1>
    __BACK__<p class="lede"><b>__N__ fields</b> for the LCO 1-m network and a <b>26′ × 26′</b> camera: galaxies that fit the field, star-forming galaxies for the u band, and Galactic dust clouds for the optical-versus-Y comparison. Each preview is 40′ wide with the <b>cyan box showing the camera footprint</b> (north up, east left). Pick months and a hemisphere to see what is up; click any panel to enlarge it and step through u, g, r, i, z, Y.__CSVLINK__</p>
  </header>

  <div class="legend">
    <div><b>u band</b>SDSS u in the north, SkyMapper u in the south. Where neither exists the panel shows GALEX NUV (0.23 µm), flagged in red.</div>
    <div><b>g, r, i, z</b>Pan-STARRS DR1 down to δ ≈ −30°, then DESI Legacy Surveys DR10, DES DR2 or SkyMapper.</div>
    <div><b>Y band</b>VISTA VVV Y in the southern Galactic plane and bulge, otherwise Pan-STARRS y or DES Y. Elsewhere in the far south it falls back to 2MASS J, flagged in red.</div>
    <div><b>Visibility</b>Hours per night with the Sun below −18° and the field above 30° (airmass &lt; 2), on the 15th of each month. Best of McDonald and Teide (north) or CTIO, SAAO and Siding Spring (south).</div>
  </div>

  <div class="bar" role="toolbar" aria-label="Filter targets">
    <div class="row"><span class="lbl">Type</span>
      <div class="seg" id="kind">
        <button type="button" data-k="all" aria-pressed="true">All</button>
        <button type="button" data-k="G" aria-pressed="false">Galaxies</button>
        <button type="button" data-k="S" aria-pressed="false">Star-forming</button>
        <button type="button" data-k="D" aria-pressed="false">Dust clouds</button>
      </div>
      <label class="chk"><input type="checkbox" id="onlyPick"> Shortlist only</label>
    </div>
    <div class="row"><span class="lbl">Sites</span>
      <div class="seg" id="hemi">
        <button type="button" data-h="NS" aria-pressed="true">North + South</button>
        <button type="button" data-h="N" aria-pressed="false">North</button>
        <button type="button" data-h="S" aria-pressed="false">South</button>
      </div>
      <span class="count" id="count"></span>
    </div>
    <div class="row"><span class="lbl">Months</span>
      <div class="seg months" id="months"></div>
      <button type="button" class="link" id="clearM">Any month</button>
    </div>
  </div>

  <section style="display:grid;gap:10px">
    <h2>Overview</h2>
    <div class="tbl"><table>
      <thead><tr><th>Target</th><th>Type</th><th>RA (J2000)</th><th>Dec</th><th>b (°)</th><th>Size</th><th>Visible N (J–D)</th><th>Visible S (J–D)</th></tr></thead>
      <tbody id="rows"></tbody>
    </table></div>
  </section>

  <section class="cards" id="cards"></section>

  <section class="credits" id="credits">
    <h2>Image credits</h2>
    <p class="foot" style="margin:0">The previews are built from the public surveys below. Each panel names its survey in the top-left label. If you reuse a preview, credit the survey and cite its reference.</p>
    <dl>__CREDLIST__</dl>
    <p class="foot" style="margin:0">__SERVICES__</p>
  </section>

  <p class="foot">A field counts as visible in a month when it gets at least 2 h of dark time above 30° at one of the selected hemisphere's sites. Sites: McDonald (+30.7°) and Teide (+28.3°) in the north; CTIO (−30.2°), SAAO Sutherland (−32.4°) and Siding Spring (−31.3°) in the south. Panels are independent asinh stretches, so compare structure between bands, not absolute brightness. The surveys differ in depth and seeing, so the previews are a lower bound on what the new camera will show. Cutouts come from CDS hips2fits. Coordinates come from Sesame/SIMBAD, or are hand-picked field centres where a field frames several objects.</p>
</div>

<div class="zoom" id="zoom" hidden>
  <div class="zbox">
    <div class="ztitle" id="ztitle"></div>
    <div class="zimg" id="zimg" role="img"></div>
    <div class="zctl" id="zctl"></div>
    <div class="zctl"><button type="button" id="zclose">Close (Esc)</button></div>
  </div>
</div>

<script>
const T = __DATA__;
const CR = __CRED__;
const MON = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
const K = {G:"Galaxy", D:"Dust", S:"Star-forming"};
const BANDS = ["colour","u","g","r","i","z","Y"];
const MINH = 2;
const S = {kind:"all", hemi:"NS", months:[], pick:false};
try{ Object.assign(S, JSON.parse(localStorage.getItem("camtargets2")||"{}")); }catch(e){}
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const pos = k => `${k*100/6}% 0`;
const ok = (t,h,m) => t.vis[h][m] >= MINH;
const visibleIn = (t,h) => h.split("").some(x => S.months.length ? S.months.some(m => ok(t,x,m)) : t.vis[x].some(v => v >= MINH));
function hemiChip(t){
  const n = t.vis.N.some(v=>v>=MINH), s = t.vis.S.some(v=>v>=MINH);
  return n&&s ? "North + South" : n ? "North only" : s ? "South only" : "Hard to reach";
}
function best(t){
  const out = [];
  for (const h of ["N","S"]) { const v=t.vis[h]; const mx=Math.max(...v); if(mx<MINH) continue;
    const ms = v.map((x,i)=>x>=mx*0.75?MON[i]:null).filter(Boolean); out.push(`${h==="N"?"North":"South"} best ${ms[0]}–${ms[ms.length-1]}`); }
  return out.join(" · ");
}
const shade = v => Math.min(1, v/10).toFixed(2);
function visGrid(t){
  let h = `<span></span>` + MON.map(m=>`<span class="ml">${m[0]}</span>`).join("");
  for (const x of ["N","S"]) {
    h += `<span class="h">${x==="N"?"North":"South"}</span>` + t.vis[x].map((v,i)=>
      `<span class="c${S.months.includes(i)?" sel":""}" title="${MON[i]}: ${v} h"><i style="opacity:${shade(v)}"></i></span>`).join("");
  }
  return `<div class="vis" aria-label="Dark hours above 30 degrees per month">${h}</div>`;
}
const mini = v => `<span class="mini">${v.map((x,i)=>`<span title="${MON[i]}: ${x} h"><i style="opacity:${shade(x)}"></i></span>`).join("")}</span>`;
function render(){
  const v = T.filter(t => (S.kind=="all"||t.kind==S.kind) && (!S.pick||t.pick) && visibleIn(t,S.hemi));
  document.getElementById("count").textContent = `${v.length} of ${T.length} fields`;
  document.getElementById("rows").innerHTML = v.map(t => `<tr><td><a href="#${t.slug}">${esc(t.name)}</a></td><td>${K[t.kind].toLowerCase()}</td><td class="m">${t.ra}</td><td class="m">${t.dec}</td><td class="m">${t.b}</td><td>${esc(t.size)}</td><td>${mini(t.vis.N)}</td><td>${mini(t.vis.S)}</td></tr>`).join("");
  document.getElementById("cards").innerHTML = v.length ? v.map(t => `<article class="card" id="${t.slug}">
    <div class="head"><h2>${esc(t.name)}</h2><div class="chips"><span class="chip ${t.kind}">${K[t.kind]}</span><span class="chip hemi">${hemiChip(t)}</span>${t.pick?`<span class="chip pick">shortlist</span>`:""}</div></div>
    <div class="meta"><span><b>${t.ra} ${t.dec}</b></span><button type="button" class="copy" data-c="${t.ra} ${t.dec}">Copy coords</button>
      <span>l,b = <b>${t.l}, ${t.b}</b></span><span>size <b>${esc(t.size)}</b></span><span>${best(t)}</span></div>
    <p class="why">${esc(t.why)}</p>
    <div class="body">
      <button type="button" class="pan" data-s="${t.slug}" data-k="0" style="background-image:url(charts/${t.strip});background-position:${pos(0)}" aria-label="${esc(t.name)}: ${esc(t.labels[0])}"></button>
      <div class="bands">${[1,2,3,4,5,6].map(k=>`<button type="button" class="pan" data-s="${t.slug}" data-k="${k}" style="background-image:url(charts/${t.strip});background-position:${pos(k)}" aria-label="${esc(t.name)}: ${esc(t.labels[k])}"></button>`).join("")}</div>
    </div>
    ${visGrid(t)}
    <div class="cred">Image credits: <b>${t.cred.map(k=>CR[k][0]).join(", ")}</b>. Full acknowledgements are under Image credits at the bottom of the page.</div>
  </article>`).join("") : `<div class="empty">No fields match. Add a month, switch to North + South, or turn off Shortlist only.</div>`;
  document.querySelectorAll("#kind button").forEach(b => b.setAttribute("aria-pressed", b.dataset.k==S.kind));
  document.querySelectorAll("#hemi button").forEach(b => b.setAttribute("aria-pressed", b.dataset.h==S.hemi));
  document.querySelectorAll("#months button").forEach(b => b.setAttribute("aria-pressed", S.months.includes(+b.dataset.m)));
  document.getElementById("onlyPick").checked = S.pick;
  try{ localStorage.setItem("camtargets2", JSON.stringify(S)); }catch(e){}
}
document.getElementById("months").innerHTML = MON.map((m,i)=>`<button type="button" data-m="${i}" aria-pressed="false">${m}</button>`).join("");
document.getElementById("kind").addEventListener("click", e => { const k=e.target.dataset?.k; if(k){S.kind=k;render();} });
document.getElementById("hemi").addEventListener("click", e => { const h=e.target.dataset?.h; if(h){S.hemi=h;render();} });
document.getElementById("months").addEventListener("click", e => { const m=e.target.dataset?.m; if(m===undefined) return; const i=+m;
  S.months = S.months.includes(i) ? S.months.filter(x=>x!==i) : [...S.months,i].sort((a,b)=>a-b); render(); });
document.getElementById("clearM").addEventListener("click", () => { S.months=[]; render(); });
document.getElementById("onlyPick").addEventListener("change", e => {S.pick=e.target.checked;render();});
let Z = null;
function showZ(){
  const t = T.find(x=>x.slug==Z.s);
  const zi = document.getElementById("zimg");
  zi.style.backgroundImage = `url(charts/${t.strip})`; zi.style.backgroundPosition = pos(Z.k);
  zi.setAttribute("aria-label", `${t.name}: ${t.labels[Z.k]}`);
  document.getElementById("ztitle").textContent = `${t.name} · ${t.labels[Z.k]}`;
  document.getElementById("zctl").innerHTML = BANDS.map((b,k)=>`<button type="button" data-k="${k}" aria-pressed="${k==Z.k}">${b}</button>`).join("");
  document.getElementById("zoom").hidden = false;
}
document.getElementById("cards").addEventListener("click", e => {
  const c = e.target.closest(".copy");
  if(c){ navigator.clipboard.writeText(c.dataset.c).then(()=>{c.textContent="Copied";setTimeout(()=>c.textContent="Copy coords",1200)}).catch(()=>{c.textContent=c.dataset.c}); return; }
  const p = e.target.closest(".pan"); if(p){ Z={s:p.dataset.s,k:+p.dataset.k}; showZ(); }
});
document.getElementById("zctl").addEventListener("click", e => { const k=e.target.dataset?.k; if(k!==undefined){Z.k=+k;showZ();} });
document.getElementById("zclose").addEventListener("click", () => document.getElementById("zoom").hidden=true);
document.getElementById("zoom").addEventListener("click", e => { if(e.target.id=="zoom") e.currentTarget.hidden=true; });
document.addEventListener("keydown", e => {
  const zo = document.getElementById("zoom"); if(zo.hidden) return;
  if(e.key=="Escape") zo.hidden=true;
  if(e.key=="ArrowRight"){Z.k=(Z.k+1)%7;showZ();}
  if(e.key=="ArrowLeft"){Z.k=(Z.k+6)%7;showZ();}
});
render();
</script>
"""
import html
cl = "".join(f"<div><dt>{html.escape(CREDITS[k][0])}</dt><dd>{html.escape(CREDITS[k][2])}</dd><dd>Reference: {html.escape(CREDITS[k][3])}. HiPS: <code>{html.escape(CREDITS[k][1])}</code></dd></div>" for k in used)
HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Galaxy, star-forming and Galactic dust fields for a 26 arcmin LCO 1-m camera, with u to Y finding charts and monthly visibility from both hemispheres.">
<style>*,*::before,*::after{box-sizing:border-box}html{color-scheme:light;-webkit-text-size-adjust:100%}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
"""
if STANDALONE:
    page = HEAD + page.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "").replace("<style>\n/* Layout", "</head>\n<body>\n<style>\n/* Layout", 1) + "</body>\n</html>\n"
    page = page.replace("__BACK__", '<a class="back" href="/">← Daniel Harbeck\'s page</a>\n    ').replace("__CSVLINK__", ' Download the full list as <a href="targets.csv">CSV</a>.')
else:
    page = page.replace("__BACK__", "").replace("__CSVLINK__", "")
open(out_html, "w").write(page.replace("__DATA__", json.dumps(T)).replace("__N__", str(len(T)))
    .replace("__CRED__", json.dumps({k: CREDITS[k] for k in used})).replace("__CREDLIST__", cl).replace("__SERVICES__", html.escape(SERVICES)))
print("ok", len(T))
