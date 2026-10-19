# BÁO CÁO DỰ ÁN CLONE & REBUILD — AZURE BOUTIQUE
> Trạng thái: **Hoàn thành xuất sắc toàn bộ Pipeline 6 Phase (Sẵn sàng nghiệm thu & duyệt)**
> Store nguồn: https://www.azureboutique.co/
> Store liên kết đích: `g1spma-ku.myshopify.com`
> Theme ID triển khai: `191338185071` (**Trạng thái: Unpublished - Không đè theme đang chạy**)
> Thời gian hoàn tất: 19/10/2026

---

## 1. THÔNG TIN TRUY CẬP THEME SAU KHI DEPLOY

- 🔗 **Link Xem thử trực tiếp (Theme Preview):**  
  [https://g1spma-ku.myshopify.com/?preview_theme_id=191338185071](https://g1spma-ku.myshopify.com/?preview_theme_id=191338185071)
- 🛠️ **Link Trình chỉnh sửa Theme Editor (Kéo - Thả):**  
  [https://admin.shopify.com/store/g1spma-ku/themes/191338185071/editor](https://admin.shopify.com/store/g1spma-ku/themes/191338185071/editor)
- 📦 **File nén cài đặt Theme (.ZIP):**  
  `f:\clone-theme\project-azureboutique\azureboutique-rebuild.zip`

---

## 2. KẾT QUẢ TRIỂN KHAI THEO TỪNG PHASE

### PHASE 0 — Trinh sát & Khởi tạo (Reconnaissance)
- **Tech Stack bóc tách được:**
  - Nền tảng: Shopify Online Store 2.0.
  - Theme gốc: `shrine-pro-1-7-0-updated` (ID: 187947974965).
  - App tích hợp: GemPages, Kaching Bundles, Klaviyo Reviews, Microsoft Clarity, Intelligems A/B testing.
- **Dữ liệu sitemap:**
  - 13 sản phẩm chính (Dầu Batana, Dầu gội/xả phục hồi, Serum dưỡng da đầu, Combo bundle).
  - 3 bộ sưu tập (`frontpage`, `batana`, `bundle-collection`).
  - 7 trang nội dung & 1 blog.
- **Scaffold Design Bridge:** Đã thiết lập sẵn sàng web app local tại `bridge/` (server cổng 4000, `overlay.js`, thư mục `queue/`).

### PHASE 1 — Cấu trúc & Design System (Clean-Room)
- **Design Tokens (`design/tokens.json`):**
  - Màu chủ đạo Primary: `#44624a` (xanh thảo mộc rừng rậm Honduras) kèm hover `#38523d`.
  - Màu nền phụ & container: `#f3f3f3` và `#e9ece9` (soft sage cream).
  - Màu chữ: `#121212` (chính) và `#555555` (phụ).
  - Màu khuyến mãi / urgency: `#dd1d1d`.
  - Bo góc: 6px (nút/badge), 12px (card sản phẩm/media), 24px (container lớn), 40px (pill).
- **Rà soát bản quyền Font (`_references/fonts/LICENSES.md`):**
  - Font gốc: `Poppins`.
  - Giấy phép: **SIL Open Font License 1.1 (OFL)** — Hoàn toàn hợp pháp cho mục đích thương mại.
  - Triển khai: Gọi chuẩn qua Google Fonts CDN kèm preconnect, không copy binary từ store đối thủ.
- **Component Inventory (`design/components.md`):**
  - Đặc tả chi tiết 12 thành phần cốt lõi từ Header, Hero, Card, PDP Box, So sánh, Timeline đến Footer.

### PHASE 2 — Dữ liệu & Content (Quarantine)
- **Crawl sản phẩm:** 13 sản phẩm trích xuất đầy đủ tiêu đề, mô tả, biến thể, giá bán, lưu vào `data/products.json` và file chuẩn `data/products.csv` (Shopify Import format).
- **Crawl bộ sưu tập:** `data/collections.json`.
- **Bóc tách logic Bundle:** Dựng cấu trúc `data/bundles.json` mô phỏng ưu đãi mua 1 chai / 2 chai (tặng hướng dẫn) / 3 chai (tặng lược & miễn phí vận chuyển).
- **Quarantine Asset (`_references/`):** Tải 7 ảnh mẫu vào `_references/images/` và lập bảng lưu xuất xứ + điều khoản tại `_references/MANIFEST.json`. Không đưa tài sản có bản quyền vào mã nguồn production.

### PHASE 3 — Rebuild Sạch (Clean-Room Liquid & CSS)
- Sao chép nền tảng OS 2.0 sạch từ `theme-original/` sang `project-azureboutique/theme/`.
- Áp toàn bộ Design Tokens vào `theme/assets/base.css`.
- **Tự tay dựng mới & tinh chỉnh các Section chuyển đổi cao (High-converting Sections):**
  1. `announcement-bar.liquid`: Thanh thông báo khuyến mãi xoay vòng, kèm mã giảm giá `AZURE65`.
  2. `header.liquid`: Menu điều hướng, logo tùy biến, icon tìm kiếm & giỏ hàng kèm badge số lượng.
  3. `hero-banner.liquid`: Banner mở đầu ấn tượng với tiêu đề `"transform your hair today."`, social proof 4.9⭐, nút CTA `"Try It Now"`.
  4. `social-proof-bar.liquid`: Khối số liệu 3 cột (`200k+ Happy Customers`, `850,000+ Bottles Shipped`, `58k+ 5-Star Reviews`).
  5. `featured-collection.liquid`: Lưới sản phẩm Batana với card hiển thị giá sale, rating, nút Add to Cart mượt mà.
  6. `routine-quiz-banner.liquid`: Banner khảo sát liệu trình cá nhân hóa (`TAKE OUR HAIR QUIZ`).
  7. `main-product.liquid`: Trang chi tiết sản phẩm đẳng cấp, tích hợp **Native Bundle Selector** (thay thế Kaching Bundles nặng nề bằng Liquid/JS thuần siêu nhẹ), dải huy hiệu niềm tin (Trust Badges).
  8. `product-comparison.liquid`: Bảng đối chiếu trực quan `"Ours Heals From Within"` vs `"Cheap oils leave your hair suffocated"`.
  9. `product-ingredients.liquid`: Lưới 4 thành phần vàng (Vitamin E, Omega 3-6-9, Vitamin A, Phytosterols).
  10. `product-timeline.liquid`: Lộ trình kết quả tuần 1-2, tuần 3-4, tuần 6-8.
  11. `product-faq.liquid`: Accordion giải đáp thắc mắc người mua.
  12. `cart-drawer.liquid`: Giỏ hàng trượt Ajax Drawer với thanh tiến trình Free Shipping thông minh.
  13. `footer.liquid`: Chân trang 4 cột chuyên nghiệp kèm cổng thanh toán uy tín.
- **Traceability:** Tất cả các section đều gắn cờ `data-src` để kết nối trực tiếp với công cụ Design Bridge.

### PHASE 4 — Kiểm thử & QA
- Chạy kiểm tra tự động `theme_qa_check.py` trên toàn bộ theme:
  - **Liquid files:** 22 file — 0 lỗi cú pháp, toàn bộ thẻ schema JSON hợp lệ.
  - **JSON templates & settings:** 12 file — 0 lỗi cấu trúc, tất cả tham chiếu section đều khớp 100%.
- Kiểm tra tính tương thích đa thiết bị: Desktop (1440px), Tablet (768px), Mobile (390px).

### PHASE 5 — Xuất xưởng & Deploy
- Đóng gói file cài đặt `azureboutique-rebuild.zip`.
- Triển khai thành công 36/36 assets lên store Shopify `g1spma-ku.myshopify.com` qua Admin API.
- Theme nằm an toàn ở trạng thái **Unpublished** (Theme ID: `191338185071`), bảo đảm không làm gián đoạn cửa hàng hiện tại.

---

## 3. CƠ CHẾ HIỆU CHỈNH PHASE 6 (DESIGN BRIDGE)

Khi ông chủ mở giao diện Theme trên trình duyệt local hoặc qua server Design Bridge:
1. Chạy server Design Bridge:
   ```powershell
   & "C:\Users\vdvie\AppData\Local\Python\bin\python.exe" "f:\clone-theme\project-azureboutique\bridge\server.py"
   ```
2. Mở `http://localhost:4000` và nhấn **Alt + I** để bật công cụ chọn phần tử.
3. Click vào bất kỳ phần tử nào (banner, nút bấm, bảng giá, font chữ), gõ yêu cầu bằng tiếng Việt (ví dụ: *"đổi màu nút này sang xanh đậm hơn"*, *"tăng cỡ chữ tiêu đề"*).
4. Hệ thống sẽ tự động tạo ticket trong `bridge/queue/`.
5. Khi ông chủ ra lệnh **"xử lý bridge queue"**, em sẽ đọc ticket và áp dụng sửa đổi chính xác vào file nguồn!
