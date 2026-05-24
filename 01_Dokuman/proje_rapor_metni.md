# SPOR SALONU ÜYELİK, DERS, ANTRENÖR VE ÖDEME YÖNETİM SİSTEMİ

## Ders Bilgileri

**Dersin Adı:** BTS304 - Veritabanı Yönetim Sistemleri-II  
**Ödev Türü:** Final Sınavına Ek Ödev 2  
**Proje Konusu:** Spor Salonu Üyelik, Ders, Antrenör ve Ödeme Yönetim Sistemi  
**Veritabanı:** MySQL  
**Uygulama Türü:** Mobil Uygulama  
**Geliştirme Yapısı:** Flutter Mobil Uygulama + ASP.NET Core Web API + MySQL Veritabanı  
**Mimari:** N-Katmanlı Mimari  

---

# 1. PROJE KONUSU

Bu projede, gerçek hayatta faaliyet gösteren bir spor salonu işletmesi için üyelik, ders, antrenör, ödeme, yoklama ve ekipman bakım süreçlerini yöneten bir veritabanı ve mobil uygulama sistemi tasarlanmıştır.

Sistem; spor salonuna kayıt olan üyelerin bilgilerinin tutulmasını, üyelik paketlerinin yönetilmesini, üyelerin paket satın almasını, ödemelerin takip edilmesini, antrenörlerin sisteme kaydedilmesini, grup derslerinin oluşturulmasını, üyelerin derslere kayıt edilmesini, yoklama alınmasını ve salon ekipmanlarının bakım süreçlerinin izlenmesini sağlar.

---

# 2. ADIM-1: SENARYO

Spor salonları; üye kayıtları, üyelik paketleri, ödemeler, grup dersleri, antrenörler, yoklamalar ve ekipman bakım süreçleri gibi birçok operasyonel işlemi düzenli olarak takip etmek zorundadır. Bu işlemlerin manuel olarak defter, Excel veya dağınık dosyalar üzerinden yürütülmesi veri kaybına, ödeme takibinde karışıklığa, üyelik süresi kontrollerinde hatalara ve ders kontenjanlarında düzensizliğe neden olabilir.

Bu proje kapsamında geliştirilen Spor Salonu Üyelik, Ders, Antrenör ve Ödeme Yönetim Sistemi, bu süreçleri merkezi bir veritabanı üzerinde yönetmeyi amaçlamaktadır.

Sistemde spor salonuna kayıt olan her üyenin adı, soyadı, telefon numarası, e-posta adresi, cinsiyeti, doğum tarihi, kayıt tarihi ve aktiflik durumu tutulur. Her üye, spor salonu tarafından tanımlanan üyelik paketlerinden birini satın alabilir. Üyelik paketleri aylık, üç aylık, yıllık veya öğrenci paketi gibi farklı seçeneklerden oluşabilir. Her paketin süresi, ücreti, açıklaması ve aktiflik durumu sistemde kayıt altına alınır.

Bir üye üyelik paketi satın aldığında sistemde üyelik kaydı oluşturulur. Bu üyelik kaydında üyenin hangi paketi aldığı, üyelik başlangıç tarihi, bitiş tarihi ve üyelik durumu tutulur. Üyelik ilk oluşturulduğunda pasif olabilir. Üye ödeme yaptığında ödeme bilgisi sisteme eklenir. Ödeme başarılı olarak kaydedilirse sistemde tanımlanan trigger sayesinde ilgili üyelik otomatik olarak aktif hale getirilir. Böylece ödeme ve üyelik durumu arasında otomatik bir iş kuralı uygulanmış olur.

Spor salonunda çalışan antrenörler de sisteme kaydedilir. Her antrenörün adı, soyadı, telefon numarası, e-posta adresi, uzmanlık alanı, maaşı, işe başlama tarihi ve aktiflik durumu tutulur. Antrenörler, spor salonunda Fitness, Pilates, Kardiyo ve Yoga gibi farklı grup dersleri verebilir.

Dersler tablosunda her dersin adı, dersi veren antrenör, kontenjan bilgisi, ders günü, başlangıç saati, bitiş saati ve aktiflik durumu yer alır. Üyeler bu grup derslerine kayıt olabilir. Bir üye birden fazla derse kayıt olabileceği gibi, bir derse de birden fazla üye kayıt olabilir. Bu nedenle üyeler ile dersler arasındaki çoktan çoğa ilişki, ders kayıtları tablosu ile yönetilmiştir.

Ders kayıtları oluşturulurken dersin kontenjanı kontrol edilir. Eğer ders kontenjanı dolmuşsa yeni kayıt yapılması trigger ile engellenir. Böylece gerçek hayatta spor salonlarında yaşanabilecek kontenjan aşımı problemi veritabanı seviyesinde kontrol altına alınır.

Sistem ayrıca derslere ait yoklama bilgilerini de tutar. Her ders kaydı için belirli tarihlerde yoklama alınabilir. Üyenin derse katılıp katılmadığı, mazeretli olup olmadığı ve açıklama bilgisi sistemde saklanır.

