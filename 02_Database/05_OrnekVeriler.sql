-- =====================================================
-- PROJE: Spor Salonu Üyelik, Ders, Antrenör ve Ödeme Yönetim Sistemi
-- DOSYA: 05_OrnekVeriler.sql
-- AÇIKLAMA: Bu dosyada sistemi test etmek için örnek veriler bulunur.
-- VERİTABANI: MySQL
-- =====================================================

USE spor_salonu_db;

-- =====================================================
-- ÖRNEK VERİLER 1: Üyeler
-- AÇIKLAMA: Sisteme örnek spor salonu üyeleri eklenir.
-- =====================================================

CALL sp_uye_ekle('Ahmet', 'Yılmaz', '05551112233', 'ahmet.yilmaz@mail.com', 'Erkek', '2000-05-12');
CALL sp_uye_ekle('Elif', 'Kaya', '05552223344', 'elif.kaya@mail.com', 'Kadın', '1999-09-20');
CALL sp_uye_ekle('Mehmet', 'Demir', '05553334455', 'mehmet.demir@mail.com', 'Erkek', '1998-03-15');
CALL sp_uye_ekle('Zeynep', 'Çelik', '05554445566', 'zeynep.celik@mail.com', 'Kadın', '2001-12-02');
CALL sp_uye_ekle('Burak', 'Arslan', '05555556677', 'burak.arslan@mail.com', 'Erkek', '1997-07-08');

-- =====================================================
-- ÖRNEK VERİLER 2: Antrenörler
-- AÇIKLAMA: Sisteme örnek spor salonu antrenörleri eklenir.
-- =====================================================

CALL sp_antrenor_ekle('Murat', 'Aydın', '05321112233', 'murat.aydin@mail.com', 'Fitness', 28000.00, '2023-01-10');
CALL sp_antrenor_ekle('Selin', 'Koç', '05322223344', 'selin.koc@mail.com', 'Pilates', 30000.00, '2022-09-15');
CALL sp_antrenor_ekle('Emre', 'Şahin', '05323334455', 'emre.sahin@mail.com', 'Kardiyo', 26000.00, '2024-02-01');
CALL sp_antrenor_ekle('Derya', 'Yıldız', '05324445566', 'derya.yildiz@mail.com', 'Yoga', 27500.00, '2023-06-20');

-- =====================================================
-- ÖRNEK VERİLER 3: Üyelik Paketleri
-- AÇIKLAMA: Spor salonunda satılan örnek üyelik paketleri eklenir.
-- =====================================================

CALL sp_uyelik_paketi_ekle('Aylık Standart Paket', 30, 750.00, 'Spor salonu kullanım hakkı sunan aylık standart paket.');
CALL sp_uyelik_paketi_ekle('3 Aylık Premium Paket', 90, 2000.00, 'Spor salonu ve grup derslerine katılım hakkı sunan üç aylık paket.');
CALL sp_uyelik_paketi_ekle('Yıllık Gold Paket', 365, 7000.00, 'Tüm salon imkanları ve grup derslerine erişim sağlayan yıllık paket.');
CALL sp_uyelik_paketi_ekle('Öğrenci Paketi', 30, 500.00, 'Öğrencilere özel indirimli aylık üyelik paketi.');

-- =====================================================
-- ÖRNEK VERİLER 4: Üyelikler
-- AÇIKLAMA: Üyelere örnek üyelik paketleri atanır.
-- =====================================================

CALL sp_uyelik_ekle(1, 1, '2026-05-01', '2026-05-31', 'Pasif');
CALL sp_uyelik_ekle(2, 2, '2026-05-05', '2026-08-03', 'Pasif');
CALL sp_uyelik_ekle(3, 4, '2026-05-10', '2026-06-09', 'Pasif');
CALL sp_uyelik_ekle(4, 3, '2026-05-15', '2027-05-15', 'Pasif');
CALL sp_uyelik_ekle(5, 1, '2026-05-20', '2026-06-19', 'Pasif');

-- =====================================================
-- ÖRNEK VERİLER 5: Ödemeler
-- AÇIKLAMA: Üyeliklere ait örnek ödeme kayıtları eklenir.
-- NOT: Ödeme başarılı olursa trigger ilgili üyeliği otomatik Aktif yapar.
-- =====================================================

