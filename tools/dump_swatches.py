import urllib.request, json
from bs4 import BeautifulSoup

url = 'https://trybronoir.com/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(urllib.request.urlopen(req).read().decode('utf-8'), 'html.parser')

products = []
for p in soup.select('.product-item'):
    title_el = p.select_one('.product-item-meta__title')
    if not title_el:
        continue
    title = title_el.get_text(strip=True)
    
    # Swatches
    swatches = []
    for sw in p.select('.color-swatch'):
        inp = sw.select_one('input')
        lbl = sw.select_one('label')
        if inp:
            color = inp.get('value')
            media_id = inp.get('data-variant-featured-media')
            color_style = lbl.get('style') if lbl else ''
            
            # Find matching image
            matched_img = p.select_one(f'img[data-media-id="{media_id}"]')
            img_url = matched_img.get('src') if matched_img else None
            if img_url and img_url.startswith('//'):
                img_url = 'https:' + img_url
            swatches.append({
                'color': color,
                'media_id': media_id,
                'style': color_style,
                'img_url': img_url
            })
    
    # Secondary image
    sec_img = p.select_one('.product-item__secondary-image')
    sec_url = ('https:' + sec_img.get('src')) if (sec_img and sec_img.get('src', '').startswith('//')) else (sec_img.get('src') if sec_img else None)
    
    products.append({
        'title': title,
        'secondary_image': sec_url,
        'swatches': swatches
    })

with open('f:\\clone-theme\\tools\\swatches_data.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, indent=2, ensure_ascii=False)
print(f"Dumped {len(products)} products with swatches.")
