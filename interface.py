from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt6.QtGui import QImage, QPixmap
from PyQt6 import QtCore


class MainWindow(QWidget):
    """Main window"""
    def __init__(self, name: str) -> None:
        # Init QWidget
        super().__init__()

        self.setWindowTitle(name)

        # ------- BUTTON --------
        self.button = QPushButton(self)
        self.button.setObjectName("button_generate")
        self.button.resize(80, 30)
        self.button.move(5, 5)
        self.button.setText("Generate")

