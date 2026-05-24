-- =====================================================
-- PROJE: Spor Salonu Üyelik, Ders, Antrenör ve Ödeme Yönetim Sistemi
-- DOSYA: 02_StoredProcedures.sql
-- AÇIKLAMA: Bu dosyada her tablo için Insert, Update, Delete ve Select Stored Procedure kodları bulunur.
-- VERİTABANI: MySQL
-- =====================================================

USE spor_salonu_db;

-- =====================================================
-- STORED PROCEDURE 1-4: uyeler tablosu işlemleri
-- AÇIKLAMA: Üye ekleme, güncelleme, silme ve listeleme işlemleri
-- =====================================================

DELIMITER $$

DROP PROCEDURE IF EXISTS sp_uye_ekle $$
CREATE PROCEDURE sp_uye_ekle (
    IN p_ad VARCHAR(50),
    IN p_soyad VARCHAR(50),
    IN p_telefon VARCHAR(20),
    IN p_email VARCHAR(100),
    IN p_cinsiyet ENUM('Erkek', 'Kadın', 'Belirtmek İstemiyor'),
    IN p_dogum_tarihi DATE
)
BEGIN
    INSERT INTO uyeler (
        ad,
        soyad,
        telefon,
        email,
        cinsiyet,
        dogum_tarihi
    )
    VALUES (
        p_ad,
        p_soyad,
        p_telefon,
        p_email,
        p_cinsiyet,
        p_dogum_tarihi
    );
END $$


DROP PROCEDURE IF EXISTS sp_uye_guncelle $$
CREATE PROCEDURE sp_uye_guncelle (
    IN p_uye_id INT,
    IN p_ad VARCHAR(50),
    IN p_soyad VARCHAR(50),
    IN p_telefon VARCHAR(20),
    IN p_email VARCHAR(100),
    IN p_cinsiyet ENUM('Erkek', 'Kadın', 'Belirtmek İstemiyor'),
    IN p_dogum_tarihi DATE,
    IN p_aktif_mi BOOLEAN
)
BEGIN
    UPDATE uyeler
    SET
        ad = p_ad,
        soyad = p_soyad,
        telefon = p_telefon,
        email = p_email,
        cinsiyet = p_cinsiyet,
        dogum_tarihi = p_dogum_tarihi,
        aktif_mi = p_aktif_mi
    WHERE uye_id = p_uye_id;
END $$


