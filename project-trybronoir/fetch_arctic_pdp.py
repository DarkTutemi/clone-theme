import urllib.request
import re

url = 'https://trybronoir.com/products/bronoir%E2%84%A2-arctic-2-0-winter-barefoot-shoes-1-1-free?cid=dpfse29nm4u0lrdcj46rhbe6'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})

html_bytes = urllib.request.urlopen(req).read()
html_str = html_bytes.decode('utf-8', errors='ignore')

# Save to bridge/product_arctic.html
target_file = 'f:/clone-theme/project-trybronoir/bridge/product_arctic.html'
with open(target_file, 'w', encoding='utf-8') as f:
    f.write(html_str)

print(f"Saved {len(html_str)} chars to {target_file}")
