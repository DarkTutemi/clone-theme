import json
import time
import sys
import pathlib
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = pathlib.Path(__file__).parent
TOOLS_DIR = BASE_DIR.parent / "tools" / "shopify-theme-cloner"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from core.store_client import ShopifyStoreClient

client = ShopifyStoreClient()
base_api = f"https://{client.store}/admin/api/{client.api_version}"

# Load products.json
with open(BASE_DIR / "data/products.json", "r", encoding="utf-8") as f:
    data = json.load(f)

raw_products = data.get("products", [])

# Select top distinct shoe models
flagship_products = []
seen_titles = set()

for p in raw_products:
    t = p.get("title", "")
    imgs = p.get("images", [])
    if any(k in t.lower() for k in ["protection", "warranty", "guarantee"]):
        continue
    if len(imgs) < 2:
        continue
    clean_t = t.split("|")[0].strip()
    if clean_t in seen_titles:
        continue
    seen_titles.add(clean_t)
    flagship_products.append(p)
    if len(flagship_products) >= 10:
        break

print(f"[*] Starting import of {len(flagship_products)} Bronoir flagship footwear models into {client.store}...", flush=True)

imported_ids = []

for i, prod in enumerate(flagship_products):
    raw_vars = prod.get("variants", [])
    first_var = raw_vars[0] if raw_vars else {}
    price_val = str(first_var.get("price", "79.90"))
    compare_val = str(first_var.get("compare_at_price") or "119.90")

    images_payload = []
    for img in prod.get("images", [])[:4]: # top 4 high-res photos
        src = img.get("src")
        if src:
            images_payload.append({"src": src})

    payload = {
        "product": {
            "title": prod.get("title"),
            "body_html": prod.get("body_html") or "<p>Anatomical barefoot shoes engineered with pure copper grounding elements, wide toe box, and zero-drop sole.</p>",
            "vendor": "Bronoir Canada",
            "product_type": "Barefoot Shoes",
            "tags": "barefoot, copper, grounding, shoes, bogo, bestsellers",
            "status": "active",
            "variants": [
                {
                    "price": price_val,
                    "compare_at_price": compare_val
                }
            ],
            "images": images_payload
        }
    }

    try:
        r = requests.post(f"{base_api}/products.json", json=payload, headers=client._headers(), timeout=45)
        if r.status_code in [200, 201]:
            created = r.json().get("product", {})
            pid = created.get("id")
            imported_ids.append(pid)
            img_count = len(created.get("images", []))
            print(f"[+] [{i+1}/{len(flagship_products)}] SUCCESS: {created.get('title')} (ID: {pid}, Images: {img_count})", flush=True)
        else:
            print(f"[-] [{i+1}] Failed: {r.status_code} {r.text[:120]}", flush=True)
    except Exception as e:
        print(f"[-] Error {prod.get('title')}: {e}", flush=True)

    time.sleep(1)

print(f"\n[+] Total imported: {len(imported_ids)} products successfully!", flush=True)

# Create Custom Collection: Bronoir Barefoot Shoes
if imported_ids:
    print("[*] Creating Custom Collection 'Bronoir Barefoot Shoes'...", flush=True)
    coll_payload = {
        "custom_collection": {
            "title": "Bronoir Barefoot Shoes",
            "handle": "bronoir-barefoot-shoes",
            "body_html": "<p>Experience true natural grounding with our doctor-approved barefoot footwear.</p>",
            "published": True
        }
    }
    r = requests.post(f"{base_api}/custom_collections.json", json=coll_payload, headers=client._headers(), timeout=20)
    if r.status_code in [200, 201]:
        coll = r.json().get("custom_collection", {})
        coll_id = coll.get("id")
        print(f"[+] Collection created: {coll.get('title')} (ID: {coll_id})", flush=True)

        collected = 0
        for pid in imported_ids:
            collect_payload = {
                "collect": {
                    "collection_id": coll_id,
                    "product_id": pid
                }
            }
            res_c = requests.post(f"{base_api}/collects.json", json=collect_payload, headers=client._headers(), timeout=10)
            if res_c.status_code in [200, 201]:
                collected += 1
        print(f"[+] Successfully linked {collected}/{len(imported_ids)} products to collection {coll_id}!", flush=True)
    else:
        print(f"[-] Collection notice: {r.status_code} {r.text[:150]}", flush=True)
