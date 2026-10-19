import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

urls_to_fetch = [
    ("CosyCloud", "f:/clone-theme/project-trybronoir/bridge/product_cosycloud.html", "https://trybronoir.com/products/bronoir-cosycloud-boot-warm-comfy-winter-barefoot-boot"),
    ("Toasty", "f:/clone-theme/project-trybronoir/bridge/product_toasty.html", "https://trybronoir.com/products/bronoir%E2%84%A2-toasty-winter-barefoot-shoes"),
    ("TrailMasters", "f:/clone-theme/project-trybronoir/bridge/product_trail_masters.html", "https://trybronoir.com/products/bronoir%E2%84%A2-trail-masters-barefoot-shoes-1")
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

for name, target_path, url in urls_to_fetch:
    try:
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ Downloaded {name}: {len(html)} chars -> {target_path}")
    except Exception as e:
        print(f"❌ Failed {name}: {e}")
