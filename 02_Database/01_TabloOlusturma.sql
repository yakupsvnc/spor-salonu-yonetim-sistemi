-- =====================================================
-- PROJE: Spor Salonu Üyelik, Ders, Antrenör ve Ödeme Yönetim Sistemi
-- DOSYA: 01_TabloOlusturma.sql
-- AÇIKLAMA: Bu dosyada proje için gerekli veritabanı ve tablolar oluşturulacaktır.
-- VERİTABANI: MySQL
-- =====================================================

USE spor_salonu_db;

-- =====================================================
-- TABLO 1: uyeler
-- AÇIKLAMA: Spor salonuna kayıtlı üyelerin bilgilerini tutar.
-- =====================================================

CREATE TABLE IF NOT EXISTS uyeler (
    uye_id INT AUTO_INCREMENT PRIMARY KEY,
    ad VARCHAR(50) NOT NULL,
    soyad VARCHAR(50) NOT NULL,
    telefon VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100) UNIQUE,
    cinsiyet ENUM('Erkek', 'Kadın', 'Belirtmek İstemiyor') DEFAULT 'Belirtmek İstemiyor',
    dogum_tarihi DATE,
    kayit_tarihi DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    aktif_mi BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT chk_uye_ad CHECK (CHAR_LENGTH(ad) >= 2),
    CONSTRAINT chk_uye_soyad CHECK (CHAR_LENGTH(soyad) >= 2)
);

-- =====================================================
-- TABLO 2: antrenorler
-- AÇIKLAMA: Spor salonunda görev yapan antrenörlerin bilgilerini tutar.
-- =====================================================

CREATE TABLE IF NOT EXISTS antrenorler (
    antrenor_id INT AUTO_INCREMENT PRIMARY KEY,
    ad VARCHAR(50) NOT NULL,
    soyad VARCHAR(50) NOT NULL,
    telefon VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100) UNIQUE,
    uzmanlik_alani VARCHAR(100) NOT NULL,
    maas DECIMAL(10,2) NOT NULL DEFAULT 0,
    ise_baslama_tarihi DATE NOT NULL,
    aktif_mi BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT chk_antrenor_ad CHECK (CHAR_LENGTH(ad) >= 2),
    CONSTRAINT chk_antrenor_soyad CHECK (CHAR_LENGTH(soyad) >= 2),
    CONSTRAINT chk_antrenor_maas CHECK (maas >= 0)
);

-- =====================================================
-- TABLO 3: uyelik_paketleri
-- AÇIKLAMA: Spor salonunda satılan üyelik paketlerini tutar.
-- =====================================================

CREATE TABLE IF NOT EXISTS uyelik_paketleri (
    paket_id INT AUTO_INCREMENT PRIMARY KEY,
    paket_adi VARCHAR(100) NOT NULL UNIQUE,
    sure_gun INT NOT NULL,
    ucret DECIMAL(10,2) NOT NULL,
    aciklama VARCHAR(255),
    aktif_mi BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT chk_paket_sure CHECK (sure_gun > 0),
    CONSTRAINT chk_paket_ucret CHECK (ucret > 0)
);

-- =====================================================
-- TABLO 4: uyelikler
-- AÇIKLAMA: Üyelerin satın aldığı üyelik paketlerini ve üyelik durumlarını tutar.
-- =====================================================

