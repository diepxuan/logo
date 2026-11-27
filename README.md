# Logo — Công ty TNHH Điệp Xuân

Kho lưu logo của công ty, dùng chung cho diepxuan.com, everon.site và dreamlandvn.com. Repo này chỉ chứa file logo (ảnh + vector), không còn code hay dữ liệu gì khác.

## Logo chính

Chữ "Đ" cách điệu kèm hình lá/cánh. Màu thương hiệu chính là nâu gỉ sắt **#A83C12** (bản MetallicBrown).

## Thư mục `icons/`

| Thư mục / file | Nội dung | Dùng khi nào |
|---|---|---|
| `brand/` | Chữ Đ đứng một mình | Logo chính, header/footer website |
| `alt/` | Chữ Đ + dòng chữ "ĐIỆP XUÂN CO." bên dưới | Bản thay thế khi cần kèm tên công ty |
| `texts/` | Chỉ dòng chữ "ĐIỆP XUÂN CO." | Chỉ cần tên công ty dạng chữ |
| `favicons/` | Chữ Đ gọn | Favicon trình duyệt |
| `Warm-Dream_Z.png` | Logo "Warm Dream" (chữ viết tay màu cam + chữ Đ) | Thương hiệu Warm Dream, chỉ có 1 file PNG |

## Màu sắc

- **MetallicBrown** — #A83C12, nâu gỉ sắt, màu thương hiệu chính.
- **Black** — đen.
- **NorthTexasGreen** — xanh lá đậm. Chỉ có bản PNG, không có SVG.

## Danh sách file

| File | Dung lượng | Ghi chú |
|---|---|---|
| `icons/brand/Black.svg` | 2,9 KB | Chữ Đ màu đen |
| `icons/brand/MetallicBrown.svg` | 2,7 KB | Chữ Đ màu #A83C12 |
| `icons/brand/MetallicBrown.png` | 213 KB | Chữ Đ màu #A83C12, bản PNG |
| `icons/brand/NorthTexasGreen.png` | 401 KB | Chữ Đ màu xanh, bản PNG |
| `icons/alt/Black.svg` | 7,5 KB | Chữ Đ + "ĐIỆP XUÂN CO." màu đen |
| `icons/alt/MetallicBrown.svg` | 7,3 KB | Chữ Đ + "ĐIỆP XUÂN CO." màu #A83C12 |
| `icons/alt/NorthTexasGreen.png` | 342 KB | Chữ Đ + "ĐIỆP XUÂN CO." màu xanh, bản PNG |
| `icons/texts/Black.svg` | 6,1 KB | Chỉ chữ "ĐIỆP XUÂN CO." màu đen |
| `icons/texts/MetallicBrown.svg` | 6,0 KB | Chỉ chữ "ĐIỆP XUÂN CO." màu #A83C12 |
| `icons/texts/MetallicBrown.png` | 110 KB | Chỉ chữ "ĐIỆP XUÂN CO." màu #A83C12, bản PNG |
| `icons/texts/NorthTexasGreen.png` | 71 KB | Chỉ chữ "ĐIỆP XUÂN CO." màu xanh, bản PNG |
| `icons/favicons/Black.svg` | 2,9 KB | Chữ Đ màu đen, bản gọn làm favicon |
| `icons/favicons/MetallicBrown.svg` | 2,9 KB | Chữ Đ màu #A83C12, bản gọn làm favicon |
| `icons/favicons/NorthTexasGreen.png` | 60 KB | Chữ Đ màu xanh, bản PNG làm favicon |
| `icons/Warm-Dream_Z.png` | 499 KB | Logo "Warm Dream" |

## File đang dùng trên website

- everon.site và dreamlandvn.com dùng `icons/favicons/MetallicBrown.svg` làm logo header/footer và favicon. File được copy sang repo của từng site thành `assets/img/logo-diep-xuan.svg` và `favicon.svg` (không link trực tiếp sang repo này).
- Bản SVG nhẹ hơn PNG nhiều (2,9 KB so với 39 KB) mà hiển thị giống hệt.

## Lịch sử

- Trước ngày 27/11/2026, repo còn chứa code crawler (`analytic/`), dữ liệu sản phẩm (`data/`, `images/`) và GitHub Actions chạy mỗi 10 phút.
- Ngày 27/11/2026 đã xóa hết, chỉ giữ lại `icons/`. Lịch sử commit vẫn còn đầy đủ trong git log.