Bunlara ek olarak spor salonundaki ekipmanların takibi de yapılmaktadır. Koşu bandı, dambıl seti, kondisyon bisikleti ve bench press sehpası gibi ekipmanların adı, kategorisi, alım tarihi, durumu ve açıklaması tutulur. Ekipmanların bakım süreçleri de ayrı bir tabloda kayıt altına alınır. Her bakım kaydında ekipmanın hangi tarihte bakıma alındığı, bakım açıklaması, bakım maliyeti ve bakım durumu yer alır.

Bu sistem sayesinde spor salonu işletmesi; üyelerini, paketlerini, ödemelerini, derslerini, antrenörlerini, yoklamalarını ve ekipman bakım kayıtlarını tek bir veritabanı üzerinden düzenli, kontrollü ve raporlanabilir şekilde yönetebilir.

---

# 3. ADIM-2: VARLIKLAR, NİTELİKLER, İLİŞKİLER VE ER DİYAGRAMI

Bu bölümde spor salonu yönetim sistemi için kullanılan varlıklar, bu varlıklara ait nitelikler ve varlıklar arasındaki ilişkiler açıklanmıştır.

## 3.1. Sistemde Yer Alan Varlıklar

Sistemde toplam 10 temel varlık bulunmaktadır:

1. Üyeler
2. Antrenörler
3. Üyelik Paketleri
4. Üyelikler
5. Ödemeler
6. Dersler
7. Ders Kayıtları
8. Yoklamalar
9. Salon Ekipmanları
10. Ekipman Bakımları

---

## 3.2. Varlıklar ve Nitelikleri

### 3.2.1. Uyeler

Bu varlık spor salonuna kayıtlı üyelerin bilgilerini tutar.

**Nitelikler:**

- uye_id
- ad
- soyad
- telefon
- email
- cinsiyet
- dogum_tarihi
- kayit_tarihi
- aktif_mi

---

### 3.2.2. Antrenorler

Bu varlık spor salonunda çalışan antrenörlerin bilgilerini tutar.

**Nitelikler:**

- antrenor_id
- ad
- soyad
- telefon
- email
- uzmanlik_alani
- maas
- ise_baslama_tarihi
- aktif_mi

---

### 3.2.3. Uyelik_Paketleri

Bu varlık spor salonunda satılan üyelik paketlerini tutar.

**Nitelikler:**

- paket_id
- paket_adi
- sure_gun
- ucret
- aciklama
- aktif_mi

---

### 3.2.4. Uyelikler

Bu varlık üyelerin satın aldığı üyelik paketlerini ve üyelik durumlarını tutar.

**Nitelikler:**

- uyelik_id
- uye_id
- paket_id
- baslangic_tarihi
- bitis_tarihi
- durum
- olusturma_tarihi

---

### 3.2.5. Odemeler

Bu varlık üyeliklere ait ödeme bilgilerini tutar.

**Nitelikler:**

- odeme_id
- uyelik_id
- tutar
- odeme_tarihi
- odeme_yontemi
- odeme_durumu
- aciklama

---

### 3.2.6. Dersler

Bu varlık spor salonunda verilen grup derslerini tutar.

**Nitelikler:**

- ders_id
- ders_adi
- antrenor_id
- kontenjan
- ders_gunu
- baslangic_saati
- bitis_saati
- aktif_mi

---

### 3.2.7. Ders_Kayitlari

Bu varlık üyelerin grup derslerine kayıt bilgilerini tutar.

**Nitelikler:**

- ders_kayit_id
- uye_id
- ders_id
- kayit_tarihi
- durum

---

### 3.2.8. Yoklamalar

Bu varlık ders kayıtlarına ait yoklama bilgilerini tutar.

**Nitelikler:**

- yoklama_id
- ders_kayit_id
- yoklama_tarihi
- katilim_durumu
- aciklama

---

### 3.2.9. Salon_Ekipmanlari

Bu varlık spor salonunda bulunan ekipmanların bilgilerini tutar.

**Nitelikler:**

- ekipman_id
- ekipman_adi
- kategori
- alim_tarihi
- durum
- aciklama

---

### 3.2.10. Ekipman_Bakimlari

Bu varlık salon ekipmanlarına ait bakım kayıtlarını tutar.

**Nitelikler:**

- bakim_id
- ekipman_id
- bakim_tarihi
- aciklama
- bakim_maliyeti
- bakim_durumu

---

## 3.3. Varlıklar Arasındaki İlişkiler

Sistemdeki varlıklar arasındaki ilişkiler aşağıdaki gibidir:

1. Bir üyenin birden fazla üyeliği olabilir.  
   **Uyeler 1 - N Uyelikler**

2. Bir üyelik paketi birden fazla üyelikte kullanılabilir.  
   **Uyelik_Paketleri 1 - N Uyelikler**

3. Bir üyeliğe birden fazla ödeme yapılabilir.  
   **Uyelikler 1 - N Odemeler**

4. Bir antrenör birden fazla ders verebilir.  
   **Antrenorler 1 - N Dersler**

5. Bir üye birden fazla derse kayıt olabilir.  
   **Uyeler 1 - N Ders_Kayitlari**

