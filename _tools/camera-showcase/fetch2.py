"""Fetch colour + u,g,r,i,z,Y cutouts for every target, with survey fallbacks,
and compute monthly dark-time visibility at the five LCO 1-m sites.
usage: python fetch2.py OUTDIR [only-slug ...]"""
import io, json, sys, os, re, urllib.parse
from concurrent.futures import ThreadPoolExecutor
import numpy as np, requests
from astropy.io import fits
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, get_sun
from astropy.time import Time
import astropy.units as u
from PIL import Image, ImageDraw, ImageFont
from targets import GALAXIES, DUST, STARBURST

OUT = sys.argv[1]; ONLY = set(sys.argv[2:])
FOV_DEG, NPIX, CAM_ARCMIN = 40/60, 320, 26
HIPS = "https://alasky.cds.unistra.fr/hips-image-services/hips2fits"
SITES = {  # LCO 1-m sites: name: (lat, lon, hemisphere)
    "McDonald": (30.68, -104.02, "N"), "Teide": (28.30, -16.51, "N"),
    "CTIO": (-30.17, -70.80, "S"), "SAAO": (-32.38, 20.81, "S"), "Siding Spring": (-31.27, 149.07, "S")}
MIN_ALT = 30.0  # deg, airmass < 2

# survey chains per band: (label, hips id). First one with real data wins.
PS1, LEG, DES, SKY = "CDS/P/PanSTARRS/DR1/", "CDS/P/DESI-Legacy-Surveys/DR10/", "CDS/P/DES-DR2/", "CDS/P/skymapper-"
CHAINS = {
    "u": [("SDSS u", "CDS/P/SDSS9/u"), ("SkyMapper u", SKY+"U"), ("no u: GALEX NUV", "CDS/P/GALEXGR6_7/NUV")],
    "g": [("PS1 g", PS1+"g"), ("Legacy g", LEG+"g"), ("DES g", DES+"g"), ("SkyMapper g", SKY+"G"), ("no g: DSS2 blue", "CDS/P/DSS2/blue")],
    "r": [("PS1 r", PS1+"r"), ("Legacy r", LEG+"r"), ("DES r", DES+"r"), ("SkyMapper r", SKY+"R"), ("no r: DSS2 red", "CDS/P/DSS2/red")],
    "i": [("PS1 i", PS1+"i"), ("Legacy i", LEG+"i"), ("DES i", DES+"i"), ("SkyMapper i", SKY+"I"), ("no i: DSS2 NIR", "CDS/P/DSS2/NIR")],
    "z": [("PS1 z", PS1+"z"), ("Legacy z", LEG+"z"), ("DES z", DES+"z"), ("SkyMapper z", SKY+"Z")],
    "Y": [("VVV Y", "CDS/P/VISTA/VVV/DR4/Y"), ("PS1 y", PS1+"y"), ("DES Y", DES+"Y"), ("no Y: 2MASS J", "CDS/P/2MASS/J")],
}
COLOUR = {"PS1": PS1+"color-i-r-g", "Legacy": LEG+"color", "DES": DES+"ColorIRG"}

def resolve(ident):
    if re.match(r"^\d\d \d\d", ident):
        return SkyCoord(ident, unit=(u.hourangle, u.deg))
    t = requests.get("https://cds.unistra.fr/cgi-bin/nph-sesame/-oI/SNV?" + urllib.parse.quote(ident), timeout=30).text
    m = re.search(r"^%J ([\d.]+) ([+-][\d.]+)", t, re.M)
    if not m: raise ValueError(f"cannot resolve {ident}")
    return SkyCoord(float(m[1]), float(m[2]), unit=u.deg)

def get(hips, c, fmt):
    p = dict(hips=hips, width=NPIX, height=NPIX, fov=FOV_DEG, projection="TAN", coordsys="icrs",
             ra=c.ra.deg, dec=c.dec.deg, format=fmt)
    for _ in range(3):
        try:
            r = requests.get(HIPS, params=p, timeout=180)
            if r.status_code == 200: return r.content
        except requests.RequestException: pass
    return None

def good(d, thr=0.85):
    if d is None: return False
    d = np.asarray(d, float); f = np.isfinite(d) & (d != 0)
    return f.mean() > thr and np.nanstd(d[f]) > 0

def fetch_band(band, c):
    for label, hips in CHAINS[band]:
        raw = get(hips, c, "fits")
        if raw is None: continue
        try: d = fits.getdata(io.BytesIO(raw))
        except Exception: continue
        if d is not None and d.ndim == 3: d = d[0]
        if good(d, 0.95 if "Legacy" in label else 0.85): return label, d
    return f"no {band} data", None

def stretch(data, arr=False):
    d = np.nan_to_num(np.asarray(data, float))
    bg = np.median(d); sig = 1.4826*np.median(np.abs(d-bg))
    if sig <= 0: sig = max(np.percentile(d, 90)-bg, 1e-6)/3
    hi = max(np.percentile(d, 99.7) - bg, 3*sig)
    x = np.arcsinh((d-bg)/(2*sig)) / np.arcsinh(hi/(2*sig))
    img = (np.clip(x, -0.05, 1)+0.05)/1.05*255
    if arr: return np.flipud(img)
    return Image.fromarray(np.flipud(img).astype(np.uint8)).convert("RGB")

try: FONT = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
except Exception: FONT = ImageFont.load_default()

