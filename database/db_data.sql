INSERT INTO SanPham (
    ten_san_pham, gia_nhap, gia_xuat, trong_luong, ma_kich_thuoc, gioi_tinh,
    so_luong, don_vi_tinh, trang_thai, mo_ta,
    ngay_tao, ngay_chinh_sua, hinh_anh,
    ma_danh_muc, loai_san_pham, bo_suu_tap, thuong_hieu
)
VALUES
('Nhẫn vàng 18K đính đá', 3500000, 4200000, 3.5, 16, 1, 20, 'chiếc', 1, 'Nhẫn vàng 18K đính đá sang trọng', NOW(), NOW(), NULL, 1, 1, 1, 1),
('Dây chuyền bạc nữ', 800000, 1200000, 5.2, 45, 0, 30, 'chiếc', 1, 'Dây chuyền bạc phong cách trẻ trung', NOW(), NOW(), NULL, 2, 2, 1, 2),
('Vòng tay vàng 24K', 5200000, 6000000, 7.0, 18, 1, 15, 'chiếc', 1, 'Vòng tay vàng 24K truyền thống', NOW(), NOW(), NULL, 1, 3, 2, 1),
('Bông tai bạc nữ', 400000, 650000, 2.1, 3, 0, 50, 'đôi', 1, 'Bông tai bạc thiết kế đơn giản', NOW(), NOW(), NULL, 2, 4, 1, 2),
('Nhẫn cưới vàng trắng', 7000000, 8500000, 4.8, 17, 2, 10, 'cặp', 1, 'Nhẫn cưới vàng trắng cao cấp', NOW(), NOW(), NULL, 1, 1, 3, 3),
('Lắc tay bạc nam', 900000, 1300000, 6.5, 20, 1, 25, 'chiếc', 1, 'Lắc tay bạc dành cho nam', NOW(), NOW(), NULL, 3, 3, 2, 2),
('Dây chuyền vàng nữ', 4500000, 5200000, 6.0, 42, 0, 18, 'chiếc', 1, 'Dây chuyền vàng nữ thanh lịch', NOW(), NOW(), NULL, 1, 2, 3, 1),
('Bông tai ngọc trai', 1500000, 2100000, 2.8, 4, 0, 22, 'đôi', 1, 'Bông tai ngọc trai sang trọng', NOW(), NOW(), NULL, 2, 4, 2, 4),
('Nhẫn bạc nam', 600000, 950000, 3.9, 18, 1, 40, 'chiếc', 1, 'Nhẫn bạc phong cách nam tính', NOW(), NOW(), NULL, 3, 1, 1, 2),
('Vòng cổ phong thủy', 1200000, 1800000, 8.2, 50, 2, 12, 'chiếc', 1, 'Vòng cổ phong thủy mang ý nghĩa may mắn', NOW(), NOW(), NULL, 4, 2, 4, 5),
('Vòng Bạc Pandora Moments Dây Mềm Khóa Tròn', 1500000, 1990000, 8.5, 20, 1, 12, 'chiếc', 1, 'Khởi đầu câu chuyện Pandora của bạn với chiếc Vòng Bạc Pandora Moments Dây Mềm Khóa Tròn', NOW(), NOW(), NULL, 3, 2, 4, 6);


-- INSERT INTO DanhMuc (ma_danh_muc, ten_danh_muc, mo_ta, trang_thai)
-- VALUES
-- (1, 'Trang sức', 'Các sản phẩm liên quan đến vòng tay, Charms, dây chuyền.', 1),
-- (2, 'Vòng tay', 'Các sản phẩm liên quan đến vòng tay', 1),
-- (3, 'Charms', 'Các sản phẩm charms và mặt dây chuyền, vòng tay.', 1),
-- (4, 'Dây chuyền', 'Các sản phẩm liên quan đến dây chuyền.', 1),
-- (5, 'Hoa tai', 'Các sản phẩm liên quan đến hoa tai.', 1),
-- (6, 'Nhẫn', 'Các sản phẩm liên quan đến nhẫn.', 1),
-- (7, 'Quà tặng', 'Các trang sức liên quan đến quà tặng.', 1);

