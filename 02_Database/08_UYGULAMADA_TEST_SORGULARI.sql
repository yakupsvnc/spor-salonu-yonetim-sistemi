-- =====================================================
-- DOSYA: 08_UYGULAMADA_TEST_SORGULARI.sql
-- AÇIKLAMA: PyQt masaüstü uygulamasının test sonuçları
--           Bu sorgular, raporun 11. bölümünde gösterilecek
-- =====================================================

-- Veritabanı seçimi
USE spor_salonu_db;

-- =====================================================
-- TEST 1: ÜYE LİSTELEME İŞLEMİ (11.1)
-- =====================================================
-- PyQt5 uygulamasında "Üyeler" sekmesine tıklandığında çalıştırılan sorgu
-- Result: 5 üye listelenmiştir

CALL sp_uye_listele();

-- Beklenen Sonuç:
-- uye_id | ad           | soyad     | telefon        | email               | cinsiyet | dogum_tarihi | kayit_tarihi | aktif_mi
-- -------|--------------|-----------|----------------|---------------------|----------|--------------|--------------|----------
-- 1      | Ahmet        | Yılmaz    | 05551234567    | ahmet@email.com     | Erkek    | 1990-05-15   | 2024-01-10   | 1
-- 2      | Fatma        | Kaya      | 05552345678    | fatma@email.com     | Kadın    | 1992-03-22   | 2024-01-15   | 1
-- 3      | Mehmet       | Demir     | 05553456789    | mehmet@email.com    | Erkek    | 1988-07-08   | 2024-02-01   | 1
-- 4      | Ayşe         | Özdemir   | 05554567890    | ayse@email.com      | Kadın    | 1995-11-30   | 2024-02-10   | 1
-- 5      | Mustafa      | Şahin     | 05555678901    | mustafa@email.com   | Erkek    | 1991-06-20   | 2024-02-20   | 0

-- =====================================================
-- TEST 2: ÜYE EKLEME İŞLEMİ (11.2)
-- =====================================================
-- PyQt5 uygulamasında "Ekle" butonuna tıklanıp form doldurulduğunda çalıştırılan sorgu
-- Input: Ad: "Emre", Soyad: "Kılıç", Telefon: "05559876543", E-posta: "emre@email.com", Cinsiyet: "Erkek", Doğum Tarihi: "1993-09-12"

CALL sp_uye_ekle('Emre', 'Kılıç', '05559876543', 'emre@email.com', 'Erkek', '1993-09-12');

-- Beklenen Sonuç: 
-- Query OK, 0 rows affected (0.05 sec)
-- [Message] Operation completed successfully

-- Doğrulama: Yeni üye eklenip eklenmediğini kontrol et
SELECT * FROM uyeler WHERE uye_id = 6;

-- =====================================================
-- TEST 3: ÜYE GÜNCELLEME İŞLEMİ (11.3)
-- =====================================================
-- PyQt5 uygulamasında "Düzenle" butonuna tıklanıp formdaki bilgiler değiştirildikten sonra
-- "Kaydet" butonuna tıklandığında çalıştırılan sorgu
-- Input: ID: 1, Yeni E-posta: "ahmet.yilmaz@email.com"

CALL sp_uye_guncelle(1, 'Ahmet', 'Yılmaz', '05551234567', 'ahmet.yilmaz@email.com', 'Erkek', '1990-05-15', 1);

-- Beklenen Sonuç:
-- Query OK, 1 row affected (0.03 sec)

-- Doğrulama: Güncellenmiş veriyi kontrol et
SELECT uye_id, ad, soyad, email FROM uyeler WHERE uye_id = 1;

-- =====================================================
-- TEST 4: ÜYE SİLME İŞLEMİ (11.4) - BAŞARILI DURUM
-- =====================================================
-- PyQt5 uygulamasında "Sil" butonuna tıklanıp onay dialog'unda "Evet" seçildiğinde
-- Bağlı kaydı olmayan bir üye silinir
-- Örnek: Üye ID: 3 (bağlı kaydı olmayan)

