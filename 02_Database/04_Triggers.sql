-- =====================================================
-- PROJE: Spor Salonu Üyelik, Ders, Antrenör ve Ödeme Yönetim Sistemi
-- DOSYA: 04_Triggers.sql
-- AÇIKLAMA: Bu dosyada gerçek hayat iş kurallarını temsil eden trigger kodları bulunur.
-- VERİTABANI: MySQL
-- =====================================================

USE spor_salonu_db;

-- =====================================================
-- TRIGGER 1: trg_odeme_eklendi_uyelik_aktif_yap
-- AÇIKLAMA: Başarılı ödeme eklendiğinde ilgili üyeliği otomatik olarak Aktif yapar.
-- =====================================================

DELIMITER $$

DROP TRIGGER IF EXISTS trg_odeme_eklendi_uyelik_aktif_yap $$

CREATE TRIGGER trg_odeme_eklendi_uyelik_aktif_yap
AFTER INSERT ON odemeler
FOR EACH ROW
BEGIN
    IF NEW.odeme_durumu = 'Başarılı' THEN
        UPDATE uyelikler
        SET durum = 'Aktif'
        WHERE uyelik_id = NEW.uyelik_id;
    END IF;
END $$


-- =====================================================
-- TRIGGER 2: trg_ders_kontenjan_kontrol
-- AÇIKLAMA: Ders kontenjanı doluysa yeni ders kaydını engeller.
-- =====================================================

DROP TRIGGER IF EXISTS trg_ders_kontenjan_kontrol $$

CREATE TRIGGER trg_ders_kontenjan_kontrol
BEFORE INSERT ON ders_kayitlari
FOR EACH ROW
BEGIN
    DECLARE mevcut_kayit INT DEFAULT 0;
    DECLARE ders_kontenjan INT DEFAULT 0;

    SELECT kontenjan
    INTO ders_kontenjan
    FROM dersler
    WHERE ders_id = NEW.ders_id;

    SELECT COUNT(*)
    INTO mevcut_kayit
    FROM ders_kayitlari
    WHERE ders_id = NEW.ders_id
      AND durum <> 'İptal';

    IF NEW.durum <> 'İptal' AND mevcut_kayit >= ders_kontenjan THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Ders kontenjanı dolu olduğu için yeni kayıt yapılamaz.';
    END IF;
END $$


-- =====================================================
-- TRIGGER 3: trg_uyelik_tarih_kontrol
-- AÇIKLAMA: Üyelik bitiş tarihi başlangıç tarihinden önce olamaz.
-- =====================================================

DROP TRIGGER IF EXISTS trg_uyelik_tarih_kontrol $$

CREATE TRIGGER trg_uyelik_tarih_kontrol
BEFORE INSERT ON uyelikler
FOR EACH ROW
BEGIN
    IF NEW.bitis_tarihi < NEW.baslangic_tarihi THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Üyelik bitiş tarihi başlangıç tarihinden önce olamaz.';
    END IF;
END $$

DELIMITER ;