# 📥 Kurulum ve Çalıştırma Rehberi

## Gereksinimler
- Python 3.8 veya üzeri → https://www.python.org/downloads/
- MySQL 8.0 veya üzeri → https://dev.mysql.com/downloads/mysql/
- MySQL Workbench (isteğe bağlı) → https://www.mysql.com/products/workbench/

---

## Adım 1: Projeyi İndir

GitHub'dan ZIP olarak indirip çıkartın, veya:
```
git clone https://github.com/kullanici/proje.git
```

---

## Adım 2: Python Paketlerini Kur

`04_Desktop_PyQt` klasöründe terminal/komut istemi açın:
```
pip install -r requirements.txt
```

---

## Adım 3: MySQL Veritabanını Kur

MySQL Workbench'i açın ve şu dosyaları **sırayla** çalıştırın:

| Sıra | Dosya | Açıklama |
|------|-------|----------|
| 1 | `02_Database/01_TabloOlusturma.sql` | 10 tablo oluşturur |
| 2 | `02_Database/02_StoredProcedures.sql` | 40 stored procedure |
| 3 | `02_Database/03_Functions.sql` | 3 hesaplama fonksiyonu |
| 4 | `02_Database/04_Triggers.sql` | 3 iş kuralı trigger'ı |
| 5 | `02_Database/05_OrnekVeriler.sql` | Örnek test verileri |

Her dosyayı açtıktan sonra **Ctrl+Shift+Enter** ile çalıştırın.

---

## Adım 4: Uygulamayı Başlat

```
python main.py
```

veya `UYGULAMAYI_BASLAT.bat` dosyasına çift tıklayın.

---

## Adım 5: Giriş Yapın

1. Giriş ekranında **"⚙️ Veritabanı Ayarları"** butonuna tıklayın
2. **MySQL Şifrenizi** girin (root kullanıcısı için)
3. **"Bağlantıyı Test Et"** butonuna tıklayın → Yeşil ✅ görünmeli
4. **Kullanıcı Adı:** `admin`
5. **Şifre:** `admin123`
6. **"🚀 Giriş Yap"** butonuna tıklayın

---

## Uygulama Özellikleri

| Özellik | Detay |
|---------|-------|
| Arayüz | PyQt5 masaüstü uygulaması |
| Veritabanı | MySQL 8.0 (Stored Procedure tabanlı) |
| Tablolar | 10 ana tablo |
| SP | 40 Stored Procedure (CRUD) |
| Function | 3 MySQL fonksiyonu |
| Trigger | 3 iş kuralı (otomatik tetikleyici) |
| Sekmeler | 11 sekme (Dashboard + 10 CRUD) |

---

## Sorun Giderme

**"Bağlantı başarısız" hatası:**
- MySQL servisinin çalıştığını kontrol edin
- Şifrenizin doğru olduğunu kontrol edin
- `spor_salonu_db` veritabanının oluşturulduğunu kontrol edin

**"Module not found" hatası:**
```
pip install PyQt5 mysql-connector-python
```

**MySQL şifresi yoksa:**
- Şifre alanını boş bırakın, "Bağlantıyı Test Et"e tıklayın
