# Spor Salonu Üyelik, Ders, Antrenör ve Ödeme Yönetim Sistemi

Bu proje, BTS304 - Veritabanı Yönetim Sistemleri-II dersi final ek ödevi kapsamında hazırlanmıştır.

Projede gerçek hayatta faaliyet gösteren bir spor salonu işletmesinin üyelik, antrenör, üyelik paketi, ödeme, ders, ders kaydı, yoklama, ekipman ve bakım süreçlerini yönetebileceği bir veritabanı ve masaüstü yönetim uygulaması geliştirilmiştir.

Ana teslim uygulaması **Python + PyQt5 masaüstü uygulamasıdır**.

---

## Proje Konusu

Spor salonlarında üye kayıtları, üyelik paketleri, ödemeler, grup dersleri, antrenörler, yoklamalar ve ekipman bakımları düzenli olarak takip edilmelidir.

Bu proje, bu süreçleri MySQL veritabanı üzerinde merkezi ve kontrollü bir şekilde yönetmek için geliştirilmiştir.

---

## Kullanılan Teknolojiler

- Python
- PyQt5
- MySQL
- MySQL Workbench
- Stored Procedure
- Function
- Trigger
- N-Katmanlı Mimari
- Git / GitHub

---

## Proje Yapısı

```text
SporSalonuProjesi
├── 01_Dokuman
├── 02_Database
├── 03_Api
├── 04_Desktop_PyQt
├── 04_Mobil
├── 05_EkranGoruntuleri
└── README.md
```

> Not: Ana teslim uygulaması `04_Desktop_PyQt` klasörü altındaki PyQt5 masaüstü uygulamasıdır.  
> `03_Api` ve `04_Mobil` klasörleri önceki/alternatif çalışma yapıları olarak repoda bulunabilir; final anlatımında ana uygulama olarak PyQt5 masaüstü uygulaması kullanılacaktır.

---

## Ana Uygulama Klasörü

```text
04_Desktop_PyQt
```

Bu klasörde PyQt5 ile geliştirilen masaüstü uygulaması yer almaktadır.

Uygulamada aşağıdaki ekranlar/modüller bulunmaktadır:

- Giriş ekranı
- Dashboard
- Üyeler
- Antrenörler
- Paketler
- Üyelikler
- Ödemeler
- Dersler
- Ders Kayıtları
- Yoklamalar
- Ekipmanlar
- Bakımlar

---

## Veritabanı Özellikleri

Projede MySQL veritabanı kullanılmıştır.

Veritabanı adı:

```text
spor_salonu_db
```

Veritabanı tarafında aşağıdaki yapılar oluşturulmuştur:

- 10 tablo
- 40 Stored Procedure
- 3 Function
- 3 Trigger
- Örnek veriler
- Test sorguları

---

## Oluşturulan Tablolar

Projede toplam 10 tablo bulunmaktadır:

- `uyeler`
- `antrenorler`
- `uyelik_paketleri`
- `uyelikler`
- `odemeler`
- `dersler`
- `ders_kayitlari`
- `yoklamalar`
- `salon_ekipmanlari`
- `ekipman_bakimlari`

---

## Stored Procedure Yapısı

Ödev şartına uygun olarak her tablo için temel CRUD işlemleri Stored Procedure olarak hazırlanmıştır.

Her tablo için:

- Ekleme
- Güncelleme
- Silme
- Listeleme / Sorgulama

işlemleri Stored Procedure ile yapılmaktadır.

Toplam:

```text
10 tablo x 4 işlem = 40 Stored Procedure
```

Örnek üye procedure’leri:

- `sp_uye_ekle`
- `sp_uye_guncelle`
- `sp_uye_sil`
- `sp_uye_listele`

---

## Function Yapısı

Projede senaryo ile ilişkili 3 adet kullanıcı tanımlı Function bulunmaktadır:

- `fn_uye_toplam_odeme`
- `fn_uyelik_kalan_gun`
- `fn_ders_doluluk_orani`

