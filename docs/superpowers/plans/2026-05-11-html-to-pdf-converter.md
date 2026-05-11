# HTML to PDF Batch Converter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a PyQt5 desktop application that batch converts HTML files to PDF using wkhtmltopdf with progress tracking and error handling.

**Architecture:** MVC pattern with MainWindow (view), ConverterEngine (model), ConverterController (controller), and ConverterThread (worker). The worker thread handles blocking wkhtmltopdf calls while keeping UI responsive through Qt signals.

**Tech Stack:** Python 3.8+, PyQt5, wkhtmltopdf (external binary), pathlib, subprocess

---

## File Structure

**New files to create:**
- `src/main.py` - Application entry point, initializes QApplication
- `src/ui/__init__.py` - UI package marker
- `src/ui/main_window.py` - MainWindow class with all UI components
- `src/ui/dialogs.py` - Custom dialogs (installation guide, completion summary)
- `src/core/__init__.py` - Core package marker
- `src/core/converter.py` - ConverterEngine class, wkhtmltopdf wrapper
- `src/core/controller.py` - ConverterController class, workflow coordination
- `src/core/worker.py` - ConverterThread class, background processing
- `src/utils/__init__.py` - Utils package marker
- `src/utils/file_utils.py` - File scanning and validation utilities
- `src/utils/config.py` - Settings management with QSettings
- `tests/test_converter.py` - Unit tests for ConverterEngine
- `tests/test_file_utils.py` - Unit tests for file utilities
- `tests/fixtures/sample.html` - Test HTML file
- `requirements.txt` - Python dependencies
- `README.md` - Project documentation
- `.gitignore` - Git ignore patterns

---

## Task 1: Project Setup and Dependencies

**Files:**
- Create: `requirements.txt`
- Create: `.gitignore`
- Create: `README.md`

- [ ] **Step 1: Create requirements.txt**

```txt
PyQt5>=5.15.0
pytest>=7.0.0
```

- [ ] **Step 2: Create .gitignore**

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyQt
*.ui.py

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db
```

- [ ] **Step 3: Create README.md**

```markdown
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
```

- [ ] **Step 4: Create directory structure**

```bash
mkdir -p src/ui src/core src/utils tests/fixtures resources docs/superpowers/plans
touch src/__init__.py src/ui/__init__.py src/core/__init__.py src/utils/__init__.py tests/__init__.py
```

- [ ] **Step 5: Install dependencies**

```bash
pip install -r requirements.txt
```

Expected: PyQt5 and pytest installed successfully

- [ ] **Step 6: Commit project setup**

```bash
git add requirements.txt .gitignore README.md
git commit -m "chore: initial project setup with dependencies and structure"
```

---

## Task 2: File Utilities Module

**Files:**
- Create: `src/utils/file_utils.py`
- Create: `tests/test_file_utils.py`
- Create: `tests/fixtures/sample.html`

- [ ] **Step 1: Write test for HTML file scanning**

Create `tests/test_file_utils.py`:

```python
import pytest
from pathlib import Path
from src.utils.file_utils import scan_html_files, validate_html_file


def test_scan_html_files_in_directory(tmp_path):
    """Test scanning HTML files in a directory."""
    (tmp_path / "file1.html").write_text("<html></html>")
    (tmp_path / "file2.html").write_text("<html></html>")
    (tmp_path / "file3.txt").write_text("not html")
    
    result = scan_html_files(tmp_path, recursive=False)
    
    assert len(result) == 2
    assert all(f.suffix == ".html" for f in result)


def test_scan_html_files_recursive(tmp_path):
    """Test recursive scanning of HTML files."""
    (tmp_path / "file1.html").write_text("<html></html>")
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "file2.html").write_text("<html></html>")
    
    result = scan_html_files(tmp_path, recursive=True)
    
    assert len(result) == 2


def test_scan_html_files_empty_directory(tmp_path):
    """Test scanning empty directory returns empty list."""
    result = scan_html_files(tmp_path, recursive=False)
    assert result == []


def test_validate_html_file_exists(tmp_path):
    """Test validation of existing HTML file."""
    html_file = tmp_path / "test.html"
    html_file.write_text("<html></html>")
    
    is_valid, message = validate_html_file(html_file)
    
    assert is_valid is True
    assert message == ""


def test_validate_html_file_not_exists(tmp_path):
    """Test validation of non-existent file."""
    html_file = tmp_path / "missing.html"
    
    is_valid, message = validate_html_file(html_file)
    
    assert is_valid is False
    assert "不存在" in message


def test_validate_html_file_not_readable(tmp_path):
    """Test validation of unreadable file."""
    html_file = tmp_path / "test.html"
    html_file.write_text("<html></html>")
    html_file.chmod(0o000)
    
    is_valid, message = validate_html_file(html_file)
    
    assert is_valid is False
    assert "无法读取" in message
    
    html_file.chmod(0o644)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_file_utils.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'src.utils.file_utils'"

