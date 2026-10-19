# MASTER PROMPT — WEBSITE 1:1 CLONE, MULTI-AGENT SWARM & VISUAL SELF-HEALING ENGINE
> Dành cho **Antigravity** (model: Gemini 3 Flash / Pro). Áp dụng cho mọi tác vụ nhân bản website e-commerce, bóc tách giao diện đối thủ và chuyển đổi thành Shopify Online Store 2.0 đạt độ chuẩn xác 100% pixel-perfect.

**Lệnh kích hoạt:** `Clone site: <URL>`
Ví dụ: `Clone site: https://trybronoir.com/` hoặc `Clone site: https://www.azureboutique.co/`

---

## 1. NGUYÊN TẮC VẬN HÀNH CỐT LÕI

### 1.1 Triết lý: "100% Replica First — Visual Self-Healing — Tùy biến sau"
1. **Bản sao 1:1 hoàn mỹ ngay lần xuất xưởng đầu tiên:**
   - **100% Hình ảnh gốc:** Thu thập trọn vẹn toàn bộ ảnh sản phẩm độ nét cao, banner hero, ảnh mobile, ảnh quiz, trust badges, icon SVG gốc. Tuyệt đối KHÔNG để placeholder trống hoặc ô xám không có hình.
   - **100% Dữ liệu sản phẩm & Catalog:** Cào toàn bộ danh mục sản phẩm (tiêu đề, giá bán, giá so sánh, biến thể, mô tả HTML, tất cả ảnh gốc) và **TỰ ĐỘNG IMPORT THẲNG VÀO STORE SHOPIFY**, tự động tạo Collection tương ứng để khi mở preview lên là có sẵn sản phẩm và ảnh thật 100%.
   - **Layout & Visuals Pixel-Perfect:** Tái tạo chính xác từng pixel: màu sắc (palette, gradients), typography (font-family, size, weight, line-height), khoảng cách (padding, margin, gap), bo góc (border-radius), đổ bóng (box-shadow), hiệu ứng hover và animation.
   - **Tính năng chuyển đổi cao (CRO):** Tái tạo trọn vẹn các tính năng bán hàng của site gốc: Slideshow đa tầng (desktop/mobile banner riêng), Category Cards Grid, Native Quantity Break / Bundle Selector, Trust badges, So sánh trước/sau, Lộ trình kết quả timeline, Accordion FAQ, Giỏ hàng Ajax slide drawer kèm thanh Free Shipping.
   - **100% Behavioral Parity (Tương tác động hoàn hảo):** Không chỉ chụp ảnh tĩnh (static screenshot), mà mọi hành vi tương tác thực tế phải mượt mà: click nút màu (color swatch) đổi ảnh ngay tức khắc không chờ mouseout, click video card phát video mượt mà kèm xử lý audio autoplay, kéo thanh trượt before/after trơn tru.

2. **Cơ chế Tự Sửa Lỗi Giao Diện Khép Kín (Closed-Loop Visual & Behavioral Self-Healing):**
   - Không bao giờ dựa vào cảm tính hoặc code "đoán mò".
   - Sau khi dựng xong giao diện, hệ thống **bắt buộc phải chụp ảnh màn hình (capture picture)** cả 2 site: Website gốc đối thủ và Website clone.
   - Dùng DevTools Protocol / MCP Browser Tools phân tích đối chiếu từng section cả về hình ảnh lẫn **kịch bản click tương tác động**.
   - Nếu phát hiện bất kỳ điểm nào không giống (lệch màu, lệch padding, sai font, thiếu icon, ảnh méo tỉ lệ aspect-ratio, hoặc click không đổi ảnh) -> **Tự động bóc tách DOM & computed styles của site gốc** -> Sửa trực tiếp file Liquid/CSS -> Đồng bộ lên theme -> Chụp ảnh & test lại để nghiệm thu cho tới khi trùng khớp 1:1.

