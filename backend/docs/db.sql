CREATE TABLE nguoi_dung (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vai_tro VARCHAR(30) NOT NULL,
    so_dien_thoai VARCHAR(20) NOT NULL,
    email VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE ho_khau (
    id INT AUTO_INCREMENT PRIMARY KEY,
    so_can_ho VARCHAR(10) NOT NULL,
    tang INT NOT NULL,
    toa_nha VARCHAR(30) NOT NULL,
    ngay_lap DATE NULL,
    ngay_chuyen_di DATE NULL,
    dien_tich FLOAT NULL,
    so_xe_may INT NULL,
    so_o_to INT NULL,
    chu_ho_id INT NULL,
    thoi_gian_bat_dau_o DATE NULL,
    thoi_gian_ket_thuc_o DATE NULL,
    trang_thai VARCHAR(20) NOT NULL,
    CONSTRAINT fk_ho_khau_chu_ho FOREIGN KEY (chu_ho_id) REFERENCES nhan_khau(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE nhan_khau (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ho_khau_id INT NOT NULL,
    ho_ten VARCHAR(100) NOT NULL,
    ngay_sinh DATE NOT NULL,
    gioi_tinh VARCHAR(3) NOT NULL,
    ma_can_cuoc VARCHAR(15) NOT NULL,
    so_dien_thoai VARCHAR(15) NOT NULL,
    trang_thai VARCHAR(20) NOT NULL,
    thoi_gian_chuyen_den DATE NOT NULL,
    thoi_gian_chuyen_di DATE NULL,
    quan_he_voi_chu_ho VARCHAR(30) NULL,
    CONSTRAINT fk_nhan_khau_ho_khau FOREIGN KEY (ho_khau_id) REFERENCES ho_khau(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE lich_su_nhan_khau (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nhan_khau_id INT NOT NULL,
    thoi_gian DATE NOT NULL,
    hanh_dong VARCHAR(30) NOT NULL,
    ghi_chu TEXT NULL,
    CONSTRAINT fk_lich_su_nhan_khau_nhan_khau FOREIGN KEY (nhan_khau_id) REFERENCES nhan_khau(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE tam_tru_tam_vang (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nhan_khau_id INT NOT NULL,
    loai VARCHAR(10) NOT NULL,
    thoi_gian_bat_dau DATE NOT NULL,
    thoi_gian_ket_thuc DATE NOT NULL,
    ly_do VARCHAR(255) NOT NULL,
    CONSTRAINT fk_tam_tru_tam_vang_nhan_khau FOREIGN KEY (nhan_khau_id) REFERENCES nhan_khau(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE phuong_tien (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ho_khau_id INT NOT NULL,
    loai_phuong_tien VARCHAR(10) NOT NULL,
    bien_so VARCHAR(50) NOT NULL,
    mau VARCHAR(50) NOT NULL,
    mo_ta TEXT NULL,
    CONSTRAINT fk_phuong_tien_ho_khau FOREIGN KEY (ho_khau_id) REFERENCES ho_khau(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE cap_nhat_phi_sinh_hoat (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ho_khau_id INT NOT NULL,
    tien_dien FLOAT NULL,
    tien_nuoc FLOAT NULL,
    tien_internet FLOAT NULL,
    thang INT NOT NULL,
    nam INT NOT NULL,
    CONSTRAINT fk_cap_nhat_phi_sinh_hoat_ho_khau FOREIGN KEY (ho_khau_id) REFERENCES ho_khau(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE danh_sach_phi_dong_gop (
    ten_phi VARCHAR(30) PRIMARY KEY,
    so_tien_goi_y FLOAT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE dong_gop_phi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phi_ten_phi VARCHAR(30) NOT NULL,
    ho_khau_id INT NOT NULL,
    ngay_dong DATE NOT NULL,
    so_tien_dong FLOAT NOT NULL,
    ghi_chu TEXT NULL,
    CONSTRAINT fk_dong_gop_phi_phi FOREIGN KEY (phi_ten_phi) REFERENCES danh_sach_phi_dong_gop(ten_phi) ON DELETE CASCADE,
    CONSTRAINT fk_dong_gop_phi_ho_khau FOREIGN KEY (ho_khau_id) REFERENCES ho_khau(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE phi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ho_khau_id INT NOT NULL,
    loai_phi VARCHAR(20) NOT NULL,
    gia_phi FLOAT NOT NULL,
    tien_nop_moi_thang FLOAT NOT NULL,
    nam INT NOT NULL,
    CONSTRAINT fk_phi_ho_khau FOREIGN KEY (ho_khau_id) REFERENCES ho_khau(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE chi_tiet_phi_theo_thang (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phi_id INT NOT NULL,
    thang INT NOT NULL,
    so_tien FLOAT NOT NULL,
    CONSTRAINT fk_chi_tiet_phi_theo_thang_phi FOREIGN KEY (phi_id) REFERENCES phi(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE phan_anh (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nhan_khau_id INT NOT NULL,
    ngay_gui DATE NOT NULL,
    noi_dung TEXT NOT NULL,
    trang_thai VARCHAR(20) NOT NULL DEFAULT 'Chưa xử lý',
    phan_hoi TEXT NULL,
    CONSTRAINT fk_phan_anh_nhan_khau FOREIGN KEY (nhan_khau_id) REFERENCES nhan_khau(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