Bu function’lar üyelerin toplam ödeme tutarını, üyeliğin kalan gün sayısını ve ders doluluk oranını hesaplamak için kullanılmaktadır.

---

## Trigger Yapısı

Projede gerçek hayattaki iş kurallarını temsil eden 3 adet Trigger bulunmaktadır:

- `trg_odeme_eklendi_uyelik_aktif_yap`
- `trg_ders_kontenjan_kontrol`
- `trg_uyelik_tarih_kontrol`

Bu trigger yapıları:

- Başarılı ödeme sonrası üyeliği otomatik aktif yapar.
- Ders kontenjanı dolduğunda yeni kayıt eklenmesini engeller.
- Üyelik bitiş tarihinin başlangıç tarihinden önce girilmesini engeller.

---

## N-Katmanlı Mimari

Proje N-katmanlı mimari mantığına uygun şekilde hazırlanmıştır.

Kullanılan genel akış:

```text
Presentation Layer
→ Service / Business Layer
→ Data Access Layer
→ Stored Procedure
→ MySQL Veritabanı
```

### Presentation Layer

PyQt5 ile geliştirilen masaüstü arayüzdür.

Kullanıcının gördüğü giriş ekranı, dashboard, üyeler, antrenörler, paketler, ödemeler, dersler, yoklamalar ve bakım ekranları bu katmanda yer alır.

### Service / Business Layer

Arayüzden gelen işlemleri karşılayan ve uygun veri erişim metoduna yönlendiren katmandır.

Bu katmanda kullanıcı işlemleri düzenlenir ve DAL katmanına aktarılır.

### Data Access Layer

MySQL veritabanı ile iletişim kuran katmandır.

Bu projede veritabanı işlemleri doğrudan SQL komutlarıyla yapılmaz. Tüm veri işlemleri Stored Procedure çağrıları üzerinden gerçekleştirilir.

---

## SQL Dosyaları

Veritabanı kodları `02_Database` klasörü altında yer almaktadır.

```text
02_Database
├── 01_TabloOlusturma.sql
├── 02_StoredProcedures.sql
├── 03_Functions.sql
├── 04_Triggers.sql
├── 05_OrnekVeriler.sql
└── 06_TestSorgulari.sql
```

Kurulum sırasında bu dosyalar sırasıyla MySQL Workbench üzerinde çalıştırılmalıdır.

---

## Uygulama Özellikleri

PyQt5 masaüstü uygulaması üzerinden aşağıdaki işlemler yapılabilmektedir:

- Üye listeleme
- Üye ekleme
- Üye güncelleme
- Üye silme
- Antrenör yönetimi
- Üyelik paketi yönetimi
- Üyelik yönetimi
- Ödeme yönetimi
- Ders yönetimi
- Ders kayıt yönetimi
- Yoklama yönetimi
- Ekipman yönetimi
- Bakım yönetimi
- Dashboard üzerinden genel özet görüntüleme

---

## Kurulum ve Çalıştırma

### 1. MySQL Veritabanını Oluşturma

Önce MySQL Workbench açılır.

`02_Database` klasöründeki SQL dosyaları aşağıdaki sırayla çalıştırılır:

```text
1. 01_TabloOlusturma.sql
2. 02_StoredProcedures.sql
3. 03_Functions.sql
4. 04_Triggers.sql
5. 05_OrnekVeriler.sql
6. 06_TestSorgulari.sql
```

Bu işlem sonunda `spor_salonu_db` veritabanı, tablolar, Stored Procedure’ler, Function’lar, Trigger’lar ve örnek veriler oluşturulur.

---

### 2. Python Paketlerini Kurma

Terminal veya PowerShell üzerinden proje klasörüne girilir:

```bash
cd 04_Desktop_PyQt
```

Gerekli Python paketleri kurulur:

```bash
pip install PyQt5
pip install mysql-connector-python
```