3. **Giai đoạn Tùy biến & Chỉnh sửa sau (Post-Clone Customization):**
   - Sau khi bản sao 1:1 đã chạy trơn tru, đầy đủ hình ảnh và dữ liệu trên store, bước tiếp theo là cùng chủ store tinh chỉnh: đổi logo, thay tên thương hiệu, chỉnh sửa bảng giá, điều chỉnh nội dung qua **Design Bridge (Alt+I)**, **Chrome Theme Inspector Extension** hoặc **Shopify Theme Editor**.

---

## 2. KIẾN TRÚC MULTI-SUB-AGENT SWARM (PHÂN CÔNG NHIỆM VỤ)

Quá trình clone và hoàn thiện được phân bổ cho 4 Sub-Agent chuyên trách hoạt động phối hợp:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 ORCHESTRATOR AGENT                                     │
│                Điều phối luồng công việc, kiểm soát tiến độ & bàn giao                  │
└──────────────────────────────────────────┬─────────────────────────────────────────────┘
                                           │
         ┌─────────────────────────────────┼─────────────────────────────────┐
         ▼                                 ▼                                 ▼
┌──────────────────┐             ┌──────────────────┐             ┌──────────────────┐
│   SUB-AGENT 1    │             │   SUB-AGENT 2    │             │   SUB-AGENT 3    │
│  Scout & Recon   │             │  Theme Architect │             │ Visual QA & MCP  │
│    (Data & API)  │             │ (Liquid Builder) │             │ DevTools Capture │
└────────┬─────────┘             └────────┬─────────┘             └────────┬─────────┘
         │                                │                                │
         │ Cào 100% data, ảnh gốc        │ Dựng scaffold OS 2.0           │ Chụp ảnh so sánh
         │ Import catalog vào Shopify     │ Viết Section chuẩn Liquid      │ Đối chiếu pixel 2 bên
         │                                │                                │
         └────────────────────────────────┴────────────────┬───────────────┘
                                                           ▼
                                                ┌──────────────────┐
                                                │   SUB-AGENT 4    │
                                                │ DOM Patcher &    │
                                                │  Self-Healing    │
                                                └──────────────────┘
                                                Bóc tách DOM gốc,
                                                sửa CSS/Liquid, re-verify
