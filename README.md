# HTML to PDF Batch Converter

A PyQt5 desktop application for batch converting HTML files to PDF with high-fidelity rendering.

## Requirements

- Python 3.8+
- wkhtmltopdf (external binary)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install wkhtmltopdf:
   - macOS: `brew install wkhtmltopdf`
   - Windows: Download from https://wkhtmltopdf.org/downloads.html
   - Linux: `sudo apt-get install wkhtmltopdf`

## Usage

```bash
python src/main.py
```

## Features

- Batch convert multiple HTML files to PDF
- Select individual files or entire folders
- Real-time progress tracking
- High-fidelity conversion preserving CSS and images
- Error handling with detailed feedback
