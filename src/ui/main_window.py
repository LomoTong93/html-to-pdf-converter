from pathlib import Path
from typing import List, Optional
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLabel, QProgressBar,
    QTextEdit, QFileDialog, QMessageBox, QDialog
)
from PyQt5.QtCore import Qt
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
