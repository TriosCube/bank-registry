"""Generate docs/<region>.md (countries -> institutions by category) and the coverage table in README.md."""
import json, os, glob, collections, re
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
idx = json.load(open(f"{root}/dist/index.json")); banks = json.load(open(f"{root}/dist/banks.json"))
names = {}
try:
    import pycountry
    names = {c.alpha_2: c.name for c in pycountry.countries}
except ImportError: pass
os.makedirs(f"{root}/docs", exist_ok=True)
by = collections.defaultdict(lambda: collections.defaultdict(list))
for b in banks: by[b["region"]][b["country"]].append(b)
rows = []
for region in sorted(by):
    lines = [f"# {region.replace('-', ' ').title()}", "", f"{sum(len(v) for v in by[region].values())} institutions in {len(by[region])} countries.", ""]
    for cc in sorted(by[region]):
        bs = by[region][cc]; cats = collections.Counter(b["category"] for b in bs)
        lines += [f"## {names.get(cc, cc)} ({cc})", "", "| Category | Count |", "|---|---|"] + [f"| {c} | {n} |" for c, n in sorted(cats.items())] + ["", f"Data: [`data/{region}/{cc}.json`](../data/{region}/{cc}.json)", ""]
    open(f"{root}/docs/{region}.md", "w").write("\n".join(lines))
    rows.append(f"| [{region.replace('-', ' ').title()}](docs/{region}.md) | {len(by[region])} | {sum(len(v) for v in by[region].values())} |")
table = "| Region | Countries | Institutions |\n|---|---|---|\n" + "\n".join(rows)
cats = "\n".join(f"- `{c}`: {n}" for c, n in sorted(idx["byCategory"].items()))
body = f"""# bank-registry

An open, maintained registry of banks, microfinance banks, fintechs, neobanks and payment providers, with logos,
organised **by region, then country, then category**. Built to drive the picker lists in [Isura](https://github.com/TriosCube)
and free for anyone to use.

**{idx['total']} institutions, {idx['withLogo']} with logos.**

## Coverage

{table}

## Categories

{cats}

## Layout

```
data/<region>/<ISO2>.json   source of truth, one file per country (edit these)
data/fintech-seed.json      hand-curated global fintechs / payment providers
logos/<iso2>/<slug>.svg|png logos; each entry records its source in logo.source
schema/bank.schema.json     entry schema
dist/                       generated: banks.json, by-region/, by-category/, index.json
scripts/                    importers, validate.py, dist.py, docs.py
```

## Use it

```sh
curl -s https://raw.githubusercontent.com/TriosCube/bank-registry/main/dist/by-region/africa.json
curl -s https://raw.githubusercontent.com/TriosCube/bank-registry/main/dist/banks.json
```

Each entry: `id` (stable), `name`, `country` (ISO 3166-1), `region`, `category`, `codes` (`nip`, `bic`, `wikidata`),
`website`, `logo`. Nigeria carries CBN/NIBSS bank codes in `codes.nip`.

## Contributing and legal

See [CONTRIBUTING.md](CONTRIBUTING.md). Data sources, logo ownership and the takedown process are in
[NOTICE.md](NOTICE.md). Code and data: MIT.
"""
open(f"{root}/README.md", "w").write(body)
