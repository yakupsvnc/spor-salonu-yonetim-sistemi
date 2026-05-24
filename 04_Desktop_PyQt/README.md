# Spor Salonu Yönetim Sistemi — PyQt5 Masaüstü

## Proje Yapısı

```
04_Desktop_PyQt/
├── UYGULAMAYI_BASLAT.bat    ← Çift tıkla başlat
├── requirements.txt
├── config_example.py        ← GitHub'da örnek ayar dosyası
├── config.py                ← Kendi ayarlarınız (gitignore)
├── main.py                  ← Giriş noktası
├── login_window.py          ← Presentation: giriş ekranı
├── main_window.py           ← Presentation: ana pencere + sekmeler
├── dialogs.py / widgets.py / styles.py
├── database/
│   └── db_connection.py     ← DAL bağlantı yöneticisi
├── dal/                     ← Data Access Layer (SP çağrıları)
└── services/                ← Business Layer (iş kuralları)
```

## Kurulum

### 1. MySQL (Workbench)

Üst dizindeki `02_Database/` klasöründeki SQL dosyalarını sırayla çalıştırın.

### 2. Python bağımlılıkları

```bash
pip install -r requirements.txt
```

### 3. Veritabanı ayarları

```bash
copy config_example.py config.py
```

`config.py` içinde `password` alanına MySQL root şifrenizi girin.  
Alternatif: Giriş ekranında **Veritabanı Ayarları** bölümünü açıp şifreyi orada girebilirsiniz.

### 4. Başlat

`UYGULAMAYI_BASLAT.bat` veya `python main.py`

**Giriş:** `admin` / `admin123`

## Mimari

| Katman | Klasör | Görev |
|--------|--------|-------|
| Presentation | `*.py` (UI) | PyQt5 arayüz |
| Business | `services/` | Validasyon, iş kuralları |
| Data Access | `dal/` + `database/` | `CALL sp_...` |
| Veritabanı | `02_Database/` | MySQL SP, trigger, function |

## Trigger & Function

1. **trg_odeme_eklendi_uyelik_aktif_yap** — Başarılı ödeme → üyelik Aktif
2. **trg_ders_kontenjan_kontrol** — Kontenjan doluysa kayıt engellenir
3. **trg_uyelik_tarih_kontrol** — Bitiş ≥ başlangıç

- **fn_uye_toplam_odeme** — Üye tablosunda gösterilir
- **fn_uyelik_kalan_gun** — Üyelik tablosunda gösterilir
- **fn_ders_doluluk_orani** — Ders tablosunda gösterilir
