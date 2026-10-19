"""
Shopify & E-Commerce Theme Cloner & Data Crawler MCP Server
Exposes automated tools for store analysis, catalog scraping, theme ripping, and Liquid generation.
"""
import os
import sys
import json
import logging

ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ENGINE_DIR)

from mcp.server.mcpserver import MCPServer
from core.analyzer import analyze_store
from core.crawler_products import crawl_products, export_to_shopify_csv, export_to_json
from core.crawler_collections import crawl_collections, export_collections_json
from core.theme_builder import ShopifyThemeBuilder
from core.section_converter import convert_html_to_liquid_section as convert_sec
from core.store_client import ShopifyStoreClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

server = MCPServer(
    name="shopify_theme_cloner",
    version="1.1.0",
    description="Full suite for Shopify competitor intelligence, catalog scraping, theme cloning, Liquid generation, and direct store deployment."
)

@server.tool(
    name="analyze_store_tech",
    description="Analyze a competitor store URL to detect e-commerce platform, Shopify theme name & ID, installed Shopify apps, page builders, tracking pixels, and active currency."
)
def tool_analyze_store_tech(store_url: str) -> str:
    res = analyze_store(store_url)
    return json.dumps(res, indent=2, ensure_ascii=False)

@server.tool(
    name="crawl_competitor_products",
    description="Crawl products from a competitor Shopify or e-commerce store and export them into standard Shopify Import CSV format and JSON. The CSV can be imported directly into Shopify Admin > Products > Import."
)
def tool_crawl_products(store_url: str, output_csv_path: str = None, max_products: int = 250) -> str:
    prods = crawl_products(store_url, max_products=max_products)
    if not output_csv_path:
        domain = store_url.replace("https://", "").replace("http://", "").split("/")[0].replace(":", "_")
        output_csv_path = os.path.join(os.getcwd(), f"{domain}_products_export.csv")

    csv_file = export_to_shopify_csv(prods, output_csv_path)
    json_file = output_csv_path.replace(".csv", ".json")
    export_to_json(prods, json_file)

    return json.dumps({
        "status": "success",
        "products_count": len(prods),
        "shopify_csv_path": csv_file,
        "json_path": json_file,
        "sample_titles": [p.get("title") for p in prods[:5]]
    }, indent=2, ensure_ascii=False)

@server.tool(
    name="crawl_store_collections",
    description="Crawl all collections, category descriptions, banner images, and handles from a target store."
)
def tool_crawl_collections(store_url: str, output_json_path: str = None, max_collections: int = 100) -> str:
    colls = crawl_collections(store_url, max_collections=max_collections)
    if not output_json_path:
        domain = store_url.replace("https://", "").replace("http://", "").split("/")[0].replace(":", "_")
        output_json_path = os.path.join(os.getcwd(), f"{domain}_collections.json")

    json_file = export_collections_json(colls, output_json_path)
    return json.dumps({
        "status": "success",
        "collections_count": len(colls),
        "output_path": json_file,
        "collection_names": [c.get("title") for c in colls[:10]]
    }, indent=2, ensure_ascii=False)

@server.tool(
    name="clone_store_theme",
    description="Deeply rip and reconstruct a competitor store's theme into a standard Shopify Online Store 2.0 theme. Downloads CSS, JS, fonts, SVGs, extracts sections, generates layout/theme.liquid, templates/index.json, and packages into a ready-to-upload .zip file."
)
def tool_clone_store_theme(store_url: str, output_dir: str = None, create_zip: bool = True) -> str:
    if not output_dir:
        domain = store_url.replace("https://", "").replace("http://", "").split("/")[0].replace(":", "_")
        output_dir = os.path.join(os.getcwd(), f"{domain}_theme_cloned")

    builder = ShopifyThemeBuilder(store_url, output_dir)
    report = builder.build_theme()

    if create_zip and report.get("status") == "success":
        zip_path = builder.create_theme_zip()
        report["theme_zip_path"] = zip_path

    return json.dumps(report, indent=2, ensure_ascii=False)

@server.tool(
    name="convert_html_to_liquid_section",
    description="Convert an arbitrary HTML snippet or section block into a modular Shopify 2.0 Liquid Section with editable schema settings for the Shopify Theme Customizer."
)
def tool_convert_html_to_liquid(html_code: str, section_name: str, section_title: str = None) -> str:
    liquid = convert_sec(html_code, section_name, section_title)
    return liquid

@server.tool(
    name="package_theme_zip",
    description="Packages any valid Shopify theme directory into an installable .zip archive ready for Shopify Admin > Online Store > Themes > Upload theme."
)
def tool_package_theme_zip(theme_dir: str, output_zip_path: str = None) -> str:
    builder = ShopifyThemeBuilder("", theme_dir)
    zip_path = builder.create_theme_zip(output_zip_path)
    return json.dumps({
        "status": "success",
        "theme_dir": theme_dir,
        "zip_path": zip_path
    }, indent=2)

@server.tool(
    name="get_connected_store_status",
    description="Check connection health, store profile, and themes of the user's connected Shopify store (g1spma-ku.myshopify.com)."
)
def tool_get_store_status() -> str:
    client = ShopifyStoreClient()
    shop = client.get_shop_info()
    themes = client.list_themes()
    return json.dumps({
        "status": "connected",
        "store_name": shop.get("name"),
        "domain": shop.get("domain"),
        "email": shop.get("email"),
        "plan": shop.get("plan_name"),
        "currency": shop.get("currency"),
        "themes": [{"id": t.get("id"), "name": t.get("name"), "role": t.get("role")} for t in themes]
    }, indent=2, ensure_ascii=False)

@server.tool(
    name="upload_theme_to_my_store",
    description="Uploads a cloned theme directory directly into the connected Shopify store (g1spma-ku.myshopify.com) as a new unpublished theme."
)
def tool_upload_theme(theme_dir: str, theme_name: str = None) -> str:
    client = ShopifyStoreClient()
    res = client.upload_theme_directory(theme_dir, theme_name=theme_name)
    return json.dumps(res, indent=2, ensure_ascii=False)

@server.tool(
    name="import_products_to_my_store",
    description="Import scraped products from a JSON catalog file directly into the connected Shopify store (g1spma-ku.myshopify.com)."
)
def tool_import_products(catalog_json_path: str, max_products: int = 50) -> str:
    client = ShopifyStoreClient()
    with open(catalog_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    products = data.get("products", [])[:max_products]
    success_count = 0
    imported = []
    for p in products:
        try:
            r = client.import_product(p)
            success_count += 1
            imported.append({"id": r.get("id"), "title": r.get("title")})
        except Exception as e:
            logger.error(f"Error importing {p.get('title')}: {e}")

    return json.dumps({
        "status": "success",
        "imported_count": success_count,
        "total_requested": len(products),
        "sample_imported": imported[:5]
    }, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    server.run(transport="stdio")
