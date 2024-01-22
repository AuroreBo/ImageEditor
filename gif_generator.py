from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QTabWidget,
    QLabel,
    QLineEdit,
    QListWidget,
    QAbstractItemView,
    QCheckBox,
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
from PyQt6.QtGui import QImage, QPixmap
from PyQt6 import QtCore

import imageio
from PIL import Image
from pathlib import Path

class gifGenerator:

    def __init__(self, name: str, parent: QTabWidget, pos: QtCore.QPoint) -> None:
        # Init QWidget
        super().__init__()

        self.ui = QWidget(parent)
        self.ui.move(pos)

        self.parent: QTabWidget = parent
        self.output_path: str = ""
        self.img_list: [str] = []
        self.duration: float = 0.3
        self.loop: bool = True
        self.width: int = 256
        self.height: int = 256

        self.setup_ui()

        # ------------- UI CALLBACK  ----------------------
        self.ui.output_button.clicked.connect(self.select_output_path)
        self.ui.import_button.clicked.connect(self.select_images)
        self.ui.output_path_label.textChanged.connect(self.update_output_path)
        self.ui.delete_button.clicked.connect(self.delete_images)
        self.ui.process_button.clicked.connect(self.process_gif)

        self.ui.duration_text.textChanged.connect(self.update_duration)
        self.ui.width_text.textChanged.connect(self.update_width)
        self.ui.height_text.textChanged.connect(self.update_height)
        self.ui.loop_checkbox.stateChanged.connect(self.update_loop)

    def select_output_path(self):
         self.output_path = QFileDialog.getSaveFileName(self.ui, "Save file location", "", "*.gif")
         self.ui.output_path_label.setText(self.output_path[0])

    def update_output_path(self):
        if self.ui.output_path_label.text():
            self.output_path = self.ui.output_path_label.text()

    def select_images(self):
        filter = "*.png *.xpm *.jpg"
        imgs = QFileDialog.getOpenFileNames(self.parent, "Select Images", ".", filter)
        for img in imgs[0]:
            self.img_list.append(img)
            self.ui.image_tab.addItem(img)

    def delete_images(self):
        items = self.ui.image_tab.selectedItems()
        if not items:
            return
        for item in items:
            id = self.ui.image_tab.row(item)
            self.img_list.remove(self.img_list[id])
            self.ui.image_tab.takeItem(id)

    def process_gif(self):
        images = []

        loop = 0
        if not self.loop:
            loop = 1

        size = (self.width, self.height)

        if self.img_list and self.output_path:
            print(f"list = {self.img_list}")
            try:
                for img in self.img_list:
                    image = imageio.v2.imread(img)
                    image = Image.fromarray(image).resize(size)
                    images.append(image)
                imageio.mimsave(self.output_path, images, loop=loop, duration=self.duration)
            except:
                print("error processing gif")

    def update_duration(self):
        if self.ui.duration_text.text():
            duration = float(self.ui.duration_text.text())
            # conversion from sec
            self.duration = duration * 1000

    def update_width(self):
        if self.ui.width_text.text():
            self.width = int(self.ui.width_text.text())

    def update_height(self):
        if self.ui.height_text.text():
            self.height = int(self.ui.height_text.text())

    def update_loop(self):
        self.loop = self.ui.loop_checkbox.isChecked()
    # ------------------- UI -------------------------
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
        self.ui.image_tab.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

        self.ui.delete_button = QPushButton(self.ui)
        self.ui.delete_button.resize(65,30)
        self.ui.delete_button.move(240, 50)
        self.ui.delete_button.setText("Delete")

        self.ui.process_button = QPushButton(self.ui)
        self.ui.process_button.resize(65, 30)
        self.ui.process_button.move(240, 385)
        self.ui.process_button.setText("Process")

        self.ui.duration_label = QLabel(self.ui)
        self.ui.duration_label.move(315, 50)
        self.ui.duration_label.setText("Duration (sec):")

        self.ui.duration_text = QLineEdit(self.ui)
        self.ui.duration_text.resize(60, 25)
        self.ui.duration_text.move(315, 70)
        self.ui.duration_text.setText(str(self.duration))

        self.ui.size_label = QLabel(self.ui)
        self.ui.size_label.move(315, 100)
        self.ui.size_label.setText("Size (pixel):")

        self.ui.width_label = QLabel(self.ui)
        self.ui.width_label.move(315, 125)
        self.ui.width_label.setText("W")
        self.ui.width_text = QLineEdit(self.ui)
        self.ui.width_text.resize(45, 25)
        self.ui.width_text.move(330, 120)
        self.ui.width_text.setText(str(self.width))

        self.ui.height_label = QLabel(self.ui)
        self.ui.height_label.move(315, 155)
        self.ui.height_label.setText("H")
        self.ui.height_text = QLineEdit(self.ui)
        self.ui.height_text.resize(45, 25)
        self.ui.height_text.move(330, 150)
        self.ui.height_text.setText(str(self.height))

        self.ui.loop_checkbox = QCheckBox(self.ui)
        self.ui.loop_checkbox.move(315, 180)
        self.ui.loop_checkbox.setText("Looping")
        self.ui.loop_checkbox.setChecked(True)