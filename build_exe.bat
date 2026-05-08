@echo off
setlocal
title WARP Configurator - EXE Build
echo.
echo  ================================
echo   WARP Configurator - EXE Build
echo  ================================
echo.

:: Python kontrolü
python --version >nul 2>&1
if errorlevel 1 (
    echo [HATA] Python bulunamadi. python.org adresinden yukleyin.
    pause & exit /b 1
)

:: Bağımlılıkları yükle
echo [1/3] Bagimliliklar yukleniyor...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [HATA] Bagimliliklar yuklenemedi.
    pause & exit /b 1
)

:: PyInstaller yoksa yükle
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo       PyInstaller yukleniyor...
    pip install pyinstaller --quiet
)

:: Önceki build'i temizle
if exist "dist\WARP Configurator.exe" del /f /q "dist\WARP Configurator.exe"
if exist "build" rmdir /s /q "build"

echo [2/3] EXE derleniyor... (1-2 dakika surebilir)
python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name "WARP Configurator" ^
    --icon "icon.ico" ^
    --add-data "logo_full.png;." ^
    --add-data "icon.ico;." ^
    --clean ^
    main.py >nul 2>&1

if errorlevel 1 (
    echo.
    echo [HATA] Build basarisiz. Detay icin:
    python -m PyInstaller --onefile --windowed --name "WARP Configurator" main.py
    pause & exit /b 1
)

echo [3/3] Temizlik yapiliyor...
if exist "build" rmdir /s /q "build"
if exist "WARP Configurator.spec" del /f /q "WARP Configurator.spec"

echo.
echo  ================================
echo   BASARILI!
echo   dist\WARP Configurator.exe
echo  ================================
echo.
explorer dist
pause
