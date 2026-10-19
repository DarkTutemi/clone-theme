import requests
import sys
sys.path.append(r'f:\clone-theme\tools\shopify-theme-cloner')
from core.store_client import ShopifyStoreClient

client = ShopifyStoreClient()
url = f"https://{client.store}/admin/api/{client.api_version}/shop.json"
r = requests.get(url, headers=client._headers())
shop = r.json().get('shop', {})
print(f"Shop Name: {shop.get('name')}")
print(f"Shop Domain: {shop.get('domain')}")
print(f"Password enabled: {shop.get('password_enabled')}")
print(f"Password: {shop.get('password')}")
