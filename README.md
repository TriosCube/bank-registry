# bank-registry

An open, maintained registry of banks, microfinance banks, fintechs, neobanks and payment providers, with logos,
organised **by region, then country, then category**. Built to drive the picker lists in [Isura](https://github.com/TriosCube)
and free for anyone to use.

**912 institutions, 549 with logos.**

## Coverage

| Region | Countries | Institutions |
|---|---|---|
| [Africa](docs/africa.md) | 44 | 347 |
| [Asia](docs/asia.md) | 45 | 103 |
| [Europe](docs/europe.md) | 48 | 331 |
| [North America](docs/north-america.md) | 22 | 87 |
| [Oceania](docs/oceania.md) | 11 | 14 |
| [South America](docs/south-america.md) | 12 | 30 |

## Categories

- `central`: 203
- `commercial`: 335
- `development`: 4
- `fintech`: 22
- `investment`: 47
- `islamic`: 2
- `microfinance`: 187
- `mobile-money`: 6
- `mortgage`: 50
- `neobank`: 11
- `other`: 9
- `payments`: 33
- `savings`: 3

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