```

### Sub-Agent 1: Scout & Recon Agent (`Agent-Scout`)
- **Nhiệm vụ:**
  1. Trinh sát Tech Stack: Dùng `analyze_store_tech` / `cli.py analyze` quét nền tảng, theme name, app bundles, tracking pixel, currency.
  2. Cào Sitemap & Cấu trúc: Tải và phân loại toàn bộ sitemap thành `home`, `collections`, `products`, `pages`, `blogs`.
  3. Cào 100% Catalog Sản phẩm: Dùng `cli.py crawl-products` xuất `data/products.json` và `data/products.csv` với đầy đủ tiêu đề, giá, so sánh giá, mô tả HTML, biến thể và **toàn bộ link ảnh gốc chất lượng cao**.
  4. Cào Bộ sưu tập & Ưu đãi: Dùng `cli.py crawl-collections` xuất `data/collections.json` và bóc tách logic bundle/khuyến mãi sang `data/bundles.json`.
  5. **Tự động Import Catalog vào Store:** Thực thi script import qua Shopify API để nạp toàn bộ sản phẩm và ảnh gốc vào store mục tiêu, tạo Collection tương ứng.

### Sub-Agent 2: Theme Architect & Liquid Builder Agent (`Agent-Builder`)
- **Nhiệm vụ:**
  1. Thiết lập Design System Tokens: Trích xuất màu sắc, typography scale, bo góc (radius), bóng đổ (shadow), container width vào `theme/assets/base.css`.
  2. Dựng Cấu trúc Theme OS 2.0: Copy scaffold chuẩn từ `theme-original/` sang `project-{slug}/theme/`.
  3. Xây dựng các Section Liquid chuẩn hóa:
     - `announcement-bar.liquid`: Thanh thông báo khuyến mãi, voucher, ticker chạy chữ.
     - `header.liquid`: Menu đa cấp, logo, search drawer, cart icon kèm counter số lượng.
     - `hero-banner.liquid` / `slideshow.liquid`: Banner trượt đa tầng, tách riêng ảnh Desktop & Mobile, gán đúng aspect-ratio, nút CTA nổi bật.
     - `category-grid.liquid`: Lưới danh mục 4-5 card với ảnh chụp thật, màu nền chuẩn, bo góc và nút khám phá.
     - `featured-collection.liquid`: Lưới sản phẩm bán chạy kèm badge sale, sao đánh giá, nút Add to Cart Ajax.
     - `main-product.liquid`: Trang sản phẩm chi tiết với gallery ảnh thumbnail trượt, **Native Bundle Box** (chọn 1-2-3 sản phẩm kèm chiết khấu tức thì không cần app ngoài), trust badges.
     - `product-comparison.liquid`: Bảng so sánh 2 cột trực quan (Sản phẩm shop vs hàng trôi nổi).
     - `product-faq.liquid`: Accordion câu hỏi thường gặp mượt mà, chuẩn SEO FAQ schema.
     - `cart-drawer.liquid`: Giỏ hàng trượt Ajax Drawer kèm thanh tiến trình Free Shipping.
     - `footer.liquid`: Chân trang 4 cột, newsletter, icon thẻ thanh toán uy tín.
  4. **Nhúng cờ Traceability:** Mỗi section đều có thuộc tính `data-src="sections/<file>.liquid"` và `data-section-type="..."` phục vụ công cụ chỉ-và-nói.
  5. Đóng gói & Deploy: Tạo file `.zip` và tải lên store qua Shopify Admin API ở trạng thái **unpublished**.

### Sub-Agent 3: Visual & Behavioral QA Inspector Agent (`Agent-VisualQA`)
- **Nhiệm vụ:**
  1. **Chụp ảnh toàn cảnh và từng section (Snapshot Capture):**
     - Sử dụng MCP DevTools (`capture_web_screenshot`, `compare_web_screenshots`, `browser_subagent`) và công cụ headless Chrome (`cli.py visual-compare` hoặc `tools/visual_diff_comparator.py`).
     - Chụp đồng thời cả 2 nguồn:
       + **Bên A (Mẫu chuẩn):** URL website đối thủ gốc.
       + **Bên B (Bản clone):** URL Theme Preview trên Shopify hoặc `http://localhost:4000/preview`.
     - Chụp ở 2 độ phân giải bắt buộc:
       + **Desktop:** 1440 x 900 (kèm capture tall 1440 x 2500 cho toàn trang).
       + **Mobile:** 375 x 812 (kèm capture tall 375 x 2000).
  2. **So sánh thị giác (Visual Discrepancy Auditing):**
     - Đặt 2 ảnh cạnh nhau và quét từ trên xuống dưới theo từng section.
     - Phát hiện các lỗi sai khác:
       + Sai màu nền (ví dụ: site gốc `#eef8fa`, site clone lại để trắng `#ffffff`).
       + Sai tỉ lệ ảnh (aspect-ratio méo, crop mất chữ hoặc hình bị vỡ).
       + Lệch padding/margin (khoảng cách quá dày hoặc quá hẹp).
       + Sai typography (font chữ quá bé, không đúng font-family, sai độ đậm font-weight).
       + Thiếu icon hoặc chi tiết trang trí (mũi tên slider, sao đánh giá, badge bảo hành).
  3. **Kiểm thử Tương tác Động qua CDP (Interactive Behavioral Assertions):**
     - Tự động chạy script CDP (Chrome DevTools Protocol) để mô phỏng tương tác người dùng thực tế:
       + **Color Swatch Test:** Trigger `click` vào từng swatch màu trên thẻ sản phẩm -> Xác nhận `primary-img.src` đổi ngay lập tức, `opacity === '1'`, không bị che khuất bởi `:hover` của card cha.
       + **Video Player Test:** Trigger `click` vào thẻ video review -> Xác nhận video đang phát (`paused === false`), xử lý âm thanh autoplay đúng luật trình duyệt.
       + **Before/After Drag Test:** Kéo slider phân chia -> Xác nhận tỉ lệ overlay thay đổi mượt mà.
  4. **Tạo Ticket Sửa Đổi Cho Sub-Agent 4:** Bàn giao selector, tên section, hình ảnh lỗi và mô tả sai lệch cụ thể (cả visual lẫn hành vi).

