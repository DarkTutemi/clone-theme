"""
Shopify & Competitor Store Product Crawler & Exporter
Fetches full catalog from competitor stores and exports directly to Shopify Import CSV & JSON.
"""
import csv
import json
import logging
import time
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger("product_crawler")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "application/json,text/html,*/*",
}

SHOPIFY_CSV_HEADERS = [
    "Handle", "Title", "Body (HTML)", "Vendor", "Product Category", "Type", "Tags", "Published",
    "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value", "Option3 Name", "Option3 Value",
    "Variant SKU", "Variant Grams", "Variant Inventory Tracker", "Variant Inventory Qty",
    "Variant Inventory Policy", "Variant Fulfillment Service", "Variant Price", "Variant Compare At Price",
    "Variant Requires Shipping", "Variant Taxable", "Variant Barcode", "Image Src", "Image Position",
    "Image Alt Text", "Gift Card", "SEO Title", "SEO Description", "Google Shopping / Google Product Category",
    "Google Shopping / Gender", "Google Shopping / Age Group", "Google Shopping / MPN",
    "Google Shopping / AdWords Grouping", "Google Shopping / AdWords Labels", "Google Shopping / Condition",
    "Google Shopping / Custom Product", "Google Shopping / Custom Label 0", "Google Shopping / Custom Label 1",
    "Google Shopping / Custom Label 2", "Google Shopping / Custom Label 3", "Google Shopping / Custom Label 4",
    "Variant Image", "Variant Weight Unit", "Variant Tax Code", "Cost per item", "Status"
]

def crawl_products(store_url: str, max_products: int = 500, delay_sec: float = 0.5) -> list:
    """
    Crawls all products from a Shopify store using /products.json pagination.
    Falls back to /collections/all/products.json if main endpoint is restricted.
    """
    if not store_url.startswith("http://") and not store_url.startswith("https://"):
        store_url = "https://" + store_url
    
    parsed = urlparse(store_url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    
    session = requests.Session()
    session.headers.update(HEADERS)
    
    all_products = []
    page = 1
    endpoints = [
        f"{base_url}/products.json",
        f"{base_url}/collections/all/products.json",
    ]
    
    active_endpoint = endpoints[0]
    
    # Test primary endpoint
    try:
        r = session.get(f"{active_endpoint}?limit=1", timeout=10)
        if r.status_code != 200 or "products" not in r.text:
            active_endpoint = endpoints[1]
    except Exception:
        active_endpoint = endpoints[1]
        
    while len(all_products) < max_products:
        limit = min(250, max_products - len(all_products))
        url = f"{active_endpoint}?limit={limit}&page={page}"
        logger.info(f"Crawling products: {url}")
        
        try:
            resp = session.get(url, timeout=15)
            if resp.status_code != 200:
                logger.warning(f"Got status {resp.status_code} on page {page}. Stopping.")
                break
                
            data = resp.json()
            products = data.get("products", [])
            if not products:
                break
                
            all_products.extend(products)
            logger.info(f"Fetched {len(products)} products (Total: {len(all_products)})")
            
            if len(products) < limit:
                break
                
            page += 1
            if delay_sec > 0:
                time.sleep(delay_sec)
        except Exception as e:
            logger.error(f"Error fetching page {page}: {e}")
            break

    # If JSON was empty/blocked, try scraping sitemap_products_1.xml
    if not all_products:
        logger.info("JSON API empty or protected. Attempting sitemap product recovery...")
        all_products = crawl_from_sitemap(base_url, session, max_products)
        
    return all_products[:max_products]

def crawl_from_sitemap(base_url: str, session: requests.Session, max_products: int) -> list:
    """Fallback parser for store XML sitemaps"""
    sitemap_url = f"{base_url}/sitemap_products_1.xml"
    products = []
    try:
        resp = session.get(sitemap_url, timeout=15)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "xml")
            urls = soup.find_all("url")
            for u in urls[:max_products]:
                loc = u.find("loc")
                if not loc:
                    continue
                product_url = loc.text
                handle = product_url.rstrip("/").split("/")[-1]
                
                # Fetch single product JSON if possible
                try:
                    p_resp = session.get(f"{product_url}.json", timeout=8)
                    if p_resp.status_code == 200 and "product" in p_resp.text:
                        products.append(p_resp.json()["product"])
                        continue
                except Exception:
                    pass
                
                # Or extract basic title from sitemap images
                images = []
                for img in u.find_all("image:image"):
                    img_loc = img.find("image:loc")
                    img_title = img.find("image:title")
                    if img_loc:
                        images.append({"src": img_loc.text, "alt": img_title.text if img_title else ""})
                        
                products.append({
                    "id": handle,
                    "title": handle.replace("-", " ").title(),
                    "handle": handle,
                    "body_html": f"<p>{handle.replace('-', ' ').title()}</p>",
                    "vendor": base_url.replace("https://", ""),
                    "product_type": "Imported Product",
                    "tags": ["imported", "scraped"],
                    "variants": [{
                        "id": 1,
                        "title": "Default Title",
                        "price": "0.00",
                        "compare_at_price": None,
                        "sku": handle.upper(),
                        "requires_shipping": True,
                        "taxable": True,
                    }],
                    "images": images,
                    "options": [{"name": "Title", "values": ["Default Title"]}]
                })
    except Exception as e:
        logger.error(f"Sitemap crawl error: {e}")
        
    return products

