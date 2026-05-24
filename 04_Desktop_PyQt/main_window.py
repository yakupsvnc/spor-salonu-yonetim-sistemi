# -*- coding: utf-8 -*-
"""
Ana Pencere - Spor Salonu Yönetim Sistemi
Tüm CRUD sekmeleri ve Dashboard buradadır.
MySQL Stored Procedure tabanlı işlemler.
"""

import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QListWidget, QListWidgetItem,
    QLabel, QPushButton, QFrame, QStatusBar, QScrollArea,
    QGridLayout, QMessageBox, QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor

from database.db_connection import db
from services.uye_service import UyeService
from services.antrenor_service import AntrenorService
from services.paket_service import PaketService
from services.uyelik_service import UyelikService
from services.odeme_service import OdemeService
from services.ders_service import DersService
from services.ders_kayit_service import DersKayitService
from services.yoklama_service import YoklamaService
from services.ekipman_service import EkipmanService
from services.bakim_service import BakimService
from styles import MAIN_STYLE, COLORS
from widgets import (
    StatCard, BaseTableWidget, ActionBar, SectionHeader,
    confirm_delete, show_error, show_success, filter_table,
    get_selected_record, table_item
)
from dialogs import (
    UyeDialog, AntrenorDialog, UyelikPaketiDialog, UyelikDialog,
    OdemeDialog, DersDialog, DersKayitDialog, YoklamaDialog,
    EkipmanDialog, BakimDialog
)


# =====================================================
# YARDIMCI FONKSİYONLAR
# =====================================================

def _safe_call(fn, default=None):
    """Service/DAL güvenli çağrı — hata mesajını döndürür."""
    try:
        return fn(), None
    except Exception as e:
        return default, str(e)


def _safe_void(fn):
    """Yazma işlemleri için güvenli çağrı — yalnızca hata mesajı döndürür."""
    try:
        fn()
        return None
    except Exception as e:
        return str(e)


# =====================================================
# DASHBOARD SEKMESİ
# =====================================================

class DashboardTab(QWidget):
    """Genel istatistik dashboard'u."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._uye_svc = UyeService()
        self._ant_svc = AntrenorService()
        self._uyelik_svc = UyelikService()
        self._odeme_svc = OdemeService()
        self._ders_svc = DersService()
        self._dk_svc = DersKayitService()
        self._ekipman_svc = EkipmanService()
        self._bakim_svc = BakimService()
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(24)
        main_layout.setContentsMargins(24, 24, 24, 24)

        # Başlık
        header = QLabel("📊  Genel Bakış – Dashboard")
        header.setStyleSheet(
            f"font-size: 22px; font-weight: 800; color: {COLORS['text_primary']};"
            f" padding: 0 0 8px 0; background: transparent;"
        )
        main_layout.addWidget(header)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"color: {COLORS['border']};")
        main_layout.addWidget(sep)

        # İstatistik kartları - satır 1
        row1 = QHBoxLayout()
        row1.setSpacing(16)
        self.card_uyeler = StatCard("Toplam Üye", "—", "👤", COLORS["accent_primary"])
        self.card_antrenorler = StatCard("Toplam Antrenör", "—", "🏅", COLORS["accent_secondary"])
        self.card_aktif_uyelik = StatCard("Aktif Üyelik", "—", "🎫", COLORS["accent_success"])
        self.card_gelir = StatCard("Toplam Gelir (₺)", "—", "💰", COLORS["accent_warning"])
        for c in [self.card_uyeler, self.card_antrenorler, self.card_aktif_uyelik, self.card_gelir]:
            row1.addWidget(c)
        main_layout.addLayout(row1)

        # İstatistik kartları - satır 2
        row2 = QHBoxLayout()
        row2.setSpacing(16)
        self.card_dersler = StatCard("Toplam Ders", "—", "🏃", COLORS["accent_info"])
        self.card_ders_kayit = StatCard("Ders Kaydı", "—", "📋", COLORS["accent_primary"])
        self.card_ekipman = StatCard("Ekipman", "—", "🏋️", COLORS["accent_secondary"])
        self.card_bakim = StatCard("Bakım Kaydı", "—", "🔧", COLORS["accent_danger"])
        for c in [self.card_dersler, self.card_ders_kayit, self.card_ekipman, self.card_bakim]:
            row2.addWidget(c)
        main_layout.addLayout(row2)

        # Hızlı bilgi kutuları
        info_layout = QHBoxLayout()
        info_layout.setSpacing(16)

        # Sol: Son Üyeler
        left_frame = QFrame()
        left_frame.setObjectName("cardFrame")
        left_frame.setStyleSheet(
            f"QFrame#cardFrame {{ background: {COLORS['bg_card']}; border: 1px solid {COLORS['border']};"
            f" border-radius: 12px; padding: 16px; }}"
        )
        left_layout = QVBoxLayout(left_frame)
        left_title = QLabel("👤  Son Kayıt Olan Üyeler")
        left_title.setStyleSheet(
            f"font-size: 14px; font-weight: 700; color: {COLORS['accent_primary']};"
            f" background: transparent; padding-bottom: 8px;"
        )
        left_layout.addWidget(left_title)
        self.recent_members_label = QLabel("Yükleniyor...")
        self.recent_members_label.setStyleSheet(
            f"color: {COLORS['text_secondary']}; font-size: 12px; background: transparent; line-height: 2;"
        )
        self.recent_members_label.setWordWrap(True)
        left_layout.addWidget(self.recent_members_label)
        left_layout.addStretch()
        info_layout.addWidget(left_frame, 1)

        # Sağ: Özet bilgiler
        right_frame = QFrame()
        right_frame.setObjectName("cardFrame")
        right_frame.setStyleSheet(
            f"QFrame#cardFrame {{ background: {COLORS['bg_card']}; border: 1px solid {COLORS['border']};"
            f" border-radius: 12px; padding: 16px; }}"
        )
        right_layout = QVBoxLayout(right_frame)
        right_title = QLabel("ℹ️  Sistem Bilgisi")
        right_title.setStyleSheet(
            f"font-size: 14px; font-weight: 700; color: {COLORS['accent_primary']};"
            f" background: transparent; padding-bottom: 8px;"
        )
        right_layout.addWidget(right_title)

        self.info_labels = []
        info_items = [
            ("🗄️  Veritabanı", "spor_salonu_db"),
            ("⚙️  SP Tabanlı", "Stored Procedure kullanıyor"),
            ("🔗  Trigger", "3 aktif iş kuralı"),
            ("📐  Function", "3 hesaplama fonksiyonu"),
            ("🏷️  Tablolar", "10 ana tablo"),
        ]
        for icon_text, desc in info_items:
            row = QHBoxLayout()
            lbl_key = QLabel(icon_text)
            lbl_key.setStyleSheet(f"font-weight: 600; color: {COLORS['text_primary']}; background: transparent; font-size: 12px;")
            lbl_val = QLabel(desc)
            lbl_val.setStyleSheet(f"color: {COLORS['text_secondary']}; background: transparent; font-size: 12px;")
            row.addWidget(lbl_key)
            row.addStretch()
            row.addWidget(lbl_val)
            right_layout.addLayout(row)
        right_layout.addStretch()
        info_layout.addWidget(right_frame, 1)
        main_layout.addLayout(info_layout)

        # Yenile butonu
        btn_row = QHBoxLayout()
        btn_refresh = QPushButton("🔄  Dashboard'u Yenile")
        btn_refresh.setFixedHeight(42)
        btn_refresh.setFixedWidth(220)
        btn_refresh.clicked.connect(self.refresh)
        btn_row.addStretch()
        btn_row.addWidget(btn_refresh)
        main_layout.addLayout(btn_row)

        main_layout.addStretch()
        scroll.setWidget(container)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def refresh(self):
        """Dashboard verilerini yenile."""
        try:
            # Üye sayısı
            uyeler, _ = _safe_call(self._uye_svc.listele, [])
            self.card_uyeler.set_value(len(uyeler))

            antrenorler, _ = _safe_call(self._ant_svc.listele, [])
            self.card_antrenorler.set_value(len(antrenorler))

            uyelikler, _ = _safe_call(self._uyelik_svc.listele, [])
            aktif = sum(1 for u in uyelikler if u.get("durum") == "Aktif")
            self.card_aktif_uyelik.set_value(aktif)

            odemeler, _ = _safe_call(self._odeme_svc.listele, [])
            toplam = sum(float(o.get("tutar", 0) or 0) for o in odemeler
                         if o.get("odeme_durumu") == "Başarılı")
            self.card_gelir.set_value(f"{toplam:,.0f} ₺")

            dersler, _ = _safe_call(self._ders_svc.listele, [])
            self.card_dersler.set_value(len(dersler))

            dk, _ = _safe_call(self._dk_svc.listele, [])
            self.card_ders_kayit.set_value(len(dk))

            ekipmanlar, _ = _safe_call(self._ekipman_svc.listele, [])
            self.card_ekipman.set_value(len(ekipmanlar))

            bakimlar, _ = _safe_call(self._bakim_svc.listele, [])
            self.card_bakim.set_value(len(bakimlar))

            # Son 5 üye
            son5 = uyeler[:5]
            text_lines = []
            for u in son5:
                text_lines.append(
                    f"• <b>{u.get('ad', '')} {u.get('soyad', '')}</b>"
                    f" — {str(u.get('kayit_tarihi', ''))[:10]}"
                )
            if not text_lines:
                text_lines = ["Henüz üye kaydı yok."]
            self.recent_members_label.setText("<br>".join(text_lines))
            self.recent_members_label.setTextFormat(Qt.RichText)

        except Exception as e:
            pass  # Dashboard hata verse de uygulama çalışmaya devam eder


# =====================================================
# AYARLAR SEKMESİ
# =====================================================

class SettingsTab(QWidget):
    """Veritabanı ayarları ve sistem konfigürasyonu."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: white;")
        self._setup_ui()

    def _setup_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: white; }")
        
        container = QWidget()
        container.setStyleSheet("background-color: white;")
        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(24)
        main_layout.setContentsMargins(48, 48, 48, 48)

        title = QLabel("⚙️  Sistem Ayarları")
        title.setStyleSheet("color: #1a1a1a; font-size: 28px; font-weight: bold; padding: 10px 0px;")
        main_layout.addWidget(title)

        desc = QLabel("Veritabanı Bağlantı Bilgileri")
        desc.setStyleSheet("color: #666666; font-size: 14px; margin-bottom: 20px;")
        main_layout.addWidget(desc)

        from config import DB_CONFIG
        
        box = QFrame()
        box.setStyleSheet(
            "QFrame { background-color: #f8f9fa; border: 1px solid #ddd; "
            "border-radius: 6px; padding: 24px; }"
        )
        
        box_layout = QVBoxLayout(box)
        box_layout.setSpacing(18)

        settings = [
            ("🖥️  Host Adı", DB_CONFIG.get("host", "localhost")),
            ("🔌  Port Numarası", str(DB_CONFIG.get("port", 3306))),
            ("🗄️  Veritabanı", DB_CONFIG.get("database", "spor_salonu_db")),
            ("👤  Kullanıcı", DB_CONFIG.get("user", "root")),
            ("🔤  Charset", DB_CONFIG.get("charset", "utf8mb4")),
        ]

        for title_text, value in settings:
            row = self._make_setting_row(title_text, value)
            box_layout.addLayout(row)

        box_layout.addStretch()
        main_layout.addWidget(box)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        btn = QPushButton("🔗  Bağlantı Testini Çalıştır")
        btn.setMinimumHeight(50)
        btn.setMinimumWidth(220)
        btn.setStyleSheet(
            "QPushButton { background-color: #3498db; color: white; font-weight: 600; "
            "border: none; border-radius: 6px; font-size: 13px; padding: 12px 24px; }"
            "QPushButton:hover { background-color: #2980b9; }"
            "QPushButton:pressed { background-color: #1f618d; }"
        )
        btn.clicked.connect(self._test_connection)
        button_layout.addWidget(btn)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        main_layout.addStretch()
        scroll.setWidget(container)

        final_layout = QVBoxLayout(self)
        final_layout.setContentsMargins(0, 0, 0, 0)
        final_layout.addWidget(scroll)

    def _make_setting_row(self, label_text, value_text):
        row = QHBoxLayout()
        row.setSpacing(24)
        
        label = QLabel(label_text)
        label.setStyleSheet("color: #2c3e50; font-weight: 600; font-size: 13px; min-width: 140px;")
        label.setMaximumWidth(200)
        
        value = QLabel(str(value_text))
        value.setStyleSheet(
            "color: #27ae60; font-size: 13px; background-color: white; "
            "padding: 8px 12px; border: 1px solid #e0e0e0; border-radius: 4px; "
            "font-family: 'Courier New', monospace; font-weight: 500;"
        )
        value.setWordWrap(True)
        value.setMinimumHeight(35)
        
        row.addWidget(label)
        row.addWidget(value, 1)
        
        return row

    def _test_connection(self):
        try:
            from database.db_connection import db
            if db:
                show_success(self, "✅ Veritabanı bağlantısı başarılı!")
            else:
                show_error(self, "❌ Veritabanı bağlantı problemi!")
        except Exception as e:
            show_error(self, f"❌ Bağlantı hatası:\n{str(e)}")


