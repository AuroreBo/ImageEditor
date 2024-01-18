from PyQt6.QtWidgets import QApplication, QWidget,QTabWidget, QLabel, QPushButton, QLineEdit, QListWidget
from PyQt6.QtGui import QImage, QPixmap
from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QColorDialog,
    QComboBox,
    QFileDialog,
    QFontComboBox,
    QLabel,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
)

class gifGenerator:

    def __init__(self, name: str, parent: QTabWidget, pos: QtCore.QPoint) -> None:
        # Init QWidget
        super().__init__()

        self.ui = QWidget(parent)
        self.ui.move(pos)

        self.parent: QTabWidget = parent
        self.output_path: str = ""
        self.img_list: [str] = []

        self.setup_ui()

    def setup_ui(self):
        self.ui.output_button = QPushButton(self.ui)
        self.ui.output_button.resize(150,25)
        self.ui.output_button.move(5, 10)
        self.ui.output_button.setText("Select Output Path")

        self.ui.output_path_label = QLineEdit(self.ui)
        self.ui.output_path_label.resize(350,25)
        self.ui.output_path_label.move(160, 10)

        self.ui.import_button = QPushButton(self.ui)
        self.ui.import_button.resize(100,30)
        self.ui.import_button.move(5, 50)
        self.ui.import_button.setText("Select images")

        self.ui.image_tab = QListWidget(self.ui)
        self.ui.image_tab.resize(300, 300)
        self.ui.image_tab.move(5, 80)

    def select_output_path(self):
         self.output_path = QFileDialog.getExistingDirectory(self.parent, "Save file location")
         self.ui.output_path_label.setText(self.output_path)

    def update_output_path(self):
        if self.ui.output_path_label.text():
            self.output_path = self.ui.output_path_label.text()


    def select_images(self):
        filter = "*.png *.xpm *.jpg"
        imgs = QFileDialog.getOpenFileNames(self.parent, "Select Images", ".", filter)
        self.img_list = imgs[0]
        for item in self.img_list:
            self.ui.image_tab.addItem(item)
