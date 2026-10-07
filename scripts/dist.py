"""Build dist/ from data/<region>/<ISO2>.json: banks.json (flat), by-region/, by-category/, index.json."""
import glob, json, os, collections, shutil
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
all_ = []
for f in sorted(glob.glob(f"{root}/data/*/*.json")): all_ += json.load(open(f))
all_.sort(key=lambda b: (b["region"], b["country"], b["category"], b["name"].lower()))
shutil.rmtree(f"{root}/dist", ignore_errors=True)
def dump(path, obj, indent=1):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(obj, open(path, "w"), ensure_ascii=False, indent=indent)
dump(f"{root}/dist/banks.json", all_)
for key, folder in (("region", "by-region"), ("category", "by-category")):
    for v in sorted({b[key] for b in all_}): dump(f"{root}/dist/{folder}/{v}.json", [b for b in all_ if b[key] == v])
idx = {"total": len(all_), "withLogo": sum("logo" in b for b in all_),
       "byRegion": dict(collections.Counter(b["region"] for b in all_)),
       "byCategory": dict(collections.Counter(b["category"] for b in all_)),
       "byCountry": dict(sorted(collections.Counter(b["country"] for b in all_).items()))}
dump(f"{root}/dist/index.json", idx)
print(json.dumps({k: v for k, v in idx.items() if k != "byCountry"}, indent=1))
