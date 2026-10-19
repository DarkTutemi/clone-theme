import urllib.request
import json
import pathlib
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

base = pathlib.Path("f:/clone-theme/project-trybronoir")
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

all_products = []
page = 1
while True:
    url = f"https://trybronoir.com/products.json?limit=250&page={page}"
    print(f"[*] Fetching products page {page}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            prods = data.get("products", [])
            if not prods:
                break
            all_products.extend(prods)
            print(f"    Page {page}: got {len(prods)} products (Total: {len(all_products)})")
            if len(prods) < 250:
                break
            page += 1
            time.sleep(0.5)
    except Exception as e:
        print(f"[-] Error fetching page {page}: {e}")
        break

output_file = base / "data" / "products.json"
output_file.write_text(json.dumps({"products": all_products}, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"[+] Total {len(all_products)} products saved to {output_file}")