CREATE TABLE IF NOT EXISTS uyelikler (
    uyelik_id INT AUTO_INCREMENT PRIMARY KEY,
    uye_id INT NOT NULL,
    paket_id INT NOT NULL,
    baslangic_tarihi DATE NOT NULL,
    bitis_tarihi DATE NOT NULL,
    durum ENUM('Aktif', 'Pasif', 'Donduruldu', 'Süresi Doldu') NOT NULL DEFAULT 'Pasif',
    olusturma_tarihi DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_uyelik_uye FOREIGN KEY (uye_id)
        REFERENCES uyeler(uye_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_uyelik_paket FOREIGN KEY (paket_id)
        REFERENCES uyelik_paketleri(paket_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT chk_uyelik_tarih CHECK (bitis_tarihi >= baslangic_tarihi)
);

-- =====================================================
-- TABLO 5: odemeler
-- AÇIKLAMA: Üyeliklere ait ödeme bilgilerini tutar.
-- =====================================================

CREATE TABLE IF NOT EXISTS odemeler (
    odeme_id INT AUTO_INCREMENT PRIMARY KEY,
    uyelik_id INT NOT NULL,
    tutar DECIMAL(10,2) NOT NULL,
    odeme_tarihi DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    odeme_yontemi ENUM('Nakit', 'Kart', 'Havale/EFT') NOT NULL,
    odeme_durumu ENUM('Başarılı', 'Beklemede', 'İptal') NOT NULL DEFAULT 'Başarılı',
    aciklama VARCHAR(255),

    CONSTRAINT fk_odeme_uyelik FOREIGN KEY (uyelik_id)
        REFERENCES uyelikler(uyelik_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT chk_odeme_tutar CHECK (tutar > 0)
);

-- =====================================================
-- TABLO 6: dersler
-- AÇIKLAMA: Spor salonunda verilen grup derslerini ve ders programını tutar.
-- =====================================================

CREATE TABLE IF NOT EXISTS dersler (
    ders_id INT AUTO_INCREMENT PRIMARY KEY,
    ders_adi VARCHAR(100) NOT NULL,
    antrenor_id INT NOT NULL,
    kontenjan INT NOT NULL,
    ders_gunu ENUM('Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar') NOT NULL,
    baslangic_saati TIME NOT NULL,
    bitis_saati TIME NOT NULL,
    aktif_mi BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT fk_ders_antrenor FOREIGN KEY (antrenor_id)
        REFERENCES antrenorler(antrenor_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT chk_ders_kontenjan CHECK (kontenjan > 0),
    CONSTRAINT chk_ders_saat CHECK (bitis_saati > baslangic_saati)
);

-- =====================================================
-- TABLO 7: ders_kayitlari
-- AÇIKLAMA: Üyelerin grup derslerine kayıt bilgilerini tutar.
-- =====================================================

CREATE TABLE IF NOT EXISTS ders_kayitlari (
    ders_kayit_id INT AUTO_INCREMENT PRIMARY KEY,
    uye_id INT NOT NULL,
    ders_id INT NOT NULL,
    kayit_tarihi DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    durum ENUM('Kayıtlı', 'İptal', 'Katıldı') NOT NULL DEFAULT 'Kayıtlı',

    CONSTRAINT fk_ders_kayit_uye FOREIGN KEY (uye_id)
        REFERENCES uyeler(uye_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_ders_kayit_ders FOREIGN KEY (ders_id)
        REFERENCES dersler(ders_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT uq_uye_ders UNIQUE (uye_id, ders_id)
);

-- =====================================================
-- TABLO 8: yoklamalar
-- AÇIKLAMA: Ders kayıtlarına ait katılım/yoklama bilgilerini tutar.
-- =====================================================

CREATE TABLE IF NOT EXISTS yoklamalar (
    yoklama_id INT AUTO_INCREMENT PRIMARY KEY,
    ders_kayit_id INT NOT NULL,
    yoklama_tarihi DATE NOT NULL,
    katilim_durumu ENUM('Katıldı', 'Gelmedi', 'Mazeretli') NOT NULL DEFAULT 'Gelmedi',
    aciklama VARCHAR(255),

    CONSTRAINT fk_yoklama_ders_kayit FOREIGN KEY (ders_kayit_id)
        REFERENCES ders_kayitlari(ders_kayit_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT uq_ders_kayit_yoklama_tarihi UNIQUE (ders_kayit_id, yoklama_tarihi)
);

-- =====================================================
-- TABLO 9: salon_ekipmanlari
-- AÇIKLAMA: Spor salonundaki ekipmanların bilgilerini tutar.
-- =====================================================

CREATE TABLE IF NOT EXISTS salon_ekipmanlari (
    ekipman_id INT AUTO_INCREMENT PRIMARY KEY,
    ekipman_adi VARCHAR(100) NOT NULL,
    kategori VARCHAR(100) NOT NULL,
    alim_tarihi DATE,
    durum ENUM('Kullanılabilir', 'Bakımda', 'Arızalı') NOT NULL DEFAULT 'Kullanılabilir',
    aciklama VARCHAR(255),

    CONSTRAINT chk_ekipman_adi CHECK (CHAR_LENGTH(ekipman_adi) >= 2)
);

-- =====================================================
-- TABLO 10: ekipman_bakimlari
-- AÇIKLAMA: Spor salonu ekipmanlarına ait bakım kayıtlarını tutar.
-- =====================================================

CREATE TABLE IF NOT EXISTS ekipman_bakimlari (
    bakim_id INT AUTO_INCREMENT PRIMARY KEY,
    ekipman_id INT NOT NULL,
    bakim_tarihi DATE NOT NULL,
    aciklama VARCHAR(255) NOT NULL,
    bakim_maliyeti DECIMAL(10,2) NOT NULL DEFAULT 0,
    bakim_durumu ENUM('Planlandı', 'Tamamlandı', 'İptal') NOT NULL DEFAULT 'Planlandı',

    CONSTRAINT fk_bakim_ekipman FOREIGN KEY (ekipman_id)
        REFERENCES salon_ekipmanlari(ekipman_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT chk_bakim_maliyeti CHECK (bakim_maliyeti >= 0)
);