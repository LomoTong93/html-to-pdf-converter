# HTML to PDF Batch Converter - Design Specification

**Date:** 2026-05-11  
**Purpose:** Personal tool for batch converting HTML files to PDF with high-fidelity rendering  
**Target Platform:** Desktop application (cross-platform)

## Overview

A PyQt5-based desktop application that allows users to batch convert HTML files to PDF format using wkhtmltopdf as the conversion engine. The tool provides a graphical interface for selecting files, monitoring conversion progress, and managing output.

## Use Case

- **Primary User:** Individual user needing occasional batch HTML-to-PDF conversion
- **Typical Workflow:** Select multiple HTML files or a folder, choose output directory, start conversion, monitor progress
- **Quality Requirement:** High-fidelity conversion preserving CSS styles, layouts, and images

## Technical Stack

- **Language:** Python 3.8+
- **GUI Framework:** PyQt5
- **Conversion Engine:** wkhtmltopdf (external binary)
- **File Handling:** pathlib
- **Threading:** QThread for background processing

## Architecture

### Component Structure

The application follows MVC architecture with three main components:

1. **MainWindow (View)**
   - PyQt5 QMainWindow subclass
   - Handles all user interface elements and user interactions
   - Connects to controller signals for updates

2. **ConverterEngine (Model)**
   - Encapsulates wkhtmltopdf interaction
   - Manages conversion parameters and execution
   - Provides single-file conversion interface

3. **ConverterController (Controller)**
   - Coordinates between UI and conversion engine
   - Manages conversion workflow and state
   - Handles file collection and validation

4. **ConverterThread (Worker)**
   - QThread subclass for background processing
   - Executes batch conversion without blocking UI
   - Emits signals for progress updates

### Data Flow

```
User Input → MainWindow → ConverterController → ConverterThread
                                                      ↓
                                                ConverterEngine
                                                      ↓
                                                  wkhtmltopdf
                                                      ↓
                                            Progress Signals
                                                      ↓
                                                 MainWindow
```

## User Interface Design

### Main Window Layout

**Window Properties:**
- Title: "HTML to PDF Converter"
- Fixed size: 800x600 pixels
- Centered on screen
- Application icon

**Layout Sections (Top to Bottom):**

1. **File Selection Area**
   - "选择HTML文件" button - Opens multi-file dialog
   - "选择文件夹" button - Opens folder dialog, scans for .html files
   - File list widget (scrollable) - Displays selected HTML file paths
   - "清空列表" button - Clears current selection

2. **Output Settings Area**
   - "选择输出目录" button - Opens directory dialog
   - Output path label - Shows selected output directory path

3. **Conversion Control Area**
   - "开始转换" button - Starts batch conversion (disabled when list empty or no output dir)
   - "停止转换" button - Interrupts ongoing conversion (enabled only during conversion)

4. **Progress Display Area**
   - Progress bar - Shows overall completion percentage
   - Current file label - Shows "正在转换: filename.html (3/10)"
   - Status text box (scrollable) - Shows per-file results with color coding:
     - Green text for successful conversions
     - Red text for failures with error messages

### User Interactions

- File selection supports both individual files and folder scanning
- Drag-and-drop support for removing individual files from list
- Double-click on status text to copy error messages
- "打开输出目录" button appears after conversion completes

## Conversion Engine

### ConverterEngine Class

**Responsibilities:**
1. Detect and validate wkhtmltopdf installation
2. Configure conversion parameters
3. Execute single-file conversions
4. Handle conversion errors

**wkhtmltopdf Detection:**
- Check common installation paths on startup
- If not found, display installation guide dialog
- Support custom path configuration via settings

**Conversion Parameters:**
- Page size: A4
- Margins: 10mm (all sides)
- Encoding: UTF-8
- Enable local file access: `--enable-local-file-access`
- Image quality: 94
- JavaScript delay: 200ms
- Disable smart shrinking: `--disable-smart-shrinking`

**Conversion Method:**
```python
def convert_single(html_path: Path, output_path: Path) -> tuple[bool, str]:
    """
    Convert single HTML file to PDF.
    
    Returns:
        (success: bool, message: str)
    """
```

**Implementation:**
- Use subprocess.run() to call wkhtmltopdf
- Capture stdout/stderr for error diagnosis
- Set timeout (e.g., 60 seconds per file)
- Return success status and descriptive message

**Output File Naming:**
- Preserve original filename, change extension to .pdf
- Example: `report.html` → `report.pdf`
- If output file exists, overwrite by default

### Error Handling

**Pre-conversion Validation:**
- HTML file exists and is readable
- Output directory exists and is writable
- wkhtmltopdf is available

**Conversion Errors:**
- File not found
- Permission denied
- wkhtmltopdf execution failure
- Timeout exceeded
- Invalid HTML structure

**Error Messages:**
- User-friendly descriptions in Chinese
- Technical details available in logs
- Suggest corrective actions when possible

## Threading and Concurrency

### Why Threading

wkhtmltopdf conversion is a blocking I/O operation. Running conversions in the main thread would freeze the UI, preventing progress updates and user interaction.

### ConverterThread Design

**Class:** `ConverterThread(QThread)`

**Input:**
- List of HTML file paths
- Output directory path
- Reference to ConverterEngine instance

**Signals:**
```python
progress_updated = pyqtSignal(int, int, str)  # current, total, filename
file_completed = pyqtSignal(str, bool, str)   # filename, success, message
all_completed = pyqtSignal(int, int)          # success_count, fail_count
conversion_stopped = pyqtSignal()             # user interrupted
```