CALL sp_odeme_ekle(1, 750.00, 'Kart', 'Başarılı', 'Aylık standart paket ödemesi.');
CALL sp_odeme_ekle(2, 2000.00, 'Nakit', 'Başarılı', '3 aylık premium paket ödemesi.');
CALL sp_odeme_ekle(3, 500.00, 'Kart', 'Başarılı', 'Öğrenci paketi ödemesi.');
CALL sp_odeme_ekle(4, 7000.00, 'Havale/EFT', 'Başarılı', 'Yıllık gold paket ödemesi.');
CALL sp_odeme_ekle(5, 750.00, 'Nakit', 'Beklemede', 'Ödeme beklemede olduğu için üyelik aktifleşmez.');

-- =====================================================
-- ÖRNEK VERİLER 6: Dersler
-- AÇIKLAMA: Spor salonunda verilen örnek grup dersleri eklenir.
-- =====================================================

CALL sp_ders_ekle('Fitness Başlangıç', 1, 20, 'Pazartesi', '10:00:00', '11:00:00');
CALL sp_ders_ekle('Pilates', 2, 15, 'Salı', '14:00:00', '15:00:00');
CALL sp_ders_ekle('Kardiyo', 3, 25, 'Çarşamba', '18:00:00', '19:00:00');
CALL sp_ders_ekle('Yoga', 4, 12, 'Perşembe', '09:00:00', '10:00:00');

-- =====================================================
-- ÖRNEK VERİLER 7: Ders Kayıtları
-- AÇIKLAMA: Üyelerin grup derslerine kayıtları eklenir.
-- =====================================================

CALL sp_ders_kayit_ekle(1, 1, 'Kayıtlı');
CALL sp_ders_kayit_ekle(2, 2, 'Kayıtlı');
CALL sp_ders_kayit_ekle(3, 3, 'Kayıtlı');
CALL sp_ders_kayit_ekle(4, 4, 'Kayıtlı');
CALL sp_ders_kayit_ekle(5, 1, 'Kayıtlı');

-- =====================================================
-- ÖRNEK VERİLER 8: Yoklamalar
-- AÇIKLAMA: Ders kayıtlarına ait örnek yoklama kayıtları eklenir.
-- =====================================================

CALL sp_yoklama_ekle(1, '2026-05-25', 'Katıldı', 'Üye derse zamanında katıldı.');
CALL sp_yoklama_ekle(2, '2026-05-25', 'Katıldı', 'Üye pilates dersine katıldı.');
CALL sp_yoklama_ekle(3, '2026-05-25', 'Gelmedi', 'Üye derse katılmadı.');
CALL sp_yoklama_ekle(4, '2026-05-25', 'Mazeretli', 'Üye mazeret bildirdi.');
CALL sp_yoklama_ekle(5, '2026-05-25', 'Katıldı', 'Üye fitness dersine katıldı.');

-- =====================================================
-- ÖRNEK VERİLER 9: Salon Ekipmanları
-- AÇIKLAMA: Spor salonunda bulunan örnek ekipman kayıtları eklenir.
-- =====================================================

CALL sp_ekipman_ekle('Koşu Bandı', 'Kardiyo', '2024-01-15', 'Kullanılabilir', 'Kardiyo alanında kullanılan koşu bandı.');
CALL sp_ekipman_ekle('Dambıl Seti', 'Ağırlık', '2023-08-10', 'Kullanılabilir', 'Farklı kilolarda dambıl seti.');
CALL sp_ekipman_ekle('Bisiklet', 'Kardiyo', '2024-03-05', 'Bakımda', 'Manyetik kondisyon bisikleti.');
CALL sp_ekipman_ekle('Bench Press Sehpası', 'Ağırlık', '2023-11-20', 'Kullanılabilir', 'Göğüs çalışmaları için kullanılan bench sehpası.');

-- =====================================================
-- ÖRNEK VERİLER 10: Ekipman Bakımları
-- AÇIKLAMA: Salon ekipmanlarına ait örnek bakım kayıtları eklenir.
-- =====================================================

CALL sp_bakim_ekle(1, '2026-05-10', 'Koşu bandı genel bakım ve kayış kontrolü yapıldı.', 850.00, 'Tamamlandı');
CALL sp_bakim_ekle(2, '2026-05-12', 'Dambıl setleri kontrol edildi, eksik ağırlık tamamlandı.', 300.00, 'Tamamlandı');
CALL sp_bakim_ekle(3, '2026-05-20', 'Bisiklet pedal ve ekran arızası için bakım planlandı.', 1200.00, 'Planlandı');
CALL sp_bakim_ekle(4, '2026-05-22', 'Bench press sehpası vida ve güvenlik kontrolü yapıldı.', 250.00, 'Tamamlandı');