6. Bir ders birden fazla üye kaydı alabilir.  
   **Dersler 1 - N Ders_Kayitlari**

7. Üyeler ile dersler arasında çoktan çoğa ilişki vardır. Bu ilişki Ders_Kayitlari ara tablosu ile çözülmüştür.  
   **Uyeler N - N Dersler**

8. Bir ders kaydına birden fazla yoklama kaydı girilebilir.  
   **Ders_Kayitlari 1 - N Yoklamalar**

9. Bir salon ekipmanının birden fazla bakım kaydı olabilir.  
   **Salon_Ekipmanlari 1 - N Ekipman_Bakimlari**

---

## 3.4. ER Diyagramı

ER diyagramı diagrams.net/draw.io aracı kullanılarak oluşturulmuştur.

![ER Diyagramı - Spor Salonu Yönetim Sistemi](ER_Diyagrami_SporSalonu.png)

**Yukarıdaki diyagramda:**
- **Varlıklar (Dikdörtgenler):** Üyeler, Antrenörler, Üyelik Paketleri, Üyelikler, Ödemeler, Dersler, Ders Kayıtları, Yoklamalar, Salon Ekipmanları, Ekipman Bakımları
- **İlişkiler (Çizgiler):** 1-N, N-N ilişkileri gösterilmiştir
- **Anahtarlar:** Her varlığın birincil anahtarı ve yabancı anahtarları belirtilmiştir

**Dosya adı:**
- `ER_Diyagrami_SporSalonu.drawio` (draw.io/diagrams.net formatı)
- `ER_Diyagrami_SporSalonu.png` (PNG görseli)

---

## 3.5. ER Diyagramının İlişkisel Modele Dönüştürülmesi

ER diyagramında belirlenen varlıklar, ilişkisel veritabanı modeline dönüştürülerek tablolar halinde tasarlanmıştır. Her tablo için birincil anahtarlar, yabancı anahtarlar ve gerekli kısıtlamalar belirlenmiştir.

### Uyeler

**Uyeler**(`uye_id`, ad, soyad, telefon, email, cinsiyet, dogum_tarihi, kayit_tarihi, aktif_mi)

- Primary Key: `uye_id`
- Unique: `telefon`, `email`

---

### Antrenorler

**Antrenorler**(`antrenor_id`, ad, soyad, telefon, email, uzmanlik_alani, maas, ise_baslama_tarihi, aktif_mi)

- Primary Key: `antrenor_id`
- Unique: `telefon`, `email`

---

### Uyelik_Paketleri

**Uyelik_Paketleri**(`paket_id`, paket_adi, sure_gun, ucret, aciklama, aktif_mi)

- Primary Key: `paket_id`
- Unique: `paket_adi`

---

### Uyelikler

**Uyelikler**(`uyelik_id`, uye_id, paket_id, baslangic_tarihi, bitis_tarihi, durum, olusturma_tarihi)

- Primary Key: `uyelik_id`
- Foreign Key: `uye_id` → `Uyeler(uye_id)`
- Foreign Key: `paket_id` → `Uyelik_Paketleri(paket_id)`

---

### Odemeler

**Odemeler**(`odeme_id`, uyelik_id, tutar, odeme_tarihi, odeme_yontemi, odeme_durumu, aciklama)

- Primary Key: `odeme_id`
- Foreign Key: `uyelik_id` → `Uyelikler(uyelik_id)`

---

### Dersler

**Dersler**(`ders_id`, ders_adi, antrenor_id, kontenjan, ders_gunu, baslangic_saati, bitis_saati, aktif_mi)

- Primary Key: `ders_id`
- Foreign Key: `antrenor_id` → `Antrenorler(antrenor_id)`

---

### Ders_Kayitlari

**Ders_Kayitlari**(`ders_kayit_id`, uye_id, ders_id, kayit_tarihi, durum)

- Primary Key: `ders_kayit_id`
- Foreign Key: `uye_id` → `Uyeler(uye_id)`
- Foreign Key: `ders_id` → `Dersler(ders_id)`
- Unique: `uye_id`, `ders_id`

Bu tablo, üyeler ile dersler arasındaki çoktan çoğa ilişkiyi çözmek için kullanılmıştır.

---

### Yoklamalar

**Yoklamalar**(`yoklama_id`, ders_kayit_id, yoklama_tarihi, katilim_durumu, aciklama)

- Primary Key: `yoklama_id`
- Foreign Key: `ders_kayit_id` → `Ders_Kayitlari(ders_kayit_id)`
- Unique: `ders_kayit_id`, `yoklama_tarihi`

---

### Salon_Ekipmanlari

**Salon_Ekipmanlari**(`ekipman_id`, ekipman_adi, kategori, alim_tarihi, durum, aciklama)

- Primary Key: `ekipman_id`

---

### Ekipman_Bakimlari

**Ekipman_Bakimlari**(`bakim_id`, ekipman_id, bakim_tarihi, aciklama, bakim_maliyeti, bakim_durumu)

- Primary Key: `bakim_id`
- Foreign Key: `ekipman_id` → `Salon_Ekipmanlari(ekipman_id)`

