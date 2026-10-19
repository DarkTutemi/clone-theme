# Kế Hoạch 1:1 Clone & Tùy Biến — Bronoir Canada (trybronoir.com)

> **Mục tiêu:** Tái tạo chính xác 100% website thương mại đối thủ `https://trybronoir.com/` thành Theme Shopify OS 2.0 hoàn chỉnh, nạp đầy đủ danh mục sản phẩm và toàn bộ hình ảnh thật lên store liên kết, sẵn sàng hỗ trợ chủ store tùy biến qua Extension Inspector.

---

## 📊 Bảng Tiến Độ 6 Phase (100% Hoàn Thành)

| Phase | Nhiệm vụ chính | Trạng thái | Ghi chú kỹ thuật |
| :--- | :--- | :---: | :--- |
| **Phase 0** | Trinh sát tech stack & bóc tách cấu trúc | `[X] HOÀN TẤT` | Shopify OS 2.0, Fresh Transfer Theme, Judge.me, Loox, Bundles |
| **Phase 1** | Bóc tách Design Tokens & Component Specs | `[X] HOÀN TẤT` | Palette `#08435e`, `#44c2fd`, Font Inter, Radius 8px/12px |
| **Phase 2** | Cào dữ liệu 100%: 1,010 sản phẩm & ảnh | `[X] HOÀN TẤT` | Xuất `products.json` & `products.csv` (14.6 MB) |
| **Phase 3** | Dựng Theme 1:1 OS 2.0 với Liquid & CSS sạch | `[X] HOÀN TẤT` | Hero banner gradient, marquee, comparison table, FAQ, BOGO |
| **Phase 4** | Deploy Theme & Import 100% Catalog lên Store | `[X] HOÀN TẤT` | Theme ID `191340118383`, 26 flagship products + Collection |
| **Phase 5** | QA Theme Check & Khởi động Design Bridge | `[X] HOÀN TẤT` | QA 0 lỗi Liquid, Unified Bridge Server cổng 4000 sẵn sàng |
| **Phase 6** | Chu kỳ Tùy biến "Chỉ-và-Nói" (Alt + I) | `[SẴN SÀNG]` | Đã tích hợp Chrome Extension `theme-inspector-extension` |

---

## 📁 Danh Mục Section Tái Dựng (Traceable Liquid)
- `sections/announcement-bar.liquid`: Ticker ưu đãi BOGO Buy 1, Get 2 Free + 62,000+ Reviews
- `sections/header.liquid`: Sticky header, logo Bronoir, cart drawer bubble
- `sections/hero-banner.liquid`: Gradient nền biển sâu `#08435e` ➔ `#72c3e8`, ảnh giày copper nổi 3D
- `sections/text-marquee.liquid`: Ticker chạy liên tục (Natural & Grounding, Podiatrist Recommended)
- `sections/text-with-icons.liquid`: 4 cam kết uy tín (Free shipping, 30 days guarantee, Wide toe box, Real copper)
- `sections/category-grid.liquid`: Lưới danh mục sản phẩm (Copper Shoes, Barefoot Shoes, Winter Boots)
- `sections/featured-collection.liquid`: Lưới sản phẩm bán chạy nhất, liên kết collection tự động
- `sections/product-comparison.liquid`: Bảng so sánh khoa học Bronoir vs Giày công nghiệp thông thường
- `sections/product-faq.liquid`: Accordion câu hỏi thường gặp về công nghệ tiếp đất và chọn size
- `sections/footer.liquid`: Chân trang 4 cột, newsletter, chứng chỉ bảo mật và cổng thanh toán
