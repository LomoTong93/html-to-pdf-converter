#!/bin/bash

# Build script for HTML to PDF Converter

echo "=== HTML to PDF Converter - Build Script ==="
echo ""

# Check if pyinstaller is installed
if ! python -c "import PyInstaller" 2>/dev/null; then
    echo "Installing PyInstaller..."
    pip install -r requirements-build.txt
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist

# Build the application
echo "Building application..."
pyinstaller HTMLtoPDF.spec

# Check if build was successful
if [ -d "dist/HTMLtoPDF.app" ]; then
    echo ""
    echo "=== Build Successful! ==="
    echo ""
    echo "macOS App Bundle: dist/HTMLtoPDF.app"
    echo ""
    echo "To run the app:"
    echo "  open dist/HTMLtoPDF.app"
    echo ""
    echo "To create a DMG installer:"
    echo "  hdiutil create -volname HTMLtoPDF -srcfolder dist/HTMLtoPDF.app -ov -format UDZO dist/HTMLtoPDF.dmg"
else
    echo ""
    echo "=== Build Failed ==="
    echo "Check the output above for errors"
    exit 1
fi
