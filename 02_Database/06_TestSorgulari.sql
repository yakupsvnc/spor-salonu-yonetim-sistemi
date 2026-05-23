-- =====================================================
-- PROJE: Spor Salonu Üyelik, Ders, Antrenör ve Ödeme Yönetim Sistemi
-- DOSYA: 06_TestSorgulari.sql
-- AÇIKLAMA: Stored Procedure, Function ve Trigger test sorguları
-- VERİTABANI: MySQL
-- =====================================================

USE spor_salonu_db;

-- =====================================================
-- 1. STORED PROCEDURE TESTLERİ
-- AÇIKLAMA: Listeleme procedure'leri test edilir.
-- =====================================================

CALL sp_uye_listele();
CALL sp_antrenor_listele();
CALL sp_uyelik_paketi_listele();
CALL sp_uyelik_listele();
CALL sp_odeme_listele();
CALL sp_ders_listele();
CALL sp_ders_kayit_listele();
CALL sp_yoklama_listele();
CALL sp_ekipman_listele();
CALL sp_bakim_listele();


-- =====================================================
-- 2. FUNCTION TESTLERİ
-- AÇIKLAMA: Kullanıcı tanımlı function'lar test edilir.
-- =====================================================

SELECT fn_uye_toplam_odeme(1) AS uye_toplam_odeme;

SELECT fn_uyelik_kalan_gun(1) AS uyelik_kalan_gun;

SELECT fn_ders_doluluk_orani(1) AS ders_doluluk_orani;


-- =====================================================
-- 3. TRIGGER TESTLERİ
-- AÇIKLAMA: Gerçek hayat iş kurallarını temsil eden trigger testleri.
-- NOT: Bu sorgular hata üretmek veya otomatik işlem göstermek için kullanılır.
-- =====================================================

-- Trigger Test 1:
-- Başarılı ödeme eklenince ilgili üyelik otomatik Aktif yapılır.
-- Örnek kontrol sorgusu:
CALL sp_uyelik_listele();


-- Trigger Test 2:
-- Bitiş tarihi başlangıç tarihinden önce olan üyelik engellenir.
-- Bu sorgu bilerek hata vermelidir.
-- CALL sp_uyelik_ekle(1, 1, '2026-06-01', '2026-05-01', 'Pasif');


-- Trigger Test 3:
-- Ders kontenjanı doluysa yeni kayıt engellenir.
-- Bu test video sırasında ayrıca gösterilebilir.