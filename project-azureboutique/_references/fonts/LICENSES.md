# FONT LICENSES & AUDIT MANIFEST
> Project: Azure Boutique Rebuild (Clean-Room)
> Target Store: https://www.azureboutique.co/

---

## 1. PHÁT HIỆN FONT TỪ SITE NGUỒN

- **Font Family sử dụng:** `Poppins`
- **Các biến thể cân nặng:**
  - `Poppins-Regular` (400)
  - `Poppins-Italic` (400 Italic)
  - `Poppins-Bold` (700)
  - `Poppins-BoldItalic` (700 Italic)

---

## 2. KẾT QUẢ RÀ SOÁT BẢN QUYỀN (LICENSE AUDIT)

- **Nhà thiết kế / Foundry:** Indian Type Foundry, Jonny Pinhorn, Ninad Kahale.
- **Giấy phép phát hành:** **SIL Open Font License, Version 1.1 (OFL)**.
- **Trạng thái bản quyền:** ✅ **100% Miễn phí & Hợp pháp** cho mục đích thương mại, nhúng web, tự lưu trữ (self-hosted) hoặc gọi qua Google Fonts CDN.
- **Đường dẫn Google Fonts chính thức:**
  ```html
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,400;0,500;0,600;0,700;1,400;1,700&display=swap" rel="stylesheet">
  ```

---

## 3. PHƯƠNG ÁN TRIỂN KHAI TRONG CLEAN-ROOM REBUILD

1. **Không copy các file nhị phân woff/woff2 tải từ CDN của store nguồn.**
2. **Khai báo chuẩn Google Fonts CDN** trực tiếp trong `theme/layout/theme.liquid` với thuộc tính `preconnect` và `font-display: swap` để tối ưu Core Web Vitals (FCP, LCP).
3. **Cấu hình fallback typography chuẩn:**
   ```css
   font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
   ```
