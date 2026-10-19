import urllib.request
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = 'https://trybronoir.com/products/bronoir%E2%84%A2-arctic-2-0-winter-barefoot-shoes-1-1-free?cid=dpfse29nm4u0lrdcj46rhbe6'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

soup = BeautifulSoup(html, 'html.parser')

# Find all custom info blocks or description blocks
info_block = soup.find('div', id='shopify-section-template--27860726153316__custom_info_block_cJKcnQ')
if info_block:
    print("Found custom_info_block_cJKcnQ, length:", len(str(info_block)))
    with open('site_goc_arctic_info_blocks.html', 'w', encoding='utf-8') as f:
        f.write(str(info_block))
    
    # Also print headings and text inside
    for h in info_block.find_all(['h2', 'h3', 'h4']):
        print("Heading:", h.get_text(strip=True))

# Check all sections on site goc
print("\nAll sections on site goc:")
for sec in soup.find_all('div', class_='shopify-section'):
    sid = sec.get('id', '')
    print(f" - {sid}")