> Not: Projede farklı MySQL bağlantı paketi kullanıldıysa, ilgili paket ayrıca kurulmalıdır.

---

### 3. Veritabanı Bağlantı Ayarları

Uygulamanın MySQL’e bağlanabilmesi için veritabanı bağlantı ayarları proje içindeki yapılandırma dosyasından düzenlenmelidir.

Genel bağlantı bilgileri:

```text
Host: localhost
Database: spor_salonu_db
User: root
Password: kendi MySQL şifreniz
```

Şifre bilgisi kişisel olduğu için GitHub üzerinde açık şekilde paylaşılmamalıdır.

---

### 4. Uygulamayı Çalıştırma

`04_Desktop_PyQt` klasörü içindeyken aşağıdaki komut çalıştırılır:

```bash
python main.py
```

Alternatif olarak varsa başlatma dosyası çalıştırılabilir:

```text
UYGULAMAYI_BASLAT.bat
```

---

## Varsayılan Giriş Bilgileri

Uygulama giriş ekranında varsayılan yönetici hesabı:

```text
Kullanıcı Adı: admin
Şifre: admin123
```

---

## Ekran Görüntüleri

Uygulama ve test ekran görüntüleri `05_EkranGoruntuleri` klasörü altında tutulmaktadır.

Rapora eklenmesi önerilen ekran görüntüleri:

- Giriş ekranı
- Dashboard ekranı
- Üye yönetimi ekranı
- Üye ekleme işlemi
- Üye güncelleme işlemi
- Üye silme işlemi
- Antrenörler ekranı
- Paketler ekranı
- Ödemeler ekranı
- Dersler ekranı
- MySQL tablo listesi
- Stored Procedure listesi
- Function testleri
- Trigger testleri
- ER diyagramı

---

## GitHub ve Teslim Notu

Proje GitHub üzerinde erişilebilir durumda tutulmalıdır.

Teslim dosyasında aşağıdakiler yer almalıdır:

- Proje raporu
- ER diyagramı
- SQL kodları
- Açıklamalar
- Uygulama ekran görüntüleri
- GitHub linki
- Video anlatım linki

GitHub linki:

```text
https://github.com/yakupsvnc/spor-salonu-yonetim-sistemi
```

---

## Video Anlatımda Gösterilecekler

Video anlatımda aşağıdaki adımlar gösterilmelidir:

1. Proje konusu ve senaryosu
2. ER diyagramı
3. MySQL tabloları
4. Stored Procedure listesi
5. Function testleri
6. Trigger testleri
7. PyQt5 giriş ekranı
8. Dashboard ekranı
9. Üye listeleme
10. Üye ekleme
11. Üye güncelleme
12. Üye silme
13. Diğer modüllerin kısa gösterimi
14. GitHub reposunun erişilebilir olduğunun gösterilmesi

---

## Önemli Not

Bu projede veritabanı işlemleri doğrudan `SELECT`, `INSERT`, `UPDATE`, `DELETE` komutlarıyla yapılmamalıdır.

Tüm veritabanı işlemleri Data Access Layer içinde Stored Procedure çağrıları üzerinden gerçekleştirilmelidir.

Bu yapı, ödevde belirtilen N-katmanlı mimari ve DAL üzerinden Stored Procedure kullanımı şartına uygun olarak hazırlanmıştır.

---

## Sonuç

Bu proje kapsamında spor salonu işletmesine yönelik üyelik, antrenör, ders, ödeme, yoklama ve ekipman bakım süreçlerini yöneten bir veritabanı ve masaüstü uygulama sistemi geliştirilmiştir.

Veritabanı tarafında MySQL kullanılmış; tablo, Stored Procedure, Function ve Trigger yapıları oluşturulmuştur.

Uygulama tarafında Python ve PyQt5 kullanılmıştır. Sistem, N-katmanlı mimariye uygun olarak hazırlanmış ve veritabanı işlemleri Data Access Layer üzerinden Stored Procedure çağrılarıyla gerçekleştirilmiştir.