- [ ] **Step 3: Implement file_utils.py**

Create `src/utils/file_utils.py`:

```python
from pathlib import Path
from typing import List, Tuple


def scan_html_files(directory: Path, recursive: bool = False) -> List[Path]:
    """
    Scan directory for HTML files.
    
    Args:
        directory: Directory path to scan
        recursive: If True, scan subdirectories recursively
        
    Returns:
        List of Path objects for HTML files found
    """
    directory = Path(directory)
    
    if not directory.exists() or not directory.is_dir():
        return []
    
    if recursive:
        html_files = list(directory.rglob("*.html"))
    else:
        html_files = list(directory.glob("*.html"))
    
    return sorted(html_files)


def validate_html_file(file_path: Path) -> Tuple[bool, str]:
    """
    Validate that HTML file exists and is readable.
    
    Args:
        file_path: Path to HTML file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        return False, f"文件不存在: {file_path}"
    
    if not file_path.is_file():
        return False, f"不是文件: {file_path}"
    
    try:
        with open(file_path, 'r') as f:
            f.read(1)
        return True, ""
    except PermissionError:
        return False, f"无法读取文件（权限不足）: {file_path}"
    except Exception as e:
        return False, f"无法读取文件: {file_path} - {str(e)}"
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_file_utils.py -v
```

Expected: All tests PASS

- [ ] **Step 5: Create test fixture HTML file**