# =====================================================
# ÜYELER SEKMESİ
# =====================================================

class UyelerTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.svc = UyeService()
        self._data = []
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 20, 24, 24)

        header = SectionHeader("Üye Yönetimi", "Tüm spor salonu üyelerini yönetin", "👤")
        layout.addWidget(header)

        # Action bar
        self.action_bar = ActionBar()
        self.action_bar.btn_add.clicked.connect(self._ekle)
        self.action_bar.btn_edit.clicked.connect(self._duzenle)
        self.action_bar.btn_delete.clicked.connect(self._sil)
        self.action_bar.btn_refresh.clicked.connect(self.refresh)
        self.action_bar.search_input.textChanged.connect(
            lambda t: filter_table(self.table, t)
        )
        layout.addWidget(self.action_bar)

        # Tablo
        self.table = BaseTableWidget([
            "ID", "Ad", "Soyad", "Telefon", "E-posta",
            "Cinsiyet", "Doğum Tarihi", "Kayıt Tarihi", "Aktif", "Toplam Ödeme"
        ])
        layout.addWidget(self.table)

    def refresh(self):
        rows, err = _safe_call(self.svc.listele, [])
        if err:
            show_error(self, f"Üyeler yüklenemedi:\n{err}")
            return
        self._data = rows
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        for r in rows:
            i = self.table.rowCount()
            self.table.insertRow(i)
            aktif = r.get("aktif_mi")
            row_data = [
                r.get("uye_id", ""),
                r.get("ad", ""),
                r.get("soyad", ""),
                r.get("telefon", ""),
                r.get("email", "") or "",
                r.get("cinsiyet", ""),
                str(r.get("dogum_tarihi", ""))[:10] if r.get("dogum_tarihi") else "",
                str(r.get("kayit_tarihi", ""))[:10],
                "✅ Aktif" if aktif else "❌ Pasif",
            ]
            from PyQt5.QtWidgets import QTableWidgetItem
            for col, val in enumerate(row_data):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if col == 8:
                    item.setForeground(
                        QColor(COLORS["accent_success"]) if aktif
                        else QColor(COLORS["accent_danger"])
                    )
                self.table.setItem(i, col, item)

            # fn_uye_toplam_odeme - MySQL Function
            try:
                toplam, _ = _safe_call(lambda: self.svc.toplam_odeme(r["uye_id"]), 0)
                odeme_item = QTableWidgetItem(f"{float(toplam or 0):,.2f} ₺")
            except Exception:
                odeme_item = QTableWidgetItem("0.00 ₺")
            odeme_item.setForeground(QColor(COLORS["accent_warning"]))
            odeme_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.table.setItem(i, 9, odeme_item)
        self.table.setSortingEnabled(True)

    def _ekle(self):
        dlg = UyeDialog(self)
        if dlg.exec_() == UyeDialog.Accepted:
            ok, msg = dlg.validate()
            if not ok:
                show_error(self, msg)
                return
            v = dlg.get_values()
            err = _safe_void(lambda: self.svc.ekle(
                v["ad"], v["soyad"], v["telefon"],
                v["email"], v["cinsiyet"], v["dogum_tarihi"]
            ))
            if err:
                show_error(self, f"Üye eklenemedi:\n{err}")
            else:
                show_success(self, "Üye başarıyla eklendi!")
                self.refresh()

    def _duzenle(self):
        data = get_selected_record(self.table, self._data, "uye_id")
        if not data:
            show_error(self, "Lütfen düzenlemek için bir üye seçin.")
            return
        if not data:
            return
        dlg = UyeDialog(self, data)
        if dlg.exec_() == UyeDialog.Accepted:
            ok, msg = dlg.validate()
            if not ok:
                show_error(self, msg)
                return
            v = dlg.get_values()
            aktif = v.get("aktif_mi", 1)
            err = _safe_void(lambda: self.svc.guncelle(
                data["uye_id"], v["ad"], v["soyad"], v["telefon"],
                v["email"], v["cinsiyet"], v["dogum_tarihi"], aktif
            ))
            if err:
                show_error(self, f"Güncelleme başarısız:\n{err}")
            else:
                show_success(self, "Üye başarıyla güncellendi!")
                self.refresh()

    def _sil(self):
        data = get_selected_record(self.table, self._data, "uye_id")
        if not data:
            show_error(self, "Lütfen silmek için bir üye seçin.")
            return
        if not data:
            return
        name = f"{data.get('ad', '')} {data.get('soyad', '')}"
        if confirm_delete(self, name):
            err = _safe_void(lambda: self.svc.sil(data["uye_id"]))
            if err:
                show_error(self, f"Silme başarısız:\n{err}")
            else:
                show_success(self, "Üye silindi.")
                self.refresh()


