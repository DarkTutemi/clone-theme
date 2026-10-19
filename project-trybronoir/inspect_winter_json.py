import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('f:/clone-theme/project-trybronoir/collections_data/winter-collection.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

prods = data.get('products', [])
print(f"Total products in winter-collection.json: {len(prods)}")
for i, p in enumerate(prods[:36]):
    print(f"{i+1}. Title: {p.get('title')} | Handle: {p.get('handle')} | Images: {len(p.get('images', []))}")