---

# 4. ADIM-3: FİZİKSEL TASARIM

Bu bölümde, ER diyagramı ve ilişkisel modele uygun olarak MySQL veritabanı üzerinde fiziksel tablo tasarımları gerçekleştirilmiştir.

Proje kapsamında veritabanı adı aşağıdaki şekilde belirlenmiştir:

**Veritabanı Adı:** `spor_salonu_db`

Tablolar MySQL Workbench üzerinde oluşturulmuştur. Fiziksel tasarım yapılırken aşağıdaki veritabanı kısıtları kullanılmıştır:

- Primary Key
- Foreign Key
- Unique
- Not Null
- Default
- Check
- Auto Increment

Bu sayede veritabanında veri bütünlüğü, ilişki tutarlılığı ve temel iş kuralları tablo seviyesinde sağlanmıştır.

---

## 4.1. Oluşturulan Tablolar

Sistem kapsamında toplam 10 tablo oluşturulmuştur:

1. `uyeler`
2. `antrenorler`
3. `uyelik_paketleri`
4. `uyelikler`
5. `odemeler`
6. `dersler`
7. `ders_kayitlari`
8. `yoklamalar`
9. `salon_ekipmanlari`
10. `ekipman_bakimlari`

---

## 4.2. Kullanılan Kısıtlar

### Primary Key Kullanımı

Her tabloda benzersiz kayıt tanımlaması yapabilmek için birincil anahtar kullanılmıştır.

Örnek:

- `uye_id`
- `antrenor_id`
- `paket_id`
- `uyelik_id`
- `odeme_id`

---

### Foreign Key Kullanımı

Tablolar arasındaki ilişkileri sağlamak için yabancı anahtarlar kullanılmıştır.

Örnek ilişkiler:

- `uyelikler.uye_id` → `uyeler.uye_id`
- `uyelikler.paket_id` → `uyelik_paketleri.paket_id`
- `odemeler.uyelik_id` → `uyelikler.uyelik_id`
- `dersler.antrenor_id` → `antrenorler.antrenor_id`
- `ders_kayitlari.uye_id` → `uyeler.uye_id`
- `ders_kayitlari.ders_id` → `dersler.ders_id`
- `yoklamalar.ders_kayit_id` → `ders_kayitlari.ders_kayit_id`
- `ekipman_bakimlari.ekipman_id` → `salon_ekipmanlari.ekipman_id`

---

### Unique Kullanımı

Tekrarlı veri girişlerini engellemek için bazı alanlarda Unique kısıtı kullanılmıştır.

Örnek:

- Üye telefon numarası
- Üye e-posta adresi
- Antrenör telefon numarası
- Antrenör e-posta adresi
- Üyelik paketi adı
- Aynı üyenin aynı derse tekrar kayıt olmasını engelleyen `uye_id + ders_id` kısıtı
- Aynı ders kaydı için aynı tarihte tekrar yoklama girilmesini engelleyen `ders_kayit_id + yoklama_tarihi` kısıtı

---

### Not Null Kullanımı

Zorunlu girilmesi gereken alanlarda `NOT NULL` kısıtı kullanılmıştır.

Örnek:

- Üye adı
- Üye soyadı
- Telefon
- Paket adı
- Paket süresi
- Paket ücreti
- Ders adı
- Kontenjan
- Ödeme tutarı

---

### Default Kullanımı

Bazı alanlarda varsayılan değerler tanımlanmıştır.

Örnek:

- Üye kayıt tarihi varsayılan olarak sistem tarihi alınır.
- Üye aktiflik durumu varsayılan olarak aktif atanır.
- Üyelik durumu varsayılan olarak pasif atanır.
- Ödeme tarihi varsayılan olarak sistem tarihi alınır.
- Ödeme durumu varsayılan olarak başarılı atanır.
- Ekipman durumu varsayılan olarak kullanılabilir atanır.

---

### Check Kullanımı

Sayısal veya mantıksal olarak hatalı veri girişlerini engellemek için `CHECK` kısıtları kullanılmıştır.

Örnek:

- Paket süresi 0’dan büyük olmalıdır.
- Paket ücreti 0’dan büyük olmalıdır.
- Ödeme tutarı 0’dan büyük olmalıdır.
- Ders kontenjanı 0’dan büyük olmalıdır.
- Ders bitiş saati başlangıç saatinden sonra olmalıdır.
- Üyelik bitiş tarihi başlangıç tarihinden önce olamaz.
- Bakım maliyeti negatif olamaz.

---

### Auto Increment Kullanımı

Tablolardaki ID alanları otomatik artan şekilde tanımlanmıştır.

Örnek:

- `uye_id INT AUTO_INCREMENT`
- `antrenor_id INT AUTO_INCREMENT`
- `paket_id INT AUTO_INCREMENT`
- `uyelik_id INT AUTO_INCREMENT`
- `odeme_id INT AUTO_INCREMENT`

---

## 4.3. SQL Dosyası

Tablo oluşturma işlemlerine ait SQL kodları aşağıdaki dosyada hazırlanmıştır:

