# -*- coding: utf-8 -*-
"""
CRUD Diyalogları - Tüm tablolar için form diyalogları
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QDateEdit, QTimeEdit,
    QSpinBox, QDoubleSpinBox, QCheckBox, QTextEdit, QGroupBox,
    QDialogButtonBox, QScrollArea, QWidget, QFrame
)
from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QFont

from styles import COLORS, MAIN_STYLE


def _make_dialog(parent, title, icon="📝"):
    """Standart diyalog oluştur."""
    dialog = QDialog(parent)
    dialog.setWindowTitle(f"{icon}  {title}")
    dialog.setMinimumWidth(500)
    dialog.setStyleSheet(MAIN_STYLE)
    dialog.setModal(True)
    return dialog


def _add_buttons(layout, dialog):
    """Kaydet/İptal butonlarını ekle."""
    btn_box = QHBoxLayout()
    btn_box.setSpacing(12)
    btn_box.addStretch()

    btn_cancel = QPushButton("✖  İptal")
    btn_cancel.setStyleSheet(f"""
        QPushButton {{
            background: {COLORS['bg_input']};
            color: {COLORS['text_secondary']};
            border: 1px solid {COLORS['border']};
            border-radius: 6px;
            padding: 10px 24px;
            font-weight: 600;
        }}
        QPushButton:hover {{
            border-color: {COLORS['accent_danger']};
            color: {COLORS['accent_danger']};
        }}
    """)
    btn_cancel.clicked.connect(dialog.reject)

    btn_save = QPushButton("✔  Kaydet")
    btn_save.setObjectName("btnSuccess")
    btn_save.setMinimumHeight(42)
    btn_save.clicked.connect(dialog.accept)

    btn_box.addWidget(btn_cancel)
    btn_box.addWidget(btn_save)
    layout.addLayout(btn_box)

    return btn_save


# =====================================================
# ÜYE DİYALOGU
# =====================================================

class UyeDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Üye Ekle" if data is None else "Üye Düzenle")
        self.setMinimumWidth(520)
        self.setStyleSheet(MAIN_STYLE)
        self.setModal(True)
        self._data = data
        self._setup_ui()
        if data:
            self._fill_data(data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        # Başlık
        title = QLabel("👤  " + ("Yeni Üye" if not self._data else "Üye Düzenle"))
        title.setStyleSheet(f"font-size: 18px; font-weight: 800; color: {COLORS['accent_primary']};")
        layout.addWidget(title)

        line = QFrame(); line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"color: {COLORS['border']};")
        layout.addWidget(line)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignRight)

        self.ad = QLineEdit()
        self.ad.setPlaceholderText("Adı (en az 2 karakter)")
        self.ad.setMinimumHeight(38)
        form.addRow("Ad *:", self.ad)

        self.soyad = QLineEdit()
        self.soyad.setPlaceholderText("Soyadı (en az 2 karakter)")
        self.soyad.setMinimumHeight(38)
        form.addRow("Soyad *:", self.soyad)

        self.telefon = QLineEdit()
        self.telefon.setPlaceholderText("05XX XXX XX XX")
        self.telefon.setMinimumHeight(38)
        form.addRow("Telefon *:", self.telefon)

        self.email = QLineEdit()
        self.email.setPlaceholderText("ornek@email.com")
        self.email.setMinimumHeight(38)
        form.addRow("E-posta:", self.email)

        self.cinsiyet = QComboBox()
        self.cinsiyet.addItems(["Erkek", "Kadın", "Belirtmek İstemiyor"])
        self.cinsiyet.setMinimumHeight(38)
        form.addRow("Cinsiyet:", self.cinsiyet)

        self.dogum_tarihi = QDateEdit()
        self.dogum_tarihi.setCalendarPopup(True)
        self.dogum_tarihi.setDate(QDate(2000, 1, 1))
        self.dogum_tarihi.setDisplayFormat("dd.MM.yyyy")
        self.dogum_tarihi.setMinimumHeight(38)
        form.addRow("Doğum Tarihi:", self.dogum_tarihi)

        if self._data:
            self.aktif_mi = QCheckBox("Aktif")
            self.aktif_mi.setChecked(True)
            form.addRow("Durum:", self.aktif_mi)

        layout.addLayout(form)
        _add_buttons(layout, self)

    def _fill_data(self, data):
        self.ad.setText(data.get("ad", ""))
        self.soyad.setText(data.get("soyad", ""))
        self.telefon.setText(data.get("telefon", ""))
        self.email.setText(data.get("email", "") or "")
        cinsiyet = data.get("cinsiyet", "Belirtmek İstemiyor")
        idx = self.cinsiyet.findText(cinsiyet)
        if idx >= 0:
            self.cinsiyet.setCurrentIndex(idx)
        dt = data.get("dogum_tarihi", "")
        if dt:
            try:
                d = QDate.fromString(str(dt)[:10], "yyyy-MM-dd")
                self.dogum_tarihi.setDate(d)
            except Exception:
                pass
        if hasattr(self, "aktif_mi"):
            aktif = data.get("aktif_mi", 1)
            self.aktif_mi.setChecked(bool(int(aktif)))

    def get_values(self):
        result = {
            "ad": self.ad.text().strip(),
            "soyad": self.soyad.text().strip(),
            "telefon": self.telefon.text().strip(),
            "email": self.email.text().strip() or None,
            "cinsiyet": self.cinsiyet.currentText(),
            "dogum_tarihi": self.dogum_tarihi.date().toString("yyyy-MM-dd"),
        }
        if self._data:
            result["aktif_mi"] = 1 if self.aktif_mi.isChecked() else 0
        return result

    def validate(self):
        if len(self.ad.text().strip()) < 2:
            return False, "Ad en az 2 karakter olmalıdır."
        if len(self.soyad.text().strip()) < 2:
            return False, "Soyad en az 2 karakter olmalıdır."
        if len(self.telefon.text().strip()) < 10:
            return False, "Geçerli bir telefon numarası girin."
        return True, ""


# =====================================================
# ANTRENÖR DİYALOGU
# =====================================================

class AntrenorDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Antrenör Ekle" if data is None else "Antrenör Düzenle")
        self.setMinimumWidth(520)
        self.setStyleSheet(MAIN_STYLE)
        self.setModal(True)
        self._data = data
        self._setup_ui()
        if data:
            self._fill_data(data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("🏅  " + ("Yeni Antrenör" if not self._data else "Antrenör Düzenle"))
        title.setStyleSheet(f"font-size: 18px; font-weight: 800; color: {COLORS['accent_primary']};")
        layout.addWidget(title)

        line = QFrame(); line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"color: {COLORS['border']};")
        layout.addWidget(line)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignRight)

        self.ad = QLineEdit(); self.ad.setPlaceholderText("Ad"); self.ad.setMinimumHeight(38)
        form.addRow("Ad *:", self.ad)
        self.soyad = QLineEdit(); self.soyad.setPlaceholderText("Soyad"); self.soyad.setMinimumHeight(38)
        form.addRow("Soyad *:", self.soyad)
        self.telefon = QLineEdit(); self.telefon.setPlaceholderText("05XX XXX XX XX"); self.telefon.setMinimumHeight(38)
        form.addRow("Telefon *:", self.telefon)
        self.email = QLineEdit(); self.email.setPlaceholderText("ornek@email.com"); self.email.setMinimumHeight(38)
        form.addRow("E-posta:", self.email)
        self.uzmanlik = QLineEdit(); self.uzmanlik.setPlaceholderText("Fitness, Pilates, Yoga..."); self.uzmanlik.setMinimumHeight(38)
        form.addRow("Uzmanlık Alanı *:", self.uzmanlik)

        self.maas = QDoubleSpinBox()
        self.maas.setRange(0, 999999.99)
        self.maas.setSuffix(" ₺")
        self.maas.setDecimals(2)
        self.maas.setMinimumHeight(38)
        form.addRow("Maaş *:", self.maas)

        self.ise_baslama = QDateEdit()
        self.ise_baslama.setCalendarPopup(True)
        self.ise_baslama.setDate(QDate.currentDate())
        self.ise_baslama.setDisplayFormat("dd.MM.yyyy")
        self.ise_baslama.setMinimumHeight(38)
        form.addRow("İşe Başlama *:", self.ise_baslama)

        if self._data:
            self.aktif_mi = QCheckBox("Aktif")
            self.aktif_mi.setChecked(True)
            form.addRow("Durum:", self.aktif_mi)

        layout.addLayout(form)
        _add_buttons(layout, self)

    def _fill_data(self, data):
        self.ad.setText(data.get("ad", ""))
        self.soyad.setText(data.get("soyad", ""))
        self.telefon.setText(data.get("telefon", ""))
        self.email.setText(data.get("email", "") or "")
        self.uzmanlik.setText(data.get("uzmanlik_alani", ""))
        try:
            self.maas.setValue(float(data.get("maas", 0)))
        except Exception:
            pass
        dt = data.get("ise_baslama_tarihi", "")
        if dt:
            try:
                d = QDate.fromString(str(dt)[:10], "yyyy-MM-dd")
                self.ise_baslama.setDate(d)
            except Exception:
                pass
        if hasattr(self, "aktif_mi"):
            self.aktif_mi.setChecked(bool(int(data.get("aktif_mi", 1))))

    def get_values(self):
        result = {
            "ad": self.ad.text().strip(),
            "soyad": self.soyad.text().strip(),
            "telefon": self.telefon.text().strip(),
            "email": self.email.text().strip() or None,
            "uzmanlik_alani": self.uzmanlik.text().strip(),
            "maas": self.maas.value(),
            "ise_baslama_tarihi": self.ise_baslama.date().toString("yyyy-MM-dd"),
        }
        if self._data:
            result["aktif_mi"] = 1 if self.aktif_mi.isChecked() else 0
        return result

    def validate(self):
        if len(self.ad.text().strip()) < 2:
            return False, "Ad en az 2 karakter olmalıdır."
        if len(self.soyad.text().strip()) < 2:
            return False, "Soyad en az 2 karakter olmalıdır."
        if len(self.telefon.text().strip()) < 10:
            return False, "Geçerli bir telefon numarası girin."
        if len(self.uzmanlik.text().strip()) < 2:
            return False, "Uzmanlık alanı boş bırakılamaz."
        return True, ""


# =====================================================
# ÜYELİK PAKETİ DİYALOGU
# =====================================================

class UyelikPaketiDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Üyelik Paketi Ekle" if data is None else "Paket Düzenle")
        self.setMinimumWidth(480)
        self.setStyleSheet(MAIN_STYLE)
        self.setModal(True)
        self._data = data
        self._setup_ui()
        if data:
            self._fill_data(data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("📦  " + ("Yeni Paket" if not self._data else "Paket Düzenle"))
        title.setStyleSheet(f"font-size: 18px; font-weight: 800; color: {COLORS['accent_primary']};")
        layout.addWidget(title)

        line = QFrame(); line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"color: {COLORS['border']};")
        layout.addWidget(line)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignRight)

        self.paket_adi = QLineEdit(); self.paket_adi.setPlaceholderText("Paket adı"); self.paket_adi.setMinimumHeight(38)
        form.addRow("Paket Adı *:", self.paket_adi)

        self.sure_gun = QSpinBox()
        self.sure_gun.setRange(1, 3650)
        self.sure_gun.setSuffix(" gün")
        self.sure_gun.setValue(30)
        self.sure_gun.setMinimumHeight(38)
        form.addRow("Süre *:", self.sure_gun)

        self.ucret = QDoubleSpinBox()
        self.ucret.setRange(0.01, 999999.99)
        self.ucret.setSuffix(" ₺")
        self.ucret.setDecimals(2)
        self.ucret.setMinimumHeight(38)
        form.addRow("Ücret *:", self.ucret)

        self.aciklama = QTextEdit()
        self.aciklama.setPlaceholderText("Paket açıklaması...")
        self.aciklama.setMaximumHeight(80)
        form.addRow("Açıklama:", self.aciklama)

        if self._data:
            self.aktif_mi = QCheckBox("Aktif")
            self.aktif_mi.setChecked(True)
            form.addRow("Durum:", self.aktif_mi)

        layout.addLayout(form)
        _add_buttons(layout, self)

    def _fill_data(self, data):
        self.paket_adi.setText(data.get("paket_adi", ""))
        try:
            self.sure_gun.setValue(int(data.get("sure_gun", 30)))
            self.ucret.setValue(float(data.get("ucret", 0)))
        except Exception:
            pass
        self.aciklama.setPlainText(data.get("aciklama", "") or "")
        if hasattr(self, "aktif_mi"):
            self.aktif_mi.setChecked(bool(int(data.get("aktif_mi", 1))))

    def get_values(self):
        result = {
            "paket_adi": self.paket_adi.text().strip(),
            "sure_gun": self.sure_gun.value(),
            "ucret": self.ucret.value(),
            "aciklama": self.aciklama.toPlainText().strip() or None,
        }
        if self._data:
            result["aktif_mi"] = 1 if self.aktif_mi.isChecked() else 0
        return result

    def validate(self):
        if not self.paket_adi.text().strip():
            return False, "Paket adı boş bırakılamaz."
        return True, ""


# =====================================================
# ÜYELİK DİYALOGU
# =====================================================

class UyelikDialog(QDialog):
    def __init__(self, parent=None, data=None, uyeler=None, paketler=None):
        super().__init__(parent)
        self.setWindowTitle("Üyelik Ekle" if data is None else "Üyelik Düzenle")
        self.setMinimumWidth(520)
        self.setStyleSheet(MAIN_STYLE)
        self.setModal(True)
        self._data = data
        self._uyeler = uyeler or []
        self._paketler = paketler or []
        self._setup_ui()
        if data:
            self._fill_data(data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("🎫  " + ("Yeni Üyelik" if not self._data else "Üyelik Düzenle"))
        title.setStyleSheet(f"font-size: 18px; font-weight: 800; color: {COLORS['accent_primary']};")
        layout.addWidget(title)

        line = QFrame(); line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"color: {COLORS['border']};")
        layout.addWidget(line)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignRight)

        self.uye_combo = QComboBox()
        self.uye_combo.setMinimumHeight(38)
        for uye in self._uyeler:
            self.uye_combo.addItem(
                f"{uye.get('ad', '')} {uye.get('soyad', '')} (ID: {uye.get('uye_id', '')})",
                uye.get("uye_id")
            )
        form.addRow("Üye *:", self.uye_combo)

        self.paket_combo = QComboBox()
        self.paket_combo.setMinimumHeight(38)
        for p in self._paketler:
            self.paket_combo.addItem(
                f"{p.get('paket_adi', '')} – {p.get('ucret', '')} ₺ / {p.get('sure_gun', '')} gün",
                p.get("paket_id")
            )
        self.paket_combo.currentIndexChanged.connect(self._auto_fill_bitis)
        form.addRow("Paket *:", self.paket_combo)

        self.baslangic = QDateEdit()
        self.baslangic.setCalendarPopup(True)
        self.baslangic.setDate(QDate.currentDate())
        self.baslangic.setDisplayFormat("dd.MM.yyyy")
        self.baslangic.setMinimumHeight(38)
        self.baslangic.dateChanged.connect(self._auto_fill_bitis)
        form.addRow("Başlangıç *:", self.baslangic)

        self.bitis = QDateEdit()
        self.bitis.setCalendarPopup(True)
        self.bitis.setDate(QDate.currentDate().addDays(30))
        self.bitis.setDisplayFormat("dd.MM.yyyy")
        self.bitis.setMinimumHeight(38)
        form.addRow("Bitiş *:", self.bitis)

        self.durum = QComboBox()
        self.durum.addItems(["Aktif", "Pasif", "Donduruldu", "Süresi Doldu"])
        self.durum.setMinimumHeight(38)
        form.addRow("Durum:", self.durum)

        layout.addLayout(form)
        _add_buttons(layout, self)

    def _auto_fill_bitis(self):
        """Paket seçimi veya başlangıç tarihi değişince bitiş tarihini otomatik hesapla."""
        idx = self.paket_combo.currentIndex()
        if idx < 0 or idx >= len(self._paketler):
            return
        paket = self._paketler[idx]
        sure = int(paket.get("sure_gun", 30))
        self.bitis.setDate(self.baslangic.date().addDays(sure))

    def _fill_data(self, data):
        # Üye bul
        uye_id = int(data.get("uye_id", 0))
        for i in range(self.uye_combo.count()):
            if self.uye_combo.itemData(i) == uye_id:
                self.uye_combo.setCurrentIndex(i)
                break
        # Paket bul
        paket_id = int(data.get("paket_id", 0))
        for i in range(self.paket_combo.count()):
            if self.paket_combo.itemData(i) == paket_id:
                self.paket_combo.setCurrentIndex(i)
                break
        # Tarihler
        for attr, key in [("baslangic", "baslangic_tarihi"), ("bitis", "bitis_tarihi")]:
            dt = data.get(key, "")
            if dt:
                try:
                    d = QDate.fromString(str(dt)[:10], "yyyy-MM-dd")
                    getattr(self, attr).setDate(d)
                except Exception:
                    pass
        # Durum
        durum = data.get("durum", "Aktif")
        idx = self.durum.findText(durum)
        if idx >= 0:
            self.durum.setCurrentIndex(idx)

    def get_values(self):
        return {
            "uye_id": self.uye_combo.currentData(),
            "paket_id": self.paket_combo.currentData(),
            "baslangic_tarihi": self.baslangic.date().toString("yyyy-MM-dd"),
            "bitis_tarihi": self.bitis.date().toString("yyyy-MM-dd"),
            "durum": self.durum.currentText(),
        }

    def validate(self):
        if self.baslangic.date() > self.bitis.date():
            return False, "Bitiş tarihi başlangıç tarihinden önce olamaz."
        if self.uye_combo.count() == 0:
            return False, "Önce üye ekleyin."
        if self.paket_combo.count() == 0:
            return False, "Önce paket ekleyin."
        return True, ""


# =====================================================
# ÖDEME DİYALOGU
# =====================================================

class OdemeDialog(QDialog):
    def __init__(self, parent=None, data=None, uyelikler=None):
        super().__init__(parent)
        self.setWindowTitle("Ödeme Ekle" if data is None else "Ödeme Düzenle")
        self.setMinimumWidth(520)
        self.setStyleSheet(MAIN_STYLE)
        self.setModal(True)
        self._data = data
        self._uyelikler = uyelikler or []
        self._setup_ui()
        if data:
            self._fill_data(data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("💳  " + ("Yeni Ödeme" if not self._data else "Ödeme Düzenle"))
        title.setStyleSheet(f"font-size: 18px; font-weight: 800; color: {COLORS['accent_primary']};")
        layout.addWidget(title)

        line = QFrame(); line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"color: {COLORS['border']};")
        layout.addWidget(line)

        # Bilgi notu
        note = QLabel("⚡ Başarılı ödeme eklendiğinde üyelik otomatik Aktif'e çekilir (Trigger).")
        note.setStyleSheet(f"color: {COLORS['accent_warning']}; font-size: 11px; background: {COLORS['bg_input']}; border-radius: 6px; padding: 8px;")
        note.setWordWrap(True)
        layout.addWidget(note)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignRight)

        self.uyelik_combo = QComboBox()
        self.uyelik_combo.setMinimumHeight(38)
        for uy in self._uyelikler:
            self.uyelik_combo.addItem(
                f"#{uy.get('uyelik_id', '')} – {uy.get('uye_ad_soyad', '')} – {uy.get('paket_adi', '')}",
                uy.get("uyelik_id")
            )
        form.addRow("Üyelik *:", self.uyelik_combo)

        self.tutar = QDoubleSpinBox()
        self.tutar.setRange(0.01, 999999.99)
        self.tutar.setSuffix(" ₺")
        self.tutar.setDecimals(2)
        self.tutar.setMinimumHeight(38)
        form.addRow("Tutar *:", self.tutar)

        self.odeme_yontemi = QComboBox()
        self.odeme_yontemi.addItems(["Nakit", "Kart", "Havale/EFT"])
        self.odeme_yontemi.setMinimumHeight(38)
        form.addRow("Ödeme Yöntemi:", self.odeme_yontemi)

        self.odeme_durumu = QComboBox()
        self.odeme_durumu.addItems(["Başarılı", "Beklemede", "İptal"])
        self.odeme_durumu.setMinimumHeight(38)
        form.addRow("Ödeme Durumu:", self.odeme_durumu)

        self.aciklama = QTextEdit()
        self.aciklama.setPlaceholderText("Ödeme açıklaması...")
        self.aciklama.setMaximumHeight(70)
        form.addRow("Açıklama:", self.aciklama)

        layout.addLayout(form)
        _add_buttons(layout, self)

    def _fill_data(self, data):
        uyelik_id = int(data.get("uyelik_id", 0))
        for i in range(self.uyelik_combo.count()):
            if self.uyelik_combo.itemData(i) == uyelik_id:
                self.uyelik_combo.setCurrentIndex(i)
                break
        try:
            self.tutar.setValue(float(data.get("tutar", 0)))
        except Exception:
            pass
        idx = self.odeme_yontemi.findText(data.get("odeme_yontemi", "Nakit"))
        if idx >= 0:
            self.odeme_yontemi.setCurrentIndex(idx)
        idx = self.odeme_durumu.findText(data.get("odeme_durumu", "Başarılı"))
        if idx >= 0:
            self.odeme_durumu.setCurrentIndex(idx)
        self.aciklama.setPlainText(data.get("aciklama", "") or "")

    def get_values(self):
        return {
            "uyelik_id": self.uyelik_combo.currentData(),
            "tutar": self.tutar.value(),
            "odeme_yontemi": self.odeme_yontemi.currentText(),
            "odeme_durumu": self.odeme_durumu.currentText(),
            "aciklama": self.aciklama.toPlainText().strip() or None,
        }

    def validate(self):
        if self.uyelik_combo.count() == 0:
            return False, "Önce üyelik ekleyin."
        return True, ""


# =====================================================
# DERS DİYALOGU
# =====================================================

class DersDialog(QDialog):
    def __init__(self, parent=None, data=None, antrenorler=None):
        super().__init__(parent)
        self.setWindowTitle("Ders Ekle" if data is None else "Ders Düzenle")
        self.setMinimumWidth(520)
        self.setStyleSheet(MAIN_STYLE)
        self.setModal(True)
        self._data = data
        self._antrenorler = antrenorler or []
        self._setup_ui()
        if data:
            self._fill_data(data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("🏃  " + ("Yeni Ders" if not self._data else "Ders Düzenle"))
        title.setStyleSheet(f"font-size: 18px; font-weight: 800; color: {COLORS['accent_primary']};")
        layout.addWidget(title)

        line = QFrame(); line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"color: {COLORS['border']};")
        layout.addWidget(line)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignRight)

        self.ders_adi = QLineEdit(); self.ders_adi.setPlaceholderText("Ders adı"); self.ders_adi.setMinimumHeight(38)
        form.addRow("Ders Adı *:", self.ders_adi)

        self.antrenor_combo = QComboBox()
        self.antrenor_combo.setMinimumHeight(38)
        for a in self._antrenorler:
            self.antrenor_combo.addItem(
                f"{a.get('ad', '')} {a.get('soyad', '')} – {a.get('uzmanlik_alani', '')}",
                a.get("antrenor_id")
            )
        form.addRow("Antrenör *:", self.antrenor_combo)

        self.kontenjan = QSpinBox()
        self.kontenjan.setRange(1, 500)
        self.kontenjan.setValue(20)
        self.kontenjan.setSuffix(" kişi")
        self.kontenjan.setMinimumHeight(38)
        form.addRow("Kontenjan *:", self.kontenjan)

        self.ders_gunu = QComboBox()
        self.ders_gunu.addItems(["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"])
        self.ders_gunu.setMinimumHeight(38)
        form.addRow("Gün *:", self.ders_gunu)

        self.baslangic_saati = QTimeEdit()
        self.baslangic_saati.setTime(QTime(9, 0))
        self.baslangic_saati.setDisplayFormat("HH:mm")
        self.baslangic_saati.setMinimumHeight(38)
        form.addRow("Başlangıç Saati *:", self.baslangic_saati)

        self.bitis_saati = QTimeEdit()
        self.bitis_saati.setTime(QTime(10, 0))
        self.bitis_saati.setDisplayFormat("HH:mm")
        self.bitis_saati.setMinimumHeight(38)
        form.addRow("Bitiş Saati *:", self.bitis_saati)

        if self._data:
            self.aktif_mi = QCheckBox("Aktif")
            self.aktif_mi.setChecked(True)
            form.addRow("Durum:", self.aktif_mi)

        layout.addLayout(form)
        _add_buttons(layout, self)

    def _fill_data(self, data):
        self.ders_adi.setText(data.get("ders_adi", ""))
        antrenor_id = int(data.get("antrenor_id", 0))
        for i in range(self.antrenor_combo.count()):
            if self.antrenor_combo.itemData(i) == antrenor_id:
                self.antrenor_combo.setCurrentIndex(i)
                break
        try:
            self.kontenjan.setValue(int(data.get("kontenjan", 20)))
        except Exception:
            pass
        idx = self.ders_gunu.findText(data.get("ders_gunu", "Pazartesi"))
        if idx >= 0:
            self.ders_gunu.setCurrentIndex(idx)
        for attr, key in [("baslangic_saati", "baslangic_saati"), ("bitis_saati", "bitis_saati")]:
            t = data.get(key, "")
            if t:
                try:
                    parts = str(t).split(":")
                    h, m = int(parts[0]), int(parts[1])
                    getattr(self, attr).setTime(QTime(h, m))
                except Exception:
                    pass
        if hasattr(self, "aktif_mi"):
            self.aktif_mi.setChecked(bool(int(data.get("aktif_mi", 1))))

    def get_values(self):
        result = {
            "ders_adi": self.ders_adi.text().strip(),
            "antrenor_id": self.antrenor_combo.currentData(),
            "kontenjan": self.kontenjan.value(),
            "ders_gunu": self.ders_gunu.currentText(),
            "baslangic_saati": self.baslangic_saati.time().toString("HH:mm:ss"),
            "bitis_saati": self.bitis_saati.time().toString("HH:mm:ss"),
        }
        if self._data:
            result["aktif_mi"] = 1 if self.aktif_mi.isChecked() else 0
        return result

    def validate(self):
        if not self.ders_adi.text().strip():
            return False, "Ders adı boş bırakılamaz."
        if self.baslangic_saati.time() >= self.bitis_saati.time():
            return False, "Bitiş saati başlangıç saatinden sonra olmalıdır."
        if self.antrenor_combo.count() == 0:
            return False, "Önce antrenör ekleyin."
        return True, ""


# =====================================================
# DERS KAYIT DİYALOGU
# =====================================================

class DersKayitDialog(QDialog):
    def __init__(self, parent=None, data=None, uyeler=None, dersler=None):
        super().__init__(parent)
        self.setWindowTitle("Ders Kaydı Ekle" if data is None else "Ders Kaydı Düzenle")
        self.setMinimumWidth(500)
        self.setStyleSheet(MAIN_STYLE)
        self.setModal(True)
        self._data = data
        self._uyeler = uyeler or []
        self._dersler = dersler or []
        self._setup_ui()
        if data:
            self._fill_data(data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("📋  " + ("Yeni Ders Kaydı" if not self._data else "Ders Kaydı Düzenle"))
        title.setStyleSheet(f"font-size: 18px; font-weight: 800; color: {COLORS['accent_primary']};")
        layout.addWidget(title)

        note = QLabel("⚡ Kontenjan doluysa kayıt veritabanı trigger'ı tarafından engellenir.")
        note.setStyleSheet(f"color: {COLORS['accent_warning']}; font-size: 11px; background: {COLORS['bg_input']}; border-radius: 6px; padding: 8px;")
        layout.addWidget(note)

        line = QFrame(); line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"color: {COLORS['border']};")
        layout.addWidget(line)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignRight)

        self.uye_combo = QComboBox()
        self.uye_combo.setMinimumHeight(38)
        for uye in self._uyeler:
            self.uye_combo.addItem(
                f"{uye.get('ad', '')} {uye.get('soyad', '')} (ID: {uye.get('uye_id', '')})",
                uye.get("uye_id")
            )
        form.addRow("Üye *:", self.uye_combo)

        self.ders_combo = QComboBox()
        self.ders_combo.setMinimumHeight(38)
        for d in self._dersler:
            self.ders_combo.addItem(
                f"{d.get('ders_adi', '')} – {d.get('ders_gunu', '')} {str(d.get('baslangic_saati', ''))[:5]}",
                d.get("ders_id")
            )
        form.addRow("Ders *:", self.ders_combo)

        self.durum = QComboBox()
        self.durum.addItems(["Kayıtlı", "İptal", "Katıldı"])
        self.durum.setMinimumHeight(38)
        form.addRow("Durum:", self.durum)

        layout.addLayout(form)
        _add_buttons(layout, self)

    def _fill_data(self, data):
        uye_id = int(data.get("uye_id", 0))
        for i in range(self.uye_combo.count()):
            if self.uye_combo.itemData(i) == uye_id:
                self.uye_combo.setCurrentIndex(i)
                break
        ders_id = int(data.get("ders_id", 0))
        for i in range(self.ders_combo.count()):
            if self.ders_combo.itemData(i) == ders_id:
                self.ders_combo.setCurrentIndex(i)
                break
        idx = self.durum.findText(data.get("durum", "Kayıtlı"))
        if idx >= 0:
            self.durum.setCurrentIndex(idx)

    def get_values(self):
        return {
            "uye_id": self.uye_combo.currentData(),
            "ders_id": self.ders_combo.currentData(),
            "durum": self.durum.currentText(),
        }

    def validate(self):
        if self.uye_combo.count() == 0:
            return False, "Önce üye ekleyin."
        if self.ders_combo.count() == 0:
            return False, "Önce ders ekleyin."
        return True, ""


# =====================================================
# YOKLAMA DİYALOGU
# =====================================================

class YoklamaDialog(QDialog):
    def __init__(self, parent=None, data=None, ders_kayitlari=None):
        super().__init__(parent)
        self.setWindowTitle("Yoklama Ekle" if data is None else "Yoklama Düzenle")
        self.setMinimumWidth(500)
        self.setStyleSheet(MAIN_STYLE)
        self.setModal(True)
        self._data = data
        self._ders_kayitlari = ders_kayitlari or []
        self._setup_ui()
        if data:
            self._fill_data(data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("✅  " + ("Yeni Yoklama" if not self._data else "Yoklama Düzenle"))
        title.setStyleSheet(f"font-size: 18px; font-weight: 800; color: {COLORS['accent_primary']};")
        layout.addWidget(title)

        line = QFrame(); line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"color: {COLORS['border']};")
        layout.addWidget(line)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignRight)

        self.kayit_combo = QComboBox()
        self.kayit_combo.setMinimumHeight(38)
        for dk in self._ders_kayitlari:
            self.kayit_combo.addItem(
                f"#{dk.get('ders_kayit_id', '')} – {dk.get('uye_ad_soyad', '')} – {dk.get('ders_adi', '')}",
                dk.get("ders_kayit_id")
            )
        form.addRow("Ders Kaydı *:", self.kayit_combo)

        self.yoklama_tarihi = QDateEdit()
        self.yoklama_tarihi.setCalendarPopup(True)
        self.yoklama_tarihi.setDate(QDate.currentDate())
        self.yoklama_tarihi.setDisplayFormat("dd.MM.yyyy")
        self.yoklama_tarihi.setMinimumHeight(38)
        form.addRow("Tarih *:", self.yoklama_tarihi)

        self.katilim = QComboBox()
        self.katilim.addItems(["Katıldı", "Gelmedi", "Mazeretli"])
        self.katilim.setMinimumHeight(38)
        form.addRow("Katılım Durumu:", self.katilim)

        self.aciklama = QTextEdit()
        self.aciklama.setPlaceholderText("Açıklama...")
        self.aciklama.setMaximumHeight(70)
        form.addRow("Açıklama:", self.aciklama)

        layout.addLayout(form)
        _add_buttons(layout, self)

    def _fill_data(self, data):
        kayit_id = int(data.get("ders_kayit_id", 0))
        for i in range(self.kayit_combo.count()):
            if self.kayit_combo.itemData(i) == kayit_id:
                self.kayit_combo.setCurrentIndex(i)
                break
        dt = data.get("yoklama_tarihi", "")
        if dt:
            try:
                d = QDate.fromString(str(dt)[:10], "yyyy-MM-dd")
                self.yoklama_tarihi.setDate(d)
            except Exception:
                pass
        idx = self.katilim.findText(data.get("katilim_durumu", "Katıldı"))
        if idx >= 0:
            self.katilim.setCurrentIndex(idx)
        self.aciklama.setPlainText(data.get("aciklama", "") or "")

    def get_values(self):
        return {
            "ders_kayit_id": self.kayit_combo.currentData(),
            "yoklama_tarihi": self.yoklama_tarihi.date().toString("yyyy-MM-dd"),
            "katilim_durumu": self.katilim.currentText(),
            "aciklama": self.aciklama.toPlainText().strip() or None,
        }

    def validate(self):
        if self.kayit_combo.count() == 0:
            return False, "Önce ders kaydı ekleyin."
        return True, ""


# =====================================================
# EKİPMAN DİYALOGU
# =====================================================

class EkipmanDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Ekipman Ekle" if data is None else "Ekipman Düzenle")
        self.setMinimumWidth(480)
        self.setStyleSheet(MAIN_STYLE)
        self.setModal(True)
        self._data = data
        self._setup_ui()
        if data:
            self._fill_data(data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("🏋️  " + ("Yeni Ekipman" if not self._data else "Ekipman Düzenle"))
        title.setStyleSheet(f"font-size: 18px; font-weight: 800; color: {COLORS['accent_primary']};")
        layout.addWidget(title)

        line = QFrame(); line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"color: {COLORS['border']};")
        layout.addWidget(line)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignRight)

        self.ekipman_adi = QLineEdit(); self.ekipman_adi.setPlaceholderText("Ekipman adı (en az 2 karakter)"); self.ekipman_adi.setMinimumHeight(38)
        form.addRow("Ekipman Adı *:", self.ekipman_adi)

        self.kategori = QLineEdit(); self.kategori.setPlaceholderText("Kardiyo, Ağırlık, vs."); self.kategori.setMinimumHeight(38)
        form.addRow("Kategori *:", self.kategori)

        self.alim_tarihi = QDateEdit()
        self.alim_tarihi.setCalendarPopup(True)
        self.alim_tarihi.setDate(QDate.currentDate())
        self.alim_tarihi.setDisplayFormat("dd.MM.yyyy")
        self.alim_tarihi.setMinimumHeight(38)
        form.addRow("Alım Tarihi:", self.alim_tarihi)

        self.durum = QComboBox()
        self.durum.addItems(["Kullanılabilir", "Bakımda", "Arızalı"])
        self.durum.setMinimumHeight(38)
        form.addRow("Durum:", self.durum)

        self.aciklama = QTextEdit()
        self.aciklama.setPlaceholderText("Açıklama...")
        self.aciklama.setMaximumHeight(70)
        form.addRow("Açıklama:", self.aciklama)

        layout.addLayout(form)
        _add_buttons(layout, self)

    def _fill_data(self, data):
        self.ekipman_adi.setText(data.get("ekipman_adi", ""))
        self.kategori.setText(data.get("kategori", ""))
        dt = data.get("alim_tarihi", "")
        if dt:
            try:
                d = QDate.fromString(str(dt)[:10], "yyyy-MM-dd")
                self.alim_tarihi.setDate(d)
            except Exception:
                pass
        idx = self.durum.findText(data.get("durum", "Kullanılabilir"))
        if idx >= 0:
            self.durum.setCurrentIndex(idx)
        self.aciklama.setPlainText(data.get("aciklama", "") or "")

    def get_values(self):
        return {
            "ekipman_adi": self.ekipman_adi.text().strip(),
            "kategori": self.kategori.text().strip(),
            "alim_tarihi": self.alim_tarihi.date().toString("yyyy-MM-dd"),
            "durum": self.durum.currentText(),
            "aciklama": self.aciklama.toPlainText().strip() or None,
        }

    def validate(self):
        if len(self.ekipman_adi.text().strip()) < 2:
            return False, "Ekipman adı en az 2 karakter olmalıdır."
        if not self.kategori.text().strip():
            return False, "Kategori boş bırakılamaz."
        return True, ""


# =====================================================
# EKİPMAN BAKIM DİYALOGU
# =====================================================

class BakimDialog(QDialog):
    def __init__(self, parent=None, data=None, ekipmanlar=None):
        super().__init__(parent)
        self.setWindowTitle("Bakım Kaydı Ekle" if data is None else "Bakım Kaydı Düzenle")
        self.setMinimumWidth(500)
        self.setStyleSheet(MAIN_STYLE)
        self.setModal(True)
        self._data = data
        self._ekipmanlar = ekipmanlar or []
        self._setup_ui()
        if data:
            self._fill_data(data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("🔧  " + ("Yeni Bakım Kaydı" if not self._data else "Bakım Kaydı Düzenle"))
        title.setStyleSheet(f"font-size: 18px; font-weight: 800; color: {COLORS['accent_primary']};")
        layout.addWidget(title)

        line = QFrame(); line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"color: {COLORS['border']};")
        layout.addWidget(line)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignRight)

        self.ekipman_combo = QComboBox()
        self.ekipman_combo.setMinimumHeight(38)
        for e in self._ekipmanlar:
            self.ekipman_combo.addItem(
                f"{e.get('ekipman_adi', '')} – {e.get('kategori', '')}",
                e.get("ekipman_id")
            )
        form.addRow("Ekipman *:", self.ekipman_combo)

        self.bakim_tarihi = QDateEdit()
        self.bakim_tarihi.setCalendarPopup(True)
        self.bakim_tarihi.setDate(QDate.currentDate())
        self.bakim_tarihi.setDisplayFormat("dd.MM.yyyy")
        self.bakim_tarihi.setMinimumHeight(38)
        form.addRow("Bakım Tarihi *:", self.bakim_tarihi)

        self.aciklama_edit = QTextEdit()
        self.aciklama_edit.setPlaceholderText("Bakım açıklaması...")
        self.aciklama_edit.setMaximumHeight(80)
        form.addRow("Açıklama *:", self.aciklama_edit)

        self.maliyet = QDoubleSpinBox()
        self.maliyet.setRange(0, 999999.99)
        self.maliyet.setSuffix(" ₺")
        self.maliyet.setDecimals(2)
        self.maliyet.setMinimumHeight(38)
        form.addRow("Maliyet:", self.maliyet)

        self.bakim_durumu = QComboBox()
        self.bakim_durumu.addItems(["Planlandı", "Tamamlandı", "İptal"])
        self.bakim_durumu.setMinimumHeight(38)
        form.addRow("Durum:", self.bakim_durumu)

        layout.addLayout(form)
        _add_buttons(layout, self)

    def _fill_data(self, data):
        ekipman_id = int(data.get("ekipman_id", 0))
        for i in range(self.ekipman_combo.count()):
            if self.ekipman_combo.itemData(i) == ekipman_id:
                self.ekipman_combo.setCurrentIndex(i)
                break
        dt = data.get("bakim_tarihi", "")
        if dt:
            try:
                d = QDate.fromString(str(dt)[:10], "yyyy-MM-dd")
                self.bakim_tarihi.setDate(d)
            except Exception:
                pass
        self.aciklama_edit.setPlainText(data.get("aciklama", "") or "")
        try:
            self.maliyet.setValue(float(data.get("bakim_maliyeti", 0)))
        except Exception:
            pass
        idx = self.bakim_durumu.findText(data.get("bakim_durumu", "Planlandı"))
        if idx >= 0:
            self.bakim_durumu.setCurrentIndex(idx)

    def get_values(self):
        return {
            "ekipman_id": self.ekipman_combo.currentData(),
            "bakim_tarihi": self.bakim_tarihi.date().toString("yyyy-MM-dd"),
            "aciklama": self.aciklama_edit.toPlainText().strip(),
            "bakim_maliyeti": self.maliyet.value(),
            "bakim_durumu": self.bakim_durumu.currentText(),
        }

    def validate(self):
        if self.ekipman_combo.count() == 0:
            return False, "Önce ekipman ekleyin."
        if not self.aciklama_edit.toPlainText().strip():
            return False, "Açıklama boş bırakılamaz."
        return True, ""