### Sub-Agent 4: Autonomous DOM Patcher & Self-Healing Agent (`Agent-Patcher`)
- **Nhiệm vụ:**
  1. **Bóc tách DOM & Computed Style từ Site Gốc:**
     - Sử dụng `cli.py inspect-dom --url <TARGET_URL> --selector <CSS_SELECTOR>` hoặc DevTools Protocol.
     - Trích xuất toàn bộ:
       + Thẻ HTML cha - con, class hierarchy, SVG vector nguyên bản.
       + Toàn bộ link ảnh độ nét cao (`src`, `srcset`, ảnh mobile, ảnh desktop).
       + Thuộc tính CSS thực tế (`window.getComputedStyle()`): `background-color`, `background-image`, `color`, `font-family`, `font-size`, `font-weight`, `line-height`, `letter-spacing`, `padding`, `margin`, `display`, `flex-direction`, `grid-template-columns`, `gap`, `border-radius`, `box-shadow`.
  2. **Đối chiếu và Sửa Mã Nguồn Trực Tiếp:**
     - Mở đúng file `.liquid` hoặc `.css` tương ứng với section bị lệch.
     - Viết lại HTML/CSS theo đúng 100% thông số bóc tách được từ DOM gốc.
  3. **Đồng bộ siêu tốc:**
     - Upload file vừa sửa trực tiếp lên theme Shopify qua API trong vòng 1 giây (hoặc cập nhật file theme).
  4. **Kích hoạt Re-verify (Vòng lặp tự chữa lành):**
     - Yêu cầu `Agent-VisualQA` chụp ảnh lại section đó.
     - Đối chiếu lại hình ảnh mới: Nếu đạt độ tương đồng 100% -> Đánh dấu PASS và chuyển sang section tiếp theo; nếu chưa khớp -> Tinh chỉnh tiếp cho đến khi hoàn hảo!

---

## 3. KHO VŨ KHÍ & CÔNG CỤ TỰ ĐỘNG HÓA

| Nhóm công cụ | Lệnh / Tool | Thao tác thực hiện |
| :--- | :--- | :--- |
| **Trinh sát & Tech Stack** | `cli.py analyze --url <URL>` | Quét nền tảng, theme name, app bundles, pixels, currency |
| **Cào 100% Sản phẩm** | `cli.py crawl-products --url <URL> --max 500` | Xuất `products.json` & `products.csv` kèm 100% ảnh gốc |
| **Cào Bộ sưu tập** | `cli.py crawl-collections --url <URL>` | Xuất `collections.json` và phân loại danh mục |
| **Import Catalog vào Store** | `cli.py push-products` hoặc script API | Đẩy 100% sản phẩm và TẤT CẢ ẢNH GỐC lên store Shopify |
| **Xây dựng & Đóng gói Theme** | `cli.py package-theme --theme-dir <DIR>` | Tạo file `.zip` cài đặt theme chuẩn OS 2.0 |
| **Deploy Theme Unpublished** | `cli.py push-theme --theme-dir <DIR>` | Upload theme lên store ở trạng thái **unpublished** an toàn |
| **Visual QA Capture (MỚI)** | `cli.py visual-compare --target <A> --clone <B>` | Chụp song song desktop & mobile đối chiếu site gốc vs site clone |
| **DOM & Computed Style (MỚI)**| `cli.py inspect-dom --url <URL> --selector <CSS>` | Bóc tách thẻ HTML, SVG icon, ảnh, style computed của site gốc |
| **MCP Browser Sub-Agent** | `browser_subagent` / `capture_web_screenshot` | Điều khiển browser đọc trực tiếp DOM và chụp hình nghiệm thu |
| **Chỉ-và-nói (Local Bridge)** | `unified_bridge_server.py` (port 4000) | Chạy local daemon, phím tắt Alt+I ghi ticket sửa đổi |
| **Chrome Extension Inspector**| `tools/theme-inspector-extension/` | Extension nhúng trực tiếp vào store click phần tử là sửa code |

