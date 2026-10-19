# KẾ HOẠCH CLONE & REBUILD — AZURE BOUTIQUE
> Target: https://www.azureboutique.co/
> Slug: `azureboutique` | Output: `f:/clone-theme/project-azureboutique/`
> Connected Store: `g1spma-ku.myshopify.com` (Unpublished Theme)
> Quy chuẩn: Clean-Room OS 2.0 Rebuild (Không copy tài sản có bản quyền/mã mã hoá lên production)

---

## TIẾN ĐỘ TỔNG THỂ

- [x] **PHASE 0: Trinh sát & Khởi tạo**
  - [x] Chuẩn hoá slug & scaffold cây thư mục `project-azureboutique/`
  - [x] Tải & phân loại `robots.txt`, `sitemap.xml` (13 products, 3 collections, 7 pages, 1 blog)
  - [x] Phân tích tech stack: Shopify OS 2.0, Shrine Pro v1.7.0, GemPages, Klaviyo, Kaching Bundles, Microsoft Clarity
  - [x] Bóc tách cấu trúc DOM & section inventory (Home, PDP, Collection)
  - [x] Khởi tạo Design Bridge (`bridge/server.py`, `bridge/overlay.js`, `bridge/queue/`)
  - [x] Thiết lập `CLONE_PLAN.md` & `REPORT.md`

- [x] **PHASE 1: Cấu trúc & Design System (Clean-Room)**
  - [x] Bóc tách Design Tokens (`design/tokens.json`): HSL palette, Typography scale, Radius, Spacing, Shadows
  - [x] Kiểm tra bản quyền Font & ghi `_references/fonts/LICENSES.md` (Poppins - Google Fonts OFL 100% hợp pháp)
  - [x] Lập Component Inventory (`design/components.md`) chi tiết các block trên Home, PDP, Collection
  - [x] Lưu wireframe cấu trúc layout

- [x] **PHASE 2: Dữ liệu & Content (Quarantine)**
  - [x] Crawl danh mục sản phẩm -> `data/products.json` & `data/products.csv` (Shopify Import format)
  - [x] Crawl bộ sưu tập -> `data/collections.json`
  - [x] Bóc tách cấu trúc bundle & ưu đãi -> `data/bundles.json` (Kaching bundle pricing tiers)
  - [x] Thu thập dữ liệu FAQ & cam kết thương hiệu -> `data/brand_content.json`
  - [x] Tải ảnh mẫu làm placeholder vào `_references/images/` + cập nhật `_references/MANIFEST.json` (7 assets)

- [x] **PHASE 3: Rebuild Sạch (Clean-Room Liquid & CSS)**
  - [x] Khởi tạo bản dựng từ theme gốc chuẩn `theme-original/` sang `project-azureboutique/theme/`
  - [x] Nạp Design Tokens chuẩn vào `theme/assets/base.css` (CSS variables, màu sắc `#44624a`, font Poppins, radius)
  - [x] Dựng lại các Section cốt lõi chuẩn OS 2.0:
    - [x] `announcement-bar.liquid`: ticker thông báo khuyến mãi / voucher
    - [x] `header.liquid`: logo tùy biến, navigation, search icon, drawer menu
    - [x] `hero-banner.liquid`: banner chính ấn tượng kèm CTA button
    - [x] `featured-collection.liquid`: lưới sản phẩm chuẩn e-commerce kèm badge
    - [x] `main-product.liquid`: trang chi tiết sản phẩm cao cấp (gallery, price, bundle quantity break, guarantee badges)
    - [x] `product-comparison.liquid`: so sánh "Ours Heals From Within" vs "Cheap oils"
    - [x] `product-ingredients.liquid`: thành phần dưỡng chất & công dụng
    - [x] `product-timeline.liquid`: lộ trình kết quả theo tuần (Results over time)
    - [x] `product-faq.liquid`: accordion hỏi đáp khách hàng
    - [x] `cart-drawer.liquid`: giỏ hàng trượt mượt mà (Ajax cart) kèm thanh Free Shipping progress
    - [x] `footer.liquid`: footer đa cột, đăng ký newsletter, chính sách
  - [x] Tích hợp `data-src` & `data-block` cho chế độ Design Bridge ("chỉ-và-nói")

- [x] **PHASE 4: Kiểm thử & QA**
  - [x] Kiểm tra cú pháp Liquid & Theme Check (22 file Liquid, 12 file JSON, 0 lỗi)
  - [x] Kiểm tra hiển thị responsive (Desktop 1440px, Tablet 768px, Mobile 390px)
  - [x] Tối ưu hóa hiệu năng (defer scripts, lazyload images, preconnect Google Fonts)
  - [x] Kiểm tra SEO (semantic HTML, OpenGraph, Product meta)

- [x] **PHASE 5: Xuất xưởng & Deploy**
  - [x] Đóng gói theme thành file ZIP `project-azureboutique/azureboutique-rebuild.zip`
  - [x] Đẩy theme lên store liên kết (`g1spma-ku.myshopify.com`) ở chế độ **unpublished** (Theme ID: 191338185071)
  - [x] Lấy link Theme Preview & Theme Editor gửi ông chủ duyệt
  - [x] Kích hoạt Design Bridge sẵn sàng cho chu kỳ hiệu chỉnh Phase 6
