"""Second pass for classes that timed out in fetch_wikidata.py (e.g. plain 'bank'): query per country."""
import json, sys, time, os
sys.path.insert(0, os.path.dirname(__file__))
from wd import sparql
kinds = json.load(open("raw/classes.json")); done = set(json.load(open("raw/done.json")))
failed = [c for c in kinds if c not in done]
print("failed classes", failed)
countries = sparql('''SELECT ?c ?iso ?cn ?contL WHERE { ?c wdt:P31 wd:Q3624078; wdt:P297 ?iso; wdt:P30 ?cont. ?c rdfs:label ?cn FILTER(lang(?cn)="en") ?cont rdfs:label ?contL FILTER(lang(?contL)="en") }''')
SETS = ("bic", "website", "logo", "classes")
out = {k: {**v, **{f: set(v[f]) for f in SETS}} for k, v in json.load(open("raw/wikidata.json")).items()}
pd = set(json.load(open("raw/done_big.json"))) if os.path.exists("raw/done_big.json") else set()
for cls in failed:
    for c in countries:
        qid = c['c']['value'].rsplit('/', 1)[1]; key = f"{cls}:{qid}"
        if key in pd: continue
        rows = sparql(f'''SELECT ?i ?l ?bic ?web ?logo WHERE {{
          ?i wdt:P17 wd:{qid}; wdt:P31 wd:{cls}.
          FILTER NOT EXISTS {{ ?i wdt:P576 [] }} ?i rdfs:label ?l FILTER(lang(?l)="en")
          OPTIONAL {{ ?i wdt:P2627 ?bic }} OPTIONAL {{ ?i wdt:P856 ?web }} OPTIONAL {{ ?i wdt:P154 ?logo }} }}''')
        if rows is None: print("FAILED", key, flush=True); continue
        for r in rows:
            id_ = r['i']['value'].rsplit('/', 1)[1]
            e = out.setdefault(id_, {"qid": id_, "name": r['l']['value'], "country": c['iso']['value'], "countryName": c['cn']['value'],
                                     "continent": c['contL']['value'], "kind": kinds[cls], "bic": set(), "website": set(), "logo": set(), "classes": set()})
            e["classes"].add(cls)
            for k, f in (('bic', 'bic'), ('web', 'website'), ('logo', 'logo')):
                if k in r: e[f].add(r[k]['value'])
        pd.add(key); time.sleep(0.5)
        if len(pd) % 10 == 0:
            json.dump(out, open("raw/wikidata.json", "w"), default=sorted); json.dump(sorted(pd), open("raw/done_big.json", "w"))
        print(key, len(rows), len(out), flush=True)
json.dump(out, open("raw/wikidata.json", "w"), default=sorted); json.dump(sorted(pd), open("raw/done_big.json", "w")); print("DONE")
