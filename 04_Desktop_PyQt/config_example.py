# =====================================================
# Veritabanı bağlantı ayarları — örnek dosya
# Kurulum: Bu dosyayı config.py olarak kopyalayın ve
# MySQL şifrenizi girin.
# =====================================================

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",              # MySQL root şifreniz
    "database": "spor_salonu_db",
    "charset": "utf8mb4",
    "use_unicode": True,
    "autocommit": True,
    "use_pure": True,
}

APP_TITLE = "Spor Salonu Yönetim Sistemi"
APP_VERSION = "1.0.0"

# Uygulama giriş bilgileri (demo yönetici)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
