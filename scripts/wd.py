import json, urllib.request, urllib.parse, time, sys
UA = {"User-Agent": "bank-registry/0.1 (https://github.com/TriosCube/bank-registry)", "Accept": "application/sparql-results+json"}
def sparql(q, retries=4):
    url = "https://query.wikidata.org/sparql?" + urllib.parse.urlencode({"query": q, "format": "json"})
    for i in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                return json.load(r)["results"]["bindings"]
        except Exception as e:
            print("retry", i, e, file=sys.stderr); time.sleep(5*(i+1))
    return None