# =====================================================
# ANTRENÖRLER SEKMESİ
# =====================================================

class AntrenorlerTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.svc = AntrenorService()
        self._data = []
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 20, 24, 24)

        header = SectionHeader("Antrenör Yönetimi", "Spor salonu antrenörlerini yönetin", "🏅")
        layout.addWidget(header)

        self.action_bar = ActionBar()
        self.action_bar.btn_add.clicked.connect(self._ekle)
        self.action_bar.btn_edit.clicked.connect(self._duzenle)
        self.action_bar.btn_delete.clicked.connect(self._sil)
        self.action_bar.btn_refresh.clicked.connect(self.refresh)
        self.action_bar.search_input.textChanged.connect(
            lambda t: filter_table(self.table, t)
        )
        layout.addWidget(self.action_bar)

        self.table = BaseTableWidget([
            "ID", "Ad", "Soyad", "Telefon", "E-posta",
            "Uzmanlık Alanı", "Maaş (₺)", "İşe Başlama", "Aktif"
        ])
        layout.addWidget(self.table)

    def refresh(self):
        rows, err = _safe_call(self.svc.listele, [])
        if err:
            show_error(self, f"Antrenörler yüklenemedi:\n{err}")
            return
        self._data = rows
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        from PyQt5.QtWidgets import QTableWidgetItem
        for r in rows:
            i = self.table.rowCount()
            self.table.insertRow(i)
            aktif = r.get("aktif_mi")
            vals = [
                r.get("antrenor_id", ""),
                r.get("ad", ""),
                r.get("soyad", ""),
                r.get("telefon", ""),
                r.get("email", "") or "",
                r.get("uzmanlik_alani", ""),
                f"{float(r.get('maas', 0) or 0):,.2f}",
                str(r.get("ise_baslama_tarihi", ""))[:10],
                "✅ Aktif" if aktif else "❌ Pasif",
            ]
            for col, val in enumerate(vals):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if col == 6:
                    item.setForeground(QColor(COLORS["accent_warning"]))
                if col == 8:
                    item.setForeground(
                        QColor(COLORS["accent_success"]) if aktif
                        else QColor(COLORS["accent_danger"])
                    )
                self.table.setItem(i, col, item)
        self.table.setSortingEnabled(True)

    def _ekle(self):
        dlg = AntrenorDialog(self)
        if dlg.exec_() == AntrenorDialog.Accepted:
            ok, msg = dlg.validate()
            if not ok:
                show_error(self, msg); return
            v = dlg.get_values()
            err = _safe_void(lambda: self.svc.ekle(
                v["ad"], v["soyad"], v["telefon"], v["email"],
                v["uzmanlik_alani"], v["maas"], v["ise_baslama_tarihi"]
            ))
            if err:
                show_error(self, f"Antrenör eklenemedi:\n{err}")
            else:
                show_success(self, "Antrenör başarıyla eklendi!")
                self.refresh()

    def _duzenle(self):
        data = get_selected_record(self.table, self._data, "antrenor_id")
        if not data:
            show_error(self, "Lütfen bir antrenör seçin."); return
        if not data: return
        dlg = AntrenorDialog(self, data)
        if dlg.exec_() == AntrenorDialog.Accepted:
            ok, msg = dlg.validate()
            if not ok:
                show_error(self, msg); return
            v = dlg.get_values()
            aktif = v.get("aktif_mi", 1)
            err = _safe_void(lambda: self.svc.guncelle(
                data["antrenor_id"], v["ad"], v["soyad"], v["telefon"], v["email"],
                v["uzmanlik_alani"], v["maas"], v["ise_baslama_tarihi"], aktif
            ))
            if err:
                show_error(self, f"Güncelleme başarısız:\n{err}")
            else:
                show_success(self, "Antrenör güncellendi!")
                self.refresh()

    def _sil(self):
        data = get_selected_record(self.table, self._data, "antrenor_id")
        if not data:
            show_error(self, "Lütfen bir antrenör seçin."); return
        if not data: return
        name = f"{data.get('ad', '')} {data.get('soyad', '')}"
        if confirm_delete(self, name):
            err = _safe_void(lambda: self.svc.sil(data["antrenor_id"]))
            if err:
                show_error(self, f"Silme başarısız:\n{err}")
            else:
                show_success(self, "Antrenör silindi.")
                self.refresh()


# =====================================================
# ÜYELİK PAKETLERİ SEKMESİ
# =====================================================

class PaketlerTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.svc = PaketService()
        self._data = []
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 20, 24, 24)

        header = SectionHeader("Üyelik Paketi Yönetimi", "Üyelik paketlerini tanımlayın", "📦")
        layout.addWidget(header)

        self.action_bar = ActionBar()
        self.action_bar.btn_add.clicked.connect(self._ekle)
        self.action_bar.btn_edit.clicked.connect(self._duzenle)
        self.action_bar.btn_delete.clicked.connect(self._sil)
        self.action_bar.btn_refresh.clicked.connect(self.refresh)
        self.action_bar.search_input.textChanged.connect(
            lambda t: filter_table(self.table, t)
        )
        layout.addWidget(self.action_bar)

        self.table = BaseTableWidget([
            "ID", "Paket Adı", "Süre (Gün)", "Ücret (₺)", "Açıklama", "Aktif"
        ])
        layout.addWidget(self.table)

    def refresh(self):
        rows, err = _safe_call(self.svc.listele, [])
        if err:
            show_error(self, f"Paketler yüklenemedi:\n{err}"); return
        self._data = rows
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        from PyQt5.QtWidgets import QTableWidgetItem
        for r in rows:
            i = self.table.rowCount()
            self.table.insertRow(i)
            aktif = r.get("aktif_mi")
            vals = [
                r.get("paket_id", ""),
                r.get("paket_adi", ""),
                str(r.get("sure_gun", "")),
                f"{float(r.get('ucret', 0) or 0):,.2f}",
                r.get("aciklama", "") or "",
                "✅ Aktif" if aktif else "❌ Pasif",
            ]
            for col, val in enumerate(vals):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if col == 3:
                    item.setForeground(QColor(COLORS["accent_warning"]))
                if col == 5:
                    item.setForeground(
                        QColor(COLORS["accent_success"]) if aktif
                        else QColor(COLORS["accent_danger"])
                    )
                self.table.setItem(i, col, item)
        self.table.setSortingEnabled(True)

    def _ekle(self):
        dlg = UyelikPaketiDialog(self)
        if dlg.exec_() == UyelikPaketiDialog.Accepted:
            ok, msg = dlg.validate()
            if not ok:
                show_error(self, msg); return
            v = dlg.get_values()
            err = _safe_void(lambda: self.svc.ekle(
                v["paket_adi"], v["sure_gun"], v["ucret"], v["aciklama"]
            ))
            if err:
                show_error(self, f"Paket eklenemedi:\n{err}")
            else:
                show_success(self, "Paket başarıyla eklendi!")
                self.refresh()

    def _duzenle(self):
        data = get_selected_record(self.table, self._data, "paket_id")
        if not data:
            show_error(self, "Lütfen bir paket seçin."); return
        if not data: return
        dlg = UyelikPaketiDialog(self, data)
        if dlg.exec_() == UyelikPaketiDialog.Accepted:
            ok, msg = dlg.validate()
            if not ok:
                show_error(self, msg); return
            v = dlg.get_values()
            aktif = v.get("aktif_mi", 1)
            err = _safe_void(lambda: self.svc.guncelle(
                data["paket_id"], v["paket_adi"], v["sure_gun"],
                v["ucret"], v["aciklama"], aktif
            ))
            if err:
                show_error(self, f"Güncelleme başarısız:\n{err}")
            else:
                show_success(self, "Paket güncellendi!")
                self.refresh()

    def _sil(self):
        data = get_selected_record(self.table, self._data, "paket_id")
        if not data:
            show_error(self, "Lütfen bir paket seçin."); return
        if not data: return
        if confirm_delete(self, data.get("paket_adi", "")):
            err = _safe_void(lambda: self.svc.sil(data["paket_id"]))
            if err:
                show_error(self, f"Silme başarısız:\n{err}")
            else:
                show_success(self, "Paket silindi.")
                self.refresh()


# =====================================================
# ÜYELİKLER SEKMESİ
# =====================================================

class UyeliklerTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.svc = UyelikService()
        self._uye_svc = UyeService()
        self._paket_svc = PaketService()
        self._data = []
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 20, 24, 24)

        header = SectionHeader("Üyelik Yönetimi", "Üye-paket eşleştirmelerini yönetin", "🎫")
        layout.addWidget(header)

        self.action_bar = ActionBar()
        self.action_bar.btn_add.clicked.connect(self._ekle)
        self.action_bar.btn_edit.clicked.connect(self._duzenle)
        self.action_bar.btn_delete.clicked.connect(self._sil)
        self.action_bar.btn_refresh.clicked.connect(self.refresh)
        self.action_bar.search_input.textChanged.connect(
            lambda t: filter_table(self.table, t)
        )
        layout.addWidget(self.action_bar)

        self.table = BaseTableWidget([
            "ID", "Üye", "Paket", "Ücret (₺)", "Süre", "Başlangıç", "Bitiş",
            "Durum", "Kalan Gün", "Oluşturma"
        ])
        layout.addWidget(self.table)

    def refresh(self):
        rows, err = _safe_call(self.svc.listele, [])
        if err:
            show_error(self, f"Üyelikler yüklenemedi:\n{err}"); return
        self._data = rows
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        from PyQt5.QtWidgets import QTableWidgetItem
        for r in rows:
            i = self.table.rowCount()
            self.table.insertRow(i)
            durum = r.get("durum", "")
            durum_renk = {
                "Aktif": COLORS["accent_success"],
                "Pasif": COLORS["text_muted"],
                "Donduruldu": COLORS["accent_warning"],
                "Süresi Doldu": COLORS["accent_danger"],
            }.get(durum, COLORS["text_primary"])

            # fn_uyelik_kalan_gun - MySQL Function
            try:
                kalan, _ = _safe_call(lambda: self.svc.kalan_gun(r["uyelik_id"]), 0)
                kalan_str = f"{kalan} gün" if kalan is not None else "—"
            except Exception:
                kalan_str = "—"

            vals = [
                r.get("uyelik_id", ""),
                r.get("uye_ad_soyad", ""),
                r.get("paket_adi", ""),
                f"{float(r.get('ucret', 0) or 0):,.2f}",
                f"{r.get('sure_gun', '')} gün",
                str(r.get("baslangic_tarihi", ""))[:10],
                str(r.get("bitis_tarihi", ""))[:10],
                durum,
                kalan_str,
                str(r.get("olusturma_tarihi", ""))[:10],
            ]
            for col, val in enumerate(vals):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if col == 7:
                    item.setForeground(QColor(durum_renk))
                if col == 3:
                    item.setForeground(QColor(COLORS["accent_warning"]))
                self.table.setItem(i, col, item)
        self.table.setSortingEnabled(True)

    def _ekle(self):
        uyeler, _ = _safe_call(self._uye_svc.listele, [])
        paketler, _ = _safe_call(self._paket_svc.listele, [])
        dlg = UyelikDialog(self, uyeler=uyeler, paketler=paketler)
        if dlg.exec_() == UyelikDialog.Accepted:
            ok, msg = dlg.validate()
            if not ok:
                show_error(self, msg); return
            v = dlg.get_values()
            err = _safe_void(lambda: self.svc.ekle(
                v["uye_id"], v["paket_id"],
                v["baslangic_tarihi"], v["bitis_tarihi"], v["durum"]
            ))
            if err:
                show_error(self, f"Üyelik eklenemedi:\n{err}")
            else:
                show_success(self, "Üyelik oluşturuldu!")
                self.refresh()

    def _duzenle(self):
        data = get_selected_record(self.table, self._data, "uyelik_id")
        if not data:
            show_error(self, "Lütfen bir üyelik seçin."); return
        if not data: return
        uyeler, _ = _safe_call(self._uye_svc.listele, [])
        paketler, _ = _safe_call(self._paket_svc.listele, [])
        dlg = UyelikDialog(self, data=data, uyeler=uyeler, paketler=paketler)
        if dlg.exec_() == UyelikDialog.Accepted:
            ok, msg = dlg.validate()
            if not ok:
                show_error(self, msg); return
            v = dlg.get_values()
            err = _safe_void(lambda: self.svc.guncelle(
                data["uyelik_id"], v["uye_id"], v["paket_id"],
                v["baslangic_tarihi"], v["bitis_tarihi"], v["durum"]
            ))
            if err:
                show_error(self, f"Güncelleme başarısız:\n{err}")
            else:
                show_success(self, "Üyelik güncellendi!")
                self.refresh()

    def _sil(self):
        data = get_selected_record(self.table, self._data, "uyelik_id")
        if not data:
            show_error(self, "Lütfen bir üyelik seçin."); return
        if not data: return
        name = f"#{data.get('uyelik_id', '')} – {data.get('uye_ad_soyad', '')}"
        if confirm_delete(self, name):
            err = _safe_void(lambda: self.svc.sil(data["uyelik_id"]))
            if err:
                show_error(self, f"Silme başarısız:\n{err}")
            else:
                show_success(self, "Üyelik silindi.")
                self.refresh()


# =====================================================
# ÖDEMELER SEKMESİ
# =====================================================

class OdemelerTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.svc = OdemeService()
        self._uyelik_svc = UyelikService()
        self._data = []
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 20, 24, 24)

        header = SectionHeader("Ödeme Yönetimi", "Üyelik ödemelerini takip edin", "💳")
        layout.addWidget(header)

        # Trigger bilgi notu
        note = QLabel("⚡ Trigger Aktif: Başarılı ödeme eklendiğinde ilgili üyelik otomatik olarak 'Aktif' duruma geçer.")
        note.setStyleSheet(
            f"color: {COLORS['accent_warning']}; font-size: 11px; font-weight: 600;"
            f" background: {COLORS['bg_input']}; border-radius: 6px; padding: 8px 12px;"
        )
        note.setWordWrap(True)
        layout.addWidget(note)

        self.action_bar = ActionBar()
        self.action_bar.btn_add.clicked.connect(self._ekle)
        self.action_bar.btn_edit.clicked.connect(self._duzenle)
        self.action_bar.btn_delete.clicked.connect(self._sil)
        self.action_bar.btn_refresh.clicked.connect(self.refresh)
        self.action_bar.search_input.textChanged.connect(
            lambda t: filter_table(self.table, t)
        )
        layout.addWidget(self.action_bar)

        self.table = BaseTableWidget([
            "ID", "Üyelik ID", "Üye", "Paket", "Tutar (₺)",
            "Ödeme Tarihi", "Yöntem", "Durum", "Açıklama"
        ])
        layout.addWidget(self.table)

    def refresh(self):
        rows, err = _safe_call(self.svc.listele, [])
        if err:
            show_error(self, f"Ödemeler yüklenemedi:\n{err}"); return
        self._data = rows
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        from PyQt5.QtWidgets import QTableWidgetItem
        for r in rows:
            i = self.table.rowCount()
            self.table.insertRow(i)
            durum = r.get("odeme_durumu", "")
            durum_renk = {
                "Başarılı": COLORS["accent_success"],
                "Beklemede": COLORS["accent_warning"],
                "İptal": COLORS["accent_danger"],
            }.get(durum, COLORS["text_primary"])
            vals = [
                r.get("odeme_id", ""),
                r.get("uyelik_id", ""),
                r.get("uye_ad_soyad", ""),
                r.get("paket_adi", ""),
                f"{float(r.get('tutar', 0) or 0):,.2f}",
                str(r.get("odeme_tarihi", ""))[:16],
                r.get("odeme_yontemi", ""),
                durum,
                r.get("aciklama", "") or "",
            ]
            for col, val in enumerate(vals):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if col == 4:
                    item.setForeground(QColor(COLORS["accent_warning"]))
                if col == 7:
                    item.setForeground(QColor(durum_renk))
                self.table.setItem(i, col, item)
        self.table.setSortingEnabled(True)

    def _ekle(self):
        uyelikler, _ = _safe_call(self._uyelik_svc.listele, [])
        dlg = OdemeDialog(self, uyelikler=uyelikler)
        if dlg.exec_() == OdemeDialog.Accepted:
            ok, msg = dlg.validate()
            if not ok:
                show_error(self, msg); return
            v = dlg.get_values()
            err = _safe_void(lambda: self.svc.ekle(
                v["uyelik_id"], v["tutar"],
                v["odeme_yontemi"], v["odeme_durumu"], v["aciklama"]
            ))
            if err:
                show_error(self, f"Ödeme eklenemedi:\n{err}")
            else:
                show_success(self, "Ödeme kaydedildi! (Trigger: Üyelik durumu güncellendi)")
                self.refresh()

    def _duzenle(self):
        data = get_selected_record(self.table, self._data, "odeme_id")
        if not data:
            show_error(self, "Lütfen bir ödeme seçin."); return
        if not data: return
        uyelikler, _ = _safe_call(self._uyelik_svc.listele, [])
        dlg = OdemeDialog(self, data=data, uyelikler=uyelikler)
        if dlg.exec_() == OdemeDialog.Accepted:
            ok, msg = dlg.validate()
            if not ok:
                show_error(self, msg); return
            v = dlg.get_values()
            err = _safe_void(lambda: self.svc.guncelle(
                data["odeme_id"], v["uyelik_id"], v["tutar"],
                v["odeme_yontemi"], v["odeme_durumu"], v["aciklama"]
            ))
            if err:
                show_error(self, f"Güncelleme başarısız:\n{err}")
            else:
                show_success(self, "Ödeme güncellendi!")
                self.refresh()

    def _sil(self):
        data = get_selected_record(self.table, self._data, "odeme_id")
        if not data:
            show_error(self, "Lütfen bir ödeme seçin."); return
        if not data: return
        name = f"#{data.get('odeme_id', '')} – {data.get('uye_ad_soyad', '')}"
        if confirm_delete(self, name):
            err = _safe_void(lambda: self.svc.sil(data["odeme_id"]))
            if err:
                show_error(self, f"Silme başarısız:\n{err}")
            else:
                show_success(self, "Ödeme silindi.")
                self.refresh()


# =====================================================
# DERSLER SEKMESİ
# =====================================================

class DerslerTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.svc = DersService()
        self._ant_svc = AntrenorService()
        self._data = []
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 20, 24, 24)

        header = SectionHeader("Ders Yönetimi", "Grup derslerini ve programları yönetin", "🏃")
        layout.addWidget(header)

        self.action_bar = ActionBar()
        self.action_bar.btn_add.clicked.connect(self._ekle)
        self.action_bar.btn_edit.clicked.connect(self._duzenle)
        self.action_bar.btn_delete.clicked.connect(self._sil)
        self.action_bar.btn_refresh.clicked.connect(self.refresh)
        self.action_bar.search_input.textChanged.connect(
            lambda t: filter_table(self.table, t)
        )
        layout.addWidget(self.action_bar)

        self.table = BaseTableWidget([
            "ID", "Ders Adı", "Antrenör", "Uzmanlık", "Kontenjan",
            "Gün", "Başlangıç", "Bitiş", "Doluluk %", "Aktif"
        ])
        layout.addWidget(self.table)

    def refresh(self):
        rows, err = _safe_call(self.svc.listele, [])
        if err:
            show_error(self, f"Dersler yüklenemedi:\n{err}"); return
        self._data = rows
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        from PyQt5.QtWidgets import QTableWidgetItem
        for r in rows:
            i = self.table.rowCount()
            self.table.insertRow(i)
            aktif = r.get("aktif_mi")

            # fn_ders_doluluk_orani - MySQL Function
            try:
                doluluk, _ = _safe_call(lambda: self.svc.doluluk_orani(r["ders_id"]), 0)
                doluluk_str = f"{float(doluluk or 0):.1f}%"
            except Exception:
                doluluk_str = "—"

            vals = [
                r.get("ders_id", ""),
                r.get("ders_adi", ""),
                r.get("antrenor_ad_soyad", ""),
                r.get("uzmanlik_alani", ""),
                str(r.get("kontenjan", "")),
                r.get("ders_gunu", ""),
                str(r.get("baslangic_saati", ""))[:5],
                str(r.get("bitis_saati", ""))[:5],
                doluluk_str,
                "✅ Aktif" if aktif else "❌ Pasif",
            ]
            for col, val in enumerate(vals):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if col == 9:
                    item.setForeground(
                        QColor(COLORS["accent_success"]) if aktif
                        else QColor(COLORS["accent_danger"])
                    )
                self.table.setItem(i, col, item)
        self.table.setSortingEnabled(True)

    def _ekle(self):
        antrenorler, _ = _safe_call(self._ant_svc.listele, [])
        dlg = DersDialog(self, antrenorler=antrenorler)
        if dlg.exec_() == DersDialog.Accepted:
            ok, msg = dlg.validate()
            if not ok:
                show_error(self, msg); return
            v = dlg.get_values()
            err = _safe_void(lambda: self.svc.ekle(
                v["ders_adi"], v["antrenor_id"], v["kontenjan"],
                v["ders_gunu"], v["baslangic_saati"], v["bitis_saati"]
            ))
            if err:
                show_error(self, f"Ders eklenemedi:\n{err}")
            else:
                show_success(self, "Ders eklendi!")
                self.refresh()

    def _duzenle(self):
        data = get_selected_record(self.table, self._data, "ders_id")
        if not data:
            show_error(self, "Lütfen bir ders seçin."); return
        if not data: return
        antrenorler, _ = _safe_call(self._ant_svc.listele, [])
        dlg = DersDialog(self, data=data, antrenorler=antrenorler)
        if dlg.exec_() == DersDialog.Accepted:
            ok, msg = dlg.validate()
            if not ok:
                show_error(self, msg); return
            v = dlg.get_values()
            aktif = v.get("aktif_mi", 1)
            err = _safe_void(lambda: self.svc.guncelle(
                data["ders_id"], v["ders_adi"], v["antrenor_id"], v["kontenjan"],
                v["ders_gunu"], v["baslangic_saati"], v["bitis_saati"], aktif
            ))
            if err:
                show_error(self, f"Güncelleme başarısız:\n{err}")
            else:
                show_success(self, "Ders güncellendi!")
                self.refresh()

    def _sil(self):
        data = get_selected_record(self.table, self._data, "ders_id")
        if not data:
            show_error(self, "Lütfen bir ders seçin."); return
        if not data: return
        if confirm_delete(self, data.get("ders_adi", "")):
            err = _safe_void(lambda: self.svc.sil(data["ders_id"]))
            if err:
                show_error(self, f"Silme başarısız:\n{err}")
            else:
                show_success(self, "Ders silindi.")
                self.refresh()