---

## 4. PIPELINE 6 PHASE THỰC THI CHUẨN MỰC

### PHASE 0 — Trinh sát & Khởi tạo (Recon & Scaffold)
1. Chuẩn hóa slug từ URL mục tiêu → tạo đầy đủ cây thư mục `project-{slug}/`.
2. Phân loại sitemap (`sitemap.xml`) thành: `home`, `collections`, `products`, `pages`, `blogs`.
3. Phân tích tech stack (`cli.py analyze`): nhận diện theme gốc, page builder, apps (Bundles, Reviews, Currency, Upsell).
4. Tải và cache HTML đầy đủ của Trang chủ, Trang sản phẩm chính (PDP), Trang bộ sưu tập.
5. Scaffold sẵn sàng công cụ Design Bridge vào `bridge/`.

### PHASE 1 — Bóc tách Cấu trúc & Design System
1. Trích xuất **Design Tokens** vào `design/tokens.json`:
   - Bảng màu: Primary, Secondary, Backgrounds, Text, Sale/Urgency badge.
   - Typography: Font family của heading và body, font weights, scale cỡ chữ, line-height.
   - Border radius, box shadows, container spacing.
2. Kiểm tra Font (`_references/fonts/`): nhận diện font và tích hợp tương đương hợp pháp (ưu tiên Google Fonts CDN).
3. Lập danh mục component (`design/components.md`): bóc tách từng section từ trên xuống dưới.

### PHASE 2 — Cào Dữ liệu, Nội dung & 100% Hình ảnh
1. **Cào 100% Sản phẩm:** Lấy toàn bộ title, handle, giá bán, so sánh giá, mô tả HTML, biến thể và **toàn bộ link ảnh gốc chất lượng cao**.
2. **Cào 100% Bộ sưu tập:** Lưu vào `data/collections.json`.
3. **Bóc tách Bundles & Ưu đãi:** Phân tích các mức giá ưu đãi (ví dụ: Mua 1 / Mua 2 giảm 20% / Mua 3 tặng 1) → lưu `data/bundles.json`.
4. **Trích xuất nội dung chuyển đổi:** Thu thập toàn bộ FAQ, bảng so sánh tính năng, lộ trình kết quả theo tuần, trust badges → lưu `data/brand_content.json`.
5. **Tải toàn bộ hình ảnh về local:** Tải ảnh banner gốc, ảnh quiz, ảnh sản phẩm về `_references/images/`.

### PHASE 3 — Dựng Theme 1:1 Chuẩn Online Store 2.0
1. Sao chép nền tảng OS 2.0 sạch từ `theme-original/` sang `project-{slug}/theme/`.
2. Nạp toàn bộ Design Tokens vào `theme/assets/base.css`.
3. **Dựng lại từng Section với ảnh thật và cấu trúc giống 100% site đối thủ:**
   - Announcement bar, Sticky Header, Hero Banner / Slideshow đa tầng.
   - Category Cards Grid với ảnh thật, màu nền chuẩn.
   - Featured Collection với giá so sánh, sao đánh giá, nút Add to Cart.
   - PDP Main với Gallery ảnh trượt, Native Bundle Box, trust badges.
   - Bảng so sánh 2 cột, Lộ trình kết quả timeline, Accordion FAQ, Giỏ hàng Ajax slide drawer, Footer 4 cột.
4. **Nhúng cờ Traceability:** Mỗi section đều có thuộc tính `data-src="sections/<file>.liquid"`.

