import json
import os
import re
import html
import urllib.parse

COLLECTIONS_DIR = "f:/clone-theme/project-trybronoir/collections_data"
PREVIEW_HTML_PATH = "f:/clone-theme/project-trybronoir/bridge/preview.html"

TITLE_MAP = {
    "barefoot-shoes-bogo-volume": "Barefoot Shoes BOGO & Volume Discounts",
    "barefoot-shoes-for-summer": "Barefoot Shoes for Summer",
    "winter-collection": "Winter Collection",
    "socks-and-insoles": "Socks & Insoles",
    "barefoot-shoes-for-winter": "Barefoot Shoes for Winter"
}

SWATCH_SCRIPT = """
<script>
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.product-item-card').forEach(function(card) {
    var primaryImg = card.querySelector('.primary-img');
    var swatches = card.querySelectorAll('.swatch-dot');
    if (!primaryImg || !swatches.length) return;

    swatches.forEach(function(swatch) {
      swatch.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        var newImg = swatch.getAttribute('data-image');
        if (newImg) {
          primaryImg.src = newImg;
          swatches.forEach(function(s) { s.classList.remove('is-active'); });
          swatch.classList.add('is-active');
        }
      });
    });
  });
});
</script>
"""

def render_collection_page(handle):
    # Handle alias
    if handle == "barefoot-shoes-for-winter" and not os.path.exists(os.path.join(COLLECTIONS_DIR, f"{handle}.json")):
        handle_to_load = "winter-collection"
    else:
        handle_to_load = handle

    json_file = os.path.join(COLLECTIONS_DIR, f"{handle_to_load}.json")
    if not os.path.exists(json_file):
        json_file = os.path.join(COLLECTIONS_DIR, "barefoot-shoes-bogo-volume.json")

    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {"products": []}

    products = data.get("products", [])
    collection_title = TITLE_MAP.get(handle, handle.replace("-", " ").title())
    product_count = len(products)

    with open(PREVIEW_HTML_PATH, "r", encoding="utf-8", errors="ignore") as f:
        preview_text = f.read()

    h_end = preview_text.find("</header>") + len("</header>")
    f_start = preview_text.find("<footer")

    layout_head_header = preview_text[:h_end]
    layout_footer = preview_text[f_start:]

    cards_html = []
    COLOR_HEX_MAP = {
        "black": "#1e293b",
        "grey": "#64748b",
        "gray": "#64748b",
        "blue": "#2563eb",
        "beige": "#d4b996",
        "pink": "#f472b6",
        "light blue": "#38bdf8",
        "green": "#15803d",
        "brown": "#78350f",
        "white": "#ffffff",
        "red": "#dc2626",
        "khaki": "#a3a375"
    }

    for idx, p in enumerate(products):
        p_handle = p.get("handle") or "bronoir-skin-pro-with-copper-grounding-allround-barefoot-shoes"
        p_url = f"/products/{urllib.parse.quote(p_handle)}"
        p_title = p.get("title", "Barefoot Shoes").replace("\ufffd", "™").replace("â„¢", "™")
        
        images = p.get("images", [])
        img1 = images[0].get("src") if len(images) > 0 else "https://trybronoir.com/cdn/shop/files/DeinAbschnittstext_11_1080x.png?v=1761602494"
        img2 = images[1].get("src") if len(images) > 1 else img1

        variants = p.get("variants", [])
        raw_price = variants[0].get("price", "74.90") if variants else "74.90"
        raw_compare = variants[0].get("compare_at_price", "129.90") if variants else "129.90"

        try:
            val_p = float(raw_price)
            if raw_compare and float(raw_compare) > val_p:
                val_c = float(raw_compare)
            else:
                val_c = val_p * 1.5
            diff = val_c - val_p
            badge_text = f"SAVE ${diff:.2f}" if diff > 0 else "SALE"
            price_display = f"${val_p:.2f}"
            compare_display = f"${val_c:.2f}"
        except Exception:
            badge_text = "SAVE $55.00"
            price_display = "$74.90"
            compare_display = "$129.90"

        # Extract authentic color swatches
        swatches_html = []
        color_map = {}
        for v in variants:
            c_name = v.get("option1") or ""
            f_img = v.get("featured_image", {}).get("src") if v.get("featured_image") else None
            if c_name and f_img and c_name not in color_map:
                color_map[c_name] = f_img

        if color_map:
            for c_idx, (c_name, c_img) in enumerate(list(color_map.items())[:6]):
                hex_col = "#64748b"
                for k, hx in COLOR_HEX_MAP.items():
                    if k in c_name.lower():
                        hex_col = hx
                        break
                is_act = "is-active" if c_idx == 0 else ""
                b_border = "border: 1px solid #cbd5e1;" if hex_col == "#ffffff" else ""
                swatches_html.append(
                    f'<span class="swatch-dot {is_act}" title="{html.escape(c_name)}" style="background-color: {hex_col}; {b_border}" data-image="{c_img}"></span>'
                )
        else:
            default_colors = ["#1e293b", "#ffffff", "#ec4899", "#94a3b8", "#0369a1"]
            for c_idx, im in enumerate(images[:5]):
                c_img = im.get("src", "")
                c_color = default_colors[c_idx % len(default_colors)]
                is_act = "is-active" if c_idx == 0 else ""
                b_border = "border: 1px solid #cbd5e1;" if c_color == "#ffffff" else ""
                swatches_html.append(
                    f'<span class="swatch-dot {is_act}" style="background-color: {c_color}; {b_border}" data-image="{c_img}"></span>'
                )

        card = f"""
        <div class="product-item-card" data-index="{idx}">
          <span class="product-save-badge">{badge_text}</span>
          <div class="product-card-media">
            <a href="{p_url}" class="product-media-link">
              <img class="product-img primary-img" src="{img1}" alt="{html.escape(p_title)}" loading="lazy">
              <img class="product-img secondary-img" src="{img2}" alt="{html.escape(p_title)}" loading="lazy">
            </a>
            <div class="quick-view-wrap">
              <button type="button" class="quick-view-btn" onclick="window.location.href='{p_url}'">
                Quick view
              </button>
            </div>
          </div>
          <div class="product-card-body">
            <div class="product-rating">
              <span class="stars">★★★★★</span>
              <span class="rating-num">(4.9)</span>
            </div>
            <h4 class="product-title">
              <a href="{p_url}">{html.escape(p_title)}</a>
            </h4>
            <div class="product-prices">
              <span class="price-sale">{price_display}</span>
              <span class="price-compare">{compare_display}</span>
            </div>
            <div class="product-swatches" aria-label="Color Swatches">
              {''.join(swatches_html)}
            </div>
            <a href="{p_url}" class="select-options-btn" style="display: flex; align-items: center; justify-content: center; gap: 8px; margin-top: 14px; width: 100%; height: 44px; background: #08435e; color: #ffffff; font-weight: 700; font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em; border-radius: 6px; text-decoration: none; transition: background 0.2s ease;">
              SELECT OPTIONS & SAVE ➔
            </a>
          </div>
        </div>
        """
        cards_html.append(card)

    collection_content = f"""
    <!-- Collection Main Content -->
    <div class="collection-page-wrapper" style="min-height: 80vh; background: #ffffff;">
      <div class="collection-hero" style="background: linear-gradient(180deg, #f1f8fa 0%, #ffffff 100%); padding: 50px 24px 36px; text-align: center; border-bottom: 1px solid #e2e8f0;">
        <div style="max-width: 1200px; margin: 0 auto;">
          <div style="font-size: 13px; color: #64748b; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600;">
            <a href="/preview" style="color: #64748b; text-decoration: none;">Home</a> <span style="margin: 0 6px;">/</span> <span style="color: #08435e;">Collections</span> <span style="margin: 0 6px;">/</span> <span style="color: #08435e; font-weight: 700;">{html.escape(collection_title)}</span>
          </div>
          <h1 style="font-size: 36px; font-weight: 900; color: #08435e; letter-spacing: -0.02em; margin-bottom: 10px;">{html.escape(collection_title)}</h1>
          <p style="font-size: 16px; color: #475569; max-width: 600px; margin: 0 auto;">Explore our authentic Bronoir collection designed for maximum comfort, grounding, and barefoot freedom.</p>
        </div>
      </div>

      <div class="collection-main" style="max-width: 1320px; margin: 36px auto 60px; padding: 0 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 28px; padding-bottom: 16px; border-bottom: 1px solid #f1f5f9;">
          <span style="font-size: 15px; color: #475569; font-weight: 600;">Showing {product_count} products</span>
          <div style="display: flex; gap: 10px; align-items: center;">
            <span style="font-size: 14px; color: #64748b; font-weight: 500;">Sort:</span>
            <select style="padding: 7px 14px; border-radius: 6px; border: 1px solid #cbd5e1; font-size: 14px; background: #fff; color: #1e293b; font-weight: 500; outline: none; cursor: pointer;">
              <option>Featured</option>
              <option>Best Selling</option>
              <option>Price: Low to High</option>
              <option>Price: High to Low</option>
            </select>
          </div>
        </div>

        <div class="product-list-grid" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px;">
          {''.join(cards_html)}
        </div>
      </div>
    </div>
    {SWATCH_SCRIPT}
    """

    return layout_head_header + collection_content + layout_footer