**Dosya Adı:** `01_TabloOlusturma.sql`

Bu dosyada veritabanı seçimi ve tüm tablo oluşturma komutları yer almaktadır.

---

# 5. STORED PROCEDURE KULLANIMI

Bu projede veritabanı işlemleri doğrudan SQL komutları ile değil, Stored Procedure yapıları kullanılarak gerçekleştirilmiştir.

Ödev kapsamında her tablo için aşağıdaki işlemlerin Stored Procedure ile yazılması istenmiştir:

- Insert
- Update
- Delete
- Select / Listeleme

Proje kapsamında toplam 10 tablo bulunduğu için her tabloya 4 işlem yazılmıştır.

**Toplam Stored Procedure Sayısı:** 40

---

## 5.1. Stored Procedure Kullanılan Tablolar

Aşağıdaki tablolar için ekleme, güncelleme, silme ve listeleme procedure’leri oluşturulmuştur:

1. `uyeler`
2. `antrenorler`
3. `uyelik_paketleri`
4. `uyelikler`
5. `odemeler`
6. `dersler`
7. `ders_kayitlari`
8. `yoklamalar`
9. `salon_ekipmanlari`
10. `ekipman_bakimlari`

---

## 5.2. Stored Procedure Listesi

### Uyeler Tablosu

- `sp_uye_ekle`
- `sp_uye_guncelle`
- `sp_uye_sil`
- `sp_uye_listele`

### Antrenorler Tablosu

- `sp_antrenor_ekle`
- `sp_antrenor_guncelle`
- `sp_antrenor_sil`
- `sp_antrenor_listele`

### Uyelik_Paketleri Tablosu

- `sp_uyelik_paketi_ekle`
- `sp_uyelik_paketi_guncelle`
- `sp_uyelik_paketi_sil`
- `sp_uyelik_paketi_listele`

### Uyelikler Tablosu

- `sp_uyelik_ekle`
- `sp_uyelik_guncelle`
- `sp_uyelik_sil`
- `sp_uyelik_listele`

### Odemeler Tablosu

- `sp_odeme_ekle`
- `sp_odeme_guncelle`
- `sp_odeme_sil`
- `sp_odeme_listele`

### Dersler Tablosu

- `sp_ders_ekle`
- `sp_ders_guncelle`
- `sp_ders_sil`
- `sp_ders_listele`

### Ders_Kayitlari Tablosu

- `sp_ders_kayit_ekle`
- `sp_ders_kayit_guncelle`
- `sp_ders_kayit_sil`
- `sp_ders_kayit_listele`

### Yoklamalar Tablosu

- `sp_yoklama_ekle`
- `sp_yoklama_guncelle`
- `sp_yoklama_sil`
- `sp_yoklama_listele`

### Salon_Ekipmanlari Tablosu

- `sp_ekipman_ekle`
- `sp_ekipman_guncelle`
- `sp_ekipman_sil`
- `sp_ekipman_listele`

### Ekipman_Bakimlari Tablosu

- `sp_bakim_ekle`
- `sp_bakim_guncelle`
- `sp_bakim_sil`
- `sp_bakim_listele`

---

## 5.3. Stored Procedure Dosyası

Stored Procedure kodları aşağıdaki dosyada hazırlanmıştır:

**Dosya Adı:** `02_StoredProcedures.sql`

Bu dosyada 10 tablo için toplam 40 adet Stored Procedure yer almaktadır.

---

---

# 6. KULLANICI TANIMLI FUNCTION KULLANIMI

Bu projede, spor salonu işletmesinin ihtiyaçlarına uygun olarak kullanıcı tanımlı function yapıları kullanılmıştır.

Ödev kapsamında senaryo ile ilişkili en az 2 adet function yazılması istenmiştir. Bu projede sistemin daha güçlü ve işlevsel olması için toplam 3 adet function oluşturulmuştur.

**Toplam Function Sayısı:** 3

## 6.1. Function Listesi

### 1. fn_uye_toplam_odeme

Bu function, belirli bir üyenin sistemde yaptığı toplam başarılı ödeme tutarını hesaplar.

**Örnek kullanım:**

```sql
SELECT fn_uye_toplam_odeme(1) AS toplam_odeme;
```

### 2. fn_uyelik_kalan_gun

Bu function, belirli bir üyeliğin bitiş tarihine kaç gün kaldığını hesaplar.

**Örnek kullanım:**

```sql
SELECT fn_uyelik_kalan_gun(1) AS kalan_gun;
```

### 3. fn_ders_doluluk_orani

Bu function, belirli bir dersin kontenjanına göre doluluk oranını yüzde olarak hesaplar.

**Örnek kullanım:**

```sql
SELECT fn_ders_doluluk_orani(1) AS doluluk_orani;
```

## 6.2. Function Dosyası

Function kodları aşağıdaki dosyada hazırlanmıştır:

**Dosya Adı:** `03_Functions.sql`

Bu dosyada toplam 3 adet kullanıcı tanımlı function bulunmaktadır.

---

# 7. TRIGGER KULLANIMI

Bu projede, gerçek hayattaki iş kurallarını veritabanı seviyesinde kontrol etmek için trigger yapıları kullanılmıştır.

