"""Validate data/<region>/<ISO2>.json: schema, unique ids, logo files exist. Exit 1 on any error."""
import glob, json, os, re, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
schema = json.load(open(f"{root}/schema/bank.schema.json"))
try:
    import jsonschema
    v = jsonschema.Draft202012Validator(schema)
except ImportError:
    v = None
errs, ids = [], set()
for f in sorted(glob.glob(f"{root}/data/*/*.json")):
    cc = os.path.basename(f)[:-5]; reg = os.path.basename(os.path.dirname(f))
    for b in json.load(open(f)):
        if v:
            for e in v.iter_errors(b): errs.append(f"{cc}/{b.get('id')}: {e.message}")
        if b["id"] in ids: errs.append(f"duplicate id {b['id']}")
        ids.add(b["id"])
        if b["region"] != reg: errs.append(f"{b['id']}: in data/{reg}/ but region={b['region']}")
        if b["country"] != cc: errs.append(f"{b['id']}: in {cc}.json but country={b['country']}")
        if not b["id"].startswith(b["country"].lower() + "-"): errs.append(f"{b['id']}: id prefix != country")
        if "logo" in b and not os.path.exists(f"{root}/{b['logo']['path']}"): errs.append(f"{b['id']}: missing {b['logo']['path']}")
print(f"{len(ids)} entries, {len(errs)} errors")
for e in errs[:50]: print(" -", e)
sys.exit(1 if errs else 0)
