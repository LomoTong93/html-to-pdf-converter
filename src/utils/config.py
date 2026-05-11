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
