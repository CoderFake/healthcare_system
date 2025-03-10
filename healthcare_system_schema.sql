
-- Bảng để lưu trữ thông tin tài khoản đăng nhập
CREATE TABLE IF NOT EXISTS TaiKhoan (
    username TEXT PRIMARY KEY,
    pass TEXT NOT NULL,
    Hovaten TEXT NOT NULL,
    Gioitinh TEXT NOT NULL,
    Quyen TEXT NOT NULL,
    SDT TEXT,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng để lưu trữ thông tin bệnh nhân
CREATE TABLE IF NOT EXISTS BenhNhan (
    MaBN INTEGER PRIMARY KEY AUTOINCREMENT,
    Ho TEXT NOT NULL,
    Ten TEXT NOT NULL,
    CMND TEXT NOT NULL UNIQUE,
    Gioitinh TEXT NOT NULL,
    Ngaysinh TEXT NOT NULL,
    SDT TEXT,
    Quequan TEXT,
    Ngaykham TEXT,
    DiaChi TEXT,
    Email TEXT,
    GhiChu TEXT,
    NhomMau TEXT,
    ChieuCao REAL,
    CanNang REAL,
    TienSuBenhAn TEXT,
    DiUng TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng để lưu trữ thông tin bác sĩ
CREATE TABLE IF NOT EXISTS BacSi (
    MaBS INTEGER PRIMARY KEY AUTOINCREMENT,
    Ho TEXT NOT NULL,
    Ten TEXT NOT NULL,
    CMND TEXT NOT NULL UNIQUE,
    Gioitinh TEXT NOT NULL,
    Ngaysinh TEXT NOT NULL,
    SDT TEXT,
    ChuyenKhoa TEXT NOT NULL,
    Email TEXT,
    DiaChi TEXT,
    BangCap TEXT,
    GhiChu TEXT,
    username TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (username) REFERENCES TaiKhoan(username)
);

-- Bảng để lưu trữ thông tin lịch khám
CREATE TABLE IF NOT EXISTS LichKham (
    MaLichKham INTEGER PRIMARY KEY AUTOINCREMENT,
    MaBN INTEGER,
    MaBS INTEGER,
    NgayKham TEXT,
    GioKham TEXT,
    LydoKham TEXT,
    TrangThai TEXT DEFAULT 'Chờ khám',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (MaBN) REFERENCES BenhNhan(MaBN),
    FOREIGN KEY (MaBS) REFERENCES BacSi(MaBS)
);

-- Bảng để lưu trữ thông tin hồ sơ bệnh án
CREATE TABLE IF NOT EXISTS HoSoBenhAn (
    MaHoSo INTEGER PRIMARY KEY AUTOINCREMENT,
    MaBN INTEGER,
    MaBS INTEGER,
    NgayKham TEXT,
    ChanDoan TEXT,
    TrieuChung TEXT,
    HuongDieuTri TEXT,
    DonThuoc TEXT,
    KetLuan TEXT,
    GhiChu TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (MaBN) REFERENCES BenhNhan(MaBN),
    FOREIGN KEY (MaBS) REFERENCES BacSi(MaBS)
);

-- Bảng để lưu trữ cài đặt ứng dụng
CREATE TABLE IF NOT EXISTS AppSettings (
    setting_key TEXT PRIMARY KEY,
    setting_value TEXT,
    setting_type TEXT,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng để lưu trữ thông tin về các migration đã chạy
CREATE TABLE IF NOT EXISTS migrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    migration_name TEXT NOT NULL,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index để tăng hiệu năng truy vấn
CREATE INDEX IF NOT EXISTS idx_bacsi_chuyenkhoa ON BacSi(ChuyenKhoa);
CREATE INDEX IF NOT EXISTS idx_lichkham_ngaykham ON LichKham(NgayKham);
CREATE INDEX IF NOT EXISTS idx_lichkham_mabs ON LichKham(MaBS);
CREATE INDEX IF NOT EXISTS idx_lichkham_mabn ON LichKham(MaBN);
CREATE INDEX IF NOT EXISTS idx_hosoba_mabn ON HoSoBenhAn(MaBN);
CREATE INDEX IF NOT EXISTS idx_hosoba_mabs ON HoSoBenhAn(MaBS);
CREATE INDEX IF NOT EXISTS idx_benhnhan_cmnd ON BenhNhan(CMND);
CREATE INDEX IF NOT EXISTS idx_bacsi_cmnd ON BacSi(CMND);
