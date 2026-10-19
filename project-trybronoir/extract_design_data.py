import re
import json
import pathlib
import sys
from bs4 import BeautifulSoup

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

base = pathlib.Path("f:/clone-theme/project-trybronoir")
html = (base / "_recon/html_cache/home.html").read_text(encoding="utf-8", errors="ignore")
soup = BeautifulSoup(html, "html.parser")

# Extract tokens
tokens = {
    "colors": {
        "primary": "#08435e",
        "primary_dark": "#052d3f",
        "accent": "#44c2fd",
        "accent_glow": "#72c3e8",
        "gradient_hero": "linear-gradient(116.53deg, rgba(8, 67, 94, 1) 12.4%, rgba(114, 195, 232, 1) 93.6%)",
        "bg_light": "#f8fafc",
        "bg_white": "#ffffff",
        "text_dark": "#0f172a",
        "text_muted": "#64748b",
        "badge_sale": "#e11d48"
    },
    "typography": {
        "font_family": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "heading_family": "'Inter', sans-serif",
        "weights": [400, 500, 600, 700, 800]
    },
    "radii": {
        "button": "8px",
        "card": "12px",
        "badge": "4px",
        "circle": "9999px"
    },
    "shadows": {
        "card": "0 4px 20px rgba(0, 0, 0, 0.06)",
        "card_hover": "0 10px 30px rgba(8, 67, 94, 0.15)",
        "button": "0 4px 14px rgba(68, 194, 253, 0.3)"
    }
}

(base / "design/tokens.json").write_text(json.dumps(tokens, indent=2, ensure_ascii=False), encoding="utf-8")
print("[+] Tokens saved to design/tokens.json")

# Extract announcements
ann_texts = []
ann = soup.find(id=re.compile(r"announcement-bar"))
if ann:
    for t in ann.stripped_strings:
        ann_texts.append(t)
print(f"[+] Announcement text: {' | '.join(ann_texts)}")

# Extract category cards
categories = []
cat_section = soup.find(id=re.compile(r"custom_category_card"))
if cat_section:
    for a in cat_section.find_all("a"):
        href = a.get("href")
        title = a.get_text(strip=True)
        img = a.find("img")
        img_src = img.get("src") if img else ""
        if title:
            categories.append({"title": title, "url": href, "image": img_src})
print(f"[+] Found {len(categories)} categories")

# Extract FAQ
faq_items = []
faq_section = soup.find(id=re.compile(r"custom_newsletter_faq"))
if faq_section:
    questions = faq_section.find_all(class_=re.compile(r"accordion|faq__question|collapsible-toggle"))
    for q in questions:
        q_text = q.get_text(strip=True)
        # Find next sibling answer
        ans = q.find_next_sibling()
        ans_text = ans.get_text(strip=True) if ans else ""
        if q_text:
            faq_items.append({"question": q_text, "answer": ans_text})
print(f"[+] Found {len(faq_items)} FAQ items")

# Extract Brand content
brand_content = {
    "store_name": "Bronoir Canada",
    "tagline": "Skin Pro Barefoot with Copper | Buy 1, Get 2 Free!",
    "announcements": ann_texts,
    "categories": categories,
    "faqs": faq_items,
    "marquee": "Natural & Grounding • Podiatrist Recommended • Maximum Comfort • Zero Drop Sole"
}
(base / "data/brand_content.json").write_text(json.dumps(brand_content, indent=2, ensure_ascii=False), encoding="utf-8")
print("[+] Brand content saved to data/brand_content.json")
