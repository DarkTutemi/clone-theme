import sys
import requests
sys.path.append(r'f:\clone-theme\tools\shopify-theme-cloner')
from core.store_client import ShopifyStoreClient

client = ShopifyStoreClient()
r = requests.get(f"https://{client.store}/admin/api/{client.api_version}/products.json", headers=client._headers())
print(f"Store products response: {r.status_code}")
prods = r.json().get('products', [])
print(f"Current product count in store: {len(prods)}")
for p in prods:
    print(f"- {p.get('id')}: {p.get('title')} ({len(p.get('images', []))} images)")