-- INSERT INTO LoaiSanPham (ma_loai_san_pham, ten_loai_san_pham, ma_danh_muc, slug)
-- VALUES
-- (1, 'Vòng tay mềm', 2, 'vong-tay-mem'),
-- (2, 'Vòng dây da', 2, 'vong-day-da'),
-- (3, 'Vòng đính đá', 2, 'vong-dinh-da'),
-- (4, 'Vòng kiềng', 2, 'vong-kieng'),

-- (5, 'Charm bấm', 3, 'charm-bam'),
-- (6, 'Charm treo', 3, 'charm-treo'),
-- (7, 'Charm thủy tinh', 3, 'charm-thuy-tinh'),
-- (8, 'Charm đính đá', 3, 'charm-dinh-da'),

-- (9, 'Dây chuyền bạc', 4, 'day-chuyen-bac'),
-- (10, 'Dây chuyền mạ vàng', 4, 'day-chuyen-ma-vang'),
-- (11, 'Dây chuyền mạ vàng hồng', 4, 'day-chuyen-ma-vang-hong'),

-- (12, 'Hoa tai kiểu tròn', 5, 'hoa-tai-kieu-tron'),
-- (13, 'Hoa tai ngọc trai', 5, 'hoa-tai-ngoc-trai'),
-- (14, 'Hoa tai kiểu rơi', 5, 'hoa-tai-kieu-roi'),

-- (15, 'Nhẫn mạ bạc', 6, 'nhan-ma-bac'),
-- (16, 'Nhẫn mạ vàng', 6, 'nhan-ma-vang'),
-- (17, 'Nhẫn mạ vàng hồng', 6, 'nhan-ma-vang-hong'),

-- (18, 'Charms', 7, 'qua-tang-charms'),
-- (19, 'Vòng tay', 7, 'qua-tang-vong-tay'),
-- (20, 'Dây chuyền', 7, 'qua-tang-day-chuyen'),
-- (21, 'Nhẫn', 7, 'qua-tang-nhan'),
-- (22, 'Hoa tai', 7, 'qua-tang-hoa-tai');

-- INSERT INTO ChatLieu (ma_chat_lieu, ten_chat_lieu)
-- VALUES
-- (1, 'Bạc'),
-- (2, 'Mạ vàng 14K'),
-- (3, 'Mạ vàng hồng 14K'),
-- (4, 'Two-tone'),
-- (5, 'Glass');

