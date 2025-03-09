SELECT CASE 
    WHEN (SELECT COUNT(*) FROM pragma_table_info('BenhNhan') WHERE name = 'NhomMau') = 0 THEN
        'ALTER TABLE BenhNhan ADD COLUMN NhomMau TEXT;'
    ELSE
        'SELECT 1;'
END;

-- ChieuCao
SELECT CASE 
    WHEN (SELECT COUNT(*) FROM pragma_table_info('BenhNhan') WHERE name = 'ChieuCao') = 0 THEN
        'ALTER TABLE BenhNhan ADD COLUMN ChieuCao REAL;'
    ELSE
        'SELECT 1;'
END;

-- CanNang 
SELECT CASE 
    WHEN (SELECT COUNT(*) FROM pragma_table_info('BenhNhan') WHERE name = 'CanNang') = 0 THEN
        'ALTER TABLE BenhNhan ADD COLUMN CanNang REAL;'
    ELSE
        'SELECT 1;'
END;

-- TienSuBenhAn
SELECT CASE 
    WHEN (SELECT COUNT(*) FROM pragma_table_info('BenhNhan') WHERE name = 'TienSuBenhAn') = 0 THEN
        'ALTER TABLE BenhNhan ADD COLUMN TienSuBenhAn TEXT;'
    ELSE
        'SELECT 1;'
END;

-- DiUng
SELECT CASE 
    WHEN (SELECT COUNT(*) FROM pragma_table_info('BenhNhan') WHERE name = 'DiUng') = 0 THEN
        'ALTER TABLE BenhNhan ADD COLUMN DiUng TEXT;'
    ELSE
        'SELECT 1;'
END;