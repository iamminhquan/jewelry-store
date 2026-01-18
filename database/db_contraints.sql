-- =========================
-- 1. FK bảng SanPham
-- =========================
ALTER TABLE SanPham
ADD CONSTRAINT fk_sanpham_danhmuc FOREIGN KEY (ma_danh_muc) REFERENCES DanhMuc (ma_danh_muc),
-- Sản phẩm thuộc 1 danh mục
ADD CONSTRAINT fk_sanpham_loai FOREIGN KEY (loai_san_pham) REFERENCES LoaiSanPham (ma_loai_san_pham),
-- Sản phẩm thuộc 1 loại sản phẩm
ADD CONSTRAINT fk_sanpham_bosuutap FOREIGN KEY (bo_suu_tap) REFERENCES BoSuuTap (ma_bo_suu_tap),
-- Sản phẩm thuộc 1 bộ sưu tập
ADD CONSTRAINT fk_sanpham_thuonghieu FOREIGN KEY (thuong_hieu) REFERENCES ThuongHieu (ma_thuong_hieu);
-- Sản phẩm thuộc 1 thương hiệu

-- =========================
-- 2. FK bảng LoaiSanPham
-- =========================

ALTER TABLE LoaiSanPham
ADD CONSTRAINT fk_loaisanpham_danhmuc FOREIGN KEY (ma_danh_muc) REFERENCES DanhMuc (ma_danh_muc);

-- =========================
-- 3. FK bảng DanhGia
-- =========================
ALTER TABLE DanhGia
ADD CONSTRAINT fk_danhgia_sanpham FOREIGN KEY (ma_san_pham) REFERENCES SanPham (ma_san_pham),
-- Đánh giá cho sản phẩm
ADD CONSTRAINT fk_danhgia_taikhoan FOREIGN KEY (nguoi_danh_gia) REFERENCES TaiKhoan (ma_tai_khoan);
-- Người đánh giá

-- =========================
-- 4. FK bảng GioHang
-- =========================
ALTER TABLE GioHang
ADD CONSTRAINT fk_giohang_taikhoan FOREIGN KEY (ma_tai_khoan) REFERENCES TaiKhoan (ma_tai_khoan);
-- Giỏ hàng của tài khoản

-- =========================
-- 5. FK bảng ChiTietGioHang
-- =========================
ALTER TABLE ChiTietGioHang
ADD CONSTRAINT fk_ctgiohang_giohang FOREIGN KEY (ma_gio_hang) REFERENCES GioHang (ma_gio_hang),
-- Chi tiết thuộc giỏ hàng
ADD CONSTRAINT fk_ctgiohang_sanpham FOREIGN KEY (ma_san_pham) REFERENCES SanPham (ma_san_pham);
-- Sản phẩm trong giỏ hàng

-- =========================
-- 6. FK bảng DonHang
-- =========================
ALTER TABLE DonHang
ADD CONSTRAINT fk_donhang_taikhoan FOREIGN KEY (ma_tai_khoan) REFERENCES TaiKhoan (ma_tai_khoan);
-- Đơn hàng do tài khoản tạo

-- =========================
-- 7. FK bảng ChiTietDonHang
-- =========================
ALTER TABLE ChiTietDonHang
ADD CONSTRAINT fk_ctdonhang_donhang FOREIGN KEY (ma_don_hang) REFERENCES DonHang (ma_don_hang),
-- Chi tiết thuộc đơn hàng
ADD CONSTRAINT fk_ctdonhang_sanpham FOREIGN KEY (ma_san_pham) REFERENCES SanPham (ma_san_pham);
-- Sản phẩm trong đơn hàng

-- =========================
-- 8. FK bảng HoaDon
-- =========================
ALTER TABLE HoaDon
ADD CONSTRAINT fk_hoadon_taikhoan FOREIGN KEY (ma_tai_khoan) REFERENCES TaiKhoan (ma_tai_khoan);
-- Hóa đơn của tài khoản

-- =========================
-- 9. FK bảng ChiTietHoaDon
-- =========================
ALTER TABLE ChiTietHoaDon
ADD CONSTRAINT fk_cthoadon_hoadon FOREIGN KEY (ma_hoa_don) REFERENCES HoaDon (ma_hoa_don),
-- Chi tiết thuộc hóa đơn
ADD CONSTRAINT fk_cthoadon_sanpham FOREIGN KEY (ma_san_pham) REFERENCES SanPham (ma_san_pham);
-- Sản phẩm trong hóa đơn

-- =========================
-- 10. FK bảng KichThuocSanPham
-- =========================
ALTER TABLE KichThuocSanPham
ADD CONSTRAINT fk_kichthuocsanpham_sanpham FOREIGN KEY (ma_san_pham) REFERENCES SanPham (ma_san_pham);
-- Kích thước thuộc về sản phẩm

-- =========================
-- 11. FK bảng HinhAnhSanPham
-- =========================
ALTER TABLE HinhAnhSanPham
ADD CONSTRAINT fk_hinhanh_sanpham FOREIGN KEY (ma_san_pham) REFERENCES SanPham (ma_san_pham);
-- Hình ảnh thuộc về sản phẩm

-- =========================
-- 12. FK ảnh đại diện sản phẩm (OPTIONAL)
-- =========================
-- Chỉ dùng nếu SanPham.hinh_anh là ảnh chính
ALTER TABLE SanPham
ADD CONSTRAINT fk_sanpham_hinhanh FOREIGN KEY (hinh_anh) REFERENCES HinhAnhSanPham (ma_hinh_anh);
-- Ảnh đại diện sản phẩm

-- =========================================================
-- END FILE
-- =========================================================