#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spor Salonu Yönetim Sistemi - Ana Giriş Noktası
"""

import os
import sys

# Proje klasörünü çalışma dizini yap (Cursor/terminal nereden açılırsa açılsın)
APP_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(APP_DIR)
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

# ÖNEMLİ: mysql.connector Qt'tan ÖNCE import edilmeli
import mysql.connector

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from login_window import LoginWindow


def main():
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("Spor Salonu Yönetim Sistemi")
        app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

        login = LoginWindow()
        login.show()

        login.raise_()
        login.activateWindow()
        QTimer.singleShot(200, login.raise_)
        QTimer.singleShot(200, login.activateWindow)

        sys.exit(app.exec_())
    except Exception as e:
        print("\n[HATA] Uygulama baslatilamadi:")
        print(e)
        import traceback
        traceback.print_exc()
        try:
            app = QApplication.instance() or QApplication(sys.argv)
            QMessageBox.critical(
                None, "Baslatma Hatasi",
                f"Uygulama acilamadi:\n\n{e}\n\n"
                "Terminalde tam hata mesajina bakin."
            )
        except Exception:
            pass
        input("\nKapatmak icin Enter'a basin...")
        sys.exit(1)


if __name__ == "__main__":
    main()
