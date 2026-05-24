# 📚 SPOR SALONU YÖNETİM SİSTEMİ - KURULUM REHBERİ

Hoşgeldiniz! Bu dokümanda projeyi kendi bilgisayarınızda kurma, veritabanı oluşturma ve çalıştırma adımları açıklanmıştır.

---

## 1️⃣ SİSTEM GEREKSINIMLERI

Aşağıdaki yazılımlar **mutlaka** yüklü olmalıdır:

- **Python 3.10+** - https://www.python.org/downloads/
- **MySQL Server 8.0+** - https://dev.mysql.com/downloads/mysql/
- **Git** - https://git-scm.com/download/win (opsiyonel ama tavsiye edilir)

---

## 2️⃣ PROJE DOSYALARINI İNDİRME

### Seçenek A: Git Kullanarak (Tavsiye Edilir)

```powershell
# Projeyi klonlayın
git clone https://github.com/username/SporSalonuProjesi.git
cd SporSalonuProjesi
```

### Seçenek B: ZIP İndir

Projeyi GitHub'dan ZIP olarak indirip açın.

---

## 3️⃣ PYTHON VE BAĞIMLILIKLARI KURMA

```powershell
# Desktop uygulaması klasörüne girin
cd 04_Desktop_PyQt

# Python sanal ortamı oluşturun (önerilir)
python -m venv venv

# Sanal ortamı etkinleştirin
# Windows için:
venv\Scripts\activate
# veya PowerShell için:
.\venv\Scripts\Activate.ps1

# Gerekli paketleri kurun
pip install -r requirements.txt
```

### Kurulacak Paketler:
- PyQt5 - Kullanıcı arayüzü
- mysql-connector-python - MySQL bağlantısı
- python-dotenv - Ayar yönetimi

---

## 4️⃣ MYSQL VERİTABANINI KURMA

### Adım 1: MySQL'i Başlatın

```powershell
# MySQL komut satırına girin
mysql -u root -p

# Şifre sorulursa MySQL kurulumunda belirlediğiniz şifreyi girin
```

### Adım 2: Veritabanı Oluşturun

MySQL komut satırında şu komutları çalıştırın:

```sql
-- Veritabanı oluştur
CREATE DATABASE IF NOT EXISTS spor_salonu_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Veritabanını seç
USE spor_salonu_db;
```

### Adım 3: Tabloları Oluşturun

Proje klasörüne gidin ve aşağıdaki SQL dosyalarını sırasıyla çalıştırın:

```powershell
# MySQL'den çık (exit yazıp Enter'e basın)

# Projeye geri dön
cd ..
cd 02_Database

# SQL dosyalarını çalıştır (sırasıyla)
mysql -u root -p spor_salonu_db < 01_TabloOlusturma.sql
mysql -u root -p spor_salonu_db < 02_StoredProcedures.sql
mysql -u root -p spor_salonu_db < 03_Functions.sql
mysql -u root -p spor_salonu_db < 04_Triggers.sql
mysql -u root -p spor_salonu_db < 05_OrnekVeriler.sql
```

> 💡 Her komut çalıştığında şifre sorulacak - MySQL şifrenizi girin

---

## 5️⃣ UYGULAMAYININ AYARLARINI YAPMA

### Adım 1: config.py Oluştur

```powershell
cd 04_Desktop_PyQt

# config_example.py'yi config.py olarak kopyala
Copy-Item config_example.py config.py
```

### Adım 2: config.py'yi Düzelt

`config.py` dosyasını not defteri ile açın ve **MySQL şifrenizi** girin:

```python
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "BuYereKendiMySQLSifreniziyaziN",  # ← BURAYA yazın!
    "database": "spor_salonu_db",
    "charset": "utf8mb4",
    ...
}

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
```

**Giriş Bilgileri:**
- Kullanıcı Adı: `admin`
- Şifre: `admin123`

> ⚠️ **GÜVENLİK NOT:** `config.py` GitHub'a yüklenmez. Gerçek şifreniz güvende kalır.

---

## 6️⃣ UYGULAMAYINI ÇALIŞTIRMA

### Adım 1: Doğru Klasörde Olun

```powershell
# Eğer değilseniz, Desktop_PyQt klasörüne girin
cd 04_Desktop_PyQt

# Sanal ortamı etkinleştirin (eğer devre dışı ise)
.\venv\Scripts\Activate.ps1
```

### Adım 2: Uygulamayı Başlat

```powershell
python main.py
```

**Başarılıysa:**
- 🎉 Giriş ekranı açılacak
- Kullanıcı adı: `admin`
- Şifre: `admin123`

---

## 7️⃣ SORUN GIDERME

### ❌ Hata: "No module named 'PyQt5'"

```powershell
# Paketleri yeniden kurun
pip install -r requirements.txt
```

### ❌ Hata: "Connection refused" veya "Can't connect to MySQL"

1. **MySQL çalışıyor mu kontrol edin:**
   ```powershell
   # Windows Services'ten MySQL'i başlatın
   # veya
   mysql -u root -p
   ```

