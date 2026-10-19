import json

with open(r'f:\clone-theme\project-azureboutique\data\products.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

prods = data.get('products', data)
print(f"Total products in data/products.json: {len(prods)}")
for p in prods:
    imgs = [i.get('src') for i in p.get('images', [])]
    print(f"- {p.get('title')} ({p.get('handle')}): {len(imgs)} images")
    if imgs:
        print(f"    sample: {imgs[0]}")
