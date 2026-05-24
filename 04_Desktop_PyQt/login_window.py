# -*- coding: utf-8 -*-
"""
Giriş Ekranı - Yönetici Girişi
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QMessageBox, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor

from database.db_connection import db
from config import DB_CONFIG, ADMIN_USERNAME, ADMIN_PASSWORD
from styles import LOGIN_STYLE, COLORS


class AnimatedBackground(QWidget):
    """Arka plan widget'ı."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {COLORS['bg_darkest']},
                    stop:0.5 #0d1530,
                    stop:1 {COLORS['bg_dark']});
            }}
        """)


class DbConfigDialog(QWidget):
    """Veritabanı bağlantı ayarları mini formu (login içinde)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)

        lbl = QLabel("⚙️  MySQL Bağlantı Ayarları")
        lbl.setStyleSheet(f"color: {COLORS['accent_primary']}; font-weight: 700; font-size: 13px;")
        layout.addWidget(lbl)

        row1 = QHBoxLayout()
        self.host_input = QLineEdit(DB_CONFIG["host"])
        self.host_input.setPlaceholderText("Host")
        self.port_input = QLineEdit(str(DB_CONFIG["port"]))
        self.port_input.setPlaceholderText("Port")
        self.port_input.setMaximumWidth(80)
        row1.addWidget(QLabel("Host:"))
        row1.addWidget(self.host_input)
        row1.addWidget(QLabel("Port:"))
        row1.addWidget(self.port_input)
        layout.addLayout(row1)

        row2 = QHBoxLayout()
        self.user_input = QLineEdit(DB_CONFIG["user"])
        self.user_input.setPlaceholderText("Kullanıcı adı")
        self.db_input = QLineEdit(DB_CONFIG["database"])
        self.db_input.setPlaceholderText("Veritabanı adı")
        row2.addWidget(QLabel("Kullanıcı:"))
        row2.addWidget(self.user_input)
        row2.addWidget(QLabel("DB:"))
        row2.addWidget(self.db_input)
        layout.addLayout(row2)

        row3 = QHBoxLayout()
        self.pass_input = QLineEdit(DB_CONFIG["password"])
        self.pass_input.setPlaceholderText("MySQL şifresi")
        self.pass_input.setEchoMode(QLineEdit.Password)
        row3.addWidget(QLabel("Şifre:"))
        row3.addWidget(self.pass_input)
        layout.addLayout(row3)


