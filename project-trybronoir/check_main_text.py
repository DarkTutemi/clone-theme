import urllib.request
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = 'https://trybronoir.com/products/bronoir%E2%84%A2-arctic-2-0-winter-barefoot-shoes-1-1-free?cid=dpfse29nm4u0lrdcj46rhbe6'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(urllib.request.urlopen(req).read().decode('utf-8', errors='ignore'), 'html.parser')

main = soup.find(class_='shopify-section--main-product')

# Find left side (product__media) and right side (product__info)
pm = main.find('product-media')
if pm:
    # Check next siblings of product-media or children of left column
    print("=== SIBLINGS OF PRODUCT-MEDIA ===")
    for sib in pm.find_all_next(limit=15):
        if sib.name in ['ul', 'div'] and 'Supports' in sib.get_text():
            print("Found Supports:", sib.prettify()[:400])
            break

# Print all text in main product that looks like checklist
for el in main.find_all(True):
    txt = el.get_text(strip=True)
    if any(k in txt for k in ['Grounding', 'Fleece', 'Waterproof', 'Posture', 'Warmth']):
        if el.name in ['li', 'p', 'h4', 'span'] and len(txt) < 100:
            print(f"{el.name}: {txt}")
