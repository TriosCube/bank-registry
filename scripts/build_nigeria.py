"""Seed data/africa/NG.json + logos from ichtrojan/nigerian-banks (MIT). One-off import; NG.json is then hand-maintained."""
import json, os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import slugify, categorize
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = f"{root}/raw/ng"
out, seen = [], set()
os.makedirs(f"{root}/logos/ng", exist_ok=True)
for b in json.load(open(f"{src}/banks.json")):
    id_ = "ng-" + slugify(b["slug"] or b["name"])
    if id_ in seen: id_ += "-" + b["code"]
    seen.add(id_)
    e = {"id": id_, "name": b["name"], "country": "NG", "region": "africa",
         "category": categorize(b["name"]), "codes": {"nip": b["code"]}}
    if b.get("ussd"): e["ussd"] = b["ussd"]
    logo = f"{src}/logos/{b['slug']}.png"
    if os.path.exists(logo):
        shutil.copy(logo, f"{root}/logos/ng/{id_[3:]}.png")
        e["logo"] = {"path": f"logos/ng/{id_[3:]}.png", "source": "https://github.com/ichtrojan/nigerian-banks", "license": "MIT (upstream collection); logo remains property of its owner"}
    out.append(e)
out.sort(key=lambda x: x["name"].lower())
os.makedirs(f"{root}/data/africa", exist_ok=True)
json.dump(out, open(f"{root}/data/africa/NG.json", "w"), ensure_ascii=False, indent=1)
print(len(out), "NG entries,", sum("logo" in e for e in out), "with logo")
