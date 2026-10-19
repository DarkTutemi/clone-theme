import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

products = [
    ("Skin Pro", "bronoir-skin-pro-with-copper-grounding-allround-barefoot-shoes", "https://trybronoir.com/products/bronoir%E2%84%A2-skin-pro-with-copper-grounding-allround-barefoot-shoes-kopie"),
    ("CosyCloud", "bronoir-cosycloud-boot-warm-comfy-winter-barefoot-boot", "https://trybronoir.com/products/bronoir-cosycloud-boot-warm-comfy-winter-barefoot-boot"),
    ("Hikers", "bronoir-hikers-orthopedic-outdoor-barefoot-shoes-bogo", "https://trybronoir.com/products/bronoir%E2%84%A2-hikers-orthopedic-outdoor-shoes-1-1-free"),
    ("Trail Masters", "bronoir-trail-masters-all-terrain-grip-barefoot-boots", "https://trybronoir.com/products/bronoir%E2%84%A2-trail-masters-all-terrain-barefoot-shoes"),
    ("Arctic 2.0", "bronoir-arctic-2-0-winter-barefoot-shoes-1-1-free", "https://trybronoir.com/products/bronoir%E2%84%A2-arctic-2-0-winter-barefoot-shoes-1-1-free"),
    ("Toasty", "bronoir-toasty-cozy-winter-barefoot-shoes-with-thermal-lining", "https://trybronoir.com/products/bronoir%E2%84%A2-toasty-winter-barefoot-shoes"),
    ("Summit", "bronoir-summit-winter-warm-insulated-barefoot-shoes", "https://trybronoir.com/products/bronoir%E2%84%A2-summit-winter-barefoot-shoes"),
    ("CloudWalk", "bronoir-cloudwalk-ultra-light-breathable-barefoot-sneakers", "https://trybronoir.com/products/bronoir%E2%84%A2-cloudwalk-barefoot-sneakers")
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for name, local_handle, live_url in products:
    try:
        req = urllib.request.Request(live_url, headers=headers)
        res = urllib.request.urlopen(req)
        print(f"✅ {name}: HTTP {res.status} | URL: {live_url}")
    except Exception as e:
        print(f"❌ {name}: {e} | URL: {live_url}")
