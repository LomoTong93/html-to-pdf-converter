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
