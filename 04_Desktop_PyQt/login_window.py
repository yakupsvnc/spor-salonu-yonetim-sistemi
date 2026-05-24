# -*- coding: utf-8 -*-
"""Giriş ekranı"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor

from database.db_connection import db
from config import DB_CONFIG, ADMIN_USERNAME, ADMIN_PASSWORD
from styles import LOGIN_STYLE, COLORS


class DbConfigDialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 8, 0, 0)

        lbl = QLabel("MySQL Bağlantı Ayarları")
        lbl.setStyleSheet(f"color: {COLORS['accent_cyan']}; font-weight: 700; font-size: 12px;")
        layout.addWidget(lbl)

        self.host_input = QLineEdit(DB_CONFIG["host"])
        self.port_input = QLineEdit(str(DB_CONFIG["port"]))
        self.port_input.setMaximumWidth(72)
        self.user_input = QLineEdit(DB_CONFIG["user"])
        self.db_input = QLineEdit(DB_CONFIG["database"])
        self.pass_input = QLineEdit(DB_CONFIG["password"])
        self.pass_input.setEchoMode(QLineEdit.Password)

        for label, widget in [
            ("Host", self.host_input), ("Port", self.port_input),
            ("Kullanıcı", self.user_input), ("Veritabanı", self.db_input),
            ("MySQL Şifre", self.pass_input),
        ]:
            row = QHBoxLayout()
            l = QLabel(label)
            l.setFixedWidth(90)
            l.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
            row.addWidget(l)
            row.addWidget(widget)
            layout.addLayout(row)


class LoginWindow(QWidget):
    login_success = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spor Salonu — Giriş")
        self.setMinimumSize(960, 620)
        self.resize(1100, 680)
        self.setStyleSheet(LOGIN_STYLE)
        self._setup_ui()

    def _setup_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Sol panel
        left = QFrame()
        left.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {COLORS['bg_darkest']}, stop:0.6 #0f172a, stop:1 #1e1b4b);
                border-right: 1px solid {COLORS['border']};
            }}
        """)
        ll = QVBoxLayout(left)
        ll.setAlignment(Qt.AlignCenter)
        ll.setContentsMargins(48, 48, 48, 48)
        ll.setSpacing(16)

        logo = QLabel("🏋️")
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("font-size: 64px; background: transparent;")
        ll.addWidget(logo)

        brand = QLabel("SPOR SALONU")
        brand.setObjectName("labelBrand")
        brand.setAlignment(Qt.AlignCenter)
        ll.addWidget(brand)

        sub = QLabel("Yönetim Paneli")
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet(
            f"font-size: 15px; color: {COLORS['accent_cyan']}; font-weight: 700;"
            f" letter-spacing: 4px; background: transparent;"
        )
        ll.addWidget(sub)

        ll.addSpacing(24)
        for txt in [
            "N-katmanlı mimari · Stored Procedure",
            "10 modül · Tam CRUD desteği",
            "Trigger & Function entegrasyonu",
        ]:
            row = QHBoxLayout()
            tick = QLabel("✓")
            tick.setStyleSheet(f"color: {COLORS['accent_success']}; font-weight: 800; font-size: 14px;")
            lbl = QLabel(txt)
            lbl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px;")
            row.addWidget(tick)
            row.addWidget(lbl)
            row.addStretch()
            ll.addLayout(row)
        ll.addStretch()
        root.addWidget(left, 5)

        # Sağ panel — giriş kartı
        right = QWidget()
        right.setStyleSheet(f"background: {COLORS['bg_dark']};")
        rl = QVBoxLayout(right)
        rl.setAlignment(Qt.AlignCenter)
        rl.setContentsMargins(40, 40, 40, 40)

        card = QFrame()
        card.setObjectName("loginCard")
        card.setMinimumWidth(400)
        card.setMaximumWidth(440)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, 120))
        shadow.setOffset(0, 8)
        card.setGraphicsEffect(shadow)

        cl = QVBoxLayout(card)
        cl.setSpacing(14)
        cl.setContentsMargins(36, 36, 36, 36)

        title = QLabel("Hoş Geldiniz")
        title.setStyleSheet("font-size: 26px; font-weight: 800; color: white;")
        title.setAlignment(Qt.AlignCenter)
        cl.addWidget(title)

        hint = QLabel("Yönetici hesabınızla giriş yapın")
        hint.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 13px;")
        hint.setAlignment(Qt.AlignCenter)
        cl.addWidget(hint)
        cl.addSpacing(8)

        cl.addWidget(self._field_label("Kullanıcı Adı"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("admin")
        self.username_input.setText("admin")
        self.username_input.setMinimumHeight(48)
        cl.addWidget(self.username_input)

        cl.addWidget(self._field_label("Şifre"))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("••••••••")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setText("admin123")
        self.password_input.setMinimumHeight(48)
        self.password_input.returnPressed.connect(self._do_login)
        cl.addWidget(self.password_input)

        self.error_label = QLabel("")
        self.error_label.setObjectName("labelError")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setWordWrap(True)
        cl.addWidget(self.error_label)

        self.db_toggle_btn = QPushButton("⚙  Veritabanı Ayarları")
        self.db_toggle_btn.setObjectName("btnDbToggle")
        self.db_toggle_btn.clicked.connect(self._toggle_db_config)
        cl.addWidget(self.db_toggle_btn)

        self.db_config_widget = DbConfigDialog()
        self.db_config_widget.setVisible(False)
        cl.addWidget(self.db_config_widget)

        self.login_btn = QPushButton("GİRİŞ YAP  →")
        self.login_btn.setObjectName("btnLogin")
        self.login_btn.setMinimumHeight(54)
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.clicked.connect(self._do_login)
        cl.addWidget(self.login_btn)

        note = QLabel("Varsayılan: admin / admin123")
        note.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
        note.setAlignment(Qt.AlignCenter)
        cl.addWidget(note)

        rl.addWidget(card)
        root.addWidget(right, 4)

    def _field_label(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet(
            f"color: {COLORS['text_secondary']}; font-size: 12px; font-weight: 600;"
            f" margin-top: 4px;"
        )
        return lbl

    def _toggle_db_config(self):
        vis = not self.db_config_widget.isVisible()
        self.db_config_widget.setVisible(vis)
        self.db_toggle_btn.setText("▲ Ayarları Gizle" if vis else "⚙  Veritabanı Ayarları")

    def _do_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if username != ADMIN_USERNAME or password != ADMIN_PASSWORD:
            self.error_label.setText("Hatalı kullanıcı adı veya şifre!")
            self.password_input.clear()
            return

        self.error_label.setText("Bağlanılıyor...")
        self.login_btn.setEnabled(False)
        self.login_btn.setText("Bağlanılıyor...")

        if self.db_config_widget.isVisible():
            c = self.db_config_widget
            success, msg = db.connect(
                host=c.host_input.text().strip() or DB_CONFIG["host"],
                port=c.port_input.text().strip() or DB_CONFIG["port"],
                user=c.user_input.text().strip() or DB_CONFIG["user"],
                password=c.pass_input.text(),
                database=c.db_input.text().strip() or DB_CONFIG["database"],
            )
        else:
            success, msg = db.connect()

        self.login_btn.setEnabled(True)
        self.login_btn.setText("GİRİŞ YAP  →")

        if not success:
            self.error_label.setText(f"DB Hatası: {msg}")
            return

        self._open_main_window()

    def _open_main_window(self):
        from main_window import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()
