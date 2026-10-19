import json
import os
import urllib.parse
from bs4 import BeautifulSoup

BRONOIR_DIR = "f:/clone-theme/project-trybronoir"
CATALOG_PATH = os.path.join(BRONOIR_DIR, "bridge/bestsellers_catalog.json")
WINTER_PATH = os.path.join(BRONOIR_DIR, "collections_data/winter-collection.json")
PRODUCTS_JSON = os.path.join(BRONOIR_DIR, "data/products.json")

_PRODUCT_CACHE = {}

def get_product_data(handle):
    global _PRODUCT_CACHE
    if not _PRODUCT_CACHE:
        # 1. Load winter collection catalog (103 products)
        if os.path.exists(WINTER_PATH):
            try:
                with open(WINTER_PATH, "r", encoding="utf-8") as f:
                    w_data = json.load(f)
                for p in w_data.get("products", []):
                    h = p.get("handle")
                    if not h:
                        continue
                    variants = p.get("variants", [])
                    images = [im.get("src") for im in p.get("images", []) if im.get("src")]
                    raw_p = variants[0].get("price", "74.90") if variants else "74.90"
                    raw_c = variants[0].get("compare_at_price", "129.90") if variants else "129.90"
                    try:
                        val_p = float(raw_p)
                        val_c = float(raw_c) if raw_c else val_p * 1.5
                        p_sale = f"${val_p:.2f}"
                        p_comp = f"${val_c:.2f}"
                    except Exception:
                        p_sale = "$74.90"
                        p_comp = "$129.90"

                    swatches = []
                    color_seen = set()
                    for v in variants:
                        c_name = v.get("option1") or ""
                        f_img = v.get("featured_image", {}).get("src") if v.get("featured_image") else None
                        if c_name and c_name not in color_seen and f_img:
                            color_seen.add(c_name)
                            swatches.append({
                                "title": c_name,
                                "image": f_img
                            })

                    if not swatches and images:
                        for idx, img_u in enumerate(images[:5]):
                            swatches.append({
                                "title": f"Color {idx+1}",
                                "image": img_u
                            })

                    clean_title = p.get("title", "Barefoot Shoes").replace("\ufffd", "™").replace("â„¢", "™")
                    _PRODUCT_CACHE[h] = {
                        "handle": h,
                        "title": clean_title,
                        "price_sale": p_sale,
                        "price_compare": p_comp,
                        "badge": "SALE",
                        "all_images": images,
                        "swatches": swatches,
                        "body_html": p.get("body_html", ""),
                        "is_winter": True
                    }
            except Exception as e:
                print(f"[!] Error loading winter catalog: {e}", flush=True)

        # 2. Load bestsellers catalog
        if os.path.exists(CATALOG_PATH):
            try:
                with open(CATALOG_PATH, "r", encoding="utf-8") as f:
                    for p in json.load(f):
                        h = p.get("handle")
                        if h and h not in _PRODUCT_CACHE:
                            _PRODUCT_CACHE[h] = p
            except Exception:
                pass

    clean_handle = urllib.parse.unquote(handle).strip()
    norm_handle = clean_handle.lower().replace("™", "").replace("%e2%84%a2", "").replace("-", "")

    # Exact match
    if clean_handle in _PRODUCT_CACHE:
        return _PRODUCT_CACHE[clean_handle]
    if handle in _PRODUCT_CACHE:
        return _PRODUCT_CACHE[handle]

    # Normalized match
    for k, v in _PRODUCT_CACHE.items():
        k_norm = k.lower().replace("™", "").replace("%e2%84%a2", "").replace("-", "")
        if k_norm == norm_handle or norm_handle in k_norm or k_norm in norm_handle:
            return v

    return None