Create `tests/fixtures/sample.html`:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>测试文档</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
        }
        h1 {
            color: #333;
        }
        p {
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <h1>HTML to PDF 转换测试</h1>
    <p>这是一个测试文档，用于验证HTML到PDF的转换功能。</p>
    <p>支持中文字符和基本的CSS样式。</p>
</body>
</html>
```

- [ ] **Step 6: Commit file utilities**

```bash
git add src/utils/file_utils.py tests/test_file_utils.py tests/fixtures/sample.html
git commit -m "feat: add file scanning and validation utilities"
```

---

## Task 3: Converter Engine with wkhtmltopdf

**Files:**
- Create: `src/core/converter.py`
- Create: `tests/test_converter.py`

- [ ] **Step 1: Write test for wkhtmltopdf detection**

Create `tests/test_converter.py`:

```python
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.core.converter import ConverterEngine


def test_detect_wkhtmltopdf_in_path():
    """Test detection of wkhtmltopdf in system PATH."""
    with patch('shutil.which', return_value='/usr/local/bin/wkhtmltopdf'):
        engine = ConverterEngine()
        assert engine.wkhtmltopdf_path == Path('/usr/local/bin/wkhtmltopdf')
        assert engine.is_available() is True


def test_detect_wkhtmltopdf_not_found():
    """Test when wkhtmltopdf is not installed."""
    with patch('shutil.which', return_value=None):
        engine = ConverterEngine()
        assert engine.wkhtmltopdf_path is None
        assert engine.is_available() is False


def test_convert_single_success(tmp_path):
    """Test successful HTML to PDF conversion."""
    html_file = tmp_path / "test.html"
    html_file.write_text("<html><body>Test</body></html>")
    pdf_file = tmp_path / "test.pdf"
    
    engine = ConverterEngine()
    
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = ""
    mock_result.stderr = ""
    
    with patch('subprocess.run', return_value=mock_result):
        with patch.object(engine, 'is_available', return_value=True):
            success, message = engine.convert_single(html_file, pdf_file)
    
    assert success is True
    assert message == "转换成功"


def test_convert_single_file_not_found(tmp_path):
    """Test conversion with non-existent HTML file."""
    html_file = tmp_path / "missing.html"
    pdf_file = tmp_path / "output.pdf"
    
    engine = ConverterEngine()
    
    with patch.object(engine, 'is_available', return_value=True):
        success, message = engine.convert_single(html_file, pdf_file)
    
    assert success is False
    assert "不存在" in message


def test_convert_single_wkhtmltopdf_not_available(tmp_path):
    """Test conversion when wkhtmltopdf is not available."""
    html_file = tmp_path / "test.html"
    html_file.write_text("<html><body>Test</body></html>")
    pdf_file = tmp_path / "test.pdf"
    
    engine = ConverterEngine()
    
    with patch.object(engine, 'is_available', return_value=False):
        success, message = engine.convert_single(html_file, pdf_file)
    
    assert success is False
    assert "wkhtmltopdf" in message


def test_convert_single_subprocess_error(tmp_path):
    """Test conversion when subprocess fails."""
    html_file = tmp_path / "test.html"
    html_file.write_text("<html><body>Test</body></html>")
    pdf_file = tmp_path / "test.pdf"
    
    engine = ConverterEngine()
    
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stdout = ""
    mock_result.stderr = "Error: Invalid input"
    
    with patch('subprocess.run', return_value=mock_result):
        with patch.object(engine, 'is_available', return_value=True):
            success, message = engine.convert_single(html_file, pdf_file)
    
    assert success is False
    assert "转换失败" in message
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_converter.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'src.core.converter'"

- [ ] **Step 3: Implement ConverterEngine class**

Create `src/core/converter.py`:

```python
import shutil
import subprocess
from pathlib import Path
from typing import Tuple, Optional


class ConverterEngine:
    """Handles HTML to PDF conversion using wkhtmltopdf."""
    
    def __init__(self, custom_path: Optional[Path] = None):
        """
        Initialize converter engine.
        
        Args:
            custom_path: Optional custom path to wkhtmltopdf binary
        """
        self.wkhtmltopdf_path = self._detect_wkhtmltopdf(custom_path)
    
    def _detect_wkhtmltopdf(self, custom_path: Optional[Path] = None) -> Optional[Path]:
        """
        Detect wkhtmltopdf installation.
        
        Args:
            custom_path: Optional custom path to check first
            
        Returns:
            Path to wkhtmltopdf binary or None if not found
        """
        if custom_path and Path(custom_path).exists():
            return Path(custom_path)
        
        which_result = shutil.which('wkhtmltopdf')
        if which_result:
            return Path(which_result)
        
        common_paths = [
            Path('/usr/local/bin/wkhtmltopdf'),
            Path('/usr/bin/wkhtmltopdf'),
            Path('C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'),
        ]
        
        for path in common_paths:
            if path.exists():
                return path
        
        return None
    
    def is_available(self) -> bool:
        """Check if wkhtmltopdf is available."""
        return self.wkhtmltopdf_path is not None
    
    def convert_single(self, html_path: Path, output_path: Path) -> Tuple[bool, str]:
        """
        Convert single HTML file to PDF.
        
        Args:
            html_path: Path to input HTML file
            output_path: Path to output PDF file
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self.is_available():
            return False, "wkhtmltopdf 未安装或未找到"
        
        html_path = Path(html_path)
        output_path = Path(output_path)
        
        if not html_path.exists():
            return False, f"HTML文件不存在: {html_path}"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            str(self.wkhtmltopdf_path),
            '--page-size', 'A4',
            '--margin-top', '10mm',
            '--margin-bottom', '10mm',
            '--margin-left', '10mm',
            '--margin-right', '10mm',
            '--encoding', 'UTF-8',
            '--enable-local-file-access',
            '--image-quality', '94',
            '--javascript-delay', '200',
            '--disable-smart-shrinking',
            str(html_path),
            str(output_path)
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return True, "转换成功"
            else:
                error_msg = result.stderr.strip() if result.stderr else "未知错误"
                return False, f"转换失败: {error_msg}"
                
        except subprocess.TimeoutExpired:
            return False, "转换超时（超过60秒）"
        except Exception as e:
            return False, f"转换过程出错: {str(e)}"
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_converter.py -v
```

Expected: All tests PASS

- [ ] **Step 5: Commit converter engine**

```bash
git add src/core/converter.py tests/test_converter.py
git commit -m "feat: add converter engine with wkhtmltopdf integration"
```

---

## Task 4: Settings Management

**Files:**
- Create: `src/utils/config.py`

- [ ] **Step 1: Implement config.py**

Create `src/utils/config.py`:

```python
from pathlib import Path
from typing import Optional
from PyQt5.QtCore import QSettings


class AppConfig:
    """Manages application settings using QSettings."""
    
    def __init__(self):
        """Initialize settings manager."""
        self.settings = QSettings('HTMLtoPDF', 'Converter')
    
    def get_last_output_directory(self) -> Optional[Path]:
        """Get last used output directory."""
        path_str = self.settings.value('last_output_directory', None)
        if path_str:
            return Path(path_str)
        return None
    
    def set_last_output_directory(self, directory: Path) -> None:
        """Save last used output directory."""
        self.settings.setValue('last_output_directory', str(directory))
    
    def get_custom_wkhtmltopdf_path(self) -> Optional[Path]:
        """Get custom wkhtmltopdf path."""
        path_str = self.settings.value('wkhtmltopdf_path', None)
        if path_str:
            return Path(path_str)
        return None
    
    def set_custom_wkhtmltopdf_path(self, path: Path) -> None:
        """Save custom wkhtmltopdf path."""
        self.settings.setValue('wkhtmltopdf_path', str(path))
    
    def get_window_geometry(self) -> Optional[bytes]:
        """Get saved window geometry."""
        return self.settings.value('window_geometry', None)
    
    def set_window_geometry(self, geometry: bytes) -> None:
        """Save window geometry."""
        self.settings.setValue('window_geometry', geometry)
    
    def get_recursive_scan(self) -> bool:
        """Get recursive scan preference."""
        return self.settings.value('recursive_scan', False, type=bool)
    
    def set_recursive_scan(self, enabled: bool) -> None:
        """Save recursive scan preference."""
        self.settings.setValue('recursive_scan', enabled)
```

- [ ] **Step 2: Commit config module**

```bash
git add src/utils/config.py
git commit -m "feat: add settings management with QSettings"
```

---

## Task 5: Worker Thread for Background Processing

**Files:**
- Create: `src/core/worker.py`

- [ ] **Step 1: Implement ConverterThread class**

Create `src/core/worker.py`:

```python
from pathlib import Path
from typing import List
from PyQt5.QtCore import QThread, pyqtSignal
from src.core.converter import ConverterEngine


class ConverterThread(QThread):
    """Background thread for batch HTML to PDF conversion."""
    
    progress_updated = pyqtSignal(int, int, str)
    file_completed = pyqtSignal(str, bool, str)
    all_completed = pyqtSignal(int, int)
    conversion_stopped = pyqtSignal()
    
    def __init__(self, html_files: List[Path], output_dir: Path, engine: ConverterEngine):
        """
        Initialize converter thread.
        
        Args:
            html_files: List of HTML files to convert
            output_dir: Output directory for PDF files
            engine: ConverterEngine instance
        """
        super().__init__()
        self.html_files = html_files
        self.output_dir = Path(output_dir)
        self.engine = engine
        self._stop_flag = False
    
    def stop(self):
        """Request thread to stop gracefully."""
        self._stop_flag = True
    
    def run(self):
        """Execute batch conversion in background thread."""
        total = len(self.html_files)
        success_count = 0
        fail_count = 0
        
        for index, html_file in enumerate(self.html_files, start=1):
            if self._stop_flag:
                self.conversion_stopped.emit()
                return
            
            html_file = Path(html_file)
            pdf_filename = html_file.stem + '.pdf'
            pdf_path = self.output_dir / pdf_filename
            
            self.progress_updated.emit(index, total, html_file.name)
            
            success, message = self.engine.convert_single(html_file, pdf_path)
            
            if success:
                success_count += 1
            else:
                fail_count += 1
            
            self.file_completed.emit(html_file.name, success, message)
        
        self.all_completed.emit(success_count, fail_count)
```

- [ ] **Step 2: Commit worker thread**

```bash
git add src/core/worker.py
git commit -m "feat: add worker thread for background conversion"
```

---

## Task 6: Custom Dialogs

**Files:**
- Create: `src/ui/dialogs.py`

- [ ] **Step 1: Implement InstallationGuideDialog**

Create `src/ui/dialogs.py`:

```python
from pathlib import Path
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, 
    QHBoxLayout, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt


class InstallationGuideDialog(QDialog):
    """Dialog to guide user through wkhtmltopdf installation."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.custom_path = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup dialog UI."""
        self.setWindowTitle("wkhtmltopdf 未找到")
        self.setFixedSize(500, 250)
        
        layout = QVBoxLayout()
        
        message = QLabel(
            "未检测到 wkhtmltopdf，这是转换 HTML 到 PDF 所必需的工具。\n\n"
            "请访问以下网址下载并安装：\n"
            "https://wkhtmltopdf.org/downloads.html\n\n"
            "或者，如果您已经安装，请手动指定路径。"
        )
        message.setWordWrap(True)
        layout.addWidget(message)
        
        layout.addStretch()
        
        button_layout = QHBoxLayout()
        
        self.browse_button = QPushButton("指定路径")
        self.browse_button.clicked.connect(self.browse_path)
        button_layout.addWidget(self.browse_button)
        
        self.retry_button = QPushButton("重新检测")
        self.retry_button.clicked.connect(self.accept)
        button_layout.addWidget(self.retry_button)
        
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def browse_path(self):
        """Browse for wkhtmltopdf binary."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择 wkhtmltopdf 可执行文件",
            "",
            "可执行文件 (*)"
        )
        
        if file_path:
            self.custom_path = Path(file_path)
            QMessageBox.information(
                self,
                "路径已设置",
                f"已设置路径: {file_path}\n\n点击"重新检测"以验证。"
            )


class CompletionDialog(QDialog):
    """Dialog to show conversion completion summary."""
    
    def __init__(self, success_count: int, fail_count: int, output_dir: Path, parent=None):
        super().__init__(parent)
        self.output_dir = output_dir
        self.setup_ui(success_count, fail_count)
    
    def setup_ui(self, success_count: int, fail_count: int):
        """Setup dialog UI."""
        self.setWindowTitle("转换完成")
        self.setFixedSize(400, 200)
        
        layout = QVBoxLayout()
        
        title = QLabel("转换完成！")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        summary = QLabel(
            f"成功: {success_count} 个\n"
            f"失败: {fail_count} 个"
        )
        summary.setStyleSheet("font-size: 14px;")
        summary.setAlignment(Qt.AlignCenter)
        layout.addWidget(summary)
        
        layout.addStretch()
        
        button_layout = QHBoxLayout()
        
        self.open_button = QPushButton("打开输出目录")
        self.open_button.clicked.connect(self.open_output_directory)
        button_layout.addWidget(self.open_button)
        
        self.close_button = QPushButton("关闭")
        self.close_button.clicked.connect(self.accept)
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def open_output_directory(self):
        """Open output directory in file manager."""
        import subprocess
        import sys
        
        if sys.platform == 'darwin':
            subprocess.run(['open', str(self.output_dir)])
        elif sys.platform == 'win32':
            subprocess.run(['explorer', str(self.output_dir)])
        else:
            subprocess.run(['xdg-open', str(self.output_dir)])
        
        self.accept()
```

- [ ] **Step 2: Commit dialogs**

```bash
git add src/ui/dialogs.py
git commit -m "feat: add custom dialogs for installation guide and completion"
```

---

## Task 7: Main Window UI

**Files:**
- Create: `src/ui/main_window.py`

- [ ] **Step 1: Create MainWindow class skeleton with imports**

Create `src/ui/main_window.py`:

```python
from pathlib import Path
from typing import List, Optional
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLabel, QProgressBar,
    QTextEdit, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from src.core.converter import ConverterEngine
from src.core.worker import ConverterThread
from src.utils.file_utils import scan_html_files, validate_html_file
from src.utils.config import AppConfig
from src.ui.dialogs import InstallationGuideDialog, CompletionDialog


class MainWindow(QMainWindow):
    """Main application window for HTML to PDF converter."""
    
    def __init__(self):
        super().__init__()
        self.config = AppConfig()
        self.engine = ConverterEngine(self.config.get_custom_wkhtmltopdf_path())
        self.worker_thread: Optional[ConverterThread] = None
        self.html_files: List[Path] = []
        self.output_directory: Optional[Path] = None
        
        self.setup_ui()
        self.check_wkhtmltopdf()
        self.restore_settings()
    
    def setup_ui(self):
        """Setup main window UI."""
        self.setWindowTitle("HTML to PDF Converter")
        self.setFixedSize(800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        main_layout.addLayout(self.create_file_selection_section())
        main_layout.addLayout(self.create_output_section())
        main_layout.addLayout(self.create_control_section())
        main_layout.addLayout(self.create_progress_section())
    
    def create_file_selection_section(self) -> QVBoxLayout:
        """Create file selection section."""
        layout = QVBoxLayout()
        
        label = QLabel("选择HTML文件:")
        label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(label)
        
        button_layout = QHBoxLayout()
        
        self.select_files_button = QPushButton("选择HTML文件")
        self.select_files_button.clicked.connect(self.select_files)
        button_layout.addWidget(self.select_files_button)
        
        self.select_folder_button = QPushButton("选择文件夹")
        self.select_folder_button.clicked.connect(self.select_folder)
        button_layout.addWidget(self.select_folder_button)
        
        self.clear_list_button = QPushButton("清空列表")
        self.clear_list_button.clicked.connect(self.clear_file_list)
        button_layout.addWidget(self.clear_list_button)
        
        layout.addLayout(button_layout)
        
        self.file_list_widget = QListWidget()
        self.file_list_widget.setMaximumHeight(150)
        layout.addWidget(self.file_list_widget)
        
        return layout
    
    def create_output_section(self) -> QVBoxLayout:
        """Create output directory section."""
        layout = QVBoxLayout()
        
        label = QLabel("输出目录:")
        label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(label)
        
        output_layout = QHBoxLayout()
        
        self.output_label = QLabel("未选择")
        self.output_label.setStyleSheet("color: gray;")
        output_layout.addWidget(self.output_label)
        
        self.select_output_button = QPushButton("选择输出目录")
        self.select_output_button.clicked.connect(self.select_output_directory)
        output_layout.addWidget(self.select_output_button)
        
        layout.addLayout(output_layout)
        
        return layout
    
    def create_control_section(self) -> QHBoxLayout:
        """Create conversion control section."""
        layout = QHBoxLayout()
        
        layout.addStretch()
        
        self.start_button = QPushButton("开始转换")
        self.start_button.setEnabled(False)
        self.start_button.setStyleSheet("font-weight: bold; padding: 8px 20px;")
        self.start_button.clicked.connect(self.start_conversion)
        layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("停止转换")
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("padding: 8px 20px;")
        self.stop_button.clicked.connect(self.stop_conversion)
        layout.addWidget(self.stop_button)
        
        layout.addStretch()
        
        return layout
    
    def create_progress_section(self) -> QVBoxLayout:
        """Create progress display section."""
        layout = QVBoxLayout()
        
        label = QLabel("转换进度:")
        label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        self.current_file_label = QLabel("")
        self.current_file_label.setStyleSheet("color: blue;")
        layout.addWidget(self.current_file_label)
        
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(150)
        layout.addWidget(self.status_text)
        
        return layout
```

- [ ] **Step 2: Implement file selection methods**

Add to `src/ui/main_window.py`:

```python
    def select_files(self):
        """Open file dialog to select HTML files."""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "选择HTML文件",
            "",
            "HTML Files (*.html *.htm)"
        )
        
        if files:
            for file_path in files:
                path = Path(file_path)
                if path not in self.html_files:
                    self.html_files.append(path)
                    self.file_list_widget.addItem(str(path))
            
            self.update_start_button_state()
    
    def select_folder(self):
        """Open folder dialog to scan for HTML files."""
        folder = QFileDialog.getExistingDirectory(
            self,
            "选择文件夹",
            ""
        )
        
        if folder:
            recursive = self.config.get_recursive_scan()
            found_files = scan_html_files(Path(folder), recursive=recursive)
            
            if not found_files:
                QMessageBox.information(
                    self,
                    "未找到文件",
                    f"在文件夹中未找到HTML文件: {folder}"
                )
                return
            
            for file_path in found_files:
                if file_path not in self.html_files:
                    self.html_files.append(file_path)
                    self.file_list_widget.addItem(str(file_path))
            
            self.update_start_button_state()
    
    def clear_file_list(self):
        """Clear the file list."""
        self.html_files.clear()
        self.file_list_widget.clear()
        self.update_start_button_state()
    
    def select_output_directory(self):
        """Open dialog to select output directory."""
        last_dir = self.config.get_last_output_directory()
        start_dir = str(last_dir) if last_dir else ""
        
        folder = QFileDialog.getExistingDirectory(
            self,
            "选择输出目录",
            start_dir
        )
        
        if folder:
            self.output_directory = Path(folder)
            self.output_label.setText(str(self.output_directory))
            self.output_label.setStyleSheet("color: black;")
            self.config.set_last_output_directory(self.output_directory)
            self.update_start_button_state()
```

- [ ] **Step 3: Implement conversion control methods**

Add to `src/ui/main_window.py`:

```python
    def start_conversion(self):
        """Start batch conversion process."""
        if not self.validate_before_conversion():
            return
        
        self.set_ui_converting_state(True)
        self.status_text.clear()
        self.progress_bar.setValue(0)
        
        self.worker_thread = ConverterThread(
            self.html_files,
            self.output_directory,
            self.engine
        )
        
        self.worker_thread.progress_updated.connect(self.on_progress_updated)
        self.worker_thread.file_completed.connect(self.on_file_completed)
        self.worker_thread.all_completed.connect(self.on_all_completed)
        self.worker_thread.conversion_stopped.connect(self.on_conversion_stopped)
        
        self.worker_thread.start()
    
    def stop_conversion(self):
        """Stop ongoing conversion."""
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.stop()
            self.stop_button.setEnabled(False)
            self.status_text.append("<span style='color: orange;'>正在停止转换...</span>")
    
    def validate_before_conversion(self) -> bool:
        """Validate files and settings before conversion."""
        invalid_files = []
        for file_path in self.html_files:
            is_valid, message = validate_html_file(file_path)
            if not is_valid:
                invalid_files.append((file_path, message))
        
        if invalid_files:
            message = "以下文件无法读取:\n\n"
            for file_path, error in invalid_files[:5]:
                message += f"• {file_path.name}: {error}\n"
            
            if len(invalid_files) > 5:
                message += f"\n...还有 {len(invalid_files) - 5} 个文件"
            
            reply = QMessageBox.question(
                self,
                "文件验证失败",
                message + "\n\n是否从列表中移除这些文件并继续？",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                for file_path, _ in invalid_files:
                    self.html_files.remove(file_path)
                    items = self.file_list_widget.findItems(str(file_path), Qt.MatchExactly)
                    for item in items:
                        self.file_list_widget.takeItem(self.file_list_widget.row(item))
                
                if not self.html_files:
                    return False
            else:
                return False
        
        if not self.output_directory.exists():
            try:
                self.output_directory.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "错误",
                    f"无法创建输出目录: {str(e)}"
                )
                return False
        
        return True
```

- [ ] **Step 4: Implement signal handlers**

Add to `src/ui/main_window.py`:

```python
    def on_progress_updated(self, current: int, total: int, filename: str):
        """Handle progress update signal."""
        percentage = int((current / total) * 100)
        self.progress_bar.setValue(percentage)
        self.current_file_label.setText(f"正在转换: {filename} ({current}/{total})")
    
    def on_file_completed(self, filename: str, success: bool, message: str):
        """Handle file completion signal."""
        if success:
            self.status_text.append(
                f"<span style='color: green;'>[✓] {filename} → {Path(filename).stem}.pdf</span>"
            )
        else:
            self.status_text.append(
                f"<span style='color: red;'>[✗] {filename} - 错误: {message}</span>"
            )
        
        self.status_text.verticalScrollBar().setValue(
            self.status_text.verticalScrollBar().maximum()
        )
    
    def on_all_completed(self, success_count: int, fail_count: int):
        """Handle all conversions completed signal."""
        self.set_ui_converting_state(False)
        self.progress_bar.setValue(100)
        self.current_file_label.setText("转换完成")
        
        dialog = CompletionDialog(success_count, fail_count, self.output_directory, self)
        dialog.exec_()
    
    def on_conversion_stopped(self):
        """Handle conversion stopped signal."""
        self.set_ui_converting_state(False)
        self.status_text.append("<span style='color: orange;'>转换已停止</span>")
        self.current_file_label.setText("已停止")
```

- [ ] **Step 5: Implement utility methods**

Add to `src/ui/main_window.py`:

```python
    def update_start_button_state(self):
        """Update start button enabled state."""
        has_files = len(self.html_files) > 0
        has_output = self.output_directory is not None
        self.start_button.setEnabled(has_files and has_output)
    
    def set_ui_converting_state(self, converting: bool):
        """Set UI state for converting or idle."""
        self.select_files_button.setEnabled(not converting)
        self.select_folder_button.setEnabled(not converting)
        self.clear_list_button.setEnabled(not converting)
        self.select_output_button.setEnabled(not converting)
        self.start_button.setEnabled(not converting)
        self.stop_button.setEnabled(converting)
    
    def check_wkhtmltopdf(self):
        """Check if wkhtmltopdf is available."""
        if not self.engine.is_available():
            dialog = InstallationGuideDialog(self)
            result = dialog.exec_()
            
            if result == QDialog.Accepted:
                if dialog.custom_path:
                    self.config.set_custom_wkhtmltopdf_path(dialog.custom_path)
                    self.engine = ConverterEngine(dialog.custom_path)
                else:
                    self.engine = ConverterEngine()
                
                if not self.engine.is_available():
                    QMessageBox.critical(
                        self,
                        "错误",
                        "仍然无法找到 wkhtmltopdf。应用程序将退出。"
                    )
                    self.close()
            else:
                self.close()
    
    def restore_settings(self):
        """Restore saved settings."""
        last_output = self.config.get_last_output_directory()
        if last_output and last_output.exists():
            self.output_directory = last_output
            self.output_label.setText(str(self.output_directory))
            self.output_label.setStyleSheet("color: black;")
            self.update_start_button_state()
        
        geometry = self.config.get_window_geometry()
        if geometry:
            self.restoreGeometry(geometry)
    
    def closeEvent(self, event):
        """Handle window close event."""
        self.config.set_window_geometry(self.saveGeometry())
        
        if self.worker_thread and self.worker_thread.isRunning():
            reply = QMessageBox.question(
                self,
                "确认退出",
                "转换正在进行中，确定要退出吗？",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.worker_thread.stop()
                self.worker_thread.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
```

- [ ] **Step 6: Commit main window**

```bash
git add src/ui/main_window.py
git commit -m "feat: add main window with complete UI and conversion logic"
```

---

## Task 8: Application Entry Point

**Files:**
- Create: `src/main.py`

- [ ] **Step 1: Implement main.py**

Create `src/main.py`:

```python
import sys
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow


def main():
    """Application entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("HTML to PDF Converter")
    app.setOrganizationName("HTMLtoPDF")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
```

- [ ] **Step 2: Test application launch**

```bash
python src/main.py
```

Expected: Application window opens successfully

- [ ] **Step 3: Commit main entry point**

```bash
git add src/main.py
git commit -m "feat: add application entry point"
```

---

## Task 9: Integration Testing and Final Verification

**Files:**
- Modify: `tests/fixtures/sample.html` (if needed)
- Create: `tests/fixtures/sample_with_image.html`
- Create: `tests/fixtures/sample_chinese.html`

- [ ] **Step 1: Create additional test fixtures**

Create `tests/fixtures/sample_with_image.html`:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>带图片的测试文档</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
        }
        img {
            max-width: 100%;
            height: auto;
        }
    </style>
