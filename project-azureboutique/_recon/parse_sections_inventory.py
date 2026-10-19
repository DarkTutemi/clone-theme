from bs4 import BeautifulSoup
import json
import os

recon_dir = r'f:\clone-theme\project-azureboutique\_recon'
cache_dir = os.path.join(recon_dir, 'html_cache')

def inspect_file(fname):
    filepath = os.path.join(cache_dir, fname)
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    main = soup.find('main', id='MainContent')
    sections_info = []
    if main:
        # direct children or section tags
        for el in main.find_all(lambda t: t.name in ['section', 'div'] and t.get('id', '').startswith('shopify-section-')):
            s_id = el.get('id')
            headings = [h.get_text(strip=True) for h in el.find_all(['h1', 'h2', 'h3'])]
            classes = el.get('class', [])
            sections_info.append({
                'id': s_id,
                'tag': el.name,
                'class': classes,
                'headings': headings[:4]
            })
    return sections_info

home_sections = inspect_file('home.html')
product_sections = inspect_file('product_batana_oil.html')
collection_sections = inspect_file('collection_batana.html')

result = {
    'home': home_sections,
    'product': product_sections,
    'collection': collection_sections
}

print(f"Home sections count: {len(home_sections)}")
for s in home_sections:
    print(f"  [Home] {s['id']} -> {s['headings']}")

print(f"\nProduct sections count: {len(product_sections)}")
for s in product_sections:
    print(f"  [Product] {s['id']} -> {s['headings']}")

print(f"\nCollection sections count: {len(collection_sections)}")
for s in collection_sections:
    print(f"  [Collection] {s['id']} -> {s['headings']}")

with open(os.path.join(recon_dir, 'page_sections_inventory.json'), 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
