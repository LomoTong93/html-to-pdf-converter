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
