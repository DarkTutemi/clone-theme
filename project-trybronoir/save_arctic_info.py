import urllib.request
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = 'https://trybronoir.com/products/bronoir%E2%84%A2-arctic-2-0-winter-barefoot-shoes-1-1-free?cid=dpfse29nm4u0lrdcj46rhbe6'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

soup = BeautifulSoup(html, 'html.parser')

sec = soup.find(id='shopify-section-template--27860726153316__custom_info_block_cJKcnQ')
if sec:
    print(f"Found section {sec.name} #{sec.get('id')}, length: {len(str(sec))}")
    with open('f:/clone-theme/project-trybronoir/arctic_info_blocks.html', 'w', encoding='utf-8') as f:
        f.write(str(sec))
    print("Saved to arctic_info_blocks.html")
else:
    print("Section not found by ID!")
