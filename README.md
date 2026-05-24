# Spor Salonu Yönetim Sistemi

BTS304 Veritabanı Yönetim Sistemleri-II — Final Ek Ödev  
**Konu:** Spor salonu üyelik, ders, ödeme ve ekipman yönetimi

## Proje Yapısı

```
SporSalonuProjesi/
├── 01_Dokuman/          Senaryo, ER diyagramı
├── 02_Database/         MySQL tablolar, SP, trigger, function
├── 03_Api/              ASP.NET Core API (referans)
├── 04_Desktop_PyQt/     ★ PyQt5 masaüstü uygulaması (ANA UYGULAMA)
├── 04_Mobil/            Flutter mobil (eski sürüm)
├── 05_EkranGoruntuleri/ Ekran görüntüleri
└── 06_Video/            Tanıtım videosu
```

## Hızlı Başlangıç (Hoca / Değerlendirici)

### 1. MySQL veritabanını kurun

MySQL Workbench'te **sırayla** çalıştırın:

1. `02_Database/01_TabloOlusturma.sql`
2. `02_Database/02_StoredProcedures.sql`
3. `02_Database/03_Functions.sql`
4. `02_Database/04_Triggers.sql`
5. `02_Database/05_OrnekVeriler.sql` *(isteğe bağlı)*

### 2. Python uygulamasını kurun

```bash
cd 04_Desktop_PyQt
pip install -r requirements.txt
copy config_example.py config.py
```

`config.py` içinde MySQL `password` alanına kendi root şifrenizi yazın.

### 3. Uygulamayı başlatın

Windows: `04_Desktop_PyQt/UYGULAMAYI_BASLAT.bat` dosyasına çift tıklayın.

veya:

```bash
cd 04_Desktop_PyQt
python main.py
```

### Giriş bilgileri

| Alan | Değer |
|------|-------|
| Kullanıcı adı | `admin` |
| Şifre | `admin123` |
| MySQL | Giriş ekranında **Veritabanı Ayarları** ile veya `config.py` ile |

## Mimari (N-Katmanlı)

```
Presentation (PyQt5 UI)
    ↓
Business Layer (services/*.py)
    ↓
Data Access Layer (dal/*.py → CALL sp_...)
    ↓
MySQL (spor_salonu_db)
```

Tüm CRUD işlemleri **yalnızca Stored Procedure** ile yapılır. UI katmanında doğrudan SQL yoktur.

## Özellikler

- 10 tablo — tam CRUD
- 40 Stored Procedure
- 3 Trigger (ödeme→üyelik aktif, kontenjan, tarih kontrolü)
- 3 Function (toplam ödeme, kalan gün, doluluk oranı)
- Dashboard, arama, modern koyu tema arayüz

## Gereksinimler

- Python 3.8+
- MySQL 8.0+
- PyQt5, mysql-connector-python
