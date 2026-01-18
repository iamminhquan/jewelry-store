CREATE TABLE
    SanPham (
        ma_san_pham INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        ten_san_pham VARCHAR(256) NOT NULL,
        gia_nhap DECIMAL(10, 2) NOT NULL,
        gia_xuat DECIMAL(10, 2) NOT NULL,
        trong_luong FLOAT NOT NULL,
        ma_kich_thuoc FLOAT NOT NULL,
        gioi_tinh TINYINT NOT NULL,
        so_luong INT NOT NULL,
        don_vi_tinh VARCHAR(256) NOT NULL,
        trang_thai TINYINT NOT NULL,
        mo_ta TEXT NULL,
        ngay_tao DATETIME NOT NULL,
        ngay_chinh_sua DATETIME NOT NULL,
        hinh_anh INT,
        ma_danh_muc INT,
        loai_san_pham INT,
        bo_suu_tap INT,
        thuong_hieu INT
    );

CREATE TABLE
    HinhAnhSanPham (
        ma_hinh_anh INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        ma_san_pham INT,
        duong_dan VARCHAR(256) NOT NULL,
        anh_chinh TINYINT (1) DEFAULT 0,
        thu_tu_sap_xep INT,
        ngay_tao DATETIME NOT NULL
    );

CREATE TABLE
    ChatLieu (
        ma_chat_lieu INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        ten_chat_lieu VARCHAR(256) NOT NULL
    );

CREATE TABLE
    SanPham__ChatLieu (
        ma_san_pham INT NOT NULL,
        ma_chat_lieu INT NOT NULL,
        PRIMARY KEY (ma_san_pham, ma_chat_lieu),
        FOREIGN KEY (ma_san_pham) REFERENCES SanPham (ma_san_pham),
        FOREIGN KEY (ma_chat_lieu) REFERENCES ChatLieu (ma_chat_lieu)
    );

CREATE TABLE
    DanhMuc (
        ma_danh_muc INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        ten_danh_muc VARCHAR(256) NOT NULL,
        mo_ta TEXT,
        trang_thai TINYINT
    );

CREATE TABLE
    LoaiSanPham (
        ma_loai_san_pham INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        ten_loai_san_pham VARCHAR(256) NOT NULL,
        slug VARCHAR(256)
    );

CREATE TABLE
    BoSuuTap (
        ma_bo_suu_tap INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        ten_bo_suu_tap VARCHAR(256) NOT NULL,
        mo_ta TEXT,
        trang_thai TINYINT
    );

CREATE TABLE
    ThuongHieu (
        ma_thuong_hieu INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        ten_thuong_hieu VARCHAR(256) NOT NULL,
        so_dien_thoai VARCHAR(11),
        email VARCHAR(256),
        dia_chi VARCHAR(256)
    );

CREATE TABLE
    TaiKhoan (
        ma_tai_khoan INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        ten_tai_khoan VARCHAR(256) NOT NULL,
        mat_khau VARCHAR(256) NOT NULL,
        ho_ten VARCHAR(256) NOT NULL,
        ngay_sinh DATETIME NOT NULL,
        gioi_tinh TINYINT NOT NULL,
        so_dien_thoai VARCHAR(11) NOT NULL,
        email VARCHAR(256) NOT NULL,
        dia_chi VARCHAR(256) NOT NULL,
        trang_thai TINYINT NOT NULL,
        role TINYINT NOT NULL
    );

CREATE TABLE
    DanhGia (
        ma_danh_gia INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        ma_san_pham INT NOT NULL,
        noi_dung TEXT NULL,
        nguoi_danh_gia INT NOT NULL,
        ngay_tao DATETIME NOT NULL,
        ngay_chinh_sua DATETIME NOT NULL,
        trang_thai TINYINT
    );

CREATE TABLE
    GioHang (
        ma_gio_hang INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        ma_tai_khoan INT NOT NULL,
        ngay_tao DATETIME,
        ngay_chinh_sua DATETIME,
        trang_thai TINYINT
    );

CREATE TABLE
    ChiTietGioHang (
        ma_chi_tiet_gio_hang INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        ma_gio_hang INT NOT NULL,
        ma_san_pham INT NOT NULL,
        so_luong INT NOT NULL,
        ngay_tao DATETIME,
        gia_tai_thoi_diem DECIMAL(10, 2)
    );

CREATE TABLE
    DonHang (
        ma_don_hang INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        ma_tai_khoan INT NOT NULL,
        tong_tien_tam_tinh DECIMAL(10, 2),
        ngay_tao DATETIME,
        ngay_dat_hang DATETIME,
        trang_thai TINYINT
    );

CREATE TABLE
    ChiTietDonHang (
        ma_chi_tiet_don_hang INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        ma_don_hang INT NOT NULL,
        ma_san_pham INT NOT NULL,
        so_luong INT NOT NULL,
        don_gia DECIMAL(10, 2),
        thanh_tien DECIMAL(10, 2),
        ngay_tao DATETIME
    );

CREATE TABLE
    HoaDon (
        ma_hoa_don INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        ma_tai_khoan INT NOT NULL,
        tong_tien_tam_tinh DECIMAL(10, 2),
        ngay_tao DATETIME,
        ngay_dat_hang DATETIME,
        trang_thai TINYINT
    );

CREATE TABLE
    ChiTietHoaDon (
        ma_chi_tiet_hoa_don INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        ma_hoa_don INT NOT NULL,
        ma_san_pham INT NOT NULL,
        so_luong INT NOT NULL,
        don_gia DECIMAL(10, 2),
        thanh_tien DECIMAL(10, 2),
        ngay_tao DATETIME
    );


CREATE TABLE
    KichThuocSanPham (
        ma_kich_thuoc_san_pham INT PRIMARY KEY AUTO_INCREMENT,
        ma_san_pham INT NOT NULL,
        ten_kich_thuoc VARCHAR(256) NOT NULL,
        so_luong INT NOT NULL DEFAULT 0
    );