"""Pull banks / neobanks / payment providers from Wikidata (CC0) into raw/wikidata.json (resumable, one query per class).
Run: python3 scripts/fetch_wikidata.py   (needs raw/classes.json: {classQid: kind})"""
import json, sys, time, os
sys.path.insert(0, os.path.dirname(__file__))
from wd import sparql
kinds = json.load(open("raw/classes.json"))
SETS = ("bic", "website", "logo", "classes")
out = {}
if os.path.exists("raw/wikidata.json"):
    out = {k: {**v, **{f: set(v[f]) for f in SETS}} for k, v in json.load(open("raw/wikidata.json")).items()}
done = set(json.load(open("raw/done.json"))) if os.path.exists("raw/done.json") else set()
for n, (cls, kind) in enumerate(kinds.items()):
    if cls in done: continue
    rows = sparql(f'''SELECT ?i ?l ?iso ?contL ?cn ?bic ?web ?logo WHERE {{
      ?i wdt:P31 wd:{cls}; wdt:P17 ?c. ?c wdt:P297 ?iso; wdt:P30 ?cont; rdfs:label ?cn FILTER(lang(?cn)="en").
      ?cont rdfs:label ?contL FILTER(lang(?contL)="en")
      FILTER NOT EXISTS {{ ?i wdt:P576 [] }}
      ?i rdfs:label ?l FILTER(lang(?l)="en")
      OPTIONAL {{ ?i wdt:P2627 ?bic }} OPTIONAL {{ ?i wdt:P856 ?web }} OPTIONAL {{ ?i wdt:P154 ?logo }}
    }}''')
    if rows is None:
        print("FAILED", cls, flush=True); continue
    for r in rows:
        id_ = r['i']['value'].rsplit('/', 1)[1]
        e = out.setdefault(id_, {"qid": id_, "name": r['l']['value'], "country": r['iso']['value'], "countryName": r['cn']['value'],
                                 "continent": r['contL']['value'], "kind": kind, "bic": set(), "website": set(), "logo": set(), "classes": set()})
        if kind != "bank": e["kind"] = kind
        e["classes"].add(cls)
        for k, f in (('bic', 'bic'), ('web', 'website'), ('logo', 'logo')):
            if k in r: e[f].add(r[k]['value'])
    done.add(cls)
    if n % 10 == 0 or rows:
        json.dump(out, open("raw/wikidata.json", "w"), default=sorted); json.dump(sorted(done), open("raw/done.json", "w"))
    print(n, cls, len(rows), len(out), flush=True); time.sleep(0.5)
json.dump(out, open("raw/wikidata.json", "w"), default=sorted); json.dump(sorted(done), open("raw/done.json", "w")); print("DONE")