class LoginWindow(QWidget):
    """Yönetici Giriş Ekranı."""

    login_success = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spor Salonu Yönetim Sistemi - Giriş")
        self.setMinimumSize(900, 600)
        self.resize(1000, 650)
        self.setStyleSheet(LOGIN_STYLE)
        self._setup_ui()

    def _setup_ui(self):
        # Ana layout - arka plan ile
        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Sol panel - Animasyonlu
        left_panel = self._build_left_panel()
        outer.addWidget(left_panel, 3)

        # Sağ panel - Login formu
        right_panel = self._build_right_panel()
        outer.addWidget(right_panel, 2)

    def _build_left_panel(self):
        """Sol taraf - marka/tanıtım paneli."""
        panel = AnimatedBackground()
        layout = QVBoxLayout(panel)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(60, 60, 60, 60)

        # Logo / ikon
        icon_lbl = QLabel("🏋️")
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setStyleSheet("font-size: 72px; background: transparent;")
        layout.addWidget(icon_lbl)

        # Marka adı
        brand = QLabel("SPOR SALONU")
        brand.setObjectName("labelBrand")
        brand.setAlignment(Qt.AlignCenter)
        layout.addWidget(brand)

        brand2 = QLabel("YÖNETİM SİSTEMİ")
        brand2.setStyleSheet(f"font-size: 20px; font-weight: 700; color: {COLORS['accent_primary']}; letter-spacing: 3px; background: transparent;")
        brand2.setAlignment(Qt.AlignCenter)
        layout.addWidget(brand2)

        layout.addSpacing(16)

        tagline = QLabel("Üyeler · Antrenörler · Dersler · Ödemeler\nEkipmanlar · Yoklamalar")
        tagline.setObjectName("labelTagline")
        tagline.setAlignment(Qt.AlignCenter)
        tagline.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px; background: transparent; line-height: 1.8;")
        layout.addWidget(tagline)

        layout.addSpacing(40)

        # Özellikler listesi
        features = [
            ("✓", "Tam CRUD desteği – Stored Procedure tabanlı"),
            ("✓", "MySQL Workbench ile uyumlu"),
            ("✓", "Gerçek zamanlı Dashboard"),
            ("✓", "Trigger & Function entegrasyonu"),
        ]
        for icon, text in features:
            row = QHBoxLayout()
            icon_l = QLabel(icon)
            icon_l.setStyleSheet(f"color: {COLORS['accent_success']}; font-weight: 800; font-size: 16px; background: transparent;")
            text_l = QLabel(text)
            text_l.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; background: transparent;")
            row.addWidget(icon_l)
            row.addWidget(text_l)
            row.addStretch()
            layout.addLayout(row)

        layout.addStretch()

        return panel

    def _build_right_panel(self):
        """Sağ taraf - login formu."""
        container = QWidget()
        container.setStyleSheet(f"background-color: {COLORS['bg_dark']};")
        outer = QVBoxLayout(container)
        outer.setAlignment(Qt.AlignCenter)
        outer.setContentsMargins(40, 40, 40, 40)

        # Login kartı
        card = QFrame()
        card.setObjectName("loginCard")
        card.setMinimumWidth(380)
        card.setMaximumWidth(420)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(16)
        card_layout.setContentsMargins(32, 32, 32, 32)

        # Başlık
        title = QLabel("Yönetici Girişi")
        title.setStyleSheet(f"font-size: 22px; font-weight: 800; color: white;")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        subtitle = QLabel("Hesabınıza giriş yapın")
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px;")
        subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(subtitle)

        card_layout.addSpacing(8)

        # Kullanıcı adı
        lbl_user = QLabel("Kullanıcı Adı")
        lbl_user.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; font-weight: 600;")
        card_layout.addWidget(lbl_user)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Kullanıcı adınızı girin")
        self.username_input.setText("admin")
        self.username_input.setMinimumHeight(44)
        card_layout.addWidget(self.username_input)

        # Şifre
        lbl_pass = QLabel("Şifre")
        lbl_pass.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; font-weight: 600;")
        card_layout.addWidget(lbl_pass)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifrenizi girin")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setText("admin123")
        self.password_input.setMinimumHeight(44)
        self.password_input.returnPressed.connect(self._do_login)
        card_layout.addWidget(self.password_input)

        # Hata mesajı
        self.error_label = QLabel("")
        self.error_label.setObjectName("labelError")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setWordWrap(True)
        card_layout.addWidget(self.error_label)

        card_layout.addSpacing(4)

        # DB Ayarları toggle
        self.db_toggle_btn = QPushButton("⚙️  Veritabanı Ayarları")
        self.db_toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {COLORS['text_secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 8px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                color: {COLORS['accent_primary']};
                border-color: {COLORS['accent_primary']};
                background: {COLORS['bg_input']};
            }}
        """)
        self.db_toggle_btn.clicked.connect(self._toggle_db_config)
        card_layout.addWidget(self.db_toggle_btn)

        # DB Config (gizli)
        self.db_config_widget = DbConfigDialog()
        self.db_config_widget.setVisible(False)
        card_layout.addWidget(self.db_config_widget)

        # Giriş butonu
        self.login_btn = QPushButton("🚀  Giriş Yap")
        self.login_btn.setObjectName("btnLogin")
        self.login_btn.setMinimumHeight(50)
        self.login_btn.clicked.connect(self._do_login)
        card_layout.addWidget(self.login_btn)

        # Bilgi notu
        note = QLabel("Varsayılan: admin / admin123")
        note.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
        note.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(note)

        outer.addWidget(card)

        # Alt bilgi
        footer = QLabel("© 2026 Spor Salonu Yönetim Sistemi  •  MySQL + PyQt5")
        footer.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
        footer.setAlignment(Qt.AlignCenter)
        outer.addWidget(footer)

        return container

    def _toggle_db_config(self):
        visible = self.db_config_widget.isVisible()
        self.db_config_widget.setVisible(not visible)
        self.db_toggle_btn.setText(
            "⚙️  Ayarları Gizle" if not visible else "⚙️  Veritabanı Ayarları"
        )
        self.adjustSize()

    def _do_login(self):
        """Giriş doğrulama ve veritabanı bağlantısı."""
        username = self.username_input.text().strip()
        password = self.password_input.text()

        # Admin kimlik doğrulama
        if username != ADMIN_USERNAME or password != ADMIN_PASSWORD:
            self.error_label.setText("❌ Hatalı kullanıcı adı veya şifre!")
            self.password_input.clear()
            self.password_input.setFocus()
            return

        # DB Bağlantı ayarlarını oku
        self.error_label.setText("⏳ Veritabanına bağlanılıyor...")
        self.login_btn.setEnabled(False)
        self.login_btn.setText("Bağlanıyor...")

        if self.db_config_widget.isVisible():
            cfg = self.db_config_widget
            success, msg = db.connect(
                host=cfg.host_input.text().strip() or DB_CONFIG["host"],
                port=cfg.port_input.text().strip() or DB_CONFIG["port"],
                user=cfg.user_input.text().strip() or DB_CONFIG["user"],
                password=cfg.pass_input.text(),
                database=cfg.db_input.text().strip() or DB_CONFIG["database"],
            )
        else:
            success, msg = db.connect()

        self.login_btn.setEnabled(True)
        self.login_btn.setText("🚀  Giriş Yap")

        if not success:
            self.error_label.setText(f"❌ DB Bağlantı Hatası:\n{msg}")
            return

        # Başarılı → Ana pencereye geç
        self._open_main_window()

    def _open_main_window(self):
        try:
            from main_window import MainWindow
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self, "Hata",
                f"Ana pencere açılamadı:\n\n{str(e)}\n\n"
                f"Detay için konsola bakın."
            )
            self.login_btn.setEnabled(True)
            self.login_btn.setText("🚀  Giriş Yap")
