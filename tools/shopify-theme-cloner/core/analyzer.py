"""
Shopify & E-Commerce Store Analyzer
Detects platform, theme name, Shopify apps, tracking pixels, and tech stack from any store URL.
"""
import re
import json
import logging
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger("store_analyzer")

COMMON_APPS = {
    "PageFly": [r"pagefly", r"__pf"],
    "GemPages": [r"gempages", r"gem-app"],
    "Shogun": [r"shogun", r"cdn\.getshogun\.com"],
    "Zipify": [r"zipify", r"oneclickupsell"],
    "Judge.me": [r"judgeme", r"cdn\.judge\.me"],
    "Loox": [r"loox\.io", r"loox-reviews"],
    "Yotpo": [r"staticw2\.yotpo\.com", r"yotpo"],
    "Klaviyo": [r"static\.klaviyo\.com", r"klaviyo"],
    "Omnisend": [r"omnisend"],
    "ReCharge": [r"rechargepayments\.com", r"rechargecdn"],
    "Privy": [r"widget\.privy\.com"],
    "Tidio": [r"code\.tidio\.co"],
    "Gorgias": [r"config\.gorgias\.chat"],
    "Smile.io": [r"smile\.io", r"cdn\.sweettooth\.io"],
    "Booster Page Speed": [r"booster-apps\.com"],
    "Vitals": [r"vitals-cdn\.com", r"appvitals"],
    "Currency Converter": [r"doubly", r"currency-converter", r"coin-currency"],
    "Bundles App": [r"bundle", r"widebundle", r"fast-bundle"],
}

PIXELS = {
    "Facebook Pixel": [r"connect\.facebook\.net", r"fbq\("],
    "TikTok Pixel": [r"analytics\.tiktok\.com", r"ttq\."],
    "Google Analytics 4": [r"googletagmanager\.com/gtag/js\?id=G-", r"gtag\("],
    "Google Tag Manager": [r"googletagmanager\.com/gtm\.js"],
    "Pinterest Tag": [r"pintrk\("],
    "Snapchat Pixel": [r"sc-static\.net/scevent\.min\.js"],
    "Hotjar": [r"static\.hotjar\.com"],
    "Clarity": [r"clarity\.ms/tag"],
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

def analyze_store(url: str, timeout: int = 15) -> dict:
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    
    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    
    result = {
        "url": url,
        "base_url": base_url,
        "is_shopify": False,
        "platform": "Unknown",
        "store_name": parsed.netloc,
        "theme": {"name": "Unknown", "id": None, "schema_version": "Unknown"},
        "currency": "USD",
        "locale": "en",
        "detected_apps": [],
        "detected_pixels": [],
        "page_builder": None,
        "has_public_products_json": False,
        "has_public_collections_json": False,
        "meta": {},
        "social_links": {},
    }
    
    try:
        session = requests.Session()
        session.headers.update(HEADERS)
        
        # 1. Fetch homepage
        resp = session.get(base_url, timeout=timeout, allow_redirects=True)
        html = resp.text
        soup = BeautifulSoup(html, "html.parser")
        
        # Detect platform
        if "cdn.shopify.com" in html or "Shopify.shop" in html or "window.Shopify" in html:
            result["is_shopify"] = True
            result["platform"] = "Shopify"
        elif "woocommerce" in html or "wp-content" in html:
            result["platform"] = "WooCommerce / WordPress"
        elif "bigcommerce" in html:
            result["platform"] = "BigCommerce"
        elif "shoplazza" in html:
            result["platform"] = "Shoplazza"
        
        # Store name
        title_tag = soup.find("title")
        if title_tag and title_tag.string:
            result["meta"]["title"] = title_tag.string.strip()
            
        desc_meta = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
        if desc_meta and desc_meta.get("content"):
            result["meta"]["description"] = desc_meta["content"].strip()
            
        site_name_meta = soup.find("meta", attrs={"property": "og:site_name"})
        if site_name_meta and site_name_meta.get("content"):
            result["store_name"] = site_name_meta["content"].strip()
            
        # Social links
        for a in soup.find_all("a", href=True):
            href = a["href"]
            for network in ["facebook.com", "instagram.com", "tiktok.com", "twitter.com", "x.com", "pinterest.com", "youtube.com"]:
                if network in href and network not in result["social_links"]:
                    result["social_links"][network.split(".")[0]] = href

        # Extract Shopify details
        if result["is_shopify"]:
            # Extract Shopify.theme
            theme_match = re.search(r"Shopify\.theme\s*=\s*({[^}]+})", html)
            if theme_match:
                try:
                    theme_info = json.loads(theme_match.group(1))
                    result["theme"]["name"] = theme_info.get("name", "Unknown")
                    result["theme"]["id"] = theme_info.get("id")
                    result["theme"]["role"] = theme_info.get("role")
                except Exception:
                    pass
            
            # Check theme name from meta or comments
            if result["theme"]["name"] == "Unknown":
                name_match = re.search(r'BOOMR\.themeName\s*=\s*["\']([^"\']+)["\']', html) or \
                             re.search(r'theme_name["\']?:\s*["\']([^"\']+)["\']', html) or \
                             re.search(r'Shopify\.theme\s*=\s*.*name:\s*["\']([^"\']+)["\']', html)
                if name_match:
                    result["theme"]["name"] = name_match.group(1)
            
            # Extract currency
            curr_match = re.search(r'Shopify\.currency\s*=\s*({[^}]+})', html)
            if curr_match:
                try:
                    curr_info = json.loads(curr_match.group(1))
                    result["currency"] = curr_info.get("active", "USD")
                except Exception:
                    pass
            
            # Check for Shopify 2.0 JSON templates
            if soup.find("template") or 'id="shopify-section-' in html or "sections--" in html:
                result["theme"]["schema_version"] = "Online Store 2.0 (OS 2.0)"
            else:
                result["theme"]["schema_version"] = "Vintage (OS 1.0)"

        # Detect Apps
        for app_name, patterns in COMMON_APPS.items():
            for pat in patterns:
                if re.search(pat, html, re.IGNORECASE):
                    result["detected_apps"].append(app_name)
                    if app_name in ["PageFly", "GemPages", "Shogun", "Zipify"]:
                        result["page_builder"] = app_name
                    break

        # Detect Pixels
        for pixel_name, patterns in PIXELS.items():
            for pat in patterns:
                if re.search(pat, html, re.IGNORECASE):
                    result["detected_pixels"].append(pixel_name)
                    break

        # 2. Check public JSON endpoints
        try:
            prod_resp = session.get(f"{base_url}/products.json?limit=1", timeout=5)
            if prod_resp.status_code == 200 and "products" in prod_resp.text:
                result["has_public_products_json"] = True
                prod_data = prod_resp.json()
                if prod_data.get("products"):
                    result["sample_product"] = prod_data["products"][0].get("title")
        except Exception:
            pass

        try:
            coll_resp = session.get(f"{base_url}/collections.json?limit=1", timeout=5)
            if coll_resp.status_code == 200 and "collections" in coll_resp.text:
                result["has_public_collections_json"] = True
        except Exception:
            pass

    except Exception as e:
        result["error"] = str(e)
        logger.error(f"Error analyzing store: {e}")

    return result
