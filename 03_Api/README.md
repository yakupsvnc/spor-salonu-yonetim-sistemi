# Spor Salonu Üyelik, Ders, Antrenör ve Ödeme Yönetim Sistemi

Bu proje, Veritabanı Yönetim Sistemleri-II dersi kapsamında hazırlanmıştır.

Projede bir spor salonu işletmesine ait üye, üyelik paketi, antrenör, ders, ödeme, yoklama ve ekipman bakım süreçleri yönetilmektedir.

## Kullanılan Teknolojiler

- MySQL
- MySQL Workbench
- ASP.NET Core Web API
- C#
- Flutter
- Dart
- N-Katmanlı Mimari

## Proje Yapısı

```text
SporSalonuProjesi
├── 01_Dokuman
├── 02_Database
├── 03_Api
├── 04_Mobil
├── 05_EkranGoruntuleri
└── 06_Video
```

## Veritabanı Özellikleri

Projede MySQL veritabanı kullanılmıştır.

Veritabanı tarafında aşağıdaki yapılar oluşturulmuştur:

- 10 tablo
- 40 Stored Procedure
- 3 Function
- 3 Trigger
- Örnek veriler
- Test sorguları

## Oluşturulan Tablolar

- uyeler
- antrenorler
- uyelik_paketleri
- uyelikler
- odemeler
- dersler
- ders_kayitlari
- yoklamalar
- salon_ekipmanlari
- ekipman_bakimlari

## Stored Procedure Yapısı

Her tablo için temel CRUD işlemleri Stored Procedure olarak hazırlanmıştır:

- Insert
- Update
- Delete
- Select / Listeleme

Toplam 10 tablo için 40 adet Stored Procedure oluşturulmuştur.

## Function Yapısı

Projede 3 adet kullanıcı tanımlı Function bulunmaktadır:

- fn_uye_toplam_odeme
- fn_uyelik_kalan_gun
- fn_ders_doluluk_orani

## Trigger Yapısı

Projede 3 adet Trigger bulunmaktadır:

- trg_odeme_eklendi_uyelik_aktif_yap
- trg_ders_kontenjan_kontrol
- trg_uyelik_tarih_kontrol

Bu trigger yapıları ödeme sonrası üyeliğin aktif yapılması, ders kontenjan kontrolü ve üyelik tarih kontrolü gibi gerçek hayat iş kurallarını temsil etmektedir.

## Uygulama Özellikleri

Flutter uygulaması üzerinden üye işlemleri yapılabilmektedir:

- Üye listeleme
- Üye ekleme
- Üye güncelleme
- Üye silme

Uygulama doğrudan veritabanına bağlanmaz. İşlemler aşağıdaki akışla çalışır:

```text
Flutter
→ ASP.NET Core Web API
→ Business Layer
→ Data Access Layer
→ Stored Procedure
→ MySQL
```

## N-Katmanlı Mimari

Proje N-katmanlı mimari yapısına uygun olarak hazırlanmıştır.

API tarafında aşağıdaki katmanlar bulunmaktadır:

```text
SporSalonu.Api
SporSalonu.Business
SporSalonu.DataAccess
SporSalonu.Entities
```

Katmanların çalışma sırası:

```text
API
→ Business
→ DataAccess
→ Entities / MySQL
```

## API Çalıştırma

Önce aşağıdaki örnek dosyaya göre kendi `appsettings.json` dosyanızı oluşturun:

```text
03_Api/SporSalonu.Api/appsettings.Example.json
```

`appsettings.json` içinde kendi MySQL şifrenizi yazmanız gerekir.

Daha sonra API projesini çalıştırmak için:

```bash
cd 03_Api
dotnet run --project SporSalonu.Api
```

API çalıştıktan sonra tarayıcıdan aşağıdaki adres test edilebilir:

```text
http://localhost:5193/api/uyeler
```

## Flutter Uygulamasını Çalıştırma

Flutter uygulamasını çalıştırmak için:

```bash
cd 04_Mobil/spor_salonu_mobil
flutter pub get
flutter run -d chrome
```

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

## Ekran Görüntüleri

Uygulama ve API ekran görüntüleri `05_EkranGoruntuleri` klasörü altında tutulmaktadır.

Örnek ekran görüntüleri:

- API üye listeleme
- Flutter üye listeleme
- Flutter üye ekleme
- Flutter üye güncelleme
- Flutter üye silme

## Güvenlik Notu

`appsettings.json` dosyası veritabanı şifresi içerdiği için GitHub’a eklenmemiştir.

Bunun yerine örnek bağlantı dosyası olarak şu dosya eklenmiştir:

```text
appsettings.Example.json
```

## Proje Durumu

Tamamlanan temel işlemler:

- Veritabanı tasarımı
- ER diyagramı
- İlişkisel model
- Fiziksel tablo tasarımı
- Stored Procedure yapıları
- Function yapıları
- Trigger yapıları
- ASP.NET Core Web API
- Flutter arayüzü
- Üye CRUD işlemleri
- API ve Flutter bağlantısı

## Sonuç

Bu proje kapsamında spor salonu işletmesine yönelik üyelik, antrenör, ders, ödeme, yoklama ve ekipman bakım süreçlerini yöneten bir veritabanı ve uygulama sistemi geliştirilmiştir.

Veritabanı tarafında MySQL kullanılmış, uygulama tarafında ASP.NET Core Web API ve Flutter tercih edilmiştir.

Sistem N-katmanlı mimariye uygun olarak hazırlanmış ve veritabanı işlemleri doğrudan SQL komutlarıyla değil, Data Access Layer üzerinden Stored Procedure çağrılarıyla gerçekleştirilmiştir.