def render_pdp(handle):
    clean = urllib.parse.unquote(handle).lower().replace("™", "").replace("%e2%84%a2", "")
    prod = get_product_data(handle)
    is_winter = (prod and prod.get("is_winter")) or any(w in clean for w in ["winter", "fleece", "boot", "arctic", "cozy", "toasty", "snow", "frost", "warm", "chill", "ice", "insul", "shearling", "fuzz", "quilt", "scout", "ranger", "hiker", "trek", "metro", "explorer", "agile", "windshield", "easyflex", "motion", "city", "glide", "easystride", "ultralite", "airlite", "flexshield", "flow", "flexwarm", "featherlite", "flextrail", "suregrip", "flexlite", "stormguard", "flexpro", "chillshield", "move", "freezeguard", "heatlock", "icelock", "nimble", "griplite", "springstep", "gripmax", "softstep", "grippro", "lightstride", "tractionpro", "naturalstride", "citygrip", "trailgrip", "snowgrip", "wintergrip", "iceguard", "knit-lined", "softshell", "fiberloft", "loft"])

    # Select base template
    if is_winter:
        if "cosycloud" in clean:
            base_file = "bridge/product_cosycloud.html"
        elif "toasty" in clean:
            base_file = "bridge/product_toasty.html"
        else:
            base_file = "bridge/product_arctic.html"
    elif "trail" in clean:
        base_file = "bridge/product_trail_masters.html"
    elif "skin-pro" in clean or not handle:
        base_file = "bridge/product.html"
    else:
        base_file = "bridge/product_arctic.html"

    base_path = os.path.join(BRONOIR_DIR, base_file)
    if not os.path.exists(base_path):
        base_path = os.path.join(BRONOIR_DIR, "bridge/product.html")

    with open(base_path, "r", encoding="utf-8", errors="ignore") as f:
        html_raw = f.read()

    # Exact static template return for default products
    if ("arctic-2-0" in clean or "arctic-barefoot-shoes-1-1-free" in clean) and "product_arctic.html" in base_file:
        return html_raw
    if "cosycloud" in clean and "product_cosycloud.html" in base_file and not prod:
        return html_raw
    if "toasty" in clean and "product_toasty.html" in base_file and not prod:
        return html_raw
    if "trail" in clean and "product_trail_masters.html" in base_file and not prod:
        return html_raw
    if ("skin-pro" in clean or not handle) and "product.html" in base_file and not prod:
        return html_raw

    if not prod:
        return html_raw

    title = prod.get("title", "Barefoot Shoes")
    price_sale = prod.get("price_sale", "$74.90")
    price_compare = prod.get("price_compare", "$129.90")
    images = prod.get("all_images", [])
    swatches = prod.get("swatches", [])

    soup = BeautifulSoup(html_raw, "html.parser")

    # 1. Update Title
    if soup.title:
        soup.title.string = f"{title} – Bronoir"
    h1 = soup.find("h1", class_="product-meta__title") or soup.find("h1")
    if h1:
        h1.string = title
    sticky_title = soup.find("span", class_="product-sticky-form__title")
    if sticky_title:
        sticky_title.string = title
    bc_items = soup.select(".breadcrumb__item")
    if len(bc_items) > 1:
        bc_items[-1].string = title

    # 2. Update Prices
    p_sale = soup.find("span", class_="price--highlight")
    if p_sale:
        p_sale.string = f"Sale price{price_sale}"
    p_sticky = soup.find("span", class_="product-sticky-form__price")
    if p_sticky:
        p_sticky.string = price_sale
    p_comp = soup.find("span", class_="price--compare")
    if p_comp and price_compare:
        p_comp.string = f"Regular price{price_compare}"

    # 3. Update Sticky Image
    sticky_img = soup.find("img", class_="product-sticky-form__image")
    if sticky_img and images:
        sticky_img["src"] = images[0]

    # 4. Update Media List
    media_list = soup.find(class_="product__media-list")
    if media_list and images:
        media_list.clear()
        for idx, img_url in enumerate(images):
            is_sel = "is-initial-selected is-selected" if idx == 0 else ""
            item_html = f'<div id="product-media-{idx}" class="product__media-item {is_sel}" data-media-type="image" data-media-id="{idx}" data-original-position="{idx}"><div class="product__media-image-wrapper aspect-ratio aspect-ratio--natural" style="padding-bottom: 100.0%; --aspect-ratio: 1.0"><img class="product__media-image" sizes="(max-width: 999px) calc(100vw - 48px), 640px" height="1080" width="1080" alt="{title}" src="{img_url}"></div></div>'
            media_list.append(BeautifulSoup(item_html, "html.parser"))

    # 5. Update Thumbnail List
    thumb_inner = soup.find(class_="product__thumbnail-list-inner")
    if thumb_inner and images:
        thumb_inner.clear()
        for idx, img_url in enumerate(images):
            t_cur = 'aria-current="true"' if idx == 0 else ''
            t_sel = 'is-nav-selected' if idx == 0 else ''
            t_html = f'<button type="button" tabindex="-1" class="product__thumbnail-item {t_sel}" {t_cur} data-media-id="{idx}" aria-controls="product-media-{idx}" data-action="select" style="cursor: pointer;"><div class="product__thumbnail" style="width: 60px; height: 60px; overflow: hidden; border-radius: 6px;"><img sizes="(max-width: 999px) 72px, 60px" height="1080" width="1080" alt="{title}" src="{img_url}" style="width: 100%; height: 100%; object-fit: cover;"></div></button>'
            thumb_inner.append(BeautifulSoup(t_html, "html.parser"))

    # 6. Update Swatches
    if swatches:
        swatch_list = soup.find(class_="variant-swatch-list")
        if swatch_list:
            swatch_list.clear()
            for idx, s in enumerate(swatches):
                s_name = s.get("title", f"Color {idx+1}")
                s_img = s.get("image", "")
                is_chk = 'checked="checked"' if idx == 0 else ''
                is_act = 'is-active' if idx == 0 else ''
                s_html = f'<div class="variant-swatch {is_act}" data-color="{s_name}" data-image="{s_img}"><input class="variant-swatch__radio visually-hidden" type="radio" name="option1" value="{s_name}" id="opt-color-{idx}" {is_chk}><label class="variant-swatch__item" for="opt-color-{idx}" title="{s_name}"><img class="variant-swatch__image" sizes="(max-width: 740px) 64px, 72px" height="1080" width="1080" alt="{s_name}" src="{s_img}"></label></div>'
                swatch_list.append(BeautifulSoup(s_html, "html.parser"))

            first_color = swatches[0].get("title", "")
            c_val = soup.find(class_="product-form__option-value")
            if c_val:
                c_val.string = first_color

    return str(soup)

