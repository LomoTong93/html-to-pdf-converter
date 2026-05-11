import pytest
import subprocess
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
        with patch('pathlib.Path.exists', return_value=False):
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


def test_convert_single_timeout(tmp_path):
    """Test conversion timeout after 60 seconds."""
    html_file = tmp_path / "test.html"
    html_file.write_text("<html><body>Test</body></html>")
    pdf_file = tmp_path / "test.pdf"

    engine = ConverterEngine()

    with patch('subprocess.run', side_effect=subprocess.TimeoutExpired('cmd', 60)):
        with patch.object(engine, 'is_available', return_value=True):
            success, message = engine.convert_single(html_file, pdf_file)

    assert success is False
    assert "超时" in message