-- INSERT INTO TaiKhoan (
--     ma_tai_khoan, ten_tai_khoan, mat_khau, ho_ten,
--     ngay_sinh, gioi_tinh, so_dien_thoai, email,
--     dia_chi, trang_thai, role
-- )
-- VALUES
-- (1, 'admin', 'admin123', 'Nguyễn Chiến Thắng', '2005-01-01', 1, '0837555958', 'chienthang@gmail.com', 'Xã Bình Hiệp, Tỉnh Tây Ninh', 1, 1),
-- (2, 'kh01', 'kh002', 'Châu Kim Xuân', '2005-09-10', 0, '0987125436', 'kimxuan@gmail.com', 'Phường 11, Thành phố Hồ Chí Minh', 1, 0),
-- (3, 'kh03', 'kh003', 'Nguyễn Thái Nguyên', '2005-05-25', 1, '083552957', 'thainguyen@gmail.com', 'Phường Kiến Tường, Tỉnh Tây Ninh', 1, 0),
-- (4, 'kh04', 'kh004', 'Trần Thị Bích Ngọc', '2003-11-12', 0, '0912345678', 'bichngoc@gmail.com', 'Quận 3, TP.HCM', 1, 0),
-- (5, 'kh05', 'kh005', 'Lê Minh Tuấn', '2000-07-08', 1, '0987654321', 'minhtuan@gmail.com', 'Quận Ninh Kiều, TP. Cần Thơ', 1, 0),
-- (6, 'kh06', 'kh006', 'Phạm Thuỳ Linh', '2004-02-20', 0, '0909123456', 'thuylinh@gmail.com', 'TP. Thủ Đức, TP.HCM', 1, 0),
-- (7, 'kh07', 'kh007', 'Võ Quốc Huy', '1999-09-15', 1, '0978123456', 'quochuy@gmail.com', 'TP. Biên Hoà, Đồng Nai', 1, 0),
-- (8, 'kh08', 'kh008', 'Nguyễn Mỹ Duyên', '2001-06-30', 0, '0845123789', 'myduyen@gmail.com', 'TP. Mỹ Tho, Tiền Giang', 1, 0),
-- (9, 'kh09', 'kh009', 'Đặng Hoàng Phúc', '2002-01-05', 1, '0934567890', 'hoangphuc@gmail.com', 'Quận Hải Châu, Đà Nẵng', 1, 0),
-- (10, 'kh10', 'kh010', 'Huỳnh Ngọc Trâm', '2005-10-18', 0, '0856789123', 'ngoctram@gmail.com', 'TP. Bến Tre, Bến Tre', 1, 0),
-- (11, 'kh11', 'kh011', 'Trương Gia Bảo', '1998-12-22', 1, '0812345987', 'giabao@gmail.com', 'TP. Long Xuyên, An Giang', 1, 0),
-- (12, 'kh12', 'kh012', 'Nguyễn Thanh Hằng', '2003-04-09', 0, '0823456798', 'thanhhang@gmail.com', 'Quận Bình Thạnh, TP.HCM', 1, 0);

-- INSERT INTO DanhGia (
--     ma_danh_gia,
--     ma_san_pham,
--     nguoi_danh_gia,
--     noi_dung,
--     ngay_tao,
--     ngay_chinh_sua,
--     trang_thai
-- )
-- VALUES
-- -- Sản phẩm 1
-- (1,  1,  3,  'Sản phẩm đẹp, đóng gói kỹ',        NOW(), NOW(), 1),
-- (2,  1,  4,  'Dùng ổn, đúng mô tả',              NOW(), NOW(), 1),
-- (3,  1,  5,  'Giá hợp lý, sẽ mua lại',           NOW(), NOW(), 1),

-- -- Sản phẩm 2
-- (4,  2,  6,  'Chất lượng tốt trong tầm giá',     NOW(), NOW(), 1),
-- (5,  2,  7,  'Giao hàng nhanh',                  NOW(), NOW(), 1),
-- (6,  2,  8,  'Nhìn chung là ổn',                 NOW(), NOW(), 1),

-- -- Sản phẩm 3
-- (7,  3,  9,  'Sản phẩm đúng như hình',           NOW(), NOW(), 1),
-- (8,  3, 10,  'Xài ok, không có gì chê',          NOW(), NOW(), 1),
-- (9,  3, 11,  'Chất lượng khá tốt',               NOW(), NOW(), 1),

-- -- Sản phẩm 4
-- (10, 4, 12,  'Màu sắc đẹp',                      NOW(), NOW(), 1),
-- (11, 4,  3,  'Cầm chắc tay',                     NOW(), NOW(), 1),
-- (12, 4,  4,  'Đáng tiền',                        NOW(), NOW(), 1),

-- -- Sản phẩm 5
-- (13, 5,  5,  'Sản phẩm dùng ổn',                 NOW(), NOW(), 1),
-- (14, 5,  6,  'Đóng gói cẩn thận',                NOW(), NOW(), 1),
-- (15, 5,  7,  'Sẽ ủng hộ thêm',                   NOW(), NOW(), 1),

-- -- Sản phẩm 6
-- (16, 6,  8,  'Chất liệu tốt',                    NOW(), NOW(), 1),
-- (17, 6,  9,  'Không bị lỗi',                     NOW(), NOW(), 1),
-- (18, 6, 10,  'Giá ok',                           NOW(), NOW(), 1),

