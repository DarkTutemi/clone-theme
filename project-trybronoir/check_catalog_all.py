import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('f:/clone-theme/project-trybronoir/bridge/bestsellers_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

print(f"Catalog contains {len(catalog)} products:\n")
for idx, p in enumerate(catalog):
    print(f"=== [{idx+1}] {p.get('title')} ===")
    print(f"  Handle: {p.get('handle')}")
    print(f"  Price: {p.get('price_sale')} (Compare: {p.get('price_compare')})")
    print(f"  Images count: {len(p.get('all_images', []))}")
    print(f"  Swatches count: {len(p.get('swatches', []))}")
    sw_names = [s.get('title') for s in p.get('swatches', [])]
    print(f"  Swatches: {', '.join(sw_names)}")
    print()
