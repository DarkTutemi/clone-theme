# Component Architecture & Design Specifications — Bronoir Canada

## 1. Design Tokens
- **Primary Color:** `#08435e` (Deep Ocean Navy)
- **Primary Dark:** `#052d3f`
- **Accent Highlight:** `#44c2fd` (Electric Ice Cyan)
- **Accent Glow:** `#72c3e8`
- **Hero Gradient:** `linear-gradient(116.53deg, #08435e 12.4%, #72c3e8 93.6%)`
- **Sale & Urgency Badge:** `#e11d48` (Vibrant Coral Red)
- **Backgrounds:** `#ffffff` (Cards), `#f8fafc` (Muted section bg), `#0f172a` (Dark footer)
- **Typography:** Modern clean sans-serif (`Inter`, `system-ui`), weights 400, 500, 600, 700, 800
- **Border Radius:** `8px` (buttons), `12px` (product & feature cards), `9999px` (pill badges)

---

## 2. Page Structure & Components Breakdown

### 1. Announcement Bar (`sections/announcement-bar.liquid`)
- Ticker banner with high-converting urgency:
  - `TODAY’S SPECIAL OFFER — BUY 1, GET 2 FREE | LIMITED OFFER ENDING SOON | ★★★★★ 62.000+ HAPPY CUSTOMERS`
- Dark ocean background with electric cyan typography and animated sliding transition.

### 2. Header & Sticky Navigation (`sections/header.liquid`)
- Left: Logo "BRONOIR" with clean modern typography.
- Center: Quick navigation links (Copper Shoes, Barefoot Shoes, Winter Boots, Reviews, FAQ).
- Right: Search, Currency switcher (VND / CAD / USD), Cart drawer icon with live bubble badge count.

### 3. Hero Slideshow & Main Banner (`sections/hero-banner.liquid`)
- Majestic gradient hero with dynamic barefoot illustration.
- Headline: "Skin Pro Barefoot with Copper — Grounding & All-Day Comfort"
- Subheading: "Podiatrist Recommended • Zero Drop • Wide Toe Box • Buy 1, Get 2 Free!"
- Primary CTA: "CLAIM BOGO OFFER NOW" (White pill button with cyan hover effect).

### 4. Text Marquee Ticker (`sections/text-marquee.liquid`)
- Smooth infinite scrolling text banner:
  - `🌿 Natural & Grounding • 🦶 Podiatrist Recommended • ⚡ Zero-Drop Sole • 🛡️ 30-Day Risk-Free Guarantee`

### 5. Category Grid Cards (`sections/category-grid.liquid`)
- Visual image cards highlighting key collections:
  - Copper Shoes
  - Barefoot Shoes
  - Winter Boots
  - Socks & Insoles

### 6. Value Props / Text with Icons (`sections/text-with-icons.liquid`)
- 4 key reassurance pillars:
  - 🚚 Free Worldwide Express Shipping
  - 🔄 30-Day Money-Back Guarantee
  - 🦶 Ergonomic Zero-Drop Sole Design
  - ⚡ Real Copper Grounding Technology

### 7. Featured Bestsellers Collection (`sections/featured-collection.liquid`)
- Responsive grid showcasing top products:
  - `Bronoir® Skin Pro Barefoot with Copper | Buy 1, Get 2 Free!`
  - `Bronoir® Toasty - Winter Barefoot Shoes`
  - `Bronoir® Arctic 2.0 - Winter Barefoot Shoes`
  - `Bronoir® Trail Masters - Barefoot Shoes`
- Product cards with multi-angle image flip on hover, star rating, strike-through compare price, and instant "Add to Cart / Select Options" CTA.

### 8. Before & After / Comparison Table (`sections/product-comparison.liquid`)
- Visual demonstration of standard narrow toe box vs. Bronoir anatomical barefoot toe box.
- Interactive side-by-side or comparison matrix.

### 9. Product Main & Native Bundle Selector (`sections/main-product.liquid`)
- 1:1 replica of the high-converting Bronoir BOGO / Tiered bundle box:
  - Tier 1: Buy 1 Pair ($49.95)
  - Tier 2: Buy 1, Get 2 Free! (Most Popular - $69.95 Total)
  - Tier 3: Buy 2, Get 4 Free! (Best Value - $99.95 Total)
- Native Liquid & vanilla JavaScript (0% external app dependencies, 100% speed).

### 10. FAQ Accordions (`sections/product-faq.liquid`)
- Accordion component addressing sizing, grounding copper tech, shipping, and returns.

### 11. Slide-out Mini Cart Drawer (`snippets/cart-drawer.liquid`)
- Ajax slide-in cart drawer with free shipping progress threshold bar, upsell item, and accelerated checkout.

### 12. Footer (`sections/footer.liquid`)
- 4-column layout with brand story, customer care, newsletter subscription, and trust checkout badges.