-- -- Sản phẩm 7
-- (19, 7, 11,  'Dùng rất ổn',                      NOW(), NOW(), 1),
-- (20, 7, 12,  'Hài lòng',                         NOW(), NOW(), 1),
-- (21, 7,  3,  'Sản phẩm đúng mô tả',              NOW(), NOW(), 1),

-- -- Sản phẩm 8
-- (22, 8,  4,  'Chất lượng khá',                   NOW(), NOW(), 1),
-- (23, 8,  5,  'Giao hàng nhanh',                  NOW(), NOW(), 1),
-- (24, 8,  6,  'Ổn áp',                            NOW(), NOW(), 1),

-- -- Sản phẩm 9
-- (25, 9,  7,  'Đáng mua',                         NOW(), NOW(), 1),
-- (26, 9,  8,  'Sản phẩm tốt',                     NOW(), NOW(), 1),
-- (27, 9,  9,  'Không có gì phàn nàn',             NOW(), NOW(), 1),

-- -- Sản phẩm 10
-- (28, 10, 10, 'Mẫu mã đẹp',                       NOW(), NOW(), 1),
-- (29, 10, 11, 'Chất lượng ổn',                    NOW(), NOW(), 1),
-- (30, 10, 12, 'Sẽ giới thiệu bạn bè',             NOW(), NOW(), 1),

-- -- Sản phẩm 11
-- (31, 11,  3, 'Dùng ổn định',                     NOW(), NOW(), 1),
-- (32, 11,  4, 'Khá hài lòng',                     NOW(), NOW(), 1),
-- (33, 11,  5, 'Ổn trong tầm giá',                 NOW(), NOW(), 1),

-- -- Sản phẩm 12
-- (34, 12,  6, 'Sản phẩm tốt',                     NOW(), NOW(), 1),
-- (35, 12,  7, 'Không lỗi',                        NOW(), NOW(), 1),
-- (36, 12,  8, 'Đúng như mô tả',                   NOW(), NOW(), 1),

-- -- Sản phẩm 13
-- (37, 13,  9, 'Dùng lâu vẫn ok',                  NOW(), NOW(), 1),
-- (38, 13, 10, 'Chất lượng ổn',                    NOW(), NOW(), 1),
-- (39, 13, 11, 'Sẽ mua lại',                       NOW(), NOW(), 1),

-- -- Sản phẩm 14
-- (40, 14, 12, 'Thiết kế đẹp',                     NOW(), NOW(), 1),
-- (41, 14,  3, 'Cảm giác dùng tốt',                NOW(), NOW(), 1),
-- (42, 14,  4, 'Giá hợp lý',                       NOW(), NOW(), 1),

-- -- Sản phẩm 15
-- (43, 15,  5, 'Không có lỗi',                     NOW(), NOW(), 1),
-- (44, 15,  6, 'Sản phẩm ổn',                      NOW(), NOW(), 1),
-- (45, 15,  7, 'Hài lòng',                         NOW(), NOW(), 1),

-- -- Sản phẩm 16
-- (46, 16,  8, 'Dùng rất ok',                      NOW(), NOW(), 1),
-- (47, 16,  9, 'Chất lượng tốt',                   NOW(), NOW(), 1),
-- (48, 16, 10, 'Ổn áp',                            NOW(), NOW(), 1),

-- -- Sản phẩm 17
-- (49, 17, 11, 'Mua về dùng thấy ổn',              NOW(), NOW(), 1),
-- (50, 17, 12, 'Không thất vọng',                  NOW(), NOW(), 1),
-- (51, 17,  3, 'Đáng tiền',                        NOW(), NOW(), 1),

-- -- Sản phẩm 18
-- (52, 18,  4, 'Dùng tốt',                         NOW(), NOW(), 1),
-- (53, 18,  5, 'Sản phẩm ổn',                      NOW(), NOW(), 1),
-- (54, 18,  6, 'Chất lượng khá',                   NOW(), NOW(), 1),

-- -- Sản phẩm 19
-- (55, 19,  7, 'Không lỗi vặt',                    NOW(), NOW(), 1),
-- (56, 19,  8, 'Giao hàng nhanh',                  NOW(), NOW(), 1),
-- (57, 19,  9, 'Ok trong tầm giá',                 NOW(), NOW(), 1),

