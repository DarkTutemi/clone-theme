#!/usr/bin/env python
"""
Shopify & E-Commerce Competitor Store Cloner CLI
Usage:
  python cli.py analyze --url https://target-store.com
  python cli.py crawl-products --url https://target-store.com --output ./products.csv --max 500
  python cli.py crawl-collections --url https://target-store.com --output ./collections.json
  python cli.py clone-theme --url https://target-store.com --output ./cloned-theme --zip
  python cli.py convert-section --input ./section.html --name hero-banner --output ./sections/hero.liquid
  python cli.py package-theme --theme-dir ./cloned-theme --output ./theme.zip
  python cli.py store-info
  python cli.py push-theme --theme-dir ./cloned-theme --name "Cloned Theme Test"
  python cli.py push-products --json ./products.json --max 20
"""
import sys
import os
import argparse
import json
import logging

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.analyzer import analyze_store
from core.crawler_products import crawl_products, export_to_shopify_csv, export_to_json
from core.crawler_collections import crawl_collections, export_collections_json
from core.theme_builder import ShopifyThemeBuilder
from core.section_converter import convert_html_to_liquid_section
from core.store_client import ShopifyStoreClient

# Try importing visual diff comparator
try:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from visual_diff_comparator import run_visual_verification, inspect_dom_element
except ImportError:
    run_visual_verification = None
    inspect_dom_element = None

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    parser = argparse.ArgumentParser(description="Shopify & Competitor Store Cloner & Crawler Suite")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 1. Analyze
    p_analyze = subparsers.add_parser("analyze", help="Analyze target store tech stack, theme, apps, pixels")
    p_analyze.add_argument("--url", required=True, help="Target store URL")
    p_analyze.add_argument("--output", help="Save analysis JSON to file")

    # 2. Crawl Products
    p_prod = subparsers.add_parser("crawl-products", help="Crawl products and export to Shopify CSV / JSON")
    p_prod.add_argument("--url", required=True, help="Target store URL")
    p_prod.add_argument("--output", default="products_export.csv", help="Output CSV path")
    p_prod.add_argument("--json-output", help="Also export full JSON to this path")
    p_prod.add_argument("--max", type=int, default=500, help="Max products to fetch (default: 500)")

    # 3. Crawl Collections
    p_coll = subparsers.add_parser("crawl-collections", help="Crawl collections and product associations")
    p_coll.add_argument("--url", required=True, help="Target store URL")
    p_coll.add_argument("--output", default="collections.json", help="Output JSON path")
    p_coll.add_argument("--max", type=int, default=100, help="Max collections to fetch")

    # 4. Clone Theme
    p_clone = subparsers.add_parser("clone-theme", help="Clone theme assets, layout, and sections into Shopify OS 2.0 theme")
    p_clone.add_argument("--url", required=True, help="Target store URL")
    p_clone.add_argument("--output", default="./cloned-shopify-theme", help="Output directory")
    p_clone.add_argument("--zip", action="store_true", help="Automatically package into .zip archive")

    # 5. Convert Section
    p_conv = subparsers.add_parser("convert-section", help="Convert raw HTML block to Shopify Liquid Section")
    p_conv.add_argument("--input", required=True, help="HTML file path")
    p_conv.add_argument("--name", default="custom-section", help="Section identifier")
    p_conv.add_argument("--title", help="Human-readable section title")
    p_conv.add_argument("--output", help="Output .liquid file path")

    # 6. Package Theme
    p_pkg = subparsers.add_parser("package-theme", help="Package theme directory into installable Shopify .zip")
    p_pkg.add_argument("--theme-dir", required=True, help="Theme directory path")
    p_pkg.add_argument("--output", help="Output .zip path")

    # 7. Store Info
    p_store = subparsers.add_parser("store-info", help="Display connected Shopify store details and themes")

    # 8. Push Theme
    p_push_theme = subparsers.add_parser("push-theme", help="Upload cloned theme directory directly into connected Shopify store")
    p_push_theme.add_argument("--theme-dir", required=True, help="Path to local theme directory")
    p_push_theme.add_argument("--name", help="Theme name in Shopify")

    # 9. Push Products
    p_push_prod = subparsers.add_parser("push-products", help="Import products from JSON catalog into connected store")
    p_push_prod.add_argument("--json", required=True, help="Path to products JSON file")
    p_push_prod.add_argument("--max", type=int, default=50, help="Max products to upload (default: 50)")

    # 10. Visual Compare
    p_vcomp = subparsers.add_parser("visual-compare", help="Capture and compare side-by-side screenshots between target and clone")
    p_vcomp.add_argument("--target", required=True, help="Target competitor URL")
    p_vcomp.add_argument("--clone", required=True, help="Cloned store or preview URL")
    p_vcomp.add_argument("--out", default="./visual_diff", help="Output directory")

    # 11. Inspect DOM
    p_idom = subparsers.add_parser("inspect-dom", help="Inspect rendered DOM and extract computed element structure")
    p_idom.add_argument("--url", required=True, help="Target URL")
    p_idom.add_argument("--selector", required=True, help="CSS Selector")

    args = parser.parse_args()

    if args.command == "analyze":
        print(f"[*] Analyzing target store: {args.url}...")
        res = analyze_store(args.url)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(res, f, indent=2, ensure_ascii=False)
            print(f"[+] Analysis saved to: {args.output}")

    elif args.command == "crawl-products":
        print(f"[*] Crawling products from: {args.url} (limit: {args.max})...")
        prods = crawl_products(args.url, max_products=args.max)
        print(f"[+] Fetched {len(prods)} products successfully.")
        
        csv_file = export_to_shopify_csv(prods, args.output)
        print(f"[+] Shopify Import CSV generated: {csv_file}")
        
        if args.json_output:
            json_file = export_to_json(prods, args.json_output)
            print(f"[+] JSON catalog saved to: {json_file}")

    elif args.command == "crawl-collections":
        print(f"[*] Crawling collections from: {args.url}...")
        colls = crawl_collections(args.url, max_collections=args.max)
        print(f"[+] Fetched {len(colls)} collections.")
        out_file = export_collections_json(colls, args.output)
        print(f"[+] Collections saved to: {out_file}")

    elif args.command == "clone-theme":
        print(f"[*] Cloning theme from: {args.url} -> {args.output}...")
        builder = ShopifyThemeBuilder(args.url, args.output)
        report = builder.build_theme()
        print(f"[+] Theme built successfully:")
        print(f"    - Sections extracted: {len(report['sections_extracted'])} ({', '.join(report['sections_extracted'][:5])}...)")
        print(f"    - Assets downloaded: {report['assets_downloaded']}")
        
        if args.zip:
            zip_path = builder.create_theme_zip()
            print(f"[+] Packaged Shopify Theme ZIP ready for upload: {zip_path}")

    elif args.command == "convert-section":
        with open(args.input, "r", encoding="utf-8") as f:
            html = f.read()
        liquid = convert_html_to_liquid_section(html, args.name, args.title)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(liquid)
            print(f"[+] Liquid Section created: {args.output}")
        else:
            print(liquid)

    elif args.command == "package-theme":
        builder = ShopifyThemeBuilder("", args.theme_dir)
        zip_path = builder.create_theme_zip(args.output)
        print(f"[+] Theme packaged: {zip_path}")

    elif args.command == "store-info":
        client = ShopifyStoreClient()
        shop = client.get_shop_info()
        themes = client.list_themes()
        print("=== CONNECTED SHOPIFY STORE ===")
        print(f"Name: {shop.get('name')}")
        print(f"Domain: {shop.get('domain')}")
        print(f"Email: {shop.get('email')}")
        print(f"Plan: {shop.get('plan_name')}")
        print(f"Currency: {shop.get('currency')}")
        print(f"Installed Themes ({len(themes)}):")
        for t in themes:
            print(f"  - [{t.get('id')}] {t.get('name')} (Role: {t.get('role')})")

    elif args.command == "push-theme":
        client = ShopifyStoreClient()
        print(f"[*] Uploading theme from '{args.theme_dir}' to {client.store}...")
        res = client.upload_theme_directory(args.theme_dir, theme_name=args.name)
        print(f"[+] Theme uploaded successfully!")
        print(f"    - Theme ID: {res['theme_id']}")
        print(f"    - Name: {res['theme_name']}")
        print(f"    - Assets uploaded: {res['uploaded_assets_count']}")
        print(f"    - Preview URL: {res['preview_url']}")
        print(f"    - Theme Editor: {res['editor_url']}")

    elif args.command == "push-products":
        client = ShopifyStoreClient()
        with open(args.json, "r", encoding="utf-8") as f:
            data = json.load(f)
        products = data.get("products", [])[:args.max]
        print(f"[*] Importing {len(products)} products to {client.store}...")
        success = 0
        for i, p in enumerate(products):
            try:
                res = client.import_product(p)
                success += 1
                print(f"  [{i+1}/{len(products)}] Imported: {res.get('title')} (ID: {res.get('id')})")
            except Exception as e:
                print(f"  [{i+1}/{len(products)}] Failed {p.get('title')}: {e}")
        print(f"[+] Import completed: {success}/{len(products)} products imported successfully.")

    elif args.command == "visual-compare":
        if not run_visual_verification:
            print("[-] visual_diff_comparator module not available.", file=sys.stderr)
            sys.exit(1)
        run_visual_verification(args.target, args.clone, args.out)

    elif args.command == "inspect-dom":
        if not inspect_dom_element:
            print("[-] visual_diff_comparator module not available.", file=sys.stderr)
            sys.exit(1)
        res = inspect_dom_element(args.url, args.selector)
        print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
