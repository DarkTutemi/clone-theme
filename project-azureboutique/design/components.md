# COMPONENT INVENTORY — AZURE BOUTIQUE REBUILD
> Clean-Room OS 2.0 Component Specification

---

## 1. GLOBAL COMPONENTS (Header, Footer, Navigation, Drawer)

### 1.1 Announcement Bar (`announcement-bar.liquid`)
- **Vị trí:** Trên cùng (Top-level header group).
- **Màu nền:** Đỏ đậm khuyến mãi (`#dd1d1d`) hoặc xanh lá thương hiệu (`#44624a`), chữ trắng.
- **Tính năng:** Ticker xoay vòng các thông điệp khuyến mãi (`✨ UP TO 65% OFF WITH FREE GIFTS`, mã giảm giá, miễn phí vận chuyển).
- **Schema:** Cho phép thêm/sửa/xóa thông điệp qua Block trong Theme Editor, cài đặt tốc độ trượt autoplay.

### 1.2 Header Navigation (`header.liquid`)
- **Vị trí:** Sticky header khi cuộn trang.
- **Cấu trúc:**
  - Trái: Nút mở Menu Drawer (Mobile/Tablet) + Logo thương hiệu (svg/image tùy biến).
  - Giữa: Menu liên kết chính (Shop, Hair Quiz, Our Story, FAQ).
  - Phải: Biểu tượng tìm kiếm + Biểu tượng giỏ hàng kèm badge số lượng sản phẩm.
- **Chi tiết UX:** Hiệu ứng hover đổi màu sang xanh primary `#44624a`, gạch chân tinh tế.

### 1.3 Ajax Cart Drawer (`cart-drawer.liquid`)
- **Vị trí:** Slide-in từ cạnh phải khi thêm vào giỏ hàng hoặc bấm icon Cart.
- **Tính năng:**
  - Cập nhật số lượng (+ / -) bằng Ajax không cần tải lại trang.
  - Thanh tiến trình nhận quà miễn phí / Free Shipping Bar (ví dụ: "Mua thêm $15 để nhận Free Shipping").
  - Nút thanh toán nhanh Checkout & liên kết trực tiếp tới giỏ hàng đầy đủ.

### 1.4 Footer (`footer.liquid`)
- **Vị trí:** Cuối trang (Footer group).
- **Cấu trúc 4 cột:**
  1. Về thương hiệu & sứ mệnh chăm sóc tóc tự nhiên từ Honduras Batana.
  2. Quick Links: All Products, Hair Quiz, Ambassador, Track Order.
  3. Customer Care: Contact Us, Shipping & Returns, Terms of Service, Privacy Policy.
  4. Đăng ký nhận tin (Newsletter signup) với cam kết bảo mật thông tin.
- **Đáy footer:** Bản quyền, biểu tượng cổng thanh toán an toàn (Visa, Mastercard, Amex, PayPal, Apple Pay).

---

## 2. HOME PAGE SECTIONS

### 2.1 Hero Banner (`hero-banner.liquid`)
- **Cấu trúc:** Khung ảnh lớn với overlay chuyển màu nhẹ.
- **Nội dung:**
  - Tiêu đề chính: `transform your hair today.`
  - Đoạn mô tả: `thousands of customers are improving their hair naturally...`
  - CTA Button: `Try It Now` dẫn thẳng tới `/collections/batana`.
- **Responsive:** Ảnh desktop tỷ lệ rộng (16:9 hoặc 21:9), ảnh mobile tối ưu tỷ lệ đứng (4:5).

### 2.2 Featured Collection Grid (`featured-collection.liquid`)
- **Cấu trúc:** Lưới 4 sản phẩm chính trên Desktop (2 cột trên Mobile).
- **Product Card (`product-card.liquid` snippet):**
  - Ảnh đại diện có hover zoom / flip sang ảnh thứ 2.
  - Huy hiệu trạng thái: `Sale` (đỏ) hoặc `Sold out` (xám).
  - Tiêu đề sản phẩm (chữ vừa, font Poppins đậm).
  - Đánh giá sao (⭐⭐⭐⭐⭐ 4.9/5).
  - Giá bán gốc & giá khuyến mãi nổi bật.
  - Nút thêm nhanh vào giỏ (Quick Add to Cart) hoặc chọn biến thể.