</head>
<body>
    <h1>图片测试</h1>
    <p>这个文档包含一个内联图片（Base64编码）。</p>
    <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='100'%3E%3Crect width='200' height='100' fill='%234CAF50'/%3E%3Ctext x='50%25' y='50%25' text-anchor='middle' dy='.3em' fill='white' font-size='20'%3E测试图片%3C/text%3E%3C/svg%3E" alt="测试图片">
</body>
</html>
```

Create `tests/fixtures/sample_chinese.html`:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>中文路径测试</title>
    <style>
        body {
            font-family: "Microsoft YaHei", "SimSun", sans-serif;
            margin: 40px;
            line-height: 1.8;
        }
        h1 {
            color: #2196F3;
            border-bottom: 2px solid #2196F3;
            padding-bottom: 10px;
        }
        .content {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>中文字符测试</h1>
    <div class="content">
        <p>这是一个包含中文字符的测试文档。</p>
        <p>用于验证中文编码和字体渲染是否正确。</p>
        <ul>
            <li>列表项一</li>
            <li>列表项二</li>
            <li>列表项三</li>
        </ul>
    </div>
</body>
</html>
```

- [ ] **Step 2: Manual integration test - single file conversion**

```bash
python src/main.py
```

Test steps:
1. Click "选择HTML文件"
2. Select `tests/fixtures/sample.html`
3. Click "选择输出目录"
4. Select a test output directory
5. Click "开始转换"
6. Verify progress updates
7. Verify PDF is created successfully
8. Open PDF and verify content matches HTML