def overlay(im, label, warn=False):
    d = ImageDraw.Draw(im)
    h = CAM_ARCMIN/60/FOV_DEG*NPIX/2; c = NPIX/2
    d.rectangle([c-h, c-h, c+h, c+h], outline=(0, 230, 255), width=2)
    d.rectangle([0, 0, 8+d.textlength(label, font=FONT), 20], fill=(150, 40, 40) if warn else (0, 0, 0))
    d.text((4, 2), label, fill=(255, 255, 255), font=FONT)
    x0, y0 = NPIX-14, NPIX-14
    d.line([x0, y0, x0, y0-26], fill=(255, 220, 0), width=2); d.text((x0-4, y0-42), "N", fill=(255, 220, 0), font=FONT)
    d.line([x0, y0, x0-26, y0], fill=(255, 220, 0), width=2); d.text((x0-42, y0-8), "E", fill=(255, 220, 0), font=FONT)
    return im

def visibility(coords):
    """hours per month (15th) with Sun < -18 and target alt > MIN_ALT; max over sites in each hemisphere."""
    ra = np.array([c.ra.rad for c in coords]); dec = np.array([c.dec.rad for c in coords])
    out = {"N": np.zeros((len(coords), 12)), "S": np.zeros((len(coords), 12))}
    step = 10/60
    for name, (lat, lon, hemi) in SITES.items():
        loc = EarthLocation(lat=lat*u.deg, lon=lon*u.deg)
        for m in range(12):
            # local noon -> next local noon
            t0 = Time(f"2027-{m+1:02d}-15T12:00:00") - lon/15*u.hour
            t = t0 + np.arange(0, 24, step)*u.hour
            sun = get_sun(t).transform_to(AltAz(obstime=t, location=loc)).alt.deg
            dark = sun < -18
            lst = t[dark].sidereal_time("mean", longitude=lon*u.deg).rad
            H = lst[None, :] - ra[:, None]
            phi = np.radians(lat)
            alt = np.degrees(np.arcsin(np.sin(phi)*np.sin(dec)[:, None] + np.cos(phi)*np.cos(dec)[:, None]*np.cos(H)))
            hrs = (alt > MIN_ALT).sum(1)*step
            out[hemi][:, m] = np.maximum(out[hemi][:, m], hrs)
    return out

def do(job):
    kind, i, (name, ident, size, why) = job
    slug = f"{kind}{i:02d}"
    meta = f"{OUT}/{slug}.json"
    if slug not in ONLY and os.path.exists(meta) and os.path.exists(f"{OUT}/{slug}.jpg"):
        m = json.load(open(meta))
        if m["ident"] == ident: return m
    c = resolve(ident)
    bands = {b: fetch_band(b, c) for b in "ugrizY"}
    src = bands["g"][0].split()[0]
    col = get(COLOUR[src], c, "jpg") if src in COLOUR else None
    if col:
        col_lab = f"{src} colour"; cim = Image.open(io.BytesIO(col)).convert("RGB").resize((NPIX, NPIX))
    elif all(bands[b][1] is not None for b in "gri"):
        col_lab = "DSS2 B,R,NIR" if src == "no" else f"{src} i,r,g"
        cim = Image.fromarray(np.dstack([stretch(bands[b][1], True) for b in "irg"]).astype(np.uint8))
    else:
        col = get("CDS/P/DSS2/color", c, "jpg")
        col_lab = "DSS2 colour" if col else "no colour data"
        cim = Image.open(io.BytesIO(col)).convert("RGB").resize((NPIX, NPIX)) if col else Image.new("RGB", (NPIX, NPIX), (25, 25, 25))
    panels = [overlay(cim, col_lab)]
    labels = [col_lab]
    for b in "ugrizY":
        lab, d = bands[b]
        warn = lab.startswith("no ")
        im = stretch(d) if d is not None else Image.new("RGB", (NPIX, NPIX), (25, 25, 25))
        panels.append(overlay(im, lab, warn)); labels.append(lab)
    strip = Image.new("RGB", (NPIX*7, NPIX))
    for k, p in enumerate(panels): strip.paste(p, (k*NPIX, 0))
    fn = f"{slug}.jpg"; strip.save(f"{OUT}/{fn}", quality=80)
    g = c.galactic
    rec = dict(kind=kind, slug=slug, name=name, ident=ident, size=size, why=why,
                ra=c.ra.to_string(u.hourangle, sep=":", precision=1, pad=True),
                dec=c.dec.to_string(u.deg, sep=":", precision=0, alwayssign=True, pad=True),
                radeg=round(c.ra.deg, 5), decdeg=round(c.dec.deg, 5), l=round(g.l.deg, 1), b=round(g.b.deg, 1),
                alt={k: round(90-abs(c.dec.deg-v[0])) for k, v in SITES.items()},
                strip=fn, labels=labels)
    json.dump(rec, open(meta, "w"))
    return rec

jobs = [(k, i, r) for k, L in (("G", GALAXIES), ("S", STARBURST), ("D", DUST)) for i, r in enumerate(L)]
if ONLY: jobs = [j for j in jobs if f"{j[0]}{j[1]:02d}" in ONLY]
with ThreadPoolExecutor(8) as ex:
    res = list(ex.map(do, jobs))
vis = visibility([SkyCoord(t["radeg"], t["decdeg"], unit=u.deg) for t in res])
for k, t in enumerate(res):
    t["vis"] = {h: [round(float(x), 1) for x in vis[h][k]] for h in "NS"}
path = f"{OUT}/targets.json"
old = json.load(open(path)) if ONLY and os.path.exists(path) else []
done = {t["slug"] for t in res}
res = [t for t in old if t["slug"] not in done] + res
order = {f"{k}{i:02d}": n for n, (k, i, _) in enumerate((k, i, r) for k, L in (("G", GALAXIES), ("S", STARBURST), ("D", DUST)) for i, r in enumerate(L))}
res.sort(key=lambda t: order.get(t["slug"], 999))
json.dump(res, open(path, "w"), indent=1)
print(len(res), "targets written")