### 2.3 Quiz / Routine Banner (`routine-quiz-banner.liquid`)
- **Cấu trúc:** Khối màu kem / xanh sage mềm mại (`#e9ece9`).
- **Nội dung:** Tiêu đề `TAKE OUR HAIR QUIZ`, mô tả giúp khách hàng tìm liệu trình phù hợp, nút bấm `Start Now`.

---

## 3. HIGH-CONVERSION PRODUCT DETAIL PAGE (PDP) SECTIONS

### 3.1 Main Product Section (`main-product.liquid`)
- **Gallery:** Slider ảnh thumbnail dạng cuộn dọc (Desktop) và vuốt ngang (Mobile) kèm tính năng phóng to.
- **Product Info:**
  - Tên sản phẩm, dòng cam kết (100% Pure Honduran Batana).
  - Review rating với tổng số đánh giá khách hàng thật.
  - **Quantity Break / Bundle Selector (Rebuild sạch thay thế Kaching Bundles):**
    - Hộp 1 chai: Giá chuẩn ($44.00)
    - Hộp 2 chai: Giảm 20% + Tặng kèm hướng dẫn chăm sóc tóc
    - Hộp 3 chai (Best Value): Giảm 35% + Quà tặng lược gỗ & Free Shipping
  - Nút "Thêm vào giỏ" (Add to Cart) to rõ ràng, hiệu ứng pulse nhẹ.
  - Nút "Mua ngay" (Dynamic Checkout Button - Buy with Shop Pay / Apple Pay / PayPal).
  - Dải huy hiệu cam kết tin cậy (Trust Badges): 30-Day Money Back Guarantee, 100% Organic, Fast US Shipping.

### 3.2 Social Proof Counter (`social-proof-bar.liquid`)
- 3 cột số liệu biết nói: `200k+ Happy Customers`, `850,000+ Bottles Shipped`, `58k+ 5-Star Reviews`.
- Tiêu đề dẫn: "What can 3-8 weeks of use do for your edges?".

### 3.3 Visual Comparison Table (`product-comparison.liquid`)
- Bảng so sánh 2 cột:
  - **Dầu Azure Batana chính hãng:** Ép lạnh nguyên chất, giàu axit béo Omega-6, thẩm thấu nuôi nang tóc từ bên trong, không paraben/silicone.
  - **Dầu pha loãng trên thị trường:** Trộn dầu khoáng (Mineral oil), gây bít tắc nang lông, chỉ phủ bóng bề mặt.

### 3.4 Weekly Results Timeline (`product-timeline.liquid`)
- Trình bày 3 mốc thời gian:
  - **Tuần 1 - 2:** Da đầu được làm dịu, giảm gàu ngứa, tóc mềm mượt hơn.
  - **Tuần 3 - 4:** Giảm rụng tóc rõ rệt khi gội đầu, chân tóc con bắt đầu nhú (Baby hairs).
  - **Tuần 6 - 8:** Tóc con mọc dày vùng thái dương và đỉnh đầu, thân tóc bóng chắc khỏe.

### 3.5 Ingredients Deep-Dive (`product-ingredients.liquid`)
- Card lưới 4 thành phần vàng:
  - `Vitamin E Complex`: Chống oxy hóa tế bào tóc.
  - `Omega 3-6-9 Fatty Acids`: Tái tạo màng lipid nang tóc.
  - `Vitamin A Complex`: Thúc đẩy phân chia tế bào mầm tóc.
  - `Natural Phytosterols`: Khóa ẩm biểu bì tóc dài lâu.

### 3.6 Accordion FAQ (`product-faq.liquid`)
- Danh sách câu hỏi thường gặp với đóng/mở mượt mà:
  1. Dầu Batana này có mùi gì? (Mùi hạt cà phê rang tự nhiên, không hương liệu nhân tạo).
  2. Dùng bao lâu thì thấy tóc con mọc lại?
  3. Cách thoa dầu lên chân tóc và ủ qua đêm như thế nào?
  4. Chính sách hoàn tiền 30 ngày hoạt động ra sao?