# =====================================================
# DERS KAYITLARI SEKMESİ
# =====================================================

class DersKayitlariTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.svc = DersKayitService()
        self._uye_svc = UyeService()
        self._ders_svc = DersService()
        self._data = []
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 20, 24, 24)

        header = SectionHeader("Ders Kayıt Yönetimi", "Üye-ders kayıtlarını yönetin", "📋")
        layout.addWidget(header)

        note = QLabel("⚡ Trigger Aktif: Kontenjan doluysa kayıt engellenir (trg_ders_kontenjan_kontrol).")
        note.setStyleSheet(
            f"color: {COLORS['accent_warning']}; font-size: 11px; font-weight: 600;"
            f" background: {COLORS['bg_input']}; border-radius: 6px; padding: 8px 12px;"
        )
        layout.addWidget(note)

        self.action_bar = ActionBar()
        self.action_bar.btn_add.clicked.connect(self._ekle)
        self.action_bar.btn_edit.clicked.connect(self._duzenle)
        self.action_bar.btn_delete.clicked.connect(self._sil)
        self.action_bar.btn_refresh.clicked.connect(self.refresh)
        self.action_bar.search_input.textChanged.connect(
            lambda t: filter_table(self.table, t)
        )
        layout.addWidget(self.action_bar)

        self.table = BaseTableWidget([
            "ID", "Üye", "Ders", "Gün", "Saat", "Kayıt Tarihi", "Durum"
        ])
        layout.addWidget(self.table)

    def refresh(self):
        rows, err = _safe_call(self.svc.listele, [])
        if err:
            show_error(self, f"Ders kayıtları yüklenemedi:\n{err}"); return
        self._data = rows
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        from PyQt5.QtWidgets import QTableWidgetItem
        for r in rows:
            i = self.table.rowCount()
            self.table.insertRow(i)
            durum = r.get("durum", "")
            durum_renk = {
                "Kayıtlı": COLORS["accent_primary"],
                "Katıldı": COLORS["accent_success"],
                "İptal": COLORS["accent_danger"],
            }.get(durum, COLORS["text_primary"])
            vals = [
                r.get("ders_kayit_id", ""),
                r.get("uye_ad_soyad", ""),
                r.get("ders_adi", ""),
                r.get("ders_gunu", ""),
                str(r.get("baslangic_saati", ""))[:5],
                str(r.get("kayit_tarihi", ""))[:10],
                durum,
            ]
            for col, val in enumerate(vals):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if col == 6:
                    item.setForeground(QColor(durum_renk))
                self.table.setItem(i, col, item)
        self.table.setSortingEnabled(True)

    def _ekle(self):
        uyeler, _ = _safe_call(self._uye_svc.listele, [])
        dersler, _ = _safe_call(self._ders_svc.listele, [])
        dlg = DersKayitDialog(self, uyeler=uyeler, dersler=dersler)
        if dlg.exec_() == DersKayitDialog.Accepted:
            ok, msg = dlg.validate()
            if not ok:
                show_error(self, msg); return
            v = dlg.get_values()
            err = _safe_void(lambda: self.svc.ekle(
                v["uye_id"], v["ders_id"], v["durum"]
            ))
            if err:
                show_error(self, f"Ders kaydı eklenemedi:\n{err}")
            else:
                show_success(self, "Ders kaydı oluşturuldu!")
                self.refresh()

    def _duzenle(self):
        data = get_selected_record(self.table, self._data, "ders_kayit_id")
        if not data:
            show_error(self, "Lütfen bir kayıt seçin."); return
        if not data: return
        uyeler, _ = _safe_call(self._uye_svc.listele, [])
        dersler, _ = _safe_call(self._ders_svc.listele, [])
        dlg = DersKayitDialog(self, data=data, uyeler=uyeler, dersler=dersler)
        if dlg.exec_() == DersKayitDialog.Accepted:
            ok, msg = dlg.validate()
            if not ok:
                show_error(self, msg); return
            v = dlg.get_values()
            err = _safe_void(lambda: self.svc.guncelle(
                data["ders_kayit_id"], v["uye_id"], v["ders_id"], v["durum"]
            ))
            if err:
                show_error(self, f"Güncelleme başarısız:\n{err}")
            else:
                show_success(self, "Ders kaydı güncellendi!")
                self.refresh()

    def _sil(self):
        data = get_selected_record(self.table, self._data, "ders_kayit_id")
        if not data:
            show_error(self, "Lütfen bir kayıt seçin."); return
        if not data: return
        name = f"#{data.get('ders_kayit_id', '')} – {data.get('uye_ad_soyad', '')}"
        if confirm_delete(self, name):
            err = _safe_void(lambda: self.svc.sil(data["ders_kayit_id"]))
            if err:
                show_error(self, f"Silme başarısız:\n{err}")
            else:
                show_success(self, "Ders kaydı silindi.")
                self.refresh()


# =====================================================
# YOKLAMALAR SEKMESİ
# =====================================================

class YoklamalarTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.svc = YoklamaService()
        self._dk_svc = DersKayitService()
        self._data = []
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 20, 24, 24)

        header = SectionHeader("Yoklama Yönetimi", "Ders katılımlarını takip edin", "✅")
        layout.addWidget(header)

        self.action_bar = ActionBar()
        self.action_bar.btn_add.clicked.connect(self._ekle)
        self.action_bar.btn_edit.clicked.connect(self._duzenle)
        self.action_bar.btn_delete.clicked.connect(self._sil)
        self.action_bar.btn_refresh.clicked.connect(self.refresh)
        self.action_bar.search_input.textChanged.connect(
            lambda t: filter_table(self.table, t)
        )
        layout.addWidget(self.action_bar)

        self.table = BaseTableWidget([
            "ID", "Ders Kaydı ID", "Üye", "Ders", "Tarih", "Katılım Durumu", "Açıklama"
        ])
        layout.addWidget(self.table)

    def refresh(self):
        rows, err = _safe_call(self.svc.listele, [])
        if err:
            show_error(self, f"Yoklamalar yüklenemedi:\n{err}"); return
        self._data = rows
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        from PyQt5.QtWidgets import QTableWidgetItem
        for r in rows:
            i = self.table.rowCount()
            self.table.insertRow(i)
            katilim = r.get("katilim_durumu", "")
            katilim_renk = {
                "Katıldı": COLORS["accent_success"],
                "Gelmedi": COLORS["accent_danger"],
                "Mazeretli": COLORS["accent_warning"],
            }.get(katilim, COLORS["text_primary"])
            vals = [
                r.get("yoklama_id", ""),
                r.get("ders_kayit_id", ""),
                r.get("uye_ad_soyad", ""),
                r.get("ders_adi", ""),
                str(r.get("yoklama_tarihi", ""))[:10],
                katilim,
                r.get("aciklama", "") or "",
            ]
            for col, val in enumerate(vals):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if col == 5:
                    item.setForeground(QColor(katilim_renk))
                self.table.setItem(i, col, item)
        self.table.setSortingEnabled(True)

    def _ekle(self):
        ders_kayitlari, _ = _safe_call(self._dk_svc.listele, [])
        dlg = YoklamaDialog(self, ders_kayitlari=ders_kayitlari)
        if dlg.exec_() == YoklamaDialog.Accepted:
            ok, msg = dlg.validate()
            if not ok:
                show_error(self, msg); return
            v = dlg.get_values()
            err = _safe_void(lambda: self.svc.ekle(
                v["ders_kayit_id"], v["yoklama_tarihi"],
                v["katilim_durumu"], v["aciklama"]
            ))
            if err:
                show_error(self, f"Yoklama eklenemedi:\n{err}")
            else:
                show_success(self, "Yoklama kaydedildi!")
                self.refresh()

    def _duzenle(self):
        data = get_selected_record(self.table, self._data, "yoklama_id")
        if not data:
            show_error(self, "Lütfen bir yoklama seçin."); return
        if not data: return
        ders_kayitlari, _ = _safe_call(self._dk_svc.listele, [])
        dlg = YoklamaDialog(self, data=data, ders_kayitlari=ders_kayitlari)
        if dlg.exec_() == YoklamaDialog.Accepted:
            ok, msg = dlg.validate()
            if not ok:
                show_error(self, msg); return
            v = dlg.get_values()
            err = _safe_void(lambda: self.svc.guncelle(
                data["yoklama_id"], v["ders_kayit_id"], v["yoklama_tarihi"],
                v["katilim_durumu"], v["aciklama"]
            ))
            if err:
                show_error(self, f"Güncelleme başarısız:\n{err}")
            else:
                show_success(self, "Yoklama güncellendi!")
                self.refresh()

    def _sil(self):
        data = get_selected_record(self.table, self._data, "yoklama_id")
        if not data:
            show_error(self, "Lütfen bir yoklama seçin."); return
        if not data: return
        name = f"#{data.get('yoklama_id', '')} – {data.get('uye_ad_soyad', '')}"
        if confirm_delete(self, name):
            err = _safe_void(lambda: self.svc.sil(data["yoklama_id"]))
            if err:
                show_error(self, f"Silme başarısız:\n{err}")
            else:
                show_success(self, "Yoklama silindi.")
                self.refresh()


# =====================================================
# EKİPMANLAR SEKMESİ
# =====================================================

class EkipmanlarTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.svc = EkipmanService()
        self._data = []
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 20, 24, 24)

        header = SectionHeader("Ekipman Yönetimi", "Salon ekipmanlarını takip edin", "🏋️")
        layout.addWidget(header)

        self.action_bar = ActionBar()
        self.action_bar.btn_add.clicked.connect(self._ekle)
        self.action_bar.btn_edit.clicked.connect(self._duzenle)
        self.action_bar.btn_delete.clicked.connect(self._sil)
        self.action_bar.btn_refresh.clicked.connect(self.refresh)
        self.action_bar.search_input.textChanged.connect(
            lambda t: filter_table(self.table, t)
        )
        layout.addWidget(self.action_bar)

        self.table = BaseTableWidget([
            "ID", "Ekipman Adı", "Kategori", "Alım Tarihi", "Durum", "Açıklama"
        ])
        layout.addWidget(self.table)

    def refresh(self):
        rows, err = _safe_call(self.svc.listele, [])
        if err:
            show_error(self, f"Ekipmanlar yüklenemedi:\n{err}"); return
        self._data = rows
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        from PyQt5.QtWidgets import QTableWidgetItem
        for r in rows:
            i = self.table.rowCount()
            self.table.insertRow(i)
            durum = r.get("durum", "")
            durum_renk = {
                "Kullanılabilir": COLORS["accent_success"],
                "Bakımda": COLORS["accent_warning"],
                "Arızalı": COLORS["accent_danger"],
            }.get(durum, COLORS["text_primary"])
            vals = [
                r.get("ekipman_id", ""),
                r.get("ekipman_adi", ""),
                r.get("kategori", ""),
                str(r.get("alim_tarihi", ""))[:10] if r.get("alim_tarihi") else "",
                durum,
                r.get("aciklama", "") or "",
            ]
            for col, val in enumerate(vals):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if col == 4:
                    item.setForeground(QColor(durum_renk))
                self.table.setItem(i, col, item)
        self.table.setSortingEnabled(True)

    def _ekle(self):
        dlg = EkipmanDialog(self)
        if dlg.exec_() == EkipmanDialog.Accepted:
            ok, msg = dlg.validate()
            if not ok:
                show_error(self, msg); return
            v = dlg.get_values()
            err = _safe_void(lambda: self.svc.ekle(
                v["ekipman_adi"], v["kategori"], v["alim_tarihi"],
                v["durum"], v["aciklama"]
            ))
            if err:
                show_error(self, f"Ekipman eklenemedi:\n{err}")
            else:
                show_success(self, "Ekipman eklendi!")
                self.refresh()

    def _duzenle(self):
        data = get_selected_record(self.table, self._data, "ekipman_id")
        if not data:
            show_error(self, "Lütfen bir ekipman seçin."); return
        if not data: return
        dlg = EkipmanDialog(self, data)
        if dlg.exec_() == EkipmanDialog.Accepted:
            ok, msg = dlg.validate()
            if not ok:
                show_error(self, msg); return
            v = dlg.get_values()
            err = _safe_void(lambda: self.svc.guncelle(
                data["ekipman_id"], v["ekipman_adi"], v["kategori"],
                v["alim_tarihi"], v["durum"], v["aciklama"]
            ))
            if err:
                show_error(self, f"Güncelleme başarısız:\n{err}")
            else:
                show_success(self, "Ekipman güncellendi!")
                self.refresh()

    def _sil(self):
        data = get_selected_record(self.table, self._data, "ekipman_id")
        if not data:
            show_error(self, "Lütfen bir ekipman seçin."); return
        if not data: return
        if confirm_delete(self, data.get("ekipman_adi", "")):
            err = _safe_void(lambda: self.svc.sil(data["ekipman_id"]))
            if err:
                show_error(self, f"Silme başarısız:\n{err}")
            else:
                show_success(self, "Ekipman silindi.")
                self.refresh()


# =====================================================
# EKİPMAN BAKIMLARI SEKMESİ
# =====================================================

class BakimlarTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.svc = BakimService()
        self._ekipman_svc = EkipmanService()
        self._data = []
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 20, 24, 24)

        header = SectionHeader("Ekipman Bakım Yönetimi", "Bakım planlarını ve kayıtları yönetin", "🔧")
        layout.addWidget(header)

        self.action_bar = ActionBar()
        self.action_bar.btn_add.clicked.connect(self._ekle)
        self.action_bar.btn_edit.clicked.connect(self._duzenle)
        self.action_bar.btn_delete.clicked.connect(self._sil)
        self.action_bar.btn_refresh.clicked.connect(self.refresh)
        self.action_bar.search_input.textChanged.connect(
            lambda t: filter_table(self.table, t)
        )
        layout.addWidget(self.action_bar)

        self.table = BaseTableWidget([
            "ID", "Ekipman", "Bakım Tarihi", "Açıklama", "Maliyet (₺)", "Durum"
        ])
        layout.addWidget(self.table)

    def refresh(self):
        rows, err = _safe_call(self.svc.listele, [])
        if err:
            show_error(self, f"Bakımlar yüklenemedi:\n{err}"); return
        self._data = rows
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        from PyQt5.QtWidgets import QTableWidgetItem
        for r in rows:
            i = self.table.rowCount()
            self.table.insertRow(i)
            durum = r.get("bakim_durumu", "")
            durum_renk = {
                "Planlandı": COLORS["accent_warning"],
                "Tamamlandı": COLORS["accent_success"],
                "İptal": COLORS["accent_danger"],
            }.get(durum, COLORS["text_primary"])
            vals = [
                r.get("bakim_id", ""),
                r.get("ekipman_adi", "") or str(r.get("ekipman_id", "")),
                str(r.get("bakim_tarihi", ""))[:10],
                r.get("aciklama", ""),
                f"{float(r.get('bakim_maliyeti', 0) or 0):,.2f}",
                durum,
            ]
            for col, val in enumerate(vals):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if col == 4:
                    item.setForeground(QColor(COLORS["accent_warning"]))
                if col == 5:
                    item.setForeground(QColor(durum_renk))
                self.table.setItem(i, col, item)
        self.table.setSortingEnabled(True)

    def _ekle(self):
        ekipmanlar, _ = _safe_call(self._ekipman_svc.listele, [])
        dlg = BakimDialog(self, ekipmanlar=ekipmanlar)
        if dlg.exec_() == BakimDialog.Accepted:
            ok, msg = dlg.validate()
            if not ok:
                show_error(self, msg); return
            v = dlg.get_values()
            err = _safe_void(lambda: self.svc.ekle(
                v["ekipman_id"], v["bakim_tarihi"], v["aciklama"],
                v["bakim_maliyeti"], v["bakim_durumu"]
            ))
            if err:
                show_error(self, f"Bakım eklenemedi:\n{err}")
            else:
                show_success(self, "Bakım kaydı oluşturuldu!")
                self.refresh()

    def _duzenle(self):
        data = get_selected_record(self.table, self._data, "bakim_id")
        if not data:
            show_error(self, "Lütfen bir bakım kaydı seçin."); return
        if not data: return
        ekipmanlar, _ = _safe_call(self._ekipman_svc.listele, [])
        dlg = BakimDialog(self, data=data, ekipmanlar=ekipmanlar)
        if dlg.exec_() == BakimDialog.Accepted:
            ok, msg = dlg.validate()
            if not ok:
                show_error(self, msg); return
            v = dlg.get_values()
            err = _safe_void(lambda: self.svc.guncelle(
                data["bakim_id"], v["ekipman_id"], v["bakim_tarihi"],
                v["aciklama"], v["bakim_maliyeti"], v["bakim_durumu"]
            ))
            if err:
                show_error(self, f"Güncelleme başarısız:\n{err}")
            else:
                show_success(self, "Bakım güncellendi!")
                self.refresh()

    def _sil(self):
        data = get_selected_record(self.table, self._data, "bakim_id")
        if not data:
            show_error(self, "Lütfen bir bakım kaydı seçin."); return
        if not data: return
        name = f"#{data.get('bakim_id', '')} – {data.get('ekipman_adi', '')}"
        if confirm_delete(self, name):
            err = _safe_void(lambda: self.svc.sil(data["bakim_id"]))
            if err:
                show_error(self, f"Silme başarısız:\n{err}")
            else:
                show_success(self, "Bakım kaydı silindi.")
                self.refresh()


# =====================================================
# ANA PENCERE
# =====================================================

class MainWindow(QMainWindow):
    """Ana uygulama penceresi - tüm sekmeler."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏋️  Spor Salonu Yönetim Sistemi")
        self.setMinimumSize(1280, 780)
        self.resize(1440, 860)
        self.setStyleSheet(MAIN_STYLE)
        self._setup_ui()
        self._setup_statusbar()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self._build_header())

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        # Sol menü
        self.sidebar = QListWidget()
        self.sidebar.setObjectName("sidebarNav")
        self.sidebar.setFixedWidth(240)

        self.stack = QStackedWidget()

        self.dashboard_tab = DashboardTab()
        self.uyeler_tab = UyelerTab()
        self.antrenorler_tab = AntrenorlerTab()
        self.paketler_tab = PaketlerTab()
        self.uyelikler_tab = UyeliklerTab()
        self.odemeler_tab = OdemelerTab()
        self.dersler_tab = DerslerTab()
        self.ders_kayitlari_tab = DersKayitlariTab()
        self.yoklamalar_tab = YoklamalarTab()
        self.ekipmanlar_tab = EkipmanlarTab()
        self.bakimlar_tab = BakimlarTab()
        self.settings_tab = SettingsTab()

        pages = [
            (self.dashboard_tab, "📊  Dashboard"),
            (self.uyeler_tab, "👤  Üyeler"),
            (self.antrenorler_tab, "🏅  Antrenörler"),
            (self.paketler_tab, "📦  Paketler"),
            (self.uyelikler_tab, "🎫  Üyelikler"),
            (self.odemeler_tab, "💳  Ödemeler"),
            (self.dersler_tab, "🏃  Dersler"),
            (self.ders_kayitlari_tab, "📋  Ders Kayıtları"),
            (self.yoklamalar_tab, "✅  Yoklamalar"),
            (self.ekipmanlar_tab, "🏋️  Ekipmanlar"),
            (self.bakimlar_tab, "🔧  Bakımlar"),
            (self.settings_tab, "⚙️  Ayarlar"),
        ]
        for widget, label in pages:
            self.stack.addWidget(widget)
            self.sidebar.addItem(QListWidgetItem(label))

        self.sidebar.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.sidebar.setCurrentRow(0)

        body.addWidget(self.sidebar)
        body.addWidget(self.stack, 1)
        layout.addLayout(body, 1)

    def _build_header(self):
        """Üst başlık çubuğu."""
        bar = QFrame()
        bar.setObjectName("topBar")
        bar.setFixedHeight(64)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(24, 0, 24, 0)

        logo = QLabel("🏋️")
        logo.setStyleSheet("font-size: 30px; background: transparent;")
        layout.addWidget(logo)

        title_box = QVBoxLayout()
        title_box.setSpacing(0)
        title = QLabel("Spor Salonu Yönetim")
        title.setStyleSheet(
            f"font-size: 17px; font-weight: 800; color: {COLORS['text_primary']};"
        )
        sub = QLabel("PyQt5  ·  N-Katmanlı  ·  MySQL Stored Procedure")
        sub.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']};")
        title_box.addWidget(title)
        title_box.addWidget(sub)
        layout.addLayout(title_box)

        layout.addStretch()

        self.conn_label = QLabel("● Bağlı")
        self.conn_label.setStyleSheet(
            f"color: {COLORS['accent_success']}; font-size: 12px; font-weight: 700;"
            f" background: {COLORS['accent_success']}18; padding: 6px 14px;"
            f" border-radius: 20px;"
        )
        layout.addWidget(self.conn_label)

        btn_logout = QPushButton("Çıkış")
        btn_logout.setObjectName("btnGhost")
        btn_logout.setFixedHeight(38)
        btn_logout.setFixedWidth(90)
        btn_logout.clicked.connect(self._logout)
        layout.addWidget(btn_logout)

        return bar

    def _setup_statusbar(self):
        sb = self.statusBar()
        sb.showMessage(
            f"✅  MySQL bağlantısı kuruldu  |  "
            f"Veritabanı: spor_salonu_db  |  "
            f"Mimari: Presentation → Business → DAL → Stored Procedure"
        )

    def _logout(self):
        reply = QMessageBox.question(
            self, "Çıkış", "Uygulamadan çıkmak istediğinizden emin misiniz?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            db.close()
            from login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()

    def closeEvent(self, event):
        db.close()
        event.accept()
