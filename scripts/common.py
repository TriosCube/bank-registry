import re, unicodedata
REGION = {"Africa": "africa", "Asia": "asia", "Europe": "europe", "North America": "north-america",
          "South America": "south-america", "Oceania": "oceania", "Insular Oceania": "oceania", "Eurasia": "europe"}
CATEGORIES = ["commercial", "central", "microfinance", "investment", "development", "islamic", "savings",
              "cooperative", "mortgage", "neobank", "fintech", "payments", "mobile-money", "other"]

def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

def categorize(name, classes=(), kind="bank"):
    n = (name + " " + " ".join(classes)).lower()
    if kind == "neobank" or "neobank" in n or "digital bank" in n or "online bank" in n: return "neobank"
    if "central bank" in n or "reserve bank" in n or name.lower().startswith("bank of ") and "central" in n: return "central"
    if re.search(r"\bpsb\b|payment service bank", n): return "payments"
    if re.search(r"mi?c?r?o?r?c?f?i?n?a?n|mircofin", n) and re.search(r"micro|mircro", n): return "microfinance"
    if re.search(r"mort+a?gage", n): return "mortgage"
    if re.search(r"\b(opay|palmpay|kuda|paga|carbon|eyowo|gomoney|pocket app|tangerine|paystack|kongapay|flutterwave|moniepoint)\b", n): return "fintech"
    if re.search(r"finance company|finance limited|finance ltd|\bfinance\b.*\b(ltd|limited|plc)\b", n) and "bank" not in n: return "other"
    if "microfinance" in n or " mfb" in n or n.endswith("mfb") or "micro-finance" in n: return "microfinance"
    if "islamic" in n or "non-interest" in n or "jaiz" in n or "sharia" in n: return "islamic"
    if "mortgage" in n or "building society" in n: return "mortgage"
    if "development bank" in n or "development finance" in n: return "development"
    if "investment bank" in n or "merchant bank" in n: return "investment"
    if "cooperative" in n or "co-operative" in n or "credit union" in n: return "cooperative"
    if "savings" in n: return "savings"
    if kind == "payment" or "payment" in n: return "payments"
    return "commercial"

import glob, os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def country_file(region, cc):
    """data/<region>/<ISO2>.json - one file per country, grouped by region."""
    return f"{ROOT}/data/{region}/{cc}.json"
def all_country_files():
    return sorted(glob.glob(f"{ROOT}/data/*/*.json"))
