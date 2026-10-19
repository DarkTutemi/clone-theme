# 🎯 Shopify Theme Visual Inspector Extension — Hướng Dẫn Cài Đặt & Sử Dụng

Extension Chrome cho phép ông chủ trỏ và click vào **bất kỳ thành phần giao diện nào** trên website (cả Localhost và Shopify Live Preview) để yêu cầu AI chỉnh sửa code Liquid / CSS chính xác 100%, sau đó đồng bộ thẳng lên cửa hàng Shopify.

---

## 🚀 1. Hướng Dẫn Cài Đặt (Chỉ 30 Giây)

1. Mở trình duyệt **Google Chrome** (hoặc Edge / Brave / Cốc Cốc).
2. Truy cập vào đường dẫn: `chrome://extensions/`
3. Ở góc trên bên phải, bật công tắc **"Developer mode" (Chế độ dành cho nhà phát triển)**.
4. Bấm vào nút **"Load unpacked" (Tải tiện ích đã giải nén)** ở góc trên bên trái.
5. Chọn thư mục sau trong máy tính của ông chủ:
   ```
   f:\clone-theme\tools\theme-inspector-extension
   ```
6. Tiện ích **Shopify Theme Visual Inspector** sẽ xuất hiện trên thanh công cụ trình duyệt! 🎉

---

## 🛠️ 2. Cách Sử Dụng Khi Duyệt Web

Ông chủ có thể dùng extension trên **bất kỳ trang web nào**, đặc biệt là:
- **Localhost Preview:** [http://localhost:4000/preview](http://localhost:4000/preview)
- **Shopify Live Preview:** [https://g1spma-ku.myshopify.com/?preview_theme_id=191338185071](https://g1spma-ku.myshopify.com/?preview_theme_id=191338185071)

### Bước 1: Kích hoạt chế độ Inspect
- Nhấn tổ hợp phím tắt: **`Alt + I`** trên bàn phím.
- Hoặc bấm vào nút tròn **🎯 Inspect DOM** ở góc dưới bên phải màn hình.

### Bước 2: Chọn phần tử muốn chỉnh sửa
- Di chuyển chuột trên trang web: Phần tử đang trỏ vào sẽ sáng viền xanh neon kèm nhãn hiển thị:
  - Thẻ HTML và class.
  - File mã nguồn Liquid tương ứng (ví dụ: `sections/hero-banner.liquid`, `snippets/product-card.liquid`).
- **Click chuột trái** vào phần tử đó để mở bảng điều khiển chỉnh sửa.

### Bước 3: Nhập yêu cầu & Gửi
- Nhập mong muốn của ông chủ vào khung văn bản. Ví dụ:
  > *"Đổi màu nền nút này thành màu đỏ rượu vang #881337, bo tròn 8px, chữ in hoa 'ĐẶT HÀNG NGAY'."*
- Chọn một trong hai cách gửi:
  - **🚀 Gửi cho AI Agent**: Gửi trực tiếp vào hàng đợi hệ thống cục bộ (`http://localhost:4000/ticket`).
  - **📋 Copy Prompt**: Tự động tạo một prompt chuẩn kỹ thuật và copy vào bộ nhớ tạm (Clipboard), ông chủ chỉ cần bấm `Ctrl + V` vào khung chat với em.

---

## ⚡ 3. Đồng Bộ Lên Shopify
Sau khi em sửa xong mã nguồn theo ý ông chủ:
- Truy cập Dashboard: [http://localhost:4000/](http://localhost:4000/) và bấm nút **"⚡ Đồng Bộ Theme Lên Shopify Ngay"**.
- Hoặc chỉ cần bảo em: *"đồng bộ lên store"* là em sẽ tự động chạy lệnh sync toàn bộ file sang theme Shopify của ông chủ ngay lập tức!
