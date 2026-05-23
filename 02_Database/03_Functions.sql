-- =====================================================
-- PROJE: Spor Salonu Üyelik, Ders, Antrenör ve Ödeme Yönetim Sistemi
-- DOSYA: 03_Functions.sql
-- AÇIKLAMA: Bu dosyada senaryo ile ilişkili kullanıcı tanımlı function kodları bulunur.
-- VERİTABANI: MySQL
-- =====================================================

USE spor_salonu_db;

-- =====================================================
-- FUNCTION 1: fn_uye_toplam_odeme
-- AÇIKLAMA: Bir üyenin yaptığı toplam başarılı ödeme tutarını hesaplar.
-- =====================================================

DELIMITER $$

DROP FUNCTION IF EXISTS fn_uye_toplam_odeme $$
CREATE FUNCTION fn_uye_toplam_odeme (
    p_uye_id INT
)
RETURNS DECIMAL(10,2)
READS SQL DATA
BEGIN
    DECLARE toplam DECIMAL(10,2);

    SELECT COALESCE(SUM(o.tutar), 0)
    INTO toplam
    FROM odemeler o
    INNER JOIN uyelikler uy ON o.uyelik_id = uy.uyelik_id
    WHERE uy.uye_id = p_uye_id
      AND o.odeme_durumu = 'Başarılı';

    RETURN toplam;
END $$


-- =====================================================
-- FUNCTION 2: fn_uyelik_kalan_gun
-- AÇIKLAMA: Bir üyeliğin bitiş tarihine kaç gün kaldığını hesaplar.
-- =====================================================

DROP FUNCTION IF EXISTS fn_uyelik_kalan_gun $$
CREATE FUNCTION fn_uyelik_kalan_gun (
    p_uyelik_id INT
)
RETURNS INT
READS SQL DATA
BEGIN
    DECLARE kalan_gun INT;

    SELECT GREATEST(DATEDIFF(bitis_tarihi, CURDATE()), 0)
    INTO kalan_gun
    FROM uyelikler
    WHERE uyelik_id = p_uyelik_id;

    RETURN COALESCE(kalan_gun, 0);
END $$


-- =====================================================
-- FUNCTION 3: fn_ders_doluluk_orani
-- AÇIKLAMA: Bir dersin kontenjanına göre doluluk oranını yüzde olarak hesaplar.
-- =====================================================

DROP FUNCTION IF EXISTS fn_ders_doluluk_orani $$
CREATE FUNCTION fn_ders_doluluk_orani (
    p_ders_id INT
)
RETURNS DECIMAL(5,2)
READS SQL DATA
BEGIN
    DECLARE mevcut_kayit INT;
    DECLARE ders_kontenjan INT;
    DECLARE oran DECIMAL(5,2);

    SELECT kontenjan
    INTO ders_kontenjan
    FROM dersler
    WHERE ders_id = p_ders_id;

    SELECT COUNT(*)
    INTO mevcut_kayit
    FROM ders_kayitlari
    WHERE ders_id = p_ders_id
      AND durum <> 'İptal';

    IF ders_kontenjan IS NULL OR ders_kontenjan = 0 THEN
        SET oran = 0;
    ELSE
        SET oran = (mevcut_kayit / ders_kontenjan) * 100;
    END IF;

    RETURN oran;
END $$

DELIMITER ;