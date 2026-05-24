@echo off
chcp 65001 > nul
title Spor Salonu Yonetim Sistemi

echo ============================================
echo   SPOR SALONU YONETIM SISTEMI
echo   PyQt5 + MySQL Stored Procedure
echo ============================================
echo.

:: Python kurulu mu kontrol et
python --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [HATA] Python bulunamadi!
    echo Lutfen Python 3.8+ yukleyin: https://www.python.org
    pause
    exit /b 1
)

:: Gerekli paketler kurulu mu kontrol et
python -c "import PyQt5; import mysql.connector" > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [BILGI] Gerekli paketler yukleniyor...
    pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo [HATA] Paketler yuklenemedi!
        pause
        exit /b 1
    )
)

:: config.py yoksa ornekten olustur
if not exist config.py (
    echo [BILGI] config.py olusturuluyor...
    copy config_example.py config.py > nul
    echo Lutfen config.py icinde MySQL sifrenizi girin.
    echo.
)

echo [OK] Uygulama baslatiliyor...
echo.
python main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [HATA] Uygulama kapandi. Hata kodu: %ERRORLEVEL%
    echo Lutfen README.md dosyasini okuyun.
    pause
)
