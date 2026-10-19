"""
Shopify Theme Builder & Section Deconstruct Engine
Converts scraped HTML, CSS, and JS into a fully functional Shopify Online Store 2.0 theme.
"""
import os
import re
import json
import zipfile
import logging
from bs4 import BeautifulSoup
from .theme_ripper import ThemeRipper

logger = logging.getLogger("theme_builder")

SETTINGS_SCHEMA_TEMPLATE = [
    {
        "name": "theme_info",
        "theme_name": "Cloned OS2 Theme",
        "theme_version": "1.0.0",
        "theme_author": "Antigravity Theme Engine",
        "theme_documentation_url": "https://shopify.dev",
        "theme_support_url": "https://shopify.dev"
    },
    {
        "name": "Colors",
        "settings": [
            {
                "type": "color",
                "id": "color_primary",
                "label": "Primary Accent Color",
                "default": "#111111"
            },
            {
                "type": "color",
                "id": "color_bg",
                "label": "Background Color",
                "default": "#ffffff"
            }
        ]
    },
    {
        "name": "Typography",
        "settings": [
            {
                "type": "font_picker",
                "id": "font_body",
                "label": "Body Font",
                "default": "assistant_n4"
            }
        ]
    }
]

SETTINGS_DATA_TEMPLATE = {
    "current": {
        "color_primary": "#111111",
        "color_bg": "#ffffff"
    }
}

LOCALES_EN_TEMPLATE = {
    "general": {
        "share": "Share",
        "close": "Close",
        "search": "Search our store"
    },
    "products": {
        "product": {
            "add_to_cart": "Add to cart",
            "sold_out": "Sold out",
            "unavailable": "Unavailable",
            "quantity": "Quantity"
        }
    },
    "cart": {
        "general": {
            "title": "Your cart",
            "checkout": "Check out",
            "empty": "Your cart is currently empty."
        }
    }
}

LAYOUT_THEME_TEMPLATE = """<!doctype html>
<html class="no-js" lang="{{ request.locale.iso_code }}">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="canonical" href="{{ canonical_url }}">
  <link rel="preconnect" href="https://cdn.shopify.com" crossorigin>

  <title>
    {{ page_title }}
    {%- if current_tags %} &ndash; tagged "{{ current_tags | join: ', ' }}"{%- endif -%}
    {%- if current_page != 1 %} &ndash; Page {{ current_page }}{%- endif -%}
    {%- unless page_title contains shop.name %} &ndash; {{ shop.name }}{%- endunless -%}
  </title>

  {% if page_description %}
    <meta name="description" content="{{ page_description | escape }}">
  {% endif %}

  <!-- Cloned Theme CSS Assets -->
{{CLONED_CSS_ASSETS}}

  {{ content_for_header }}
</head>

<body class="gradient template-{{ template.name }}">
{{CLONED_HEADER_SECTIONS}}

  <main id="MainContent" class="content-for-layout focus-none" role="main" tabindex="-1">
    {{ content_for_layout }}
  </main>

{{CLONED_FOOTER_SECTIONS}}

  <!-- Cloned Theme JS Assets -->
{{CLONED_JS_ASSETS}}
</body>
</html>
"""