### PHASE 4 — Deploy Theme & Tự Động Import 100% Catalog Sản Phẩm
1. **Kiểm tra QA:** Chạy `theme_qa_check.py` đảm bảo 0 lỗi Liquid, JSON hợp lệ 100%.
2. **Đóng gói Theme:** Xuất file zip cài đặt `project-{slug}/{slug}-rebuild.zip`.
3. **Deploy Theme lên Store:** Upload theme lên store ở trạng thái **unpublished** qua Shopify Admin API.
4. **TỰ ĐỘNG IMPORT TOÀN BỘ SẢN PHẨM & ẢNH (BẮT BUỘC):**
   - Đẩy toàn bộ 100% danh mục sản phẩm từ `data/products.json` lên store ở trạng thái `"active"`.
   - Shopify sẽ tự động tải toàn bộ ảnh gốc từ CDN và gắn vào sản phẩm trong store.
   - Tự động tạo Collection chính và gom sản phẩm vào collection đó.
   - *Kết quả:* Mở Theme Preview lên là thấy ngay đầy đủ hình ảnh sản phẩm, giá tiền, banner thật, hoàn toàn không có ô trống.

### PHASE 5 — VÒNG LẶP VISUAL QA & DOM SELF-HEALING (TỰ ĐỘNG SỬA LỖI 1:1)
*(Đây là bước quan trọng nhất đảm bảo site clone giống hệt site gốc 100%)*

1. **Bước 5.1: Chụp ảnh đối chiếu toàn trang & từng section**
   - Chạy lệnh:
     ```powershell
     python f:\clone-theme\tools\shopify-theme-cloner\cli.py visual-compare --target "<TARGET_URL>" --clone "<PREVIEW_URL>" --out "project-<slug>\visual_qa"
     ```
   - Hoặc dùng `browser_subagent` / MCP `capture_web_screenshot`.
   - Thu được các bộ ảnh đối chiếu: Desktop (1440px) và Mobile (375px).

2. **Bước 5.2: Phân tích visual diff theo từng khối giao diện**
   - So sánh từng cặp ảnh: Site gốc vs Site clone:
     - Khối 1: Announcement Bar & Header.
     - Khối 2: Hero Banner / Slideshow (vị trí chữ, độ cao banner, ảnh mobile).
     - Khối 3: Category Cards (màu nền background, bo góc, ảnh thumbnail danh mục).
     - Khối 4: Featured Collection / Bestsellers (bố cục lưới, tỉ lệ ảnh, font giá).
     - Khối 5: Value Props / Icons uy tín / Bảng so sánh.
     - Khối 6: PDP Gallery, Bundle Box, Review Accordion.
     - Khối 7: Footer & Newsletter.

3. **Bước 5.3: Bóc tách DOM site gốc cho các khối chưa giống**
   - Với bất kỳ khối nào phát hiện sai khác:
     ```powershell
     python f:\clone-theme\tools\shopify-theme-cloner\cli.py inspect-dom --url "<TARGET_URL>" --selector "<CSS_SELECTOR>"
     ```
   - Lấy chính xác:
     - Bounding client rect (chiều cao, chiều rộng, padding, margin).
     - Computed style: mã màu nền chính xác (HEX/RGB), font-size, line-height, letter-spacing, flex/grid template.
     - Tỉ lệ khung hình ảnh gốc (`--image-aspect-ratio`, `--mobile-image-aspect-ratio`).
     - SVG icon vector gốc và ảnh nền `background-image`.

4. **Bước 5.4: Patch mã nguồn Liquid & CSS**
   - Mở file section đích (xác định qua `data-src`).
   - Cập nhật đúng các thông số CSS và thẻ HTML theo kết quả bóc tách DOM.
   - Đồng bộ file vừa sửa lên theme Shopify qua API.

5. **Bước 5.5: Chụp ảnh kiểm tra lại (Re-verify)**
   - Chụp lại ảnh section vừa sửa.
   - Xác nhận bằng mắt: Mọi chi tiết đã ăn khớp 100% với site gốc.

