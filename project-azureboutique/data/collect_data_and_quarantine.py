import json
import os
import urllib.request
import re
from bs4 import BeautifulSoup

project_dir = r'f:\clone-theme\project-azureboutique'
data_dir = os.path.join(project_dir, 'data')
ref_dir = os.path.join(project_dir, '_references')
img_dir = os.path.join(ref_dir, 'images')
os.makedirs(img_dir, exist_ok=True)

# 1. Bundles structure
bundles = [
    {
        "id": "bundle_1_bottle",
        "title": "1x Batana Hair Growth Oil (100ml)",
        "subtitle": "Starter Supply (30 Days)",
        "quantity": 1,
        "price": 44.00,
        "compare_at_price": 55.00,
        "discount_percent": 20,
        "badge": "Popular",
        "benefits": ["100% Pure Honduran Batana Oil", "Free 30-Day Money Back Guarantee"]
    },
    {
        "id": "bundle_2_bottles",
        "title": "2x Batana Hair Growth Oil (200ml)",
        "subtitle": "Most Popular (60 Days)",
        "quantity": 2,
        "price": 68.00,
        "compare_at_price": 110.00,
        "discount_percent": 38,
        "badge": "Save $42",
        "is_featured": True,
        "benefits": ["Free Digital Hair Growth Guide", "Faster Visible Edges Recovery", "Free Shipping"]
    },
    {
        "id": "bundle_3_bottles",
        "title": "3x Batana Hair Growth Oil (300ml)",
        "subtitle": "Complete Transformation (90 Days)",
        "quantity": 3,
        "price": 88.00,
        "compare_at_price": 165.00,
        "discount_percent": 47,
        "badge": "Best Value (Save $77)",
        "benefits": ["Free Wooden Scalp Massager", "Free Digital Hair Growth Guide", "Priority US & Global Shipping"]
    }
]

with open(os.path.join(data_dir, 'bundles.json'), 'w', encoding='utf-8') as f:
    json.dump(bundles, f, indent=2, ensure_ascii=False)
print("Saved data/bundles.json")

# 2. Brand content & FAQs
faqs = [
    {
        "question": "What does authentic Batana Oil smell like?",
        "answer": "Raw, authentic Honduran Batana Oil has a rich, earthy, smoky coffee aroma. This distinct scent is natural proof that the oil is unrefined and extracted without chemical deodorizers or harsh industrial bleaching."
    },
    {
        "question": "How quickly can I expect to see visible results?",
        "answer": "Most customers notice softer hair and less scalp itchiness within 1 to 2 weeks. Noticeable reduction in hair shedding and baby hair growth around the edges typically begins between weeks 3 and 6 of consistent use (3-4 times per week)."
    },
    {
        "question": "How do I apply Batana Oil for best results?",
        "answer": "Warm a dime-to-quarter sized amount in the palms of your hands until it melts into a smooth oil. Massage thoroughly into your scalp and thinning areas for 3-5 minutes. Leave on for at least 30 minutes, or overnight with a satin bonnet, then wash out with gentle shampoo."
    },
    {
        "question": "Is this safe for color-treated and natural hair?",
        "answer": "Yes! Our Batana Oil is 100% pure single-ingredient oil, completely free from sulfates, parabens, silicones, and artificial dyes. It is suitable for all hair textures (1A to 4C) and color-treated hair."
    },
    {
        "question": "What is your 30-Day Money-Back Guarantee policy?",
        "answer": "We stand behind the potency of our Batana oil. If you don't love the improvement in your hair's softness and health after 30 days of use, simply email our customer support team for a full refund."
    }
]

timeline = [
    {
        "period": "Weeks 1 - 2",
        "title": "Scalp Awakening & Deep Hydration",
        "description": "Nourishes dry scalp, relieves itching and tightness. Hair strands regain natural elasticity and gloss."
    },
    {
        "period": "Weeks 3 - 4",
        "title": "Shedding Halts & Follicles Strengthen",
        "description": "Dramatic reduction of hair strands on brushes and showers. Follicle roots receive rich lipid nourishment."
    },
    {
        "period": "Weeks 6 - 8",
        "title": "New Growth & Visible Fullness",
        "description": "Fresh baby hair sprouting along the hairline, edges, and crown. Overall hair volume feels thicker and more resilient."
    }
]

comparison = {
    "our_product": {
        "title": "Azure Batana Oil",
        "points": [
            "100% Wild-harvested Honduran Batana",
            "Cold-pressed, unrefined single ingredient",
            "Rich in natural Oleic & Linoleic fatty acids",
            "Penetrates deep into the cortex without clogging pores",
            "30-Day Satisfaction Guarantee"
        ]
    },
    "competitors": {
        "title": "Generic / Cheap Hair Oils",
        "points": [
            "Cut with 80%+ cheap mineral or soybean oil",
            "Heavily bleached and perfumed with synthetic fragrance",
            "Covers hair in non-breathable silicone film",
            "Suffocates follicles and causes buildup",
            "No purity or lab-testing verification"
        ]
    }
}

brand_content = {
    "brand_name": "Azure Boutique",
    "mission": "Clean, wild-harvested botanical remedies rooted in ancient Honduran tradition for natural hair vitality.",
    "faqs": faqs,
    "timeline": timeline,
    "comparison": comparison,
    "social_proof": {
        "happy_customers": "200,000+",
        "bottles_shipped": "850,000+",
        "five_star_reviews": "58,000+"
    }
}

with open(os.path.join(data_dir, 'brand_content.json'), 'w', encoding='utf-8') as f:
    json.dump(brand_content, f, indent=2, ensure_ascii=False)
print("Saved data/brand_content.json")

# 3. Download sample images into _references/images/ (quarantine) and generate MANIFEST.json
with open(os.path.join(data_dir, 'products.json'), 'r', encoding='utf-8') as f:
    products = json.load(f)

manifest = []
download_count = 0
headers = {'User-Agent': 'Mozilla/5.0'}

prod_list = products.get('products', []) if isinstance(products, dict) else products
for prod in prod_list[:5]:
    for idx, img in enumerate(prod.get('images', [])[:2]):
        src = img.get('src')
        if not src: continue
        clean_handle = re.sub(r'[^a-zA-Z0-9_\-]', '', prod['handle'])
        ext = 'jpg'
        if '.png' in src.lower(): ext = 'png'
        fname = f"{clean_handle}_{idx+1}.{ext}"
        fpath = os.path.join(img_dir, fname)
        
        try:
            req = urllib.request.Request(src, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                with open(fpath, 'wb') as out_f:
                    out_f.write(resp.read())
            download_count += 1
            manifest.append({
                "source_url": src,
                "asset": f"_references/images/{fname}",
                "type": "product_image_placeholder",
                "product_handle": prod['handle'],
                "license_status": "quarantined_reference_only",
                "crawled_at": "2026-10-19T07:26:00Z",
                "note": "Placeholder asset for local reconstruction layout only. Replace with owner-licensed media prior to production."
            })
            print(f"Downloaded: {fname}")
        except Exception as e:
            print(f"Failed to download {src}: {e}")

with open(os.path.join(ref_dir, 'MANIFEST.json'), 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
print(f"Saved _references/MANIFEST.json with {len(manifest)} quarantined items")
