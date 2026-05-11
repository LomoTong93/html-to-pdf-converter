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
                f"已设置路径: {file_path}\n\n点击\"重新检测\"以验证。"
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
