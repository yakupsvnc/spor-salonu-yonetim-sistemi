# -*- coding: utf-8 -*-
"""Modern koyu tema — Spor Salonu Yönetim Sistemi"""

COLORS = {
    "bg_darkest": "#06080f",
    "bg_dark": "#0c1018",
    "bg_sidebar": "#101622",
    "bg_card": "#151c2c",
    "bg_panel": "#1a2336",
    "bg_input": "#1e2940",
    "bg_elevated": "#222d45",
    "accent_primary": "#3b82f6",
    "accent_secondary": "#8b5cf6",
    "accent_cyan": "#22d3ee",
    "accent_success": "#22c55e",
    "accent_warning": "#fbbf24",
    "accent_danger": "#f87171",
    "accent_info": "#38bdf8",
    "text_primary": "#f1f5f9",
    "text_secondary": "#94a3b8",
    "text_muted": "#64748b",
    "border": "#2a3548",
    "border_light": "#3d4f6a",
    "hover": "#243049",
    "selected": "#1d4ed8",
    "glow": "#60a5fa",
}

MAIN_STYLE = f"""
QMainWindow, QDialog, QWidget {{
    background-color: {COLORS['bg_dark']};
    color: {COLORS['text_primary']};
    font-family: 'Segoe UI', 'Inter', Arial, sans-serif;
    font-size: 13px;
}}

QStackedWidget {{
    background-color: {COLORS['bg_dark']};
    border: none;
}}

/* Sidebar */
QListWidget#sidebarNav {{
    background-color: {COLORS['bg_sidebar']};
    border: none;
    border-right: 1px solid {COLORS['border']};
    outline: none;
    padding: 12px 8px;
}}

QListWidget#sidebarNav::item {{
    color: {COLORS['text_secondary']};
    border-radius: 10px;
    padding: 14px 16px;
    margin: 3px 4px;
    font-size: 13px;
    font-weight: 600;
}}

QListWidget#sidebarNav::item:hover {{
    background-color: {COLORS['hover']};
    color: {COLORS['text_primary']};
}}

QListWidget#sidebarNav::item:selected {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {COLORS['accent_primary']}, stop:1 {COLORS['accent_secondary']});
    color: white;
    border: 1px solid {COLORS['glow']}40;
}}

/* Buttons */
QPushButton {{
    background-color: {COLORS['bg_elevated']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 13px;
    min-height: 38px;
}}

QPushButton:hover {{
    background-color: {COLORS['hover']};
    border-color: {COLORS['border_light']};
}}

QPushButton:pressed {{
    background-color: {COLORS['bg_panel']};
}}

QPushButton#btnPrimary {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {COLORS['accent_primary']}, stop:1 {COLORS['accent_secondary']});
    color: white;
    border: none;
}}

QPushButton#btnPrimary:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #60a5fa, stop:1 #a78bfa);
    border: 1px solid {COLORS['glow']};
}}

QPushButton#btnDanger {{
    background-color: #7f1d1d40;
    color: {COLORS['accent_danger']};
    border: 1px solid #ef444450;
}}

QPushButton#btnDanger:hover {{
    background-color: #ef4444;
    color: white;
    border-color: #ef4444;
}}

QPushButton#btnSuccess {{
    background-color: #14532d50;
    color: {COLORS['accent_success']};
    border: 1px solid #22c55e50;
}}

QPushButton#btnSuccess:hover {{
    background-color: {COLORS['accent_success']};
    color: #052e16;
    border-color: {COLORS['accent_success']};
}}

QPushButton#btnWarning {{
    background-color: #78350f40;
    color: {COLORS['accent_warning']};
    border: 1px solid #fbbf2450;
}}

QPushButton#btnWarning:hover {{
    background-color: {COLORS['accent_warning']};
    color: #422006;
    border-color: {COLORS['accent_warning']};
}}

QPushButton#btnGhost {{
    background: transparent;
    border: 1px solid {COLORS['border']};
    color: {COLORS['text_secondary']};
}}

QPushButton#btnGhost:hover {{
    color: {COLORS['accent_danger']};
    border-color: {COLORS['accent_danger']};
    background: #7f1d1d30;
}}

/* Inputs */
QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit, QComboBox {{
    background-color: {COLORS['bg_input']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 13px;
    selection-background-color: {COLORS['accent_primary']};
}}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus,
QDateEdit:focus, QTimeEdit:focus, QComboBox:focus {{
    border: 2px solid {COLORS['accent_primary']};
    background-color: {COLORS['bg_panel']};
}}

QComboBox::drop-down {{ border: none; width: 28px; }}
QComboBox QAbstractItemView {{
    background-color: {COLORS['bg_panel']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    color: {COLORS['text_primary']};
    selection-background-color: {COLORS['accent_primary']};
    padding: 6px;
}}

/* Table */
QTableWidget {{
    background-color: {COLORS['bg_card']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 12px;
    gridline-color: {COLORS['border']}80;
    selection-background-color: {COLORS['selected']};
    alternate-background-color: {COLORS['bg_panel']};
}}

QTableWidget::item {{
    padding: 12px 14px;
    border: none;
}}

QTableWidget::item:selected {{
    background-color: {COLORS['selected']};
    color: white;
}}

QTableWidget::item:hover {{
    background-color: {COLORS['hover']};
}}

QHeaderView::section {{
    background-color: {COLORS['bg_elevated']};
    color: {COLORS['accent_cyan']};
    border: none;
    border-bottom: 2px solid {COLORS['accent_primary']};
    border-right: 1px solid {COLORS['border']};
    padding: 12px 14px;
    font-weight: 700;
    font-size: 11px;
    letter-spacing: 0.8px;
}}

QScrollBar:vertical {{
    background: transparent;
    width: 10px;
    margin: 4px;
}}
QScrollBar::handle:vertical {{
    background: {COLORS['border_light']};
    border-radius: 5px;
    min-height: 40px;
}}
QScrollBar::handle:vertical:hover {{
    background: {COLORS['accent_primary']};
}}
QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; }}

QLabel {{ color: {COLORS['text_primary']}; background: transparent; }}

QGroupBox {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 12px;
    margin-top: 14px;
    padding: 14px;
    font-weight: 600;
    color: {COLORS['accent_primary']};
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 14px;
    padding: 0 8px;
}}

QCheckBox {{ color: {COLORS['text_primary']}; spacing: 8px; }}
QCheckBox::indicator {{
    width: 18px; height: 18px;
    border: 2px solid {COLORS['border']};
    border-radius: 5px;
    background: {COLORS['bg_input']};
}}
QCheckBox::indicator:checked {{
    background: {COLORS['accent_primary']};
    border-color: {COLORS['accent_primary']};
}}

QStatusBar {{
    background-color: {COLORS['bg_darkest']};
    color: {COLORS['text_muted']};
    border-top: 1px solid {COLORS['border']};
    padding: 6px 16px;
    font-size: 12px;
}}

QFrame#topBar {{
    background-color: {COLORS['bg_sidebar']};
    border-bottom: 1px solid {COLORS['border']};
}}

QFrame#contentCard {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 14px;
}}

QFrame#toolbarFrame {{
    background-color: {COLORS['bg_panel']};
    border: 1px solid {COLORS['border']};
    border-radius: 12px;
}}

QFrame#statCard {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 14px;
}}
QFrame#statCard:hover {{
    border-color: {COLORS['accent_primary']};
}}
"""