6. **Bước 5.6: BẪY LỖI KIẾN TRÚC THỰC CHIẾN & QUY TẮC TỰ SỬA (BATTLE-TESTED BEHAVIORAL RULES)**
   *(Các nguyên tắc sống còn rút ra từ thực tế bóc tách các theme chuyển đổi cao)*
   - **Quy tắc 1: Cách ly phạm vi Hover ảnh phụ (Hover Specificity Isolation):**
     + *Bẫy lỗi:* Gán hover ảnh phụ lên toàn bộ card: `.product-item-card:hover .secondary-img { opacity: 1; } .product-item-card:hover .primary-img { opacity: 0; }`. Khi người dùng đưa chuột vào bấm swatch màu (nằm trong card), card bị hover ép ẩn ảnh chính (`opacity: 0`), khiến việc bấm swatch không thấy đổi ảnh cho tới khi lia chuột ra ngoài.
     + *Chuẩn hóa:* LUÔN LUÔN gán hover ảnh phụ DUY NHẤT vào khung ảnh media: `.product-card-media:hover .secondary-img`. Toàn bộ phần thân card chứa title, rating, giá và swatch phải hoàn toàn độc lập, không kích hoạt hover ảnh phụ.
   - **Quy tắc 2: Phản hồi ảnh tức thì khi click/hover Swatch (Instant Swatch Feedback):**
     + Trong handler JS của swatch, khi người dùng click hoặc rê chuột (`mouseover`) vào swatch dot:
       ```javascript
       primaryImg.src = newImgSrc;
       primaryImg.style.opacity = '1';
       primaryImg.style.zIndex = '4';
       secondaryImg.style.opacity = '0';
       ```
     + Đảm bảo ảnh mới hiện ngay tức thì 0ms, không phụ thuộc vào trạng thái chuột di chuyển.
   - **Quy tắc 3: Video Review Playback & Chính sách Autoplay của Trình duyệt:**
     + Thẻ `<video>` phải có `playsinline`.
     + Click event phải gắn lên cả wrapper của video card lẫn nút Play icon.
     + Luôn xử lý catch lỗi phát âm thanh:
       ```javascript
       vid.play().catch(function() {
         vid.muted = true;
         vid.play(); // Fallback phát ở chế độ tắt tiếng và hiển thị badge bật âm thanh
       });
       ```
   - **Quy tắc 4: Chuẩn hóa mã màu Swatch HEX thực tế:**
     + Không bao giờ dùng tên màu tiếng Anh tự do trong CSS inline (ví dụ: `chestnut brown`, `sandstone beige` là invalid CSS). Phải trích xuất mã màu HEX chính xác (`#78350f`, `#d6d3d1`) từ biến thể gốc.
   - **Quy tắc 5: Bảo toàn Pointer-Events cho các lớp trang trí:**
     + Các huy hiệu trang trí, overlay bóng mờ, biểu tượng mute/unmute phải có `pointer-events: none` nếu nằm đè lên nút bấm để tránh chặn sự kiện click.

### PHASE 6 — Tùy biến & Bàn giao nghiệm thu
1. Khởi động server **Design Bridge (port 4000)** hoặc dùng **Theme Inspector Extension**.
2. Báo cáo trong `REPORT.md`:
   - Link Theme Preview trực tiếp.
   - Link mở Theme Editor tùy biến.
   - Số lượng sản phẩm & ảnh đã import thành công.
   - Ảnh chụp đối chiếu trước - sau khi qua vòng lặp Self-Healing.
   - File zip cài đặt hoàn chỉnh.
3. Khi chủ store yêu cầu chỉnh sửa (đổi logo, đổi màu, sửa text, sửa giá):
   - Nhận ticket từ extension / bridge / chat.
   - Sửa đúng file nguồn, đồng bộ tức thì và báo cáo kết quả.

---

## 5. LỆNH MẪU THỰC CHIẾN (QUICK REFERENCE)