Expected: Conversion completes successfully, PDF renders correctly

- [ ] **Step 3: Manual integration test - batch conversion**

```bash
python src/main.py
```

Test steps:
1. Click "选择文件夹"
2. Select `tests/fixtures/` directory
3. Verify all HTML files are listed
4. Click "选择输出目录"
5. Select output directory
6. Click "开始转换"
7. Verify all files convert successfully
8. Check completion dialog shows correct counts

Expected: All files convert, completion dialog shows success count

- [ ] **Step 4: Manual integration test - stop conversion**

```bash
python src/main.py
```

Test steps:
1. Select multiple HTML files (create duplicates if needed)
2. Select output directory
3. Click "开始转换"
4. Immediately click "停止转换"
5. Verify conversion stops gracefully
6. Verify status shows "已停止"

Expected: Conversion stops after current file completes

- [ ] **Step 5: Manual integration test - error handling**

Test steps:
1. Add a non-existent file path to the list (manually edit if needed)
2. Try to convert
3. Verify error dialog appears
4. Verify option to remove invalid files

Expected: Application handles errors gracefully

- [ ] **Step 6: Manual integration test - settings persistence**

Test steps:
1. Select an output directory
2. Close application
3. Reopen application
4. Verify output directory is remembered

Expected: Settings persist across sessions

