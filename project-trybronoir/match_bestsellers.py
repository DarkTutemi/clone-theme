import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('f:/clone-theme/project-trybronoir/data/all_trybronoir_products.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data.get('products', [])
keywords = ['skin pro', 'cosycloud', 'hiker', 'trail master', 'arctic', 'toasty', 'summit', 'cloudwalk']

for kw in keywords:
    matches = [p for p in products if kw in p['title'].lower() or kw in p['handle'].lower()]
    print(f"\n=== KEYWORD: {kw} (found {len(matches)}) ===")
    for m in matches[:5]:
        print(f"  - Title: {m['title']} | Handle: {m['handle']}")
