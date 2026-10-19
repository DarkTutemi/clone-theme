"""
Shopify Store Direct Admin API Client
Automates theme uploading, asset synchronization, and catalog importing directly to the user's store.
"""
import os
import time
import json
import base64
import logging
from concurrent.futures import ThreadPoolExecutor
import requests

logger = logging.getLogger("shopify_store_client")

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "shopify_store_config.json")
LOCAL_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "shopify_store_config.local.json")

class ShopifyStoreClient:
    def __init__(self, config_file: str = None):
        if config_file is None:
            self.config_file = LOCAL_CONFIG_PATH if os.path.exists(LOCAL_CONFIG_PATH) else CONFIG_PATH
        else:
            self.config_file = config_file
        self.store = os.getenv("SHOPIFY_STORE", "g1spma-ku.myshopify.com")
        self.client_id = os.getenv("SHOPIFY_CLIENT_ID", "")
        self.client_secret = os.getenv("SHOPIFY_CLIENT_SECRET", "")
        self.access_token = os.getenv("SHOPIFY_ACCESS_TOKEN", None)
        self.token_expiry = 0
        self.api_version = "2024-07"
        
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.store = data.get("store", self.store)
                    self.client_id = data.get("client_id", self.client_id)
                    self.client_secret = data.get("client_secret", self.client_secret)
                    self.access_token = data.get("access_token")
                    self.token_expiry = data.get("token_expiry", 0)
            except Exception as e:
                logger.warning(f"Failed to read config: {e}")

    def save_config(self):
        data = {
            "store": self.store,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "access_token": self.access_token,
            "token_expiry": self.token_expiry,
            "api_version": self.api_version
        }
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def get_token(self) -> str:
        """Retrieves active token, refreshing via client_credentials if expired or missing."""
        now = time.time()
        if self.access_token and now < self.token_expiry - 60:
            return self.access_token

        url = f"https://{self.store}/admin/oauth/access_token"
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        resp = requests.post(url, json=payload, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            self.access_token = data["access_token"]
            expires_in = data.get("expires_in", 86400)
            self.token_expiry = now + expires_in
            self.save_config()
            logger.info("Shopify access token refreshed successfully.")
            return self.access_token
        else:
            raise Exception(f"Failed to obtain token from Shopify: {resp.status_code} - {resp.text}")

    def _headers(self) -> dict:
        return {
            "X-Shopify-Access-Token": self.get_token(),
            "Content-Type": "application/json"
        }

    def get_shop_info(self) -> dict:
        url = f"https://{self.store}/admin/api/{self.api_version}/shop.json"
        r = requests.get(url, headers=self._headers(), timeout=12)
        if r.status_code == 200:
            return r.json().get("shop", {})
        raise Exception(f"Shop info error: {r.status_code} {r.text}")

    def list_themes(self) -> list:
        url = f"https://{self.store}/admin/api/{self.api_version}/themes.json"
        r = requests.get(url, headers=self._headers(), timeout=12)
        if r.status_code == 200:
            return r.json().get("themes", [])
        raise Exception(f"List themes error: {r.status_code} {r.text}")

    def create_empty_theme(self, name: str, role: str = "unpublished") -> dict:
        url = f"https://{self.store}/admin/api/{self.api_version}/themes.json"
        payload = {"theme": {"name": name, "role": role}}
        r = requests.post(url, json=payload, headers=self._headers(), timeout=15)
        if r.status_code == 201:
            return r.json().get("theme", {})
        raise Exception(f"Create theme error: {r.status_code} {r.text}")

    def upload_asset_to_theme(self, theme_id: int, key: str, value: str = None, attachment_bytes: bytes = None):
        """Uploads a single asset (liquid, css, js, json or binary image/font) to a theme."""
        url = f"https://{self.store}/admin/api/{self.api_version}/themes/{theme_id}/assets.json"
        
        asset_payload = {"key": key}
        if attachment_bytes is not None:
            asset_payload["attachment"] = base64.b64encode(attachment_bytes).decode("utf-8")
        else:
            asset_payload["value"] = value

        r = requests.put(url, json={"asset": asset_payload}, headers=self._headers(), timeout=20)
        if r.status_code not in [200, 201]:
            logger.warning(f"Failed to upload asset {key}: {r.status_code} {r.text}")
            return False
        return True

    def upload_theme_directory(self, theme_dir: str, theme_name: str = None, max_workers: int = 5) -> dict:
        """Uploads an entire cloned theme directory directly into a new theme on the store."""
        if not theme_name:
            theme_name = f"Cloned Theme - {time.strftime('%Y-%m-%d %H:%M')}"

        logger.info(f"Creating new theme '{theme_name}' on {self.store}...")
        theme = self.create_empty_theme(theme_name)
        theme_id = theme["id"]

        logger.info(f"Theme created with ID: {theme_id}. Uploading assets...")
        uploaded = []
        failed = []

        files_to_upload = []
        for root, _, files in os.walk(theme_dir):
            for f in files:
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, theme_dir).replace("\\", "/")
                files_to_upload.append((full_path, rel_path))

        base_files = []
        template_files = []
        for item in files_to_upload:
            p = item[1]
            if "group.json" in p or (p.startswith("templates/") and p.endswith(".json")):
                template_files.append(item)
            else:
                base_files.append(item)

        def _worker(item):
            full_path, rel_path = item
            try:
                # Text files (Liquid, CSS, JS, JSON)
                if rel_path.endswith((".liquid", ".json", ".css", ".js", ".html", ".txt", ".svg")):
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f_obj:
                        content = f_obj.read()
                    ok = self.upload_asset_to_theme(theme_id, rel_path, value=content)
                else:
                    # Binary files (images, woff, woff2, ttf)
                    with open(full_path, "rb") as f_obj:
                        b_content = f_obj.read()
                    ok = self.upload_asset_to_theme(theme_id, rel_path, attachment_bytes=b_content)
                
                if ok:
                    return (True, rel_path)
                else:
                    return (False, rel_path)
            except Exception as e:
                logger.error(f"Error uploading {rel_path}: {e}")
                return (False, rel_path)

        # Phase 1: Upload sections, snippets, layout, assets, config, locales
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for is_ok, path in executor.map(_worker, base_files):
                if is_ok:
                    uploaded.append(path)
                else:
                    failed.append(path)

        # Phase 2: Upload section groups and templates (now all referenced sections exist)
        with ThreadPoolExecutor(max_workers=2) as executor:
            for is_ok, path in executor.map(_worker, template_files):
                if is_ok:
                    uploaded.append(path)
                else:
                    failed.append(path)

        preview_url = f"https://{self.store}/?preview_theme_id={theme_id}"
        editor_url = f"https://admin.shopify.com/store/{self.store.split('.')[0]}/themes/{theme_id}/editor"

        return {
            "status": "success",
            "theme_id": theme_id,
            "theme_name": theme_name,
            "uploaded_assets_count": len(uploaded),
            "failed_assets_count": len(failed),
            "preview_url": preview_url,
            "editor_url": editor_url,
        }

    def import_product(self, product: dict) -> dict:
        """Pushes a single product to Shopify Admin."""
        url = f"https://{self.store}/admin/api/{self.api_version}/products.json"
        
        # Prepare variants
        variants = []
        for v in product.get("variants", []):
            variants.append({
                "option1": v.get("option1", "Default Title"),
                "option2": v.get("option2"),
                "option3": v.get("option3"),
                "price": str(v.get("price", "0.00")),
                "compare_at_price": str(v.get("compare_at_price")) if v.get("compare_at_price") else None,
                "sku": v.get("sku", ""),
                "inventory_management": "shopify",
                "inventory_policy": "deny",
            })
            
        # Prepare images
        images = []
        for img in product.get("images", []):
            if img.get("src"):
                images.append({"src": img["src"], "alt": img.get("alt")})

        payload = {
            "product": {
                "title": product.get("title"),
                "body_html": product.get("body_html"),
                "vendor": product.get("vendor"),
                "product_type": product.get("product_type"),
                "tags": product.get("tags") if isinstance(product.get("tags"), str) else ", ".join(product.get("tags", [])),
                "variants": variants or [{"price": "0.00"}],
                "images": images,
                "status": "active"
            }
        }
        r = requests.post(url, json=payload, headers=self._headers(), timeout=15)
        if r.status_code in [200, 201]:
            return r.json().get("product", {})
        raise Exception(f"Product import error: {r.status_code} {r.text}")