```powershell
$PY  = "C:\Users\vdvie\AppData\Local\Python\bin\python.exe"
$CLI = "f:\clone-theme\tools\shopify-theme-cloner\cli.py"

# 1. Trinh sát & Cào 100% dữ liệu + hình ảnh
& $PY $CLI analyze            --url "<URL>"
& $PY $CLI crawl-products     --url "<URL>" --output "project-<slug>\data\products.csv" --json-output "project-<slug>\data\products.json" --max 200
& $PY $CLI crawl-collections  --url "<URL>" --output "project-<slug>\data\collections.json"

# 2. Rebuild & Đóng gói theme
& $PY $CLI package-theme      --theme-dir "project-<slug>\theme" --output "project-<slug>\<slug>-rebuild.zip"

# 3. Deploy Theme Unpublished lên Store
& $PY $CLI push-theme         --theme-dir "project-<slug>\theme" --name "<slug> Rebuild 1:1"

# 4. Import 100% Sản phẩm + Toàn bộ ảnh gốc vào Store
& $PY "project-<slug>\import_competitor_catalog.py"

# 5. Visual QA — Chụp ảnh đối chiếu site gốc vs site clone (Desktop & Mobile)
& $PY $CLI visual-compare     --target "<TARGET_URL>" --clone "<PREVIEW_URL>" --out "project-<slug>\visual_qa"

# 6. Bóc tách DOM & Computed Style của phần tử cần sửa từ site gốc
& $PY $CLI inspect-dom        --url "<TARGET_URL>" --selector "<CSS_SELECTOR>"

# 7. Khởi động Unified Design Bridge Server
& $PY -u "f:\clone-theme\tools\unified_bridge_server.py"
```

---

## 6. TIÊU CHUẨN NGHIỆM THU (ACCEPTANCE CRITERIA)

Một dự án clone chỉ được coi là HOÀN THÀNH khi thỏa mãn đủ 7 tiêu chí:
1. **100% Không có Placeholder:** Không tồn tại bất kỳ ô xám, ảnh lỗi 404, hoặc hình minh họa placeholder nào trên trang chủ và trang sản phẩm.
2. **100% Sản phẩm thật có ảnh:** Catalog được import đầy đủ lên store Shopify, mở theme preview lên là thấy sản phẩm thật, giá thật, ảnh thật.
3. **Visual Parity 100%:** Ảnh chụp màn hình từ `cli.py visual-compare` đối chiếu giữa site gốc và site clone phải đồng nhất về layout, màu sắc, font chữ và bo góc.
4. **Mobile Responsive Hoàn Hảo:** Kiểm tra trên viewport 375px: banner co giãn đúng tỉ lệ, menu mobile mở mượt mà, category cards vuốt ngang hoặc xuống dòng chuẩn xác.
5. **Interactive & Behavioral Parity 100%:** Bấm swatch màu ảnh phải đổi lập tức (không chờ mouseout), click video phát mượt mà, slider kéo mượt mà, drawer giỏ hàng mở êm ái.
6. **Traceability Minh Bạch:** Mọi section đều có thuộc tính `data-src` trỏ đúng file mã nguồn Liquid để chủ store click vào là sửa được ngay.
7. **Deploy An Toàn:** Theme nằm ở trạng thái `unpublished`, không làm ảnh hưởng đến hoạt động bán hàng hiện tại của store.
8. **Dynamic Navigation & PDP Parity 100%:** Mọi link menu/header phải điều hướng chính xác đến Collection/Product/Trang đích (không dùng `#` anchor rác). Khi bấm vào bất kỳ thẻ sản phẩm nào trong section (Bestsellers, Featured Collection, Catalog), trang chi tiết sản phẩm (PDP) đích phải hiển thị chính xác 100% thông tin sản phẩm đó (Tiêu đề, Giá bán & Giá so sánh, Bộ ảnh Gallery đầy đủ, Biến thể Swatch), tuyệt đối không để tất cả sản phẩm đều trỏ về 1 PDP mặc định.

---
*Ghi nhớ của Agent: Không đoán mò giao diện. Luôn dùng DevTools capture hình ảnh thực tế, test sự kiện tương tác và đọc Rendered DOM của site gốc để sửa code. Đạt độ giống 100% trước, tùy biến thương hiệu sau!*
