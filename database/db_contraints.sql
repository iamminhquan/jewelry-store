-- ==================================================================================
-- Bảng SanPham.
ALTER TABLE SanPham ADD CONSTRAINT fk_sanpham_danhmuc FOREIGN KEY (ma_danh_muc) REFERENCES DanhMuc (ma_danh_muc),
ADD CONSTRAINT fk_sanpham_loai FOREIGN KEY (loai_san_pham) REFERENCES LoaiSanPham (ma_loai_san_pham),
ADD CONSTRAINT fk_sanpham_bosuutap FOREIGN KEY (bo_suu_tap) REFERENCES BoSuuTap (ma_bo_suu_tap),
ADD CONSTRAINT fk_sanpham_thuonghieu FOREIGN KEY (thuong_hieu) REFERENCES ThuongHieu (ma_thuong_hieu);

-- Bảng LoaiSanPham.
ALTER TABLE LoaiSanPham ADD CONSTRAINT fk_loaisanpham_danhmuc FOREIGN KEY (ma_danh_muc) REFERENCES DanhMuc(ma_danh_muc) 

-- Bảng DanhGia.
ALTER TABLE DanhGia ADD CONSTRAINT fk_danhgia_sanpham FOREIGN KEY (ma_san_pham) REFERENCES SanPham (ma_san_pham),
ADD CONSTRAINT fk_danhgia_taikhoan FOREIGN KEY (nguoi_danh_gia) REFERENCES TaiKhoan (ma_tai_khoan);

-- Bảng GioHang.
ALTER TABLE GioHang ADD CONSTRAINT fk_giohang_taikhoan FOREIGN KEY (ma_tai_khoan) REFERENCES TaiKhoan (ma_tai_khoan);

-- Bảng ChiTietGioHang.
ALTER TABLE ChiTietGioHang ADD CONSTRAINT fk_ctgiohang_giohang FOREIGN KEY (ma_gio_hang) REFERENCES GioHang (ma_gio_hang),
ADD CONSTRAINT fk_ctgiohang_sanpham FOREIGN KEY (ma_san_pham) REFERENCES SanPham (ma_san_pham);

-- Bảng DonHang.
ALTER TABLE DonHang ADD CONSTRAINT fk_donhang_taikhoan FOREIGN KEY (ma_tai_khoan) REFERENCES TaiKhoan (ma_tai_khoan);

-- Bảng ChiTietDonHang.
ALTER TABLE ChiTietDonHang ADD CONSTRAINT fk_ctdonhang_donhang FOREIGN KEY (ma_don_hang) REFERENCES DonHang (ma_don_hang),
ADD CONSTRAINT fk_ctdonhang_sanpham FOREIGN KEY (ma_san_pham) REFERENCES SanPham (ma_san_pham);

-- Bảng HoaDon.
ALTER TABLE HoaDon ADD CONSTRAINT fk_hoadon_taikhoan FOREIGN KEY (ma_tai_khoan) REFERENCES TaiKhoan (ma_tai_khoan);

-- Bảng ChiTietHoaDon.
ALTER TABLE ChiTietHoaDon ADD CONSTRAINT fk_cthoadon_hoadon FOREIGN KEY (ma_hoa_don) REFERENCES HoaDon (ma_hoa_don),
ADD CONSTRAINT fk_cthoadon_sanpham FOREIGN KEY (ma_san_pham) REFERENCES SanPham (ma_san_pham);

-- Bảng KichThuocSanPham.
ALTER TABLE KichThuocSanPham ADD CONSTRAINT fk_soluongsanpham_masanpham FOREIGN KEY (ma_san_pham) REFERENCES SanPham (ma_kich_thuoc)

-- ==================================================================================
