import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('f:/clone-theme/project-trybronoir/data/all_trybronoir_products.json', 'r', encoding='utf-8') as f:
    products = json.load(f).get('products', [])

print(f"Total products available: {len(products)}")

targets = [
    ("Skin Pro", ["skin-pro", "skinpro"]),
    ("CosyCloud", ["cosycloud", "cosy"]),
    ("Hikers", ["hiker", "trekker", "outdoor", "orthopedic"]),
    ("Trail Masters", ["trail-master", "trail_master", "trailmaster", "trail"]),
    ("Arctic 2.0", ["arctic"]),
    ("Toasty", ["toasty"]),
    ("Summit", ["summit"]),
    ("CloudWalk", ["cloudwalk", "cloud", "walk", "sneaker", "runner"])
]

for name, kws in targets:
    print(f"\n=================== TARGET: {name} ===================")
    found = []
    for p in products:
        h = p['handle'].lower()
        t = p['title'].lower()
        if any(k in h or k in t for k in kws):
            found.append(p)
    for f in found[:6]:
        print(f"  - Title: {f['title']} | Handle: {f['handle']}")