LOGIN_STYLE = f"""
QWidget {{
    background-color: {COLORS['bg_darkest']};
    color: {COLORS['text_primary']};
    font-family: 'Segoe UI', Arial, sans-serif;
}}

QLineEdit {{
    background-color: {COLORS['bg_input']};
    color: {COLORS['text_primary']};
    border: 2px solid {COLORS['border']};
    border-radius: 12px;
    padding: 14px 18px;
    font-size: 14px;
}}

QLineEdit:focus {{
    border-color: {COLORS['accent_primary']};
    background-color: {COLORS['bg_panel']};
}}

QPushButton#btnLogin {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {COLORS['accent_primary']}, stop:0.5 {COLORS['accent_cyan']}, stop:1 {COLORS['accent_secondary']});
    color: white;
    border: 2px solid transparent;
    border-radius: 14px;
    padding: 16px 24px;
    font-size: 16px;
    font-weight: 800;
    letter-spacing: 1px;
    min-height: 52px;
}}

QPushButton#btnLogin:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #60a5fa, stop:0.5 #67e8f9, stop:1 #c4b5fd);
    border: 2px solid {COLORS['glow']};
    color: white;
}}

QPushButton#btnLogin:pressed {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #2563eb, stop:1 #6d28d9);
    border-color: {COLORS['accent_primary']};
    padding-top: 18px;
    padding-bottom: 14px;
}}

QPushButton#btnDbToggle {{
    background: transparent;
    color: {COLORS['text_muted']};
    border: 1px dashed {COLORS['border']};
    border-radius: 10px;
    padding: 10px;
    font-size: 12px;
    min-height: 36px;
}}

QPushButton#btnDbToggle:hover {{
    color: {COLORS['accent_cyan']};
    border-color: {COLORS['accent_cyan']};
    background: {COLORS['bg_panel']};
}}

QLabel#labelBrand {{
    font-size: 32px;
    font-weight: 900;
    color: white;
    letter-spacing: 3px;
}}

QLabel#labelTagline {{ font-size: 14px; color: {COLORS['text_secondary']}; }}
QLabel#labelError {{ color: {COLORS['accent_danger']}; font-size: 12px; font-weight: 600; }}

QFrame#loginCard {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 20px;
}}

QFrame#loginCard:hover {{
    border-color: {COLORS['border_light']};
}}
"""