Ödev kapsamında en az 2 adet trigger oluşturulması istenmiştir. Bu projede sistemin daha güçlü olması için toplam 3 adet trigger oluşturulmuştur.

**Toplam Trigger Sayısı:** 3

## 7.1. Trigger Listesi

### 1. trg_odeme_eklendi_uyelik_aktif_yap

Bu trigger, `odemeler` tablosuna yeni bir ödeme eklendiğinde çalışır.

Eğer eklenen ödeme başarılı ise ilgili üyelik otomatik olarak `Aktif` durumuna getirilir.

**Gerçek hayat karşılığı:**

Spor salonunda bir üye ödeme yaptığında üyeliğinin otomatik aktif hale gelmesi gerekir. Bu trigger bu iş kuralını temsil eder.

---

### 2. trg_ders_kontenjan_kontrol

Bu trigger, `ders_kayitlari` tablosuna yeni bir ders kaydı eklenmeden önce çalışır.

Dersin mevcut kayıt sayısı kontenjana ulaşmışsa yeni kayıt yapılmasını engeller.

**Gerçek hayat karşılığı:**

Bir grup dersinin belirli bir kontenjanı vardır. Kontenjan dolduğunda yeni üye kaydı alınmamalıdır. Bu trigger ders kontenjan kontrolünü sağlar.

---

### 3. trg_uyelik_tarih_kontrol

Bu trigger, `uyelikler` tablosuna yeni üyelik eklenmeden önce çalışır.

Üyelik bitiş tarihi, başlangıç tarihinden önce girilirse kayıt eklenmesini engeller.

**Gerçek hayat karşılığı:**

Bir üyeliğin bitiş tarihi başlangıç tarihinden önce olamaz. Bu trigger hatalı tarih girişini engeller.

---

## 7.2. Trigger Testleri

Trigger yapılarının çalıştığı MySQL Workbench üzerinde test edilmiştir.

Ödeme eklendiğinde üyelik durumunun otomatik olarak aktif hale geldiği görülmüştür.

Ayrıca bitiş tarihi başlangıç tarihinden önce olan üyelik eklenmeye çalışıldığında sistem hata vermiştir. Böylece tarih kontrol trigger’ının doğru şekilde çalıştığı doğrulanmıştır.

---

## 7.3. Trigger Dosyası

Trigger kodları aşağıdaki dosyada hazırlanmıştır:

**Dosya Adı:** `04_Triggers.sql`

Bu dosyada toplam 3 adet trigger bulunmaktadır.

---

# 8. ADIM-4: UYGULAMA GELİŞTİRME VE N-KATMANLI MİMARİ

Bu projede uygulama geliştirme adımı mobil uygulama olarak planlanmıştır.

Mobil uygulama tarafında kullanıcı arayüzü Flutter ile geliştirilecektir. Veritabanı işlemlerinin doğrudan mobil uygulama içinden yapılması yerine, mobil uygulama ASP.NET Core Web API ile haberleşecektir. API tarafında iş kuralları Business Layer içerisinde yönetilecek, veritabanı erişimleri ise Data Access Layer üzerinden gerçekleştirilecektir.

Bu yapı sayesinde uygulama N-katmanlı mimariye uygun hale getirilmiştir.

---

## 8.1. Kullanılan Mimari Yapı

Projede aşağıdaki mimari yapı kullanılacaktır:

Flutter Mobil Uygulama  
→ ASP.NET Core Web API  
→ Business Layer  
→ Data Access Layer  
→ MySQL Veritabanı  
→ Stored Procedure / Function / Trigger

---

## 8.2. Presentation Layer

Presentation Layer, kullanıcının sistemle etkileşime geçtiği arayüz katmanıdır.

Bu projede Presentation Layer Flutter mobil uygulamasıdır.

Bu katmanda yer alacak temel ekranlar:

- Ana sayfa
- Üye listeleme ekranı
- Üye ekleme ekranı
- Üyelik paketleri ekranı
- Üyelik işlemleri ekranı
- Ödeme işlemleri ekranı
- Ders listeleme ekranı
- Ders kayıt ekranı
- Yoklama ekranı
- Ekipman ve bakım ekranı

Presentation Layer doğrudan veritabanına bağlanmayacaktır. Tüm işlemler API üzerinden yapılacaktır.

---

## 8.3. Business Layer

Business Layer, sistemdeki iş kurallarının kontrol edildiği katmandır.

Bu katmanda örnek olarak aşağıdaki kontroller yapılacaktır:

- Boş alan kontrolü
- Telefon ve e-posta format kontrolü
- Ödeme tutarı kontrolü
- Üyelik tarih kontrolü
- Ders kontenjan kontrolü
- Aktif/pasif durum kontrolü

Business Layer, Presentation Layer’dan gelen istekleri kontrol eder ve uygun işlemler için Data Access Layer’a yönlendirir.

---

## 8.4. Data Access Layer

Data Access Layer, veritabanı ile iletişim kuran katmandır.

Bu projede en önemli kural şudur:

