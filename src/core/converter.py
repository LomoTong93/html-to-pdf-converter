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
