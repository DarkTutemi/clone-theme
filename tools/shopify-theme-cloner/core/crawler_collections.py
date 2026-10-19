"""
Shopify Collections Crawler
Crawls all collections, category descriptions, banner images, and product associations.
"""
import json
import logging
from urllib.parse import urlparse
import requests

logger = logging.getLogger("collections_crawler")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "application/json,text/html,*/*",
}

def crawl_collections(store_url: str, max_collections: int = 100) -> list:
    if not store_url.startswith("http://") and not store_url.startswith("https://"):
        store_url = "https://" + store_url
    
    parsed = urlparse(store_url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    
    session = requests.Session()
    session.headers.update(HEADERS)
    
    all_collections = []
    page = 1
    
    while len(all_collections) < max_collections:
        url = f"{base_url}/collections.json?page={page}&limit=50"
        try:
            resp = session.get(url, timeout=12)
            if resp.status_code != 200:
                break
                
            data = resp.json()
            collections = data.get("collections", [])
            if not collections:
                break
                
            all_collections.extend(collections)
            if len(collections) < 50:
                break
                
            page += 1
        except Exception as e:
            logger.error(f"Error crawling collections page {page}: {e}")
            break
            
    return all_collections[:max_collections]

def export_collections_json(collections: list, output_path: str) -> str:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"collections": collections, "count": len(collections)}, f, ensure_ascii=False, indent=2)
    return output_path
