"""Merge raw/wikidata.json (+ data/fintech-seed.json) into data/banks/<ISO2>.json and fetch logos from Wikimedia Commons.
Never touches NG.json entries that already exist (Nigeria is hand-maintained). Idempotent: existing ids are kept as-is."""
import json, os, re, sys, time, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
from common import slugify, categorize, REGION, country_file
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "bank-registry/0.1 (https://github.com/TriosCube/bank-registry)"}
MAX_LOGO = 400_000
def load(region, cc):
    p = country_file(region, cc)
    return json.load(open(p)) if os.path.exists(p) else []
def save(region, cc, rows):
    rows.sort(key=lambda b: (b["category"], b["name"].lower()))
    os.makedirs(os.path.dirname(country_file(region, cc)), exist_ok=True)
    json.dump(rows, open(country_file(region, cc), "w"), ensure_ascii=False, indent=1)

def commons_file(url):
    m = re.search(r"Special:FilePath/(.+)$", url)
    return urllib.parse.unquote(m.group(1)) if m else None

def fetch_logo(url, dest_noext):
    fn = commons_file(url)
    if not fn: return None
    ext = fn.rsplit(".", 1)[-1].lower()
    if ext not in ("svg", "png", "jpg", "jpeg", "webp"): return None
    # SVGs are served as-is; rasters are requested at 256px wide to keep the repo small
    u = "https://commons.wikimedia.org/wiki/Special:FilePath/" + urllib.parse.quote(fn) + ("" if ext == "svg" else "?width=256")
    try:
        data = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read()
    except Exception as e:
        print("  logo fail", fn, e); return None
    if len(data) > MAX_LOGO or len(data) < 100: return None
    out_ext = "svg" if ext == "svg" else ("png" if ext == "png" else "jpg" if ext in ("jpg", "jpeg") else ext)
    os.makedirs(os.path.dirname(dest_noext), exist_ok=True)
    open(f"{dest_noext}.{out_ext}", "wb").write(data)
    return f"{dest_noext}.{out_ext}", "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(fn.replace(" ", "_"))

LABELS = json.load(open(f"{root}/raw/class_labels.json"))
wd = json.load(open(f"{root}/raw/wikidata.json"))
by_cc = {}
for e in wd.values():
    cc = e["country"]
    if cc == "NG": continue
    by_cc.setdefault(cc, []).append(e)

want_logos = "--no-logos" not in sys.argv
n_new = n_logo = 0
for cc, ents in sorted(by_cc.items()):
    region = REGION.get(ents[0]["continent"], "asia")
    rows = load(region, cc); have = {b["id"] for b in rows}; have_q = {b.get("codes", {}).get("wikidata") for b in rows}
    for e in ents:
        if e["qid"] in have_q: continue
        slug = slugify(e["name"])
        if not slug: continue
        id_ = f"{cc.lower()}-{slug}"
        if id_ in have: id_ += "-" + e["qid"].lower()
        classes = [LABELS.get(c, "") for c in e["classes"]]
        cat = categorize(e["name"], classes, e["kind"])
        b = {"id": id_, "name": e["name"], "country": cc, "region": region, "category": cat,
             "codes": {"wikidata": e["qid"]}}
        bic = sorted(x for x in e["bic"] if re.fullmatch(r"[A-Z0-9]{8}([A-Z0-9]{3})?", x))
        if bic: b["codes"]["bic"] = bic[0]
        if e["website"]: b["website"] = sorted(e["website"])[0]
        if want_logos and e["logo"]:
            r = fetch_logo(sorted(e["logo"])[0], f"{root}/logos/{cc.lower()}/{slug}")
            if r:
                b["logo"] = {"path": os.path.relpath(r[0], root), "source": r[1], "license": "See Wikimedia Commons file page; trademark of its owner"}
                n_logo += 1; time.sleep(0.25)
        rows.append(b); have.add(id_); have_q.add(e["qid"]); n_new += 1
    save(region, cc, rows)
    print(cc, len(rows), flush=True)
print("new", n_new, "logos", n_logo)
