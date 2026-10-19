import urllib.request
import os

pages = {
    'home.html': 'https://www.azureboutique.co/',
    'product_batana_oil.html': 'https://www.azureboutique.co/products/batana-natural-hair-growth-oil',
    'collection_batana.html': 'https://www.azureboutique.co/collections/batana'
}

out_dir = r'f:\clone-theme\project-azureboutique\_recon\html_cache'
os.makedirs(out_dir, exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

for fname, url in pages.items():
    print(f"Fetching {url} -> {fname}")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            content = resp.read()
            with open(os.path.join(out_dir, fname), 'wb') as f:
                f.write(content)
            print(f"  Saved {len(content)} bytes")
    except Exception as e:
        print(f"  Error: {e}")
