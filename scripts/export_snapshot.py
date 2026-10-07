"""Export a trimmed snapshot for apps: <out>/banks.registry.json plus logos copied to <out_logos>/<iso2>/<file>.
Usage: python3 scripts/export_snapshot.py <registry.json out> <logos dir out>"""
import json, os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from wd import sparql
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out_json, out_logos = sys.argv[1], sys.argv[2]
rows = sparql('SELECT ?iso ?l WHERE { ?c wdt:P31 wd:Q3624078; wdt:P297 ?iso; rdfs:label ?l FILTER(lang(?l)="en") }') or []
names = {r['iso']['value']: r['l']['value'] for r in rows}
banks = json.load(open(f"{root}/dist/banks.json"))
out = []
for b in banks:
    if b.get("status") == "inactive": continue
    e = {"id": b["id"], "name": b["name"], "country": b["country"], "country_name": names.get(b["country"], b["country"]), "category": b["category"]}
    if b.get("codes", {}).get("nip"): e["nip"] = b["codes"]["nip"]
    if "logo" in b:
        rel = b["logo"]["path"].removeprefix("logos/")
        e["logo"] = rel
        os.makedirs(os.path.dirname(f"{out_logos}/{rel}"), exist_ok=True)
        shutil.copy(f"{root}/{b['logo']['path']}", f"{out_logos}/{rel}")
    out.append(e)
out.sort(key=lambda e: e["name"].lower())
os.makedirs(os.path.dirname(out_json), exist_ok=True)
json.dump(out, open(out_json, "w"), ensure_ascii=False, separators=(",", ":"))
print(len(out), "banks;", sum("logo" in e for e in out), "logos;", len({e['country'] for e in out}), "countries")