2. **config.py'de host ve port doğru mu kontrol edin:**
   - Host: `localhost` (veya `127.0.0.1`)
   - Port: `3306` (varsayılan)
   - Kullanıcı: `root`
   - Şifre: **MySQL kurulumu sırasında belirlediğiniz şifre**

### ❌ Hata: "Database 'spor_salonu_db' doesn't exist"

SQL dosyalarını yeniden çalıştırın (Bölüm 4, Adım 3):

```powershell
cd 02_Database
mysql -u root -p spor_salonu_db < 01_TabloOlusturma.sql
mysql -u root -p spor_salonu_db < 02_StoredProcedures.sql
# vs...
```

### ❌ Hata: "Access denied for user 'root'"

`config.py` dosyasındaki MySQL şifresini kontrol edin. Doğru şifre yazıldığından emin olun.

---

## 8️⃣ PROJE YAPISI

```
SporSalonuProjesi/
├── 01_Dokuman/           # Proje belgeleri, ER diyagramı
├── 02_Database/          # MySQL SQL dosyaları
├── 03_Api/               # C# .NET API (opsiyonel)
├── 04_Desktop_PyQt/      # Ana Desktop Uygulaması 👈 BURADAN ÇALIŞTIRIN
│   ├── main.py           # Uygulamayı başlatan dosya
│   ├── login_window.py   # Giriş ekranı
│   ├── main_window.py    # Ana pencere ve tüm sekmeler
│   ├── config.py         # Ayarlar (GitHub'a yüklenmez)
│   ├── config_example.py # Ayar şablonu
│   ├── requirements.txt   # Python paketleri
│   ├── styles.py         # UI tasarımı
│   ├── dialogs.py        # Diyaloglar
│   ├── widgets.py        # Yardımcı widgetler
│   ├── database/         # Veritabanı bağlantısı
│   ├── dal/              # Veri erişim katmanı
│   └── services/         # İş mantığı servisleri
├── 04_Mobil/            # Flutter mobil uygulaması
├── README.md            # Proje açıklaması
└── KURULUM_METNI.md     # Bu dosya
```

---

## 9️⃣ VERİTABANI BAĞLANTISINI TEST ETME

Uygulamayı çalıştırdıktan sonra:

1. **Giriş yapın:**
   - Kullanıcı Adı: `admin`
   - Şifre: `admin123`

2. **Ana pencereye girin**

3. **Sağ alttaki ⚙️ Ayarlar sekmesine tıklayın**

4. **"🔗 Bağlantı Testini Çalıştır" butonuna basın**

✅ Yeşil başarı mesajı görülürse bağlantı tamam!

---

## 🔟 VERITABANINDA VERİ KONTROL ETME

```powershell
mysql -u root -p

# MySQL'de
USE spor_salonu_db;
SHOW TABLES;                    # Tüm tabloları listele
SELECT * FROM uyeler LIMIT 5;  # Üyeleri gör
```

---

## 1️⃣1️⃣ GITHUB'A GÖNDERME (Opsiyonel)

Eğer kendi GitHub hesabınıza güncellemek istiyorsanız:

```powershell
# Projeye git girin
cd SporSalonuProjesi

# Değişiklikleri ekleyin
git add .

# Commit yapın
git commit -m "Proje güncellemeleri"

# Push yapın
git push origin main
```

> ⚠️ **Dikkat:** `config.py` otomatik olarak yüklenmez (`.gitignore`'da var)

---

## 1️⃣2️⃣ ÖNEMLİ BİLGİLER

### Giriş Bilgileri:
| Alan | Değer |
|------|-------|
| Kullanıcı Adı | `admin` |
| Şifre | `admin123` |

### Veritabanı Bilgileri:
| Ayar | Varsayılan |
|------|------------|
| Host | `localhost` |
| Port | `3306` |
| Kullanıcı | `root` |
| Veritabanı | `spor_salonu_db` |

### Uygulama İçeriği (11 Sekme):
1. 📊 **Dashboard** - İstatistikler ve özet
2. 👤 **Üyeler** - Üye yönetimi
3. 🏅 **Antrenörler** - Antrenör yönetimi
4. 📦 **Paketler** - Paket tanımları
5. 🎫 **Üyelikler** - Üyelik işlemleri
6. 💳 **Ödemeler** - Ödeme takibi
7. 🏃 **Dersler** - Ders yönetimi
8. 📋 **Ders Kayıtları** - Kayıt takibi
9. ✅ **Yoklamalar** - Devam kontrolü
10. 🏋️ **Ekipmanlar** - Ekipman yönetimi
11. 🔧 **Bakımlar** - Bakım kaydı
12. ⚙️ **Ayarlar** - Sistem ayarları

---

## 📞 DESTEK

Sorun yaşarsanız:

1. Bu dosyayı baştan okuyun
2. Sorun Giderme bölümüne bakın
3. Hata mesajını not edin

---

**Kurulum başarılı! Uygulama hazır. 🎉**
