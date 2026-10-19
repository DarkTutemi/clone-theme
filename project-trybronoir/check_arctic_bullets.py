import urllib.request
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = 'https://trybronoir.com/products/bronoir%E2%84%A2-arctic-2-0-winter-barefoot-shoes-1-1-free?cid=dpfse29nm4u0lrdcj46rhbe6'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(urllib.request.urlopen(req).read().decode('utf-8', errors='ignore'), 'html.parser')

main = soup.find(class_='shopify-section--main-product')

# 1. Product icons grid
icons = main.find(class_='product-icons-grid')
if icons:
    print("=== PRODUCT ICONS GRID ===")
    print(icons.get_text(strip=True, separator=' | '))

# 2. Checklists / bullets
checklists = main.find_all(class_='checklist')
for idx, cl in enumerate(checklists):
    print(f"=== CHECKLIST {idx} ===")
    print(cl.get_text(strip=True, separator='\n'))

# Also search for any ul or checklist in main
for ul in main.find_all(['ul', 'div']):
    txt = ul.get_text(strip=True)
    if 'Warm' in txt and ('Fleece' in txt or 'Water' in txt or 'Comfort' in txt) and len(txt) < 300:
        print("=== MATCHING BULLETS ===")
        print(ul.prettify()[:300])
        break
