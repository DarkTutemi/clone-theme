import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('f:/clone-theme/project-trybronoir/bridge/preview.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

pos = text.find('id="bestsellers"')
if pos != -1:
    end_pos = text.find('</section>', pos)
    sub = text[pos:end_pos] if end_pos != -1 else text[pos:pos+25000]
    
    # Extract each card block
    cards = re.findall(r'<div class="product-card[^>]*>.*?</div>\s*</div>\s*</div>', sub, re.DOTALL)
    print(f"Total product cards found in #bestsellers: {len(cards)}")
    
    links = re.findall(r'href="(/products/[^"]+)"', sub)
    unique_links = []
    for l in links:
        if l not in unique_links:
            unique_links.append(l)
    print(f"\nUnique product URLs ({len(unique_links)}):")
    for idx, l in enumerate(unique_links):
        print(f"{idx+1}. {l}")
