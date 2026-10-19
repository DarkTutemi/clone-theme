import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = 'https://trybronoir.com/products.json?limit=250'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
data = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))

print(f"Total products on trybronoir.com: {len(data.get('products', []))}")
for p in data.get('products', []):
    print(f"- Title: {p['title']} | Handle: {p['handle']}")

with open('f:/clone-theme/project-trybronoir/data/all_trybronoir_products.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