class ShopifyThemeBuilder:
    def __init__(self, target_url: str, output_theme_dir: str):
        self.target_url = target_url
        self.output_dir = output_theme_dir
        self.ripper = ThemeRipper(target_url, output_theme_dir)

        # Standard Shopify folder structure
        self.dirs = {
            "assets": os.path.join(output_theme_dir, "assets"),
            "config": os.path.join(output_theme_dir, "config"),
            "layout": os.path.join(output_theme_dir, "layout"),
            "locales": os.path.join(output_theme_dir, "locales"),
            "sections": os.path.join(output_theme_dir, "sections"),
            "snippets": os.path.join(output_theme_dir, "snippets"),
            "templates": os.path.join(output_theme_dir, "templates"),
        }
        for d in self.dirs.values():
            os.makedirs(d, exist_ok=True)

    def build_theme(self) -> dict:
        """Executes full theme cloning and reconstruction workflow."""
        report = {
            "target_url": self.target_url,
            "output_dir": self.output_dir,
            "sections_extracted": [],
            "assets_downloaded": {},
            "status": "success",
        }

        # 1. Fetch Homepage
        html = self.ripper.fetch_page_html("/")
        if not html:
            report["status"] = "error"
            report["error"] = "Failed to fetch homepage HTML"
            return report

        soup = BeautifulSoup(html, "html.parser")

        # 2. Rip assets (CSS, JS, Fonts, Images)
        asset_map = self.ripper.rip_assets(soup)
        report["assets_downloaded"] = {k: len(v) for k, v in asset_map.items()}

        # 3. Extract & generate sections
        sections = self._extract_sections(soup, asset_map)
        report["sections_extracted"] = [s["name"] for s in sections]

        # 4. Generate layout/theme.liquid
        self._generate_layout(soup, asset_map, sections)

        # 5. Generate templates/index.json (Shopify 2.0 JSON template)
        self._generate_index_json(sections)

        # 6. Generate fallback templates
        self._generate_standard_templates()

        # 7. Generate config and locales
        self._generate_config_and_locales()

        return report

    def _extract_sections(self, soup: BeautifulSoup, asset_map: dict) -> list:
        sections = []
        found_elements = []

        # Find header
        header_el = soup.find("header") or soup.find(id=re.compile(r"header", re.I)) or soup.find(class_=re.compile(r"shopify-section-header|site-header", re.I))
        if header_el:
            found_elements.append(("header", header_el, "Header"))

        # Find announcement bar
        announce_el = soup.find(class_=re.compile(r"announcement", re.I))
        if announce_el and announce_el != header_el:
            found_elements.append(("announcement-bar", announce_el, "Announcement Bar"))

        # Find main sections
        raw_sections = soup.find_all(class_=re.compile(r"shopify-section"))
        if not raw_sections:
            raw_sections = soup.find_all("section")

        sec_idx = 1
        for sec in raw_sections:
            if sec == header_el or (header_el and header_el in sec.parents):
                continue
            if "footer" in sec.get("class", []) or sec.find("footer"):
                continue

            sec_id = sec.get("id", "")
            clean_name = re.sub(r"^(shopify-section-|template--[0-9]+__|sections--[0-9]+__)", "", sec_id)
            if not clean_name or clean_name.isdigit():
                clean_name = f"custom-section-{sec_idx}"
                sec_idx += 1
            clean_name = re.sub(r"[^a-zA-Z0-9_-]", "-", clean_name).strip("-").lower()
            
            title = clean_name.replace("-", " ").replace("_", " ").title()
            found_elements.append((clean_name, sec, title))

        # Find footer
        footer_el = soup.find("footer") or soup.find(id=re.compile(r"footer", re.I)) or soup.find(class_=re.compile(r"shopify-section-footer|site-footer", re.I))
        if footer_el:
            found_elements.append(("footer", footer_el, "Footer"))

        # Process each section into a .liquid file
        for name, el, title in found_elements:
            liquid_path = os.path.join(self.dirs["sections"], f"{name}.liquid")
            
            # Rewrite asset URLs inside section HTML
            inner_html = str(el)
            for item in asset_map.get("images", []):
                inner_html = inner_html.replace(item["orig"], f"{{{{ '{item['local']}' | asset_url }}}}")

            schema_obj = {
                "name": title,
                "tag": "section",
                "class": f"section-{name}",
                "settings": [
                    {
                        "type": "text",
                        "id": "heading",
                        "label": "Section Heading",
                        "default": title
                    }
                ],
                "presets": [
                    {
                        "name": title
                    }
                ]
            }

            section_content = (
                f"{{% comment %}}\n"
                f"  Cloned Section: {title}\n"
                f"  Generated by Antigravity Theme Engine\n"
                f"{{% endcomment %}}\n\n"
                f'<div id="{name}-section" class="cloned-section cloned-{name}">\n'
                f"  {inner_html}\n"
                f"</div>\n\n"
                f"{{% schema %}}\n"
                f"{json.dumps(schema_obj, indent=2)}\n"
                f"{{% endschema %}}\n"
            )

            with open(liquid_path, "w", encoding="utf-8") as f:
                f.write(section_content)

            sections.append({"name": name, "title": title})

        return sections

    def _generate_layout(self, soup: BeautifulSoup, asset_map: dict, sections: list):
        """Generates layout/theme.liquid linking local cloned assets and rendering layout."""
        css_tags = []
        for c in asset_map.get("css", []):
            css_tags.append(f"  {{{{ '{c['local']}' | asset_url | stylesheet_tag }}}}")
            
        js_tags = []
        for j in asset_map.get("js", []):
            js_tags.append(f"  {{{{ '{j['local']}' | asset_url | script_tag }}}}")

        header_tags = []
        if any(s["name"] == "announcement-bar" for s in sections):
            header_tags.append("  {% section 'announcement-bar' %}")
        if any(s["name"] == "header" for s in sections):
            header_tags.append("  {% section 'header' %}")

        footer_tags = []
        if any(s["name"] == "footer" for s in sections):
            footer_tags.append("  {% section 'footer' %}")

        theme_liquid = LAYOUT_THEME_TEMPLATE
        theme_liquid = theme_liquid.replace("{{CLONED_CSS_ASSETS}}", "\n".join(css_tags))
        theme_liquid = theme_liquid.replace("{{CLONED_JS_ASSETS}}", "\n".join(js_tags))
        theme_liquid = theme_liquid.replace("{{CLONED_HEADER_SECTIONS}}", "\n".join(header_tags))
        theme_liquid = theme_liquid.replace("{{CLONED_FOOTER_SECTIONS}}", "\n".join(footer_tags))

        with open(os.path.join(self.dirs["layout"], "theme.liquid"), "w", encoding="utf-8") as f:
            f.write(theme_liquid)

    def _generate_index_json(self, sections: list):
        """Generates Shopify 2.0 templates/index.json registering all extracted homepage sections."""
        body_sections = [s for s in sections if s["name"] not in ["header", "footer", "announcement-bar"]]
        
        index_data = {
            "sections": {},
            "order": []
        }
        for s in body_sections:
            key = f"{s['name']}_cloned"
            index_data["sections"][key] = {
                "type": s["name"],
                "settings": {}
            }
            index_data["order"].append(key)

        with open(os.path.join(self.dirs["templates"], "index.json"), "w", encoding="utf-8") as f:
            json.dump(index_data, f, indent=2)

    def _generate_standard_templates(self):
        """Generates product, collection, cart, and 404 templates."""
        product_liquid = """<div class="product-page-container page-width">
  <div class="product-grid">
    <div class="product-media">
      {% if product.featured_image %}
        <img src="{{ product.featured_image | image_url: width: 800 }}" alt="{{ product.title }}" loading="lazy">
      {% endif %}
    </div>
    <div class="product-info">
      <h1>{{ product.title }}</h1>
      <div class="product-price">{{ product.price | money }}</div>
      <div class="product-description">{{ product.description }}</div>
      
      {% form 'product', product %}
        <input type="hidden" name="id" value="{{ product.selected_or_first_available_variant.id }}">
        <button type="submit" class="button button--primary" {% unless product.available %}disabled{% endunless %}>
          {% if product.available %}Add to Cart{% else %}Sold Out{% endif %}
        </button>
      {% endform %}
    </div>
  </div>
</div>
"""
        with open(os.path.join(self.dirs["templates"], "product.liquid"), "w", encoding="utf-8") as f:
            f.write(product_liquid)

        collection_liquid = """<div class="collection-page-container page-width">
  <h1>{{ collection.title }}</h1>
  {% if collection.description != blank %}
    <div class="collection-desc">{{ collection.description }}</div>
  {% endif %}
  <div class="products-grid">
    {% for product in collection.products %}
      <div class="product-card">
        <a href="{{ product.url }}">
          {% if product.featured_image %}
            <img src="{{ product.featured_image | image_url: width: 400 }}" alt="{{ product.title }}" loading="lazy">
          {% endif %}
          <h3>{{ product.title }}</h3>
          <p>{{ product.price | money }}</p>
        </a>
      </div>
    {% endfor %}
  </div>
</div>
"""
        with open(os.path.join(self.dirs["templates"], "collection.liquid"), "w", encoding="utf-8") as f:
            f.write(collection_liquid)

        cart_liquid = """<div class="cart-container page-width">
  <h1>{{ 'cart.general.title' | t }}</h1>
  {% if cart.item_count > 0 %}
    <form action="{{ routes.cart_url }}" method="post">
      {% for item in cart.items %}
        <div class="cart-item">
          <h3>{{ item.product.title }}</h3>
          <p>{{ item.price | money }} x {{ item.quantity }}</p>
        </div>
      {% endfor %}
      <p>Total: {{ cart.total_price | money }}</p>
      <button type="submit" name="checkout" class="button button--primary">{{ 'cart.general.checkout' | t }}</button>
    </form>
  {% else %}
    <p>{{ 'cart.general.empty' | t }}</p>
  {% endif %}
</div>
"""
        with open(os.path.join(self.dirs["templates"], "cart.liquid"), "w", encoding="utf-8") as f:
            f.write(cart_liquid)

    def _generate_config_and_locales(self):
        """Generates settings_schema.json, settings_data.json and en.default.json."""
        with open(os.path.join(self.dirs["config"], "settings_schema.json"), "w", encoding="utf-8") as f:
            json.dump(SETTINGS_SCHEMA_TEMPLATE, f, indent=2)

        with open(os.path.join(self.dirs["config"], "settings_data.json"), "w", encoding="utf-8") as f:
            json.dump(SETTINGS_DATA_TEMPLATE, f, indent=2)

        with open(os.path.join(self.dirs["locales"], "en.default.json"), "w", encoding="utf-8") as f:
            json.dump(LOCALES_EN_TEMPLATE, f, indent=2)

    def create_theme_zip(self, zip_output_path: str = None) -> str:
        """Packages the cloned theme directory into a Shopify-ready installable .zip archive."""
        if not zip_output_path:
            zip_output_path = f"{self.output_dir.rstrip('/\\\\')}.zip"

        with zipfile.ZipFile(zip_output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(self.output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.output_dir)
                    zipf.write(file_path, rel_path)

        logger.info(f"Theme packaged successfully into {zip_output_path}")
        return zip_output_path