**Execution Flow:**
1. Iterate through HTML file list
2. For each file:
   - Check stop flag
   - Call ConverterEngine.convert_single()
   - Emit file_completed signal
   - Emit progress_updated signal
3. Emit all_completed signal
4. Thread terminates

**Stop Mechanism:**
- Thread checks `self._stop_flag` before each conversion
- Controller sets flag when user clicks "停止转换"
- Thread exits gracefully after current file completes

### UI Thread Safety

**Signal-Slot Connections:**
- All UI updates triggered by signals from worker thread
- Qt automatically handles cross-thread signal delivery
- No direct UI manipulation from worker thread

**Button State Management:**
- Disable file selection during conversion
- Enable "停止转换" only during active conversion
- Re-enable controls after completion or stop

## Error Handling and User Experience

### Startup Checks

**wkhtmltopdf Detection:**
- Check system PATH for wkhtmltopdf binary
- Check common installation locations:
  - macOS: `/usr/local/bin/wkhtmltopdf`
  - Windows: `C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe`
  - Linux: `/usr/bin/wkhtmltopdf`

**Installation Guide Dialog:**
If wkhtmltopdf not found, show dialog with:
- Explanation of requirement
- Download link: https://wkhtmltopdf.org/downloads.html
- Option to specify custom path
- "重新检测" button to retry detection

### Pre-conversion Validation

**File List Validation:**
- At least one HTML file selected
- All files exist and are readable
- Show warning for non-existent files, offer to remove them

**Output Directory Validation:**
- Directory selected
- Directory exists and is writable
- Show error dialog if validation fails

### Conversion Error Handling

**Per-file Error Strategy:**
- Single file failure does not stop batch process
- Continue to next file after logging error
- Accumulate success/failure counts

**Error Display:**
- Status text box shows real-time results
- Format: `[✓] filename.html → filename.pdf`
- Format: `[✗] filename.html - 错误: <message>`
- Auto-scroll to latest entry

### User Experience Enhancements

**Settings Persistence (QSettings):**
- Remember last output directory
- Remember window position
- Remember custom wkhtmltopdf path

**Completion Summary:**
- Show modal dialog after batch completes
- Display: "转换完成！成功: X个，失败: Y个"
- Provide "打开输出目录" button
- Provide "查看详细日志" button

**Optional Features:**
- Recursive folder scanning (checkbox option)
- File list drag-and-drop reordering
- Export status log to text file
- Dark mode support

## Testing Strategy

### Unit Tests

**ConverterEngine:**
- Test wkhtmltopdf detection
- Test parameter generation
- Test error handling for missing files
- Mock subprocess calls

**File Collection:**
- Test folder scanning
- Test file filtering (.html only)
- Test recursive scanning
- Test handling of symlinks

### Integration Tests

**End-to-End Scenarios:**
1. Convert single HTML file
2. Convert multiple files from selection
3. Convert all files in folder
4. Handle conversion failure gracefully
5. Stop conversion mid-process

**Edge Cases:**
- Empty HTML file
- HTML with Chinese characters in path
- HTML with external CSS/images
- Large HTML file (>10MB)
- Output directory with limited permissions
- Disk space exhaustion

### Manual Testing Checklist

- [ ] UI renders correctly on different screen sizes
- [ ] Progress updates smoothly during conversion
- [ ] Stop button interrupts conversion
- [ ] Settings persist across application restarts
- [ ] Error messages are clear and actionable
- [ ] Application handles wkhtmltopdf not installed
- [ ] Conversion quality matches browser rendering

## Project Structure

```
html-pdf/
├── src/
│   ├── main.py                 # Application entry point
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py      # MainWindow class
│   │   └── dialogs.py          # Custom dialogs
│   ├── core/
│   │   ├── __init__.py
│   │   ├── converter.py        # ConverterEngine class
│   │   ├── controller.py       # ConverterController class
│   │   └── worker.py           # ConverterThread class
│   └── utils/
│       ├── __init__.py
│       ├── file_utils.py       # File scanning utilities
│       └── config.py           # Settings management
├── tests/
│   ├── test_converter.py
│   ├── test_file_utils.py
│   └── fixtures/               # Test HTML files
├── resources/
│   ├── icon.png                # Application icon
│   └── styles.qss              # Qt stylesheet (optional)
├── docs/
│   └── superpowers/
│       └── specs/
│           └── 2026-05-11-html-to-pdf-converter-design.md
├── requirements.txt
├── README.md
└── .gitignore
```

## Dependencies

**Core:**
- PyQt5 >= 5.15.0
- Python >= 3.8

**External:**
- wkhtmltopdf (binary, not Python package)

**Development:**
- pytest (testing)
- black (code formatting)
- mypy (type checking)

## Installation and Deployment

**For Development:**
```bash
pip install -r requirements.txt
python src/main.py
```

**For Distribution:**
- Use PyInstaller to create standalone executable
- Bundle wkhtmltopdf binary with application
- Create installer for target platforms (macOS .dmg, Windows .exe)

## Future Enhancements

Potential features for future versions:
- Batch conversion presets (different page sizes, margins)
- PDF metadata editing (title, author, keywords)
- Watermark support
- Page numbering options
- Parallel conversion (multiple wkhtmltopdf processes)
- Cloud storage integration (Google Drive, Dropbox)
- Command-line interface for automation
- Conversion history and favorites

## Success Criteria

The application is considered successful if:
1. Converts HTML to PDF with high visual fidelity
2. Handles batch operations efficiently (10+ files)
3. Provides clear progress feedback
4. Recovers gracefully from errors
5. Maintains responsive UI during conversion
6. Persists user preferences
7. Works reliably on macOS, Windows, and Linux