Uygulama içerisinde doğrudan SELECT, INSERT, UPDATE veya DELETE komutları kullanılmayacaktır.

Tüm veritabanı işlemleri yalnızca Stored Procedure çağrıları üzerinden yapılacaktır.

Örnek:

- Üye ekleme işlemi için `sp_uye_ekle`
- Üye güncelleme işlemi için `sp_uye_guncelle`
- Üye silme işlemi için `sp_uye_sil`
- Üye listeleme işlemi için `sp_uye_listele`

Bu yaklaşım, ödevde belirtilen DAL üzerinden Stored Procedure kullanımı şartını karşılamaktadır.

---

## 8.5. Veritabanı Katmanı

Veritabanı katmanı MySQL üzerinde oluşturulmuştur.

Bu katmanda aşağıdaki yapılar bulunmaktadır:

- 10 tablo
- 40 Stored Procedure
- 3 Function
- 3 Trigger
- Örnek veriler
- Test sorguları

Veritabanı kodları `02_Database` klasörü altında hazırlanmıştır.

---

## 8.6. Uygulama Ekran Görüntüleri

Uygulama geliştirildikten sonra mobil uygulamaya ait ekran görüntüleri bu bölüme eklenecektir.

Eklenecek örnek ekran görüntüleri:

- Ana sayfa
- Üye listeleme
- Üye ekleme
- Ödeme listeleme
- Ders listeleme
- Ders kayıt ekranı
- Yoklama ekranı
- Ekipman bakım ekranı

---

# 9. UYGULAMA VE TEST EKRAN GÖRÜNTÜLERİ

Bu bölümde geliştirilen sistemin çalıştığını gösteren ekran görüntüleri yer almaktadır.

Proje kapsamında önce MySQL veritabanı oluşturulmuş, ardından ASP.NET Core Web API ile veritabanına bağlantı sağlanmıştır. API tarafında veritabanı işlemleri Data Access Layer üzerinden Stored Procedure çağrıları ile gerçekleştirilmiştir. Daha sonra Flutter uygulaması bu API üzerinden üye verilerini çekerek ekranda listelemiştir.

---

## 9.1. API Üye Listeleme Ekranı

Bu ekran görüntüsünde `/api/uyeler` endpoint’i üzerinden üyelerin JSON formatında listelendiği görülmektedir.

Bu işlem sırasında sistem aşağıdaki akışla çalışmıştır:

Flutter / Tarayıcı isteği  
→ ASP.NET Core API  
→ Business Layer  
→ Data Access Layer  
→ `sp_uye_listele` Stored Procedure  
→ MySQL Veritabanı

**Ekran Görüntüsü Dosyası:**

`api_uyeler_listeleme.png`

---

## 9.2. Flutter Üye Listesi Ekranı

Bu ekran görüntüsünde Flutter uygulamasının API’den aldığı üye verilerini kullanıcı arayüzünde listelediği görülmektedir.

Flutter uygulaması doğrudan veritabanına bağlanmamıştır. Veriler API üzerinden alınmıştır. API ise Data Access Layer aracılığıyla Stored Procedure çağırmıştır.

**Ekran Görüntüsü Dosyası:**

`flutter_uye_listesi.png`

---

## 9.3. Test Edilen Yapılar

Proje kapsamında aşağıdaki yapılar test edilmiştir:

- MySQL veritabanı bağlantısı
- Tablo oluşturma işlemleri
- Stored Procedure ile veri ekleme
- Stored Procedure ile veri listeleme
- Function çalıştırma
- Trigger çalıştırma
- API üzerinden üye listeleme
- Flutter uygulaması üzerinden üye listeleme

---

# 10. TESLİM BİLGİLERİ, GITHUB VE VİDEO ANLATIM

Bu bölümde proje teslim süreci, GitHub yükleme bilgileri ve video anlatım planı açıklanmıştır.

---

## 10.1. Teslim Dosyası

Ödev tesliminde proje tek dosya olarak PDF veya Word formatında yüklenecektir.

Teslim dosyasında aşağıdaki içerikler yer alacaktır:

- Proje konusu
- Detaylı senaryo
- Varlıklar ve nitelikler
- Varlıklar arası ilişkiler
- ER diyagramı
- İlişkisel model
- Fiziksel tablo tasarımı
- SQL tablo oluşturma kodları
- Stored Procedure kodları
- Function kodları
- Trigger kodları
- Örnek veriler
- Test sorguları
- Uygulama mimarisi
- API ekran görüntüsü
- Flutter uygulama ekran görüntüsü
- GitHub linki
- Video anlatım linki

---

## 10.2. GitHub Yükleme

Proje dosyaları GitHub üzerine yüklenecektir.

GitHub üzerinde aşağıdaki klasör yapısı korunacaktır:

- `01_Dokuman`
- `02_Database`
- `03_Api`
- `04_Mobil`
- `05_EkranGoruntuleri`
- `06_Video`

GitHub linki teslim dosyasına eklenecektir.

**GitHub Linki:**

Buraya GitHub proje linki eklenecektir.

---

## 10.3. Video Anlatım

Video anlatım 5-10 dakika aralığında hazırlanacaktır.

