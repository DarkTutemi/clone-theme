import urllib.request
import json
import pathlib
import sys

base = pathlib.Path("f:/clone-theme/project-trybronoir")
(base / "_recon/html_cache").mkdir(parents=True, exist_ok=True)
(base / "data").mkdir(parents=True, exist_ok=True)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# 1. Fetch homepage HTML
try:
    req = urllib.request.Request("https://trybronoir.com/", headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
        (base / "_recon/html_cache/home.html").write_text(html, encoding="utf-8")
        print(f"[+] Homepage HTML saved: {len(html)} bytes")
except Exception as e:
    print(f"[-] Error fetching homepage: {e}")

# 2. Fetch products.json
try:
    req = urllib.request.Request("https://trybronoir.com/products.json?limit=250", headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        products_data = json.loads(resp.read().decode("utf-8"))
        (base / "data/products.json").write_text(json.dumps(products_data, indent=2, ensure_ascii=False), encoding="utf-8")
        prods = products_data.get("products", [])
        print(f"[+] Products saved: {len(prods)} products")
        for p in prods:
            t = p.get("title")
            imgs = len(p.get("images", []))
            h = p.get("handle")
            print(f"    - {t} | {imgs} images | handle: {h}")
except Exception as e:
    print(f"[-] Error fetching products: {e}")

# 3. Fetch collections.json
try:
    req = urllib.request.Request("https://trybronoir.com/collections.json?limit=100", headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        coll_data = json.loads(resp.read().decode("utf-8"))
        (base / "data/collections.json").write_text(json.dumps(coll_data, indent=2, ensure_ascii=False), encoding="utf-8")
        colls = coll_data.get("collections", [])
        print(f"[+] Collections saved: {len(colls)} collections")
        for c in colls:
            print(f"    - {c.get('title')} (handle: {c.get('handle')})")
except Exception as e:
    print(f"[-] Collections fetch error: {e}")
