from PyQt6.QtWidgets import QApplication, QTabWidget, QLabel, QPushButton
from PyQt6.QtGui import QImage, QPixmap
from PyQt6 import QtCore


class MainWindow(QTabWidget):
    """Main window"""
    def __init__(self, name: str) -> None:
        # Init QWidget
        super().__init__()

        self.setWindowTitle(name)