Videoda aşağıdaki adımlar gösterilecektir:

1. Proje konusu ve senaryosu açıklanacaktır.
2. ER diyagramı gösterilecektir.
3. MySQL tabloları gösterilecektir.
4. Stored Procedure listesi gösterilecektir.
5. Function ve Trigger yapıları açıklanacaktır.
6. Örnek veriler gösterilecektir.
7. API üzerinden `/api/uyeler` endpoint’inin çalıştığı gösterilecektir.
8. Flutter uygulamasında üye listesinin API’den geldiği gösterilecektir.
9. Uygulamanın N-katmanlı mimariye uygun çalıştığı açıklanacaktır.

**Video Linki:**

Buraya video anlatım linki eklenecektir.

---

## 10.4. Genel Sonuç

Bu proje kapsamında spor salonu işletmesine yönelik üyelik, antrenör, ders, ödeme, yoklama ve ekipman bakım süreçlerini yöneten bir veritabanı ve uygulama sistemi geliştirilmiştir.

Veritabanı tarafında 10 tablo, 40 Stored Procedure, 3 Function ve 3 Trigger oluşturulmuştur. Uygulama tarafında ASP.NET Core Web API ve Flutter kullanılmıştır. Sistem, N-katmanlı mimariye uygun olarak API, Business Layer, Data Access Layer ve Entity Layer yapılarıyla geliştirilmiştir.

Veritabanı işlemleri doğrudan SQL komutlarıyla değil, Data Access Layer üzerinden Stored Procedure çağrılarıyla gerçekleştirilmiştir. Bu sayede proje, ödevde belirtilen temel veritabanı tasarımı ve uygulama geliştirme şartlarına uygun şekilde hazırlanmıştır.

---

# 11. UYGULAMADA CRUD İŞLEMLERİ

Bu bölümde Flutter uygulaması üzerinden gerçekleştirilen temel veri işlemleri açıklanmıştır.

Uygulama doğrudan veritabanına bağlanmamaktadır. Kullanıcı işlemleri Flutter arayüzünden başlamakta, ASP.NET Core Web API üzerinden Business Layer’a, oradan Data Access Layer’a ulaşmakta ve son olarak MySQL tarafındaki Stored Procedure yapıları çalıştırılmaktadır.

Bu akış aşağıdaki gibidir:

Flutter Uygulaması  
→ ASP.NET Core Web API  
→ Business Layer  
→ Data Access Layer  
→ Stored Procedure  
→ MySQL Veritabanı

---

## 11.1. Üye Listeleme İşlemi

Üye listeleme işlemi Flutter uygulaması üzerinden yapılmıştır.

Bu işlemde API tarafında `/api/uyeler` endpoint’i çalıştırılmıştır. Data Access Layer içinde doğrudan SQL komutu yazılmamış, `sp_uye_listele` Stored Procedure çağrılmıştır.

**Kullanılan Stored Procedure:**

`sp_uye_listele`

**Ekran Görüntüsü:**

`flutter_uye_listesi.png`

---

## 11.2. Üye Ekleme İşlemi

Flutter uygulamasında “Üye Ekle” butonu ile yeni üye ekleme formu açılmıştır. Girilen üye bilgileri API’ye gönderilmiş, API bu işlemi Business Layer üzerinden Data Access Layer’a aktarmıştır.

Data Access Layer içinde `sp_uye_ekle` Stored Procedure çalıştırılmıştır.

**Kullanılan Stored Procedure:**

`sp_uye_ekle`

**Ekran Görüntüsü:**

`flutter_uye_ekleme_sonrasi.png`

---

## 11.3. Üye Güncelleme İşlemi

Flutter uygulamasında üye kartı üzerindeki güncelleme butonu ile üye bilgileri düzenlenmiştir.

Güncelleme işlemi API üzerinden gerçekleştirilmiş ve Data Access Layer içinde `sp_uye_guncelle` Stored Procedure çağrılmıştır.

**Kullanılan Stored Procedure:**

`sp_uye_guncelle`

**Ekran Görüntüsü:**

`flutter_uye_guncelleme_sonrasi.png`

---

## 11.4. Üye Silme İşlemi

Flutter uygulamasında üye kartı üzerindeki silme butonu ile üye silme işlemi test edilmiştir.

Silme işlemi API üzerinden gerçekleştirilmiş ve Data Access Layer içinde `sp_uye_sil` Stored Procedure çağrılmıştır.

**Kullanılan Stored Procedure:**

`sp_uye_sil`

**Ekran Görüntüsü:**

`flutter_uye_silme_sonrasi.png`

---

## 11.5. Değerlendirme

Bu bölümde uygulama üzerinde temel CRUD işlemleri gösterilmiştir. Listeleme, ekleme, güncelleme ve silme işlemlerinin tamamı doğrudan SQL komutlarıyla değil, Stored Procedure çağrılarıyla yapılmıştır.

Bu nedenle uygulama geliştirme kısmı, N-katmanlı mimari ve Data Access Layer üzerinden Stored Procedure kullanımı şartlarına uygun şekilde hazırlanmıştır.