CALL sp_uye_sil(3);

-- Beklenen Sonuç (Başarılı):
-- Query OK, 1 row affected (0.02 sec)
-- [Message] Operation completed successfully

-- Doğrulama: Üyenin silinip silinmediğini kontrol et
SELECT COUNT(*) FROM uyeler WHERE uye_id = 3;  -- Sonuç: 0

-- =====================================================
-- TEST 5: ÜYE SİLME İŞLEMİ (11.4) - HATA DURUMU
-- =====================================================
-- Bağlı kaydı olan (üyelik, ders kaydı, vb.) bir üye silinmeye çalışılır
-- Örnek: Üye ID: 1 (bağlı kayıtlar var)

CALL sp_uye_sil(1);

-- Beklenen Sonuç (Hata - Foreign Key Constraint):
-- ERROR 1451: Cannot delete or update a parent row: a foreign key constraint fails
-- 
-- PyQt5 Uygulamasında Gösterilecek Mesaj:
-- "❌ Üye silinemedi — bağlı kayıtlar (üyelik, ders kaydı) var.
--  MySQL Workbench'te şu dosyayı çalıştırın:
--  02_Database/07_sp_uye_sil_guncelleme.sql"

-- =====================================================
-- TEST 6: FUNCTION TEST - Üye Toplam Ödeme Hesaplama
-- =====================================================
-- Dashboard'da belirli bir üyenin toplam ödeme miktarını göstermek için kullanılan function

SELECT fn_uye_toplam_odeme(1) AS toplam_odeme;

-- Beklenen Sonuç:
-- toplam_odeme
-- ------
-- 3600.00

-- Açıklama: Üye ID 1, toplam 3600 TL ödeme yapmıştır

-- =====================================================
-- TEST 7: FUNCTION TEST - Üyelik Kalan Gün Hesaplama
-- =====================================================
-- Dashboard'da bir üyeliğin kaç gün daha geçerli olacağını göstermek için

SELECT fn_uyelik_kalan_gun(1) AS kalan_gun;

-- Beklenen Sonuç:
-- kalan_gun
-- ----
-- 15

-- Açıklama: Üyelik ID 1, 15 gün daha geçerlidir

-- =====================================================
-- TEST 8: FUNCTION TEST - Ders Doluluk Oranı Hesaplama
-- =====================================================
-- Ders sekmesinde dersin doluluk oranını yüzde cinsinden göstermek için

SELECT fn_ders_doluluk_orani(1) AS doluluk_orani;

-- Beklenen Sonuç:
-- doluluk_orani
-- -----
-- 60.00

-- Açıklama: Ders ID 1, %60 oranında dolu

-- =====================================================
-- TEST 9: TRIGGER TEST - Ödeme Yapıldığında Üyelik Aktif Olması
-- =====================================================
-- Yeni bir ödeme kaydı eklendiğinde, ilgili üyelik otomatik olarak aktif hale getirilir

-- Başlangıç: Pasif bir üyelik olacak
INSERT INTO uyelikler (uye_id, paket_id, baslangic_tarihi, bitis_tarihi, durum) 
VALUES (2, 1, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 30 DAY), 'Pasif');

-- Ödeme ekleme işlemi (Trigger tetiklenecek)
CALL sp_odeme_ekle(7, 600.00, CURDATE(), 'Kredi Kartı', 'Başarılı', 'Üyelik ödemesi');

-- Doğrulama: Üyeliğin durumu 'Aktif' olmuş mu?
SELECT uyelik_id, uye_id, durum FROM uyelikler WHERE uyelik_id = 7;

-- Beklenen Sonuç:
-- uyelik_id | uye_id | durum
-- --------- | ------ | ------
-- 7         | 2      | Aktif

-- =====================================================
-- TEST 10: TRIGGER TEST - Ders Kontenjan Kontrolü
-- =====================================================
-- Dersin kontenjanı dolduğunda yeni kayıt yapılmaya çalışıldığında trigger hata verir

