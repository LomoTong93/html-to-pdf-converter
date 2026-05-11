@echo off
echo ========================================
echo Building HTML to PDF Converter for Windows
echo ========================================

echo.
echo Step 1: Installing dependencies...
pip install -r requirements.txt
pip install -r requirements-build.txt

echo.
echo Step 2: Checking wkhtmltopdf...
if not exist "wkhtmltopdf-windows\bin\wkhtmltopdf.exe" (
    echo ERROR: wkhtmltopdf.exe not found!
    echo Please download wkhtmltopdf and place it in wkhtmltopdf-windows\bin\
    echo Download from: https://wkhtmltopdf.org/downloads.html
    pause
    exit /b 1
)

echo.
echo Step 3: Building executable...
pyinstaller HTMLtoPDF-windows.spec --clean --noconfirm

echo.
echo ========================================
echo Build completed!
echo ========================================
echo Executable: dist\HTMLtoPDF\HTMLtoPDF.exe
echo.
pause
