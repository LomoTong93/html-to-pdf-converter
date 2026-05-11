# HTML to PDF Batch Converter

A PyQt5 desktop application for batch converting HTML files to PDF with high-fidelity rendering using wkhtmltopdf.

## Features

- ✅ Batch convert multiple HTML files to PDF
- ✅ Select individual files or scan entire folders
- ✅ Real-time progress tracking with detailed status
- ✅ High-fidelity conversion preserving CSS, images, and layouts
- ✅ Comprehensive error handling with user-friendly messages
- ✅ Settings persistence (remembers output directory)
- ✅ Stop conversion mid-process
- ✅ Cross-platform support (macOS, Windows, Linux)

## Requirements

- Python 3.8 or higher
- wkhtmltopdf (external binary)

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install wkhtmltopdf

**macOS:**
```bash
brew install wkhtmltopdf
```

**Windows:**
Download installer from https://wkhtmltopdf.org/downloads.html

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install wkhtmltopdf
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install wkhtmltopdf
```

## Usage

### Running the Application

```bash
python src/main.py
```

### Basic Workflow

1. **Select Files:**
   - Click "选择HTML文件" to select individual files
   - Or click "选择文件夹" to scan a directory for HTML files

2. **Choose Output Directory:**
   - Click "选择输出目录" to specify where PDFs will be saved

3. **Start Conversion:**
   - Click "开始转换" to begin batch conversion
   - Monitor progress in real-time

4. **View Results:**
   - Check status log for success/failure details
   - Click "打开输出目录" when complete

### Features

- **Progress Tracking:** Real-time progress bar and current file indicator
- **Status Log:** Color-coded success (green) and failure (red) messages
- **Stop Conversion:** Click "停止转换" to gracefully interrupt
- **Settings Persistence:** Output directory is remembered between sessions

## Project Structure

```
html-pdf/
├── src/
│   ├── main.py                 # Application entry point
│   ├── ui/
│   │   ├── main_window.py      # Main window UI
│   │   └── dialogs.py          # Custom dialogs
│   ├── core/
│   │   ├── converter.py        # Conversion engine
│   │   └── worker.py           # Background worker thread
│   └── utils/
│       ├── file_utils.py       # File utilities
│       └── config.py           # Settings management
├── tests/
│   ├── test_converter.py       # Converter tests
│   ├── test_file_utils.py      # File utils tests
│   └── fixtures/               # Test HTML files
├── requirements.txt
└── README.md
```

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Code Style

This project follows PEP 8 style guidelines.

## Troubleshooting

### wkhtmltopdf Not Found

If the application shows "wkhtmltopdf 未找到":
1. Verify wkhtmltopdf is installed: `wkhtmltopdf --version`
2. If installed but not detected, use "指定路径" in the dialog
3. Restart the application after installation

### Conversion Fails

Common issues:
- **File not found:** Ensure HTML file exists and is readable
- **Permission denied:** Check output directory write permissions
- **Timeout:** Large files may exceed 60-second timeout
- **Invalid HTML:** Malformed HTML may cause conversion errors

### Chinese Characters Not Displaying

Ensure your system has Chinese fonts installed:
- macOS: Built-in support
- Windows: Built-in support
- Linux: Install `fonts-wqy-zenhei` or similar

## License

MIT License

## Contributing

Contributions welcome! Please open an issue or submit a pull request.
