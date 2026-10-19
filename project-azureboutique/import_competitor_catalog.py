import os
import sys
import json
import time
import requests

sys.path.append(r'f:\clone-theme\tools\shopify-theme-cloner')
from core.store_client import ShopifyStoreClient

client = ShopifyStoreClient()

products_file = r'f:\clone-theme\project-azureboutique\data\products.json'
with open(products_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data.get('products', data)
print(f"[*] Starting import of {len(products)} products with ALL competitor images into {client.store}...")

imported = []
failed = []

for idx, p in enumerate(products):
    title = p.get('title')
    handle = p.get('handle')
    body_html = p.get('body_html', '')
    vendor = p.get('vendor', 'Azure')
    product_type = p.get('product_type', 'Hair Care')
    tags = p.get('tags', [])
    if isinstance(tags, list):
        tags_str = ", ".join(tags)
    else:
        tags_str = str(tags)

    # Images
    images = []
    for img in p.get('images', []):
        src = img.get('src')
        if src:
            images.append({'src': src, 'alt': title})

    # Variants
    variants = []
    for v in p.get('variants', []):
        var_data = {
            'title': v.get('title', 'Default Title'),
            'option1': v.get('option1', 'Default Title'),
            'price': str(v.get('price', '44.00')),
            'requires_shipping': True,
            'taxable': True
        }
        if v.get('compare_at_price'):
            var_data['compare_at_price'] = str(v.get('compare_at_price'))
        if v.get('sku'):
            var_data['sku'] = v.get('sku')
        variants.append(var_data)

    payload = {
        'product': {
            'title': title,
            'handle': handle,
            'body_html': body_html,
            'vendor': vendor,
            'product_type': product_type,
            'tags': tags_str,
            'status': 'active',
            'images': images,
            'variants': variants or [{'price': '44.00', 'title': 'Default'}]
        }
    }

    url = f"https://{client.store}/admin/api/{client.api_version}/products.json"
    try:
        r = requests.post(url, json=payload, headers=client._headers(), timeout=30)
        if r.status_code in [200, 201]:
            created = r.json().get('product', {})
            p_id = created.get('id')
            img_count = len(created.get('images', []))
            imported.append({'id': p_id, 'title': title, 'images': img_count})
            print(f"[{idx+1}/{len(products)}] SUCCESS: {title} (ID: {p_id}, Images: {img_count})")
        else:
            failed.append({'title': title, 'error': f"{r.status_code} {r.text}"})
            print(f"[{idx+1}/{len(products)}] FAILED: {title} -> {r.status_code} {r.text}")
    except Exception as e:
        failed.append({'title': title, 'error': str(e)})
        print(f"[{idx+1}/{len(products)}] ERROR: {title} -> {e}")

    # Slight pause to respect Shopify API rate limits (2 req/s bucket)
    time.sleep(0.5)

print("\n" + "="*50)
print(f"[+] Import Finished: {len(imported)} successfully imported, {len(failed)} failed.")
print("="*50)

# Create 'Batana' Smart Collection containing all Batana products
print("\n[*] Setting up 'Batana' Collection...")
coll_url = f"https://{client.store}/admin/api/{client.api_version}/custom_collections.json"
coll_payload = {
    "custom_collection": {
        "title": "Batana",
        "handle": "batana",
        "body_html": "<p>100% Pure, Wild-Harvested Honduran Batana Oil formulas.</p>",
        "published": True
    }
}
try:
    cr = requests.post(coll_url, json=coll_payload, headers=client._headers(), timeout=15)
    if cr.status_code in [200, 201]:
        c_data = cr.json().get('custom_collection', {})
        c_id = c_data.get('id')
        print(f"[+] Collection 'Batana' created (ID: {c_id})")
        # Collect all imported products into this collection
        collect_url = f"https://{client.store}/admin/api/{client.api_version}/collects.json"
        for item in imported:
            collect_payload = {
                "collect": {
                    "collection_id": c_id,
                    "product_id": item['id']
                }
            }
            requests.post(collect_url, json=collect_payload, headers=client._headers(), timeout=10)
        print(f"[+] Added {len(imported)} products to 'Batana' collection!")
    else:
        print(f"[*] Collection creation response: {cr.status_code} {cr.text}")
except Exception as e:
    print(f"Error setting up collection: {e}")