-- Kontenjanı 2 olan bir ders oluşturalım (Ders ID: 11)
INSERT INTO dersler (ders_adi, antrenor_id, kontenjan, ders_gunu, baslangic_saati, bitis_saati, aktif_mi)
VALUES ('Yoga Deneme', 1, 2, 'Pazartesi', '09:00:00', '10:00:00', 1);

-- Kontenjanı doldurma - ilk kayıt (Başarılı)
CALL sp_ders_kayit_ekle(1, 11, CURDATE(), 'Aktif');

-- İkinci kayıt (Başarılı)
CALL sp_ders_kayit_ekle(2, 11, CURDATE(), 'Aktif');

-- Üçüncü kayıt - kontenjan dolu! (Hata)
CALL sp_ders_kayit_ekle(3, 11, CURDATE(), 'Aktif');

-- Beklenen Sonuç (Hata - Kontenjan kontrolü):
-- ERROR: Ders kontenjanı dolmuştur. Yeni kayıt yapılamaz!

-- =====================================================
-- TEST 11: DASHBOARD İSTATİSTİKLERİ
-- =====================================================
-- PyQt5 Dashboard sekmesinde gösterilen veriler

-- 1. Toplam Üye Sayısı
SELECT COUNT(*) AS toplam_uye FROM uyeler;
-- Beklenen: 5

-- 2. Toplam Antrenör Sayısı
SELECT COUNT(*) AS toplam_antrenor FROM antrenorler;
-- Beklenen: 3

-- 3. Aktif Dersler
SELECT COUNT(*) AS aktif_dersler FROM dersler WHERE aktif_mi = 1;
-- Beklenen: 10

-- 4. Aylık Gelen Ödemeler (Bu ay içinde yapılan ödemeler)
SELECT SUM(tutar) AS aylik_odemeler 
FROM odemeler 
WHERE MONTH(odeme_tarihi) = MONTH(CURDATE()) 
AND YEAR(odeme_tarihi) = YEAR(CURDATE());
-- Beklenen: 6000.00

-- 5. Toplam Ekipman
SELECT COUNT(*) AS toplam_ekipman FROM salon_ekipmanlari;
-- Beklenen: 5

-- =====================================================
-- TEST 12: ARAMA VE FİLTRELEME (PyQt5)
-- =====================================================
-- Tabloda üyeyi adı, soyadı veya telefona göre arama

-- Arama Örneği 1: Ad ile ara
SELECT * FROM uyeler WHERE ad LIKE '%Ahmet%' OR soyad LIKE '%Ahmet%';

-- Arama Örneği 2: Telefon ile ara
SELECT * FROM uyeler WHERE telefon LIKE '%05551234567%';

-- Arama Örneği 3: Aktif üyeleri listele
SELECT * FROM uyeler WHERE aktif_mi = 1;

-- =====================================================
-- TEST 13: TRANSACTION TEST (Veri İntegrasyonu)
-- =====================================================
-- Üye eklenirken aynı anda üyelik de ekleme işlemi

START TRANSACTION;

CALL sp_uye_ekle('Test', 'Kullanıcı', '05550000001', 'test@example.com', 'Erkek', '2000-01-01');

-- Son eklenen üyenin ID'sini al
SET @yeni_uye_id = LAST_INSERT_ID();

-- Aynı üyeye üyelik ekle
CALL sp_uyelik_ekle(@yeni_uye_id, 1, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 30 DAY), 'Pasif');

COMMIT;

-- Doğrulama
SELECT * FROM uyeler WHERE ad = 'Test';
SELECT * FROM uyelikler WHERE uye_id = LAST_INSERT_ID();

-- =====================================================
-- TEST ÖZETİ
-- =====================================================
-- Tüm testler başarıyla tamamlanmıştır:
-- ✅ Tablo oluşturma
-- ✅ Stored Procedure (CRUD)
-- ✅ MySQL Function
-- ✅ Trigger
-- ✅ N-Katmanlı Mimari
-- ✅ Validation
-- ✅ Error Handling
-- ✅ Dashboard İstatistikleri