def export_to_shopify_csv(products: list, output_csv_path: str) -> str:
    """
    Transforms scraped product dictionary into Shopify Products Import standard CSV format.
    Handles multiple variants and multiple images cleanly.
    """
    rows = []
    
    for prod in products:
        handle = prod.get("handle", "")
        title = prod.get("title", "")
        body_html = prod.get("body_html", "") or ""
        vendor = prod.get("vendor", "")
        product_type = prod.get("product_type", "")
        tags = prod.get("tags", "")
        if isinstance(tags, list):
            tags = ", ".join(str(t) for t in tags)
        published = "TRUE"
        
        options = prod.get("options", [])
        opt1_name = options[0]["name"] if len(options) > 0 else "Title"
        opt2_name = options[1]["name"] if len(options) > 1 else ""
        opt3_name = options[2]["name"] if len(options) > 2 else ""
        
        variants = prod.get("variants", [])
        images = prod.get("images", [])
        
        max_rows = max(len(variants), len(images), 1)
        
        for i in range(max_rows):
            v = variants[i] if i < len(variants) else None
            img = images[i] if i < len(images) else None
            
            row = {h: "" for h in SHOPIFY_CSV_HEADERS}
            row["Handle"] = handle
            
            # First row carries main product info
            if i == 0:
                row["Title"] = title
                row["Body (HTML)"] = body_html
                row["Vendor"] = vendor
                row["Type"] = product_type
                row["Tags"] = tags
                row["Published"] = published
                row["Status"] = "active"
                
            # Variant fields
            if v:
                row["Option1 Name"] = opt1_name if i == 0 else ""
                row["Option1 Value"] = v.get("option1", "Default Title")
                row["Option2 Name"] = opt2_name if i == 0 else ""
                row["Option2 Value"] = v.get("option2", "")
                row["Option3 Name"] = opt3_name if i == 0 else ""
                row["Option3 Value"] = v.get("option3", "")
                row["Variant SKU"] = v.get("sku", "")
                row["Variant Grams"] = v.get("grams", 0)
                row["Variant Inventory Tracker"] = "shopify"
                row["Variant Inventory Qty"] = 100
                row["Variant Inventory Policy"] = "deny"
                row["Variant Fulfillment Service"] = "manual"
                row["Variant Price"] = v.get("price", "0.00")
                row["Variant Compare At Price"] = v.get("compare_at_price", "") or ""
                row["Variant Requires Shipping"] = "TRUE" if v.get("requires_shipping", True) else "FALSE"
                row["Variant Taxable"] = "TRUE" if v.get("taxable", True) else "FALSE"
                row["Variant Barcode"] = v.get("barcode", "") or ""
                row["Variant Weight Unit"] = v.get("weight_unit", "kg")
                
            # Image fields
            if img:
                row["Image Src"] = img.get("src", "")
                row["Image Position"] = i + 1
                row["Image Alt Text"] = img.get("alt", "") or title
                
            rows.append(row)
            
    with open(output_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=SHOPIFY_CSV_HEADERS)
        writer.writeheader()
        writer.writerows(rows)
        
    return output_csv_path

def export_to_json(products: list, output_json_path: str) -> str:
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump({"products": products, "count": len(products)}, f, ensure_ascii=False, indent=2)
    return output_json_path
