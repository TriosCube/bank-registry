"""Merge data/fintech-seed.json into data/<region>/<ISO2>.json. Skips names already present in that country."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import slugify, country_file
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = json.load(open(f"{root}/data/country-regions.json"))
NEO = {"wise","revolut","monzo","starling-bank","n26","chime","sofi","nubank","tymebank","kuda","chipper-cash"}
MOMO = {"m-pesa","mtn-mobile-money","wave","airtel-money","orange-money","gcash"}
PAY = {"stripe","paypal","square","block-inc","adyen","checkout-com","visa","mastercard","flutterwave","paystack","interswitch","remita","fawry","pesapal","cellulant","razorpay","alipay","wechat-pay","payoneer","western-union","moneygram","remitly","sendwave","paga","opay","palmpay","moniepoint","fincra","ozow","stitch","plaid","yoco"}
n = 0
for s in json.load(open(f"{root}/data/fintech-seed.json")):
    cc, slug = s["country"], slugify(s["name"]); region = REG[cc]
    p = country_file(region, cc); rows = json.load(open(p)) if os.path.exists(p) else []
    if any(slugify(b["name"]).startswith(slug) or slug in slugify(b["name"]) for b in rows): continue
    cat = "neobank" if slug in NEO else "mobile-money" if slug in MOMO else "payments" if slug in PAY else "fintech"
    rows.append({"id": f"{cc.lower()}-{slug}", "name": s["name"], "country": cc, "region": region, "category": cat, "website": s["website"]})
    rows.sort(key=lambda b: (b["category"], b["name"].lower()))
    os.makedirs(os.path.dirname(p), exist_ok=True); json.dump(rows, open(p, "w"), ensure_ascii=False, indent=1); n += 1
print("added", n, "fintech entries")
