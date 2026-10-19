"""
Theme Ripper & Asset Downloader
Downloads CSS, JS, fonts, SVGs, and images from competitor store and maps them into Shopify Theme Asset structure.
"""
import os
import re
import logging
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger("theme_ripper")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}

def sanitize_filename(filename: str) -> str:
    name = re.sub(r'[\\/*?:"<>|]', "", filename)
    name = name.split("?")[0].split("#")[0]
    return name or "asset"

class ThemeRipper:
    def __init__(self, target_url: str, output_theme_dir: str):
        if not target_url.startswith("http://") and not target_url.startswith("https://"):
            target_url = "https://" + target_url
        parsed = urlparse(target_url)
        self.target_url = target_url
        self.base_url = f"{parsed.scheme}://{parsed.netloc}"
        self.output_dir = output_theme_dir
        self.assets_dir = os.path.join(output_theme_dir, "assets")
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.downloaded_assets = {} # url -> local_filename

        os.makedirs(self.assets_dir, exist_ok=True)

    def download_file(self, url: str, fallback_prefix: str = "asset", ext_hint: str = None) -> str:
        """Downloads a remote URL asset and saves it into assets/"""
        if not url:
            return None
        full_url = urljoin(self.base_url, url)
        if full_url in self.downloaded_assets:
            return self.downloaded_assets[full_url]

        parsed = urlparse(full_url)
        raw_name = os.path.basename(parsed.path)
        clean_name = sanitize_filename(raw_name)

        if not clean_name or "." not in clean_name:
            clean_name = f"{fallback_prefix}_{abs(hash(full_url)) % 10000}"
            if ext_hint:
                clean_name += f".{ext_hint}"

        # Prevent duplicate filenames with different content
        dest_path = os.path.join(self.assets_dir, clean_name)
        counter = 1
        base, ext = os.path.splitext(clean_name)
        while os.path.exists(dest_path) and full_url not in self.downloaded_assets:
            clean_name = f"{base}_{counter}{ext}"
            dest_path = os.path.join(self.assets_dir, clean_name)
            counter += 1

        try:
            r = self.session.get(full_url, timeout=12, stream=True)
            if r.status_code == 200:
                with open(dest_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                self.downloaded_assets[full_url] = clean_name
                logger.info(f"Downloaded asset: {clean_name} from {full_url}")
                return clean_name
        except Exception as e:
            logger.warning(f"Failed to download {full_url}: {e}")

        return None

    def fetch_page_html(self, path: str = "/") -> str:
        url = urljoin(self.base_url, path)
        try:
            r = self.session.get(url, timeout=15)
            if r.status_code == 200:
                return r.text
        except Exception as e:
            logger.error(f"Error fetching page {url}: {e}")
        return ""

    def rip_assets(self, soup: BeautifulSoup) -> dict:
        """
        Scans DOM for stylesheets, scripts, fonts, and images, downloading them locally.
        Returns a mapping of original URLs to downloaded local filenames.
        """
        asset_map = {
            "css": [],
            "js": [],
            "images": [],
            "fonts": [],
        }

        # 1. Stylesheets
        for link in soup.find_all("link", rel=lambda r: r and "stylesheet" in r):
            href = link.get("href")
            if href:
                # Filter out obvious 3rd party spam tracking stylesheets if needed
                local_file = self.download_file(href, fallback_prefix="theme", ext_hint="css")
                if local_file:
                    asset_map["css"].append({"orig": href, "local": local_file})

        # 2. Scripts (Shopify theme core scripts)
        for s in soup.find_all("script", src=True):
            src = s.get("src")
            if src and any(term in src for term in ["cdn.shopify.com", "theme", "vendor", "bundle", "global", "cart", "product"]):
                # Avoid downloading heavy external tracking scripts
                if not any(skip in src for skip in ["google", "facebook", "tiktok", "klaviyo", "hotjar"]):
                    local_file = self.download_file(src, fallback_prefix="vendor", ext_hint="js")
                    if local_file:
                        asset_map["js"].append({"orig": src, "local": local_file})

        # 3. Web Fonts
        for font_link in soup.find_all("link", rel="preload", as_="font"):
            href = font_link.get("href")
            if href:
                local_file = self.download_file(href, fallback_prefix="font", ext_hint="woff2")
                if local_file:
                    asset_map["fonts"].append({"orig": href, "local": local_file})

        # 4. Critical brand images (Logo, Favicon, Hero banner)
        favicon_link = soup.find("link", rel=lambda r: r and "icon" in r)
        if favicon_link and favicon_link.get("href"):
            self.download_file(favicon_link.get("href"), fallback_prefix="favicon", ext_hint="png")

        for img in soup.find_all("img", src=True)[:15]:
            src = img.get("src")
            if src and ("logo" in src.lower() or "banner" in src.lower() or "hero" in src.lower()):
                local_file = self.download_file(src, fallback_prefix="image", ext_hint="png")
                if local_file:
                    asset_map["images"].append({"orig": src, "local": local_file})

        return asset_map
