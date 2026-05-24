# -*- coding: utf-8 -*-
"""Ortak UI bileşenleri"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame,
    QMessageBox, QLineEdit, QAbstractItemView
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor

from styles import COLORS

ROW_ID_ROLE = Qt.UserRole


def table_item(value, record_id=None, align=Qt.AlignVCenter | Qt.AlignLeft):
    """Tablo hücresi — sıralama sonrası doğru kayıt için ID saklar."""
    item = QTableWidgetItem(str(value) if value is not None else "")
    item.setTextAlignment(align)
    if record_id is not None:
        item.setData(ROW_ID_ROLE, record_id)
    return item


def get_selected_record(table, data_list, id_key):
    """Sıralama/filtre sonrası doğru satır kaydını döndürür."""
    row = table.currentRow()
    if row < 0:
        return None
    item = table.item(row, 0)
    if item is not None:
        rid = item.data(ROW_ID_ROLE)
        if rid is None:
            txt = item.text().strip()
            if txt.isdigit():
                rid = int(txt)
        if rid is not None:
            for rec in data_list:
                if rec.get(id_key) == rid:
                    return rec
    if row < len(data_list):
        return data_list[row]
    return None


class StatCard(QFrame):
    """Dashboard istatistik kartı."""

    def __init__(self, title, value, icon, color, parent=None):
        super().__init__(parent)
        self.setObjectName("statCard")
        self.setMinimumHeight(130)
        self.setMinimumWidth(180)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(10)

        top = QHBoxLayout()
        badge = QLabel(icon)
        badge.setStyleSheet(
            f"font-size: 26px; background: {color}22; border-radius: 10px;"
            f" padding: 8px 10px; min-width: 20px;"
        )
        badge.setAlignment(Qt.AlignCenter)
        top.addWidget(badge)
        top.addStretch()
        dot = QLabel("●")
        dot.setStyleSheet(f"color: {color}; font-size: 10px; background: transparent;")
        top.addWidget(dot)
        layout.addLayout(top)

        self._val_lbl = QLabel(str(value))
        self._val_lbl.setStyleSheet(
            f"font-size: 32px; font-weight: 800; color: {color}; background: transparent;"
        )
        layout.addWidget(self._val_lbl)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(
            f"font-size: 12px; color: {COLORS['text_secondary']}; font-weight: 600;"
            f" background: transparent; letter-spacing: 0.3px;"
        )
        title_lbl.setWordWrap(True)
        layout.addWidget(title_lbl)

        bar = QFrame()
        bar.setFixedHeight(4)
        bar.setStyleSheet(f"background: {color}; border-radius: 2px;")
        layout.addWidget(bar)

    def set_value(self, value):
        self._val_lbl.setText(str(value))


class BaseTableWidget(QTableWidget):
    """Gelişmiş tablo."""

    row_selected = pyqtSignal(int)

    def __init__(self, columns, parent=None):
        super().__init__(parent)
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(48)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.horizontalHeader().setMinimumSectionSize(80)
        self.setSortingEnabled(True)
        self.setShowGrid(False)
        self.itemSelectionChanged.connect(self._on_selection_changed)

    def _on_selection_changed(self):
        if self.selectedItems():
            self.row_selected.emit(self.currentRow())


class ActionBar(QFrame):
    """CRUD araç çubuğu."""

    def __init__(self, parent=None, show_search=True):
        super().__init__(parent)
        self.setObjectName("toolbarFrame")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(10)

        self.btn_add = QPushButton("  +  Yeni Ekle")
        self.btn_add.setObjectName("btnSuccess")
        self.btn_add.setFixedHeight(42)
        self.btn_add.setMinimumWidth(120)

        self.btn_edit = QPushButton("  Düzenle")
        self.btn_edit.setObjectName("btnWarning")
        self.btn_edit.setFixedHeight(42)

        self.btn_delete = QPushButton("  Sil")
        self.btn_delete.setObjectName("btnDanger")
        self.btn_delete.setFixedHeight(42)

        self.btn_refresh = QPushButton("  Yenile")
        self.btn_refresh.setObjectName("btnPrimary")
        self.btn_refresh.setFixedHeight(42)

        for b in (self.btn_add, self.btn_edit, self.btn_delete, self.btn_refresh):
            layout.addWidget(b)

        if show_search:
            layout.addStretch()
            self.search_input = QLineEdit()
            self.search_input.setPlaceholderText("🔍  Tabloda ara...")
            self.search_input.setFixedWidth(260)
            self.search_input.setFixedHeight(42)
            layout.addWidget(self.search_input)
        else:
            layout.addStretch()
            self.search_input = None


class SectionHeader(QFrame):
    """Sayfa başlığı."""

    def __init__(self, title, subtitle="", icon="", parent=None):
        super().__init__(parent)
        self.setObjectName("contentCard")
        outer = QHBoxLayout(self)
        outer.setContentsMargins(20, 18, 20, 18)
        outer.setSpacing(16)

        if icon:
            ic = QLabel(icon)
            ic.setStyleSheet(
                f"font-size: 28px; background: {COLORS['accent_primary']}25;"
                f" border-radius: 12px; padding: 10px;"
            )
            ic.setFixedSize(56, 56)
            ic.setAlignment(Qt.AlignCenter)
            outer.addWidget(ic)

        text = QVBoxLayout()
        text.setSpacing(4)
        t = QLabel(title)
        t.setStyleSheet(
            f"font-size: 20px; font-weight: 800; color: {COLORS['text_primary']};"
        )
        text.addWidget(t)
        if subtitle:
            s = QLabel(subtitle)
            s.setStyleSheet(f"font-size: 13px; color: {COLORS['text_secondary']};")
            s.setWordWrap(True)
            text.addWidget(s)
        outer.addLayout(text, 1)


def confirm_delete(parent, name="bu kaydı"):
    msg = QMessageBox(parent)
    msg.setWindowTitle("Silme Onayı")
    msg.setText(f"<b>{name}</b> silinsin mi?")
    msg.setInformativeText("Bağlı kayıtlar (üyelik, ders kaydı vb.) varsa birlikte silinir.")
    msg.setIcon(QMessageBox.Warning)
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msg.setDefaultButton(QMessageBox.No)
    msg.button(QMessageBox.Yes).setText("Evet, Sil")
    msg.button(QMessageBox.No).setText("İptal")
    return msg.exec_() == QMessageBox.Yes


def show_error(parent, message, title="Hata"):
    QMessageBox.critical(parent, title, message)


def show_success(parent, message, title="Başarılı"):
    QMessageBox.information(parent, title, message)


def filter_table(table: QTableWidget, search_text: str):
    text = search_text.lower().strip()
    for row in range(table.rowCount()):
        match = not text
        if text:
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item and text in item.text().lower():
                    match = True
                    break
        table.setRowHidden(row, not match)
