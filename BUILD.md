# Build Instructions

## Building Standalone Executable

This project can be packaged into a standalone application that includes wkhtmltopdf.

### Prerequisites

```bash
pip install -r requirements-build.txt
```

### Build on macOS

```bash
./build.sh
```

This will create:
- `dist/HTMLtoPDF.app` - macOS application bundle

To create a DMG installer:
```bash
hdiutil create -volname HTMLtoPDF -srcfolder dist/HTMLtoPDF.app -ov -format UDZO dist/HTMLtoPDF.dmg
```

### Build on Windows

```bash
pip install -r requirements-build.txt
pyinstaller HTMLtoPDF.spec
```

This will create:
- `dist/HTMLtoPDF.exe` - Windows executable

**Note for Windows:** Update `HTMLtoPDF.spec` to point to your wkhtmltopdf installation path.

### Build on Linux

```bash
pip install -r requirements-build.txt
pyinstaller HTMLtoPDF.spec
```

This will create:
- `dist/HTMLtoPDF` - Linux executable

## Distribution

The built application includes:
- All Python dependencies
- PyQt5 libraries
- wkhtmltopdf binary (embedded)

Users can run the application without installing Python or wkhtmltopdf separately.