DROP PROCEDURE IF EXISTS sp_uye_sil $$
CREATE PROCEDURE sp_uye_sil (
    IN p_uye_id INT
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    ROLLBACK;
    RESIGNAL;
  END;

  START TRANSACTION;

  -- Bağlı yoklama kayıtları
  DELETE y FROM yoklamalar y
  INNER JOIN ders_kayitlari dk ON y.ders_kayit_id = dk.ders_kayit_id
  WHERE dk.uye_id = p_uye_id;

  -- Ders kayıtları
  DELETE FROM ders_kayitlari WHERE uye_id = p_uye_id;

  -- Üyeliğe bağlı ödemeler
  DELETE o FROM odemeler o
  INNER JOIN uyelikler u ON o.uyelik_id = u.uyelik_id
  WHERE u.uye_id = p_uye_id;

  -- Üyelikler
  DELETE FROM uyelikler WHERE uye_id = p_uye_id;

  -- Üye
  DELETE FROM uyeler WHERE uye_id = p_uye_id;

  COMMIT;
END $$


DROP PROCEDURE IF EXISTS sp_uye_listele $$
CREATE PROCEDURE sp_uye_listele ()
BEGIN
    SELECT
        uye_id,
        ad,
        soyad,
        telefon,
        email,
        cinsiyet,
        dogum_tarihi,
        kayit_tarihi,
        aktif_mi
    FROM uyeler
    ORDER BY uye_id DESC;
END $$

DELIMITER ;

-- =====================================================
-- STORED PROCEDURE 5-8: antrenorler tablosu işlemleri
-- AÇIKLAMA: Antrenör ekleme, güncelleme, silme ve listeleme işlemleri
-- =====================================================

DELIMITER $$

DROP PROCEDURE IF EXISTS sp_antrenor_ekle $$
CREATE PROCEDURE sp_antrenor_ekle (
    IN p_ad VARCHAR(50),
    IN p_soyad VARCHAR(50),
    IN p_telefon VARCHAR(20),
    IN p_email VARCHAR(100),
    IN p_uzmanlik_alani VARCHAR(100),
    IN p_maas DECIMAL(10,2),
    IN p_ise_baslama_tarihi DATE
)
BEGIN
    INSERT INTO antrenorler (
        ad,
        soyad,
        telefon,
        email,
        uzmanlik_alani,
        maas,
        ise_baslama_tarihi
    )
    VALUES (
        p_ad,
        p_soyad,
        p_telefon,
        p_email,
        p_uzmanlik_alani,
        p_maas,
        p_ise_baslama_tarihi
    );
END $$


DROP PROCEDURE IF EXISTS sp_antrenor_guncelle $$
CREATE PROCEDURE sp_antrenor_guncelle (
    IN p_antrenor_id INT,
    IN p_ad VARCHAR(50),
    IN p_soyad VARCHAR(50),
    IN p_telefon VARCHAR(20),
    IN p_email VARCHAR(100),
    IN p_uzmanlik_alani VARCHAR(100),
    IN p_maas DECIMAL(10,2),
    IN p_ise_baslama_tarihi DATE,
    IN p_aktif_mi BOOLEAN
)
BEGIN
    UPDATE antrenorler
    SET
        ad = p_ad,
        soyad = p_soyad,
        telefon = p_telefon,
        email = p_email,
        uzmanlik_alani = p_uzmanlik_alani,
        maas = p_maas,
        ise_baslama_tarihi = p_ise_baslama_tarihi,
        aktif_mi = p_aktif_mi
    WHERE antrenor_id = p_antrenor_id;
END $$


DROP PROCEDURE IF EXISTS sp_antrenor_sil $$
CREATE PROCEDURE sp_antrenor_sil (
    IN p_antrenor_id INT
)
BEGIN
    DELETE FROM antrenorler
    WHERE antrenor_id = p_antrenor_id;
END $$


DROP PROCEDURE IF EXISTS sp_antrenor_listele $$
CREATE PROCEDURE sp_antrenor_listele ()
BEGIN
    SELECT
        antrenor_id,
        ad,
        soyad,
        telefon,
        email,
        uzmanlik_alani,
        maas,
        ise_baslama_tarihi,
        aktif_mi
    FROM antrenorler
    ORDER BY antrenor_id DESC;
END $$

DELIMITER ;

-- =====================================================
-- STORED PROCEDURE 9-12: uyelik_paketleri tablosu işlemleri
-- AÇIKLAMA: Üyelik paketi ekleme, güncelleme, silme ve listeleme işlemleri
-- =====================================================

DELIMITER $$

DROP PROCEDURE IF EXISTS sp_uyelik_paketi_ekle $$
CREATE PROCEDURE sp_uyelik_paketi_ekle (
    IN p_paket_adi VARCHAR(100),
    IN p_sure_gun INT,
    IN p_ucret DECIMAL(10,2),
    IN p_aciklama VARCHAR(255)
)
BEGIN
    INSERT INTO uyelik_paketleri (
        paket_adi,
        sure_gun,
        ucret,
        aciklama
    )
    VALUES (
        p_paket_adi,
        p_sure_gun,
        p_ucret,
        p_aciklama
    );
END $$


DROP PROCEDURE IF EXISTS sp_uyelik_paketi_guncelle $$
CREATE PROCEDURE sp_uyelik_paketi_guncelle (
    IN p_paket_id INT,
    IN p_paket_adi VARCHAR(100),
    IN p_sure_gun INT,
    IN p_ucret DECIMAL(10,2),
    IN p_aciklama VARCHAR(255),
    IN p_aktif_mi BOOLEAN
)
BEGIN
    UPDATE uyelik_paketleri
    SET
        paket_adi = p_paket_adi,
        sure_gun = p_sure_gun,
        ucret = p_ucret,
        aciklama = p_aciklama,
        aktif_mi = p_aktif_mi
    WHERE paket_id = p_paket_id;
END $$


DROP PROCEDURE IF EXISTS sp_uyelik_paketi_sil $$
CREATE PROCEDURE sp_uyelik_paketi_sil (
    IN p_paket_id INT
)
BEGIN
    DELETE FROM uyelik_paketleri
    WHERE paket_id = p_paket_id;
END $$


DROP PROCEDURE IF EXISTS sp_uyelik_paketi_listele $$
CREATE PROCEDURE sp_uyelik_paketi_listele ()
BEGIN
    SELECT
        paket_id,
        paket_adi,
        sure_gun,
        ucret,
        aciklama,
        aktif_mi
    FROM uyelik_paketleri
    ORDER BY paket_id DESC;
END $$

DELIMITER ;

-- =====================================================
-- STORED PROCEDURE 13-16: uyelikler tablosu işlemleri
-- AÇIKLAMA: Üyeye paket atama, üyelik güncelleme, silme ve listeleme işlemleri
-- =====================================================

DELIMITER $$

DROP PROCEDURE IF EXISTS sp_uyelik_ekle $$
CREATE PROCEDURE sp_uyelik_ekle (
    IN p_uye_id INT,
    IN p_paket_id INT,
    IN p_baslangic_tarihi DATE,
    IN p_bitis_tarihi DATE,
    IN p_durum ENUM('Aktif', 'Pasif', 'Donduruldu', 'Süresi Doldu')
)
BEGIN
    INSERT INTO uyelikler (
        uye_id,
        paket_id,
        baslangic_tarihi,
        bitis_tarihi,
        durum
    )
    VALUES (
        p_uye_id,
        p_paket_id,
        p_baslangic_tarihi,
        p_bitis_tarihi,
        p_durum
    );
END $$


DROP PROCEDURE IF EXISTS sp_uyelik_guncelle $$
CREATE PROCEDURE sp_uyelik_guncelle (
    IN p_uyelik_id INT,
    IN p_uye_id INT,
    IN p_paket_id INT,
    IN p_baslangic_tarihi DATE,
    IN p_bitis_tarihi DATE,
    IN p_durum ENUM('Aktif', 'Pasif', 'Donduruldu', 'Süresi Doldu')
)
BEGIN
    UPDATE uyelikler
    SET
        uye_id = p_uye_id,
        paket_id = p_paket_id,
        baslangic_tarihi = p_baslangic_tarihi,
        bitis_tarihi = p_bitis_tarihi,
        durum = p_durum
    WHERE uyelik_id = p_uyelik_id;
END $$


DROP PROCEDURE IF EXISTS sp_uyelik_sil $$
CREATE PROCEDURE sp_uyelik_sil (
    IN p_uyelik_id INT
)
BEGIN
    DELETE FROM uyelikler
    WHERE uyelik_id = p_uyelik_id;
END $$


DROP PROCEDURE IF EXISTS sp_uyelik_listele $$
CREATE PROCEDURE sp_uyelik_listele ()
BEGIN
    SELECT
        uyl.uyelik_id,
        uyl.uye_id,
        CONCAT(u.ad, ' ', u.soyad) AS uye_ad_soyad,
        uyl.paket_id,
        p.paket_adi,
        p.ucret,
        p.sure_gun,
        uyl.baslangic_tarihi,
        uyl.bitis_tarihi,
        uyl.durum,
        uyl.olusturma_tarihi
    FROM uyelikler uyl
    INNER JOIN uyeler u ON uyl.uye_id = u.uye_id
    INNER JOIN uyelik_paketleri p ON uyl.paket_id = p.paket_id
    ORDER BY uyl.uyelik_id DESC;
END $$

DELIMITER ;

-- =====================================================
-- STORED PROCEDURE 17-20: odemeler tablosu işlemleri
-- AÇIKLAMA: Ödeme ekleme, güncelleme, silme ve listeleme işlemleri
-- =====================================================

DELIMITER $$

DROP PROCEDURE IF EXISTS sp_odeme_ekle $$
CREATE PROCEDURE sp_odeme_ekle (
    IN p_uyelik_id INT,
    IN p_tutar DECIMAL(10,2),
    IN p_odeme_yontemi ENUM('Nakit', 'Kart', 'Havale/EFT'),
    IN p_odeme_durumu ENUM('Başarılı', 'Beklemede', 'İptal'),
    IN p_aciklama VARCHAR(255)
)
BEGIN
    INSERT INTO odemeler (
        uyelik_id,
        tutar,
        odeme_yontemi,
        odeme_durumu,
        aciklama
    )
    VALUES (
        p_uyelik_id,
        p_tutar,
        p_odeme_yontemi,
        p_odeme_durumu,
        p_aciklama
    );
END $$


DROP PROCEDURE IF EXISTS sp_odeme_guncelle $$
CREATE PROCEDURE sp_odeme_guncelle (
    IN p_odeme_id INT,
    IN p_uyelik_id INT,
    IN p_tutar DECIMAL(10,2),
    IN p_odeme_yontemi ENUM('Nakit', 'Kart', 'Havale/EFT'),
    IN p_odeme_durumu ENUM('Başarılı', 'Beklemede', 'İptal'),
    IN p_aciklama VARCHAR(255)
)
BEGIN
    UPDATE odemeler
    SET
        uyelik_id = p_uyelik_id,
        tutar = p_tutar,
        odeme_yontemi = p_odeme_yontemi,
        odeme_durumu = p_odeme_durumu,
        aciklama = p_aciklama
    WHERE odeme_id = p_odeme_id;
END $$


DROP PROCEDURE IF EXISTS sp_odeme_sil $$
CREATE PROCEDURE sp_odeme_sil (
    IN p_odeme_id INT
)
BEGIN
    DELETE FROM odemeler
    WHERE odeme_id = p_odeme_id;
END $$


DROP PROCEDURE IF EXISTS sp_odeme_listele $$
CREATE PROCEDURE sp_odeme_listele ()
BEGIN
    SELECT
        o.odeme_id,
        o.uyelik_id,
        CONCAT(u.ad, ' ', u.soyad) AS uye_ad_soyad,
        p.paket_adi,
        o.tutar,
        o.odeme_tarihi,
        o.odeme_yontemi,
        o.odeme_durumu,
        o.aciklama
    FROM odemeler o
    INNER JOIN uyelikler uy ON o.uyelik_id = uy.uyelik_id
    INNER JOIN uyeler u ON uy.uye_id = u.uye_id
    INNER JOIN uyelik_paketleri p ON uy.paket_id = p.paket_id
    ORDER BY o.odeme_id DESC;
END $$

DELIMITER ;

-- =====================================================
-- STORED PROCEDURE 21-24: dersler tablosu işlemleri
-- AÇIKLAMA: Ders ekleme, güncelleme, silme ve listeleme işlemleri
-- =====================================================

DELIMITER $$

DROP PROCEDURE IF EXISTS sp_ders_ekle $$
CREATE PROCEDURE sp_ders_ekle (
    IN p_ders_adi VARCHAR(100),
    IN p_antrenor_id INT,
    IN p_kontenjan INT,
    IN p_ders_gunu ENUM('Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar'),
    IN p_baslangic_saati TIME,
    IN p_bitis_saati TIME
)
BEGIN
    INSERT INTO dersler (
        ders_adi,
        antrenor_id,
        kontenjan,
        ders_gunu,
        baslangic_saati,
        bitis_saati
    )
    VALUES (
        p_ders_adi,
        p_antrenor_id,
        p_kontenjan,
        p_ders_gunu,
        p_baslangic_saati,
        p_bitis_saati
    );
END $$


DROP PROCEDURE IF EXISTS sp_ders_guncelle $$
CREATE PROCEDURE sp_ders_guncelle (
    IN p_ders_id INT,
    IN p_ders_adi VARCHAR(100),
    IN p_antrenor_id INT,
    IN p_kontenjan INT,
    IN p_ders_gunu ENUM('Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar'),
    IN p_baslangic_saati TIME,
    IN p_bitis_saati TIME,
    IN p_aktif_mi BOOLEAN
)
BEGIN
    UPDATE dersler
    SET
        ders_adi = p_ders_adi,
        antrenor_id = p_antrenor_id,
        kontenjan = p_kontenjan,
        ders_gunu = p_ders_gunu,
        baslangic_saati = p_baslangic_saati,
        bitis_saati = p_bitis_saati,
        aktif_mi = p_aktif_mi
    WHERE ders_id = p_ders_id;
END $$


DROP PROCEDURE IF EXISTS sp_ders_sil $$
CREATE PROCEDURE sp_ders_sil (
    IN p_ders_id INT
)
BEGIN
    DELETE FROM dersler
    WHERE ders_id = p_ders_id;
END $$


DROP PROCEDURE IF EXISTS sp_ders_listele $$
CREATE PROCEDURE sp_ders_listele ()
BEGIN
    SELECT
        d.ders_id,
        d.ders_adi,
        d.antrenor_id,
        CONCAT(a.ad, ' ', a.soyad) AS antrenor_ad_soyad,
        a.uzmanlik_alani,
        d.kontenjan,
        d.ders_gunu,
        d.baslangic_saati,
        d.bitis_saati,
        d.aktif_mi
    FROM dersler d
    INNER JOIN antrenorler a ON d.antrenor_id = a.antrenor_id
    ORDER BY d.ders_id DESC;
END $$

DELIMITER ;

-- =====================================================
-- STORED PROCEDURE 25-28: ders_kayitlari tablosu işlemleri
-- AÇIKLAMA: Üyelerin derslere kayıt, güncelleme, silme ve listeleme işlemleri
-- =====================================================

DELIMITER $$

DROP PROCEDURE IF EXISTS sp_ders_kayit_ekle $$
CREATE PROCEDURE sp_ders_kayit_ekle (
    IN p_uye_id INT,
    IN p_ders_id INT,
    IN p_durum ENUM('Kayıtlı', 'İptal', 'Katıldı')
)
BEGIN
    INSERT INTO ders_kayitlari (
        uye_id,
        ders_id,
        durum
    )
    VALUES (
        p_uye_id,
        p_ders_id,
        p_durum
    );
END $$


DROP PROCEDURE IF EXISTS sp_ders_kayit_guncelle $$
CREATE PROCEDURE sp_ders_kayit_guncelle (
    IN p_ders_kayit_id INT,
    IN p_uye_id INT,
    IN p_ders_id INT,
    IN p_durum ENUM('Kayıtlı', 'İptal', 'Katıldı')
)
BEGIN
    UPDATE ders_kayitlari
    SET
        uye_id = p_uye_id,
        ders_id = p_ders_id,
        durum = p_durum
    WHERE ders_kayit_id = p_ders_kayit_id;
END $$


DROP PROCEDURE IF EXISTS sp_ders_kayit_sil $$
CREATE PROCEDURE sp_ders_kayit_sil (
    IN p_ders_kayit_id INT
)
BEGIN
    DELETE FROM ders_kayitlari
    WHERE ders_kayit_id = p_ders_kayit_id;
END $$


DROP PROCEDURE IF EXISTS sp_ders_kayit_listele $$
CREATE PROCEDURE sp_ders_kayit_listele ()
BEGIN
    SELECT
        dk.ders_kayit_id,
        dk.uye_id,
        CONCAT(u.ad, ' ', u.soyad) AS uye_ad_soyad,
        dk.ders_id,
        d.ders_adi,
        d.ders_gunu,
        d.baslangic_saati,
        d.bitis_saati,
        dk.kayit_tarihi,
        dk.durum
    FROM ders_kayitlari dk
    INNER JOIN uyeler u ON dk.uye_id = u.uye_id
    INNER JOIN dersler d ON dk.ders_id = d.ders_id
    ORDER BY dk.ders_kayit_id DESC;
END $$

DELIMITER ;

-- =====================================================
-- STORED PROCEDURE 29-32: yoklamalar tablosu işlemleri
-- AÇIKLAMA: Ders yoklama ekleme, güncelleme, silme ve listeleme işlemleri
-- =====================================================

DELIMITER $$

DROP PROCEDURE IF EXISTS sp_yoklama_ekle $$
CREATE PROCEDURE sp_yoklama_ekle (
    IN p_ders_kayit_id INT,
    IN p_yoklama_tarihi DATE,
    IN p_katilim_durumu ENUM('Katıldı', 'Gelmedi', 'Mazeretli'),
    IN p_aciklama VARCHAR(255)
)
BEGIN
    INSERT INTO yoklamalar (
        ders_kayit_id,
        yoklama_tarihi,
        katilim_durumu,
        aciklama
    )
    VALUES (
        p_ders_kayit_id,
        p_yoklama_tarihi,
        p_katilim_durumu,
        p_aciklama
    );
END $$


DROP PROCEDURE IF EXISTS sp_yoklama_guncelle $$
CREATE PROCEDURE sp_yoklama_guncelle (
    IN p_yoklama_id INT,
    IN p_ders_kayit_id INT,
    IN p_yoklama_tarihi DATE,
    IN p_katilim_durumu ENUM('Katıldı', 'Gelmedi', 'Mazeretli'),
    IN p_aciklama VARCHAR(255)
)
BEGIN
    UPDATE yoklamalar
    SET
        ders_kayit_id = p_ders_kayit_id,
        yoklama_tarihi = p_yoklama_tarihi,
        katilim_durumu = p_katilim_durumu,
        aciklama = p_aciklama
    WHERE yoklama_id = p_yoklama_id;
END $$


DROP PROCEDURE IF EXISTS sp_yoklama_sil $$
CREATE PROCEDURE sp_yoklama_sil (
    IN p_yoklama_id INT
)
BEGIN
    DELETE FROM yoklamalar
    WHERE yoklama_id = p_yoklama_id;
END $$


DROP PROCEDURE IF EXISTS sp_yoklama_listele $$
CREATE PROCEDURE sp_yoklama_listele ()
BEGIN
    SELECT
        y.yoklama_id,
        y.ders_kayit_id,
        CONCAT(u.ad, ' ', u.soyad) AS uye_ad_soyad,
        d.ders_adi,
        y.yoklama_tarihi,
        y.katilim_durumu,
        y.aciklama
    FROM yoklamalar y
    INNER JOIN ders_kayitlari dk ON y.ders_kayit_id = dk.ders_kayit_id
    INNER JOIN uyeler u ON dk.uye_id = u.uye_id
    INNER JOIN dersler d ON dk.ders_id = d.ders_id
    ORDER BY y.yoklama_id DESC;
END $$

DELIMITER ;

-- =====================================================
-- STORED PROCEDURE 33-36: salon_ekipmanlari tablosu işlemleri
-- AÇIKLAMA: Salon ekipmanı ekleme, güncelleme, silme ve listeleme işlemleri
-- =====================================================

DELIMITER $$

DROP PROCEDURE IF EXISTS sp_ekipman_ekle $$
CREATE PROCEDURE sp_ekipman_ekle (
    IN p_ekipman_adi VARCHAR(100),
    IN p_kategori VARCHAR(100),
    IN p_alim_tarihi DATE,
    IN p_durum ENUM('Kullanılabilir', 'Bakımda', 'Arızalı'),
    IN p_aciklama VARCHAR(255)
)
BEGIN
    INSERT INTO salon_ekipmanlari (
        ekipman_adi,
        kategori,
        alim_tarihi,
        durum,
        aciklama
    )
    VALUES (
        p_ekipman_adi,
        p_kategori,
        p_alim_tarihi,
        p_durum,
        p_aciklama
    );
END $$


DROP PROCEDURE IF EXISTS sp_ekipman_guncelle $$
CREATE PROCEDURE sp_ekipman_guncelle (
    IN p_ekipman_id INT,
    IN p_ekipman_adi VARCHAR(100),
    IN p_kategori VARCHAR(100),
    IN p_alim_tarihi DATE,
    IN p_durum ENUM('Kullanılabilir', 'Bakımda', 'Arızalı'),
    IN p_aciklama VARCHAR(255)
)
BEGIN
    UPDATE salon_ekipmanlari
    SET
        ekipman_adi = p_ekipman_adi,
        kategori = p_kategori,
        alim_tarihi = p_alim_tarihi,
        durum = p_durum,
        aciklama = p_aciklama
    WHERE ekipman_id = p_ekipman_id;
END $$


DROP PROCEDURE IF EXISTS sp_ekipman_sil $$
CREATE PROCEDURE sp_ekipman_sil (
    IN p_ekipman_id INT
)
BEGIN
    DELETE FROM salon_ekipmanlari
    WHERE ekipman_id = p_ekipman_id;
END $$


DROP PROCEDURE IF EXISTS sp_ekipman_listele $$
CREATE PROCEDURE sp_ekipman_listele ()
BEGIN
    SELECT
        ekipman_id,
        ekipman_adi,
        kategori,
        alim_tarihi,
        durum,
        aciklama
    FROM salon_ekipmanlari
    ORDER BY ekipman_id DESC;
END $$

DELIMITER ;

-- =====================================================
-- STORED PROCEDURE 37-40: ekipman_bakimlari tablosu işlemleri
-- AÇIKLAMA: Ekipman bakım ekleme, güncelleme, silme ve listeleme işlemleri
-- =====================================================

DELIMITER $$

DROP PROCEDURE IF EXISTS sp_bakim_ekle $$
CREATE PROCEDURE sp_bakim_ekle (
    IN p_ekipman_id INT,
    IN p_bakim_tarihi DATE,
    IN p_aciklama VARCHAR(255),
    IN p_bakim_maliyeti DECIMAL(10,2),
    IN p_bakim_durumu ENUM('Planlandı', 'Tamamlandı', 'İptal')
)
BEGIN
    INSERT INTO ekipman_bakimlari (
        ekipman_id,
        bakim_tarihi,
        aciklama,
        bakim_maliyeti,
        bakim_durumu
    )
    VALUES (
        p_ekipman_id,
        p_bakim_tarihi,
        p_aciklama,
        p_bakim_maliyeti,
        p_bakim_durumu
    );
END $$


DROP PROCEDURE IF EXISTS sp_bakim_guncelle $$
CREATE PROCEDURE sp_bakim_guncelle (
    IN p_bakim_id INT,
    IN p_ekipman_id INT,
    IN p_bakim_tarihi DATE,
    IN p_aciklama VARCHAR(255),
    IN p_bakim_maliyeti DECIMAL(10,2),
    IN p_bakim_durumu ENUM('Planlandı', 'Tamamlandı', 'İptal')
)
BEGIN
    UPDATE ekipman_bakimlari
    SET
        ekipman_id = p_ekipman_id,
        bakim_tarihi = p_bakim_tarihi,
        aciklama = p_aciklama,
        bakim_maliyeti = p_bakim_maliyeti,
        bakim_durumu = p_bakim_durumu
    WHERE bakim_id = p_bakim_id;
END $$


DROP PROCEDURE IF EXISTS sp_bakim_sil $$
CREATE PROCEDURE sp_bakim_sil (
    IN p_bakim_id INT
)
BEGIN
    DELETE FROM ekipman_bakimlari
    WHERE bakim_id = p_bakim_id;
END $$


DROP PROCEDURE IF EXISTS sp_bakim_listele $$
CREATE PROCEDURE sp_bakim_listele ()
BEGIN
    SELECT
        eb.bakim_id,
        eb.ekipman_id,
        se.ekipman_adi,
        se.kategori,
        eb.bakim_tarihi,
        eb.aciklama,
        eb.bakim_maliyeti,
        eb.bakim_durumu
    FROM ekipman_bakimlari eb
    INNER JOIN salon_ekipmanlari se ON eb.ekipman_id = se.ekipman_id
    ORDER BY eb.bakim_id DESC;
END $$

DELIMITER ;