-- -- Sản phẩm 20
-- (58, 20, 10, 'Sản phẩm tốt',                     NOW(), NOW(), 1),
-- (59, 20, 11, 'Hài lòng',                         NOW(), NOW(), 1),
-- (60, 20, 12, 'Sẽ ủng hộ thêm',                   NOW(), NOW(), 1);

-- INSERT INTO ThuongHieu (
--     ma_thuong_hieu,
--     ten_thuong_hieu,
--     so_dien_thoai,
--     email,
--     dia_chi
-- )
-- VALUES
-- (1, 'Pandora Global',                 '+45 3672 0044', 'info@pandora.net',         'Havneholmen 17-19, 1561 Copenhagen V, Đan Mạch'),
-- (2, 'Pandora Vietnam',                '028 7300 6699', 'cs@pandora.vn',             'Tầng 15, Tòa nhà Vincom Center, TP. Hồ Chí Minh'),
-- (3, 'Pandora Manufacturing Thailand', NULL,           'manufacturing@pandora.net', 'Bangkok, Thái Lan'),
-- (4, 'Pandora Italy Design',           NULL,           'design@pandora.net',        'Milan, Ý'),
-- (5, 'Pandora Distribution Asia',      NULL,           'asia@pandora.net',          'Singapore'),
-- (6, 'Pandora Retail & Franchise',     NULL,           'retail@pandora.net',        'Khu vực Châu Á – Thái Bình Dương');

-- INSERT INTO BoSuuTap (
--     ma_bo_suu_tap,
--     ten_bo_suu_tap,
--     mo_ta,
--     trang_thai
-- )
-- VALUES
-- (1,  'Zodiac Signs', 
--      'Trang sức lấy cảm hứng từ 12 cung hoàng đạo, thể hiện cá tính và dấu ấn riêng.', 1),

-- (2,  'Bảng Chữ Cái', 
--      'Charm chữ cái tinh tế, hoàn hảo để cá nhân hóa theo tên và thông điệp.', 1),

-- (3,  'Stranger Things x Pandora', 
--      'Thiết kế độc đáo lấy cảm hứng từ series Stranger Things đình đám.', 1),

-- (4,  'Unicef x Pandora', 
--      'Trang sức mang thông điệp nhân văn, kết hợp vẻ đẹp tối giản và ý nghĩa.', 1),

-- (5,  'Game of Thrones x Pandora', 
--      'Thiết kế mạnh mẽ, lấy cảm hứng từ thế giới huyền thoại Game of Thrones.', 1),

-- (6,  'Disney x Pandora', 
--      'Trang sức ngọt ngào tái hiện các nhân vật Disney kinh điển.', 1),

-- (7,  'Marvel x Pandora', 
--      'Phong cách cá tính, dành cho fan siêu anh hùng Marvel.', 1),

-- (8,  'Tự Hào Việt Nam', 
--      'Trang sức hiện đại tôn vinh bản sắc và tinh thần Việt.', 1),

-- (9,  'Thiên nhiên và vũ trụ', 
--      'Thiết kế lấy cảm hứng từ thiên nhiên và những vì sao.', 1),

-- (10, 'Vương Quyền', 
--      'Trang sức mang phong cách quyền lực, sang trọng và cuốn hút.', 1),

-- (11, 'Pandora Moments', 
--      'Trang sức quý phái, lịch lãm, sang trọng', 1),

-- (12, 'Pandora Signature', 
--      'Trang sức phong cách, cá tính, sang trọng', 1),

-- (13, 'Pandora Timeless', 
--      'Trang sức phong cách cổ điển, tinh tế, đính đá sang trọng.', 1),

-- (14, 'Pandora Nature', 
--      'Charm lấy cảm hứng từ thiên nhiên, hoa lá và động vật.', 1),

-- (15, 'Pandora Necklace', 
--      'Bộ sưu tập dây chuyền Pandora thanh lịch và hiện đại.', 1);
