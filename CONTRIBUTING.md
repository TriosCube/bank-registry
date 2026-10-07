# Contributing

Source of truth is `data/<region>/<ISO2>.json`, one file per country. `dist/` is generated: never edit it by hand.

1. Edit or add an entry in the country file. Follow `schema/bank.schema.json`.
2. `id` is `<iso2>-<slug>` and is **stable**: never rename it, other systems key on it. To retire an
   institution set `"status": "inactive"` rather than deleting it.
3. Put a logo in `logos/<iso2>/<slug>.svg` (preferred) or `.png`, under 400 KB, and set `logo.path`, `logo.source`
   (page you got it from) and `logo.license`.
4. Run `python3 scripts/validate.py && python3 scripts/dist.py`. CI runs the same checks.

Categories: commercial, central, microfinance, investment, development, islamic, savings, cooperative,
mortgage, neobank, fintech, payments, mobile-money, other.
