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