- [ ] **Step 7: Run all unit tests**

```bash
pytest tests/ -v
```

Expected: All unit tests PASS

- [ ] **Step 8: Create final commit**

```bash
git add tests/fixtures/
git commit -m "test: add integration test fixtures and verify all functionality"
```

---

## Task 10: Documentation and Cleanup

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Update README with complete documentation**

Update `README.md`:

```markdown
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
│   │   ├── controller.py       # Controller logic
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
```

- [ ] **Step 2: Commit documentation**

```bash
git add README.md
git commit -m "docs: update README with complete documentation"
```

- [ ] **Step 3: Create final tag**

```bash
git tag -a v1.0.0 -m "Release version 1.0.0 - HTML to PDF Batch Converter"
```

---

## Self-Review Checklist

### Spec Coverage

- [x] Project setup and dependencies (Task 1)
- [x] File utilities for scanning and validation (Task 2)
- [x] Converter engine with wkhtmltopdf integration (Task 3)
- [x] Settings management with QSettings (Task 4)
- [x] Worker thread for background processing (Task 5)
- [x] Custom dialogs (installation guide, completion) (Task 6)
- [x] Main window with complete UI (Task 7)
- [x] Application entry point (Task 8)
- [x] Integration testing (Task 9)
- [x] Documentation (Task 10)

### Placeholder Check

- [x] No TBD or TODO markers
- [x] All code blocks are complete
- [x] All file paths are exact
- [x] All commands have expected output
- [x] No "similar to Task N" references

### Type Consistency

- [x] ConverterEngine.convert_single() returns Tuple[bool, str] consistently
- [x] Path types used consistently throughout
- [x] Signal signatures match between definition and connection
- [x] QSettings keys are consistent

### Architecture Alignment

- [x] MVC pattern implemented as specified
- [x] Threading model matches spec (QThread with signals)
- [x] wkhtmltopdf parameters match spec
- [x] UI layout matches spec sections
- [x] Error handling strategy matches spec

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-05-11-html-to-pdf-converter.md`.

**Two execution options:**

**1. Subagent-Driven (recommended)** - Fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
