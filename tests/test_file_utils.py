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


def test_validate_html_file_is_directory(tmp_path):
    """Test validation fails when path is a directory."""
    directory = tmp_path / "subdir"
    directory.mkdir()

    is_valid, message = validate_html_file(directory)

    assert is_valid is False
    assert "不是文件" in message
