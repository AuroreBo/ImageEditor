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
    QHeaderView,
)
from PyQt6.QtGui import QImage, QPixmap
from PyQt6 import QtCore

import imageio
from PIL import Image
from pathlib import Path

from enum import Enum
import os
import shutil



class TableColumnsImages(Enum):
    """Image table columns enumeration."""

    PREVIEW = 0
    PATH = 1

class gifGenerator:

    def __init__(self, name: str, parent: QTabWidget, pos: QtCore.QPoint) -> None:
        # Init QWidget
        super().__init__()

        self.ui = QWidget(parent)
        self.ui.move(pos)

        self.parent: QTabWidget = parent
        self.output_path: str = ""
        self.duration: float = 0.3
        self.loop: bool = True
        self.width: int = 256
        self.height: int = 256

        self.frames: [] = []
        self.nb_frames: int = 3
        self.enable_interpolation: bool = True
        self.path_temp_folder: str = ""
        self.delete_temp_folder: bool = False


        self.setup_ui()

        # ------------- UI CALLBACK  ----------------------
        self.ui.output_button.clicked.connect(self.select_output_path)
        self.ui.import_button.clicked.connect(self.select_images)
        self.ui.output_path_label.textChanged.connect(self.update_output_path)
        self.ui.delete_button.clicked.connect(self.delete_images)
        self.ui.select_all_button.clicked.connect(self.select_all_images)
        self.ui.process_button.clicked.connect(self.process_gif)
        self.ui.debug_button.clicked.connect(self.setup_fading)

        self.ui.duration_text.textChanged.connect(self.update_duration)
        self.ui.width_text.textChanged.connect(self.update_width)
        self.ui.height_text.textChanged.connect(self.update_height)
        self.ui.loop_checkbox.stateChanged.connect(self.update_loop)

        self.ui.image_tab.verticalHeader().setSectionsMovable(True)

    def select_output_path(self):
         path = QFileDialog.getSaveFileName(self.ui, "Save file location", "", "*.gif")
         if path:
            self.output_path = path[0]
            self.ui.output_path_label.setText(self.output_path)

    def update_output_path(self):
        if self.ui.output_path_label.text():
            self.output_path = self.ui.output_path_label.text()

    def select_images(self):
        filter = "*.png *.xpm *.jpg"
        imgs = QFileDialog.getOpenFileNames(self.parent, "Select Images", ".", filter)

        for img in imgs[0]:
            self.add_table(img)

    def add_table(self, p_path : str):
        table_row = self.ui.image_tab.rowCount()
        self.ui.image_tab.insertRow(table_row)
        self.ui.image_tab.verticalHeader().setDefaultSectionSize(50)

        pixmap = QPixmap(p_path)
        pixmap = pixmap.scaledToHeight(50)
        img_preview = QLabel()
        img_preview.setPixmap(pixmap)

        self.ui.image_tab.setCellWidget(table_row, TableColumnsImages.PREVIEW.value, img_preview)
        self.ui.image_tab.setItem(table_row, TableColumnsImages.PATH.value, QTableWidgetItem(p_path))

    def delete_images(self):
        items = self.ui.image_tab.selectedItems()
        if not items:
            return
        for item in items:
            id = self.ui.image_tab.row(item)
            self.ui.image_tab.removeRow(id)

    def select_all_images(self):
        self.ui.image_tab.selectAll()

    def process_gif(self):
        self.frames = self.setup_key_images_data_list()

        loop = 0
        if not self.loop:
            loop = 1

        if self.output_path:
            # try:
            if self.enable_interpolation:

                path = Path(self.output_path)
                folder_name = path.parent.absolute()
                file_name = path.stem
                output_path_with_fade = f"{folder_name}\{file_name}_fade.gif"

                #process interpolation
                self.setup_fading(self.frames, file_name)
                #process new list with interpolated frames
                frames_with_fade = self.compute_new_frame_list(self.frames)
                imageio.mimsave(output_path_with_fade, frames_with_fade, loop=loop, duration=self.duration)
                print(f"[Success] Gif exported at : {output_path_with_fade}")

            imageio.mimsave(self.output_path, self.frames, loop=loop, duration=self.duration)
            print(f"[Success] Gif exported at : {self.output_path}")
            # except:
            #     print("[Error] Error processing gif")

    def setup_key_images_data_list(self) -> []:
        # be sure our list is empty
        frames = []

        count = self.ui.image_tab.rowCount()
        header = self.ui.image_tab.verticalHeader()
        size = (self.width, self.height)

        try:
            for vrow in range(count):
                row = header.logicalIndex(vrow)
                current_path = self.ui.image_tab.item(row, TableColumnsImages.PATH.value).text()

                image = imageio.v2.imread(current_path)
                image = Image.fromarray(image).resize(size)
                frames.append(image)
            return frames
            print(f"[Success] Images list done {frames}")
        except:
            print("[Error] Error setup list")

    def compute_new_frame_list(self, p_frames) -> []:
        new_frames_list = []
        total_frames = len(p_frames)

        # add key frames
        for i in range(total_frames):
            new_frames_list.append(p_frames[i])
            if i+1 < total_frames:
                #add interpolation frames
                for j in range(self.nb_frames):
                    current_path = f"{self.path_temp_folder}/folder_img{i}/img{j}.png"
                    current_image = imageio.v2.imread(current_path)
                    image = Image.fromarray(current_image)
                    new_frames_list.append(image)

        return new_frames_list

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

    def setup_fading(self, p_frames:[], p_name: str):
        if self.output_path:
            path = Path(self.output_path)
            self.path_temp_folder = str(path.parent.absolute())+"/"+p_name+"_temp"
            print(self.path_temp_folder)

            # Creation of a temporary folder to stock interpolating images
            try:
                os.mkdir(self.path_temp_folder)
                print("[Success] Folder created.")
            except:
                print("[Error] Couldn't creating Folder.")

            #  // TEMP SETUP FOR DEBUG PUSHBUTTON //
            self.frames = self.setup_key_images_data_list()
            p_frames = self.frames
            # // _______________________________//
            total_frame = len(p_frames)
            for i in range(total_frame):
                if i+1 < total_frame:
                    path1 = self.ui.image_tab.item(i, TableColumnsImages.PATH.value).text()
                    path2 = self.ui.image_tab.item(i+1, TableColumnsImages.PATH.value).text()
                    self.compute_interpolated_frame(path1, path2, i)


            # Delete the temporary folder to stock interpolating images
            if self.delete_temp_folder:
                try:
                    # os.rmdir(temp_folder_path)
                    shutil.rmtree(self.path_temp_folder)
                    print("[Success] Folder deleted.")
                except:
                    print("[Error] Couldn't delete folder.")

    def compute_interpolated_frame(self, p_path_image1 : str, p_path_image2 : str, p_step: int) -> None:
        """ Save interpolated image in a temp folder """
        im1 = Image.open(p_path_image1)
        resized_img1 = im1.resize((self.width, self.height))
        px1 = resized_img1.load()

        im2 = Image.open(p_path_image2)
        resized_img2 = im2.resize((self.width, self.height))
        px2 = resized_img2.load()

        img_list = []

        folder_path = f"{self.path_temp_folder}/folder_img{p_step}"
        os.mkdir(folder_path)

        # Create new frames
        for i in range(self.nb_frames):
            int_img = Image.new("RGB", (self.width, self.height))
            img_list.append(int_img)

        try:
            for x in range(self.width):
                for y in range(self.height):
                    pixel1 = px1[x, y]
                    pixel2 = px2[x, y]
                    # print(f"{pixel1} / {pixel2}")

                    new_pixel_values = self.compute_intermediate_pixel(pixel1, pixel2,   self.nb_frames)

                    # Set pixels of frames
                    for i in range(self.nb_frames):
                        img = img_list[i]
                        img.putpixel((x,y), new_pixel_values[i])
        except:
            print("[Error] Error during processing image")

        try:
            if folder_path:
                # Save frames
                for i in range(self.nb_frames):
                    img = img_list[i]
                    name = f"/img{i}.png"
                    output_path = folder_path + name
                    img.save(output_path)
                    print(f"[Success] Frame saved at {output_path}")

        except:
            print("[Error] Couldn't save interpolated images")

    def compute_intermediate_pixel(self, p_pixel1 : tuple, p_pixel2: tuple, p_iteration: int) -> [tuple]:
        colors = []
        for i in range(p_iteration):
            r = self.compute_channel(p_pixel1[0], p_pixel2[0], i, p_iteration)
            g = self.compute_channel(p_pixel1[1], p_pixel2[1], i, p_iteration)
            b = self.compute_channel(p_pixel1[2], p_pixel2[2], i, p_iteration)
            colors.append((r,g,b,255))

        return colors

    def compute_channel(self, p_v1 : int, p_v2: int, p_current_step: int, p_total_step: int) -> int:
        if p_v1 > p_v2:
            val = p_v2 + (((p_v1 - p_v2)/ p_total_step) * (p_current_step+1))
        else:
            val = p_v1 + (((p_v2 - p_v1)/ p_total_step) * (p_current_step+1))
        return int(val)

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

        self.ui.image_tab = QTableWidget(self.ui)
        self.ui.image_tab.resize(450, 300)
        self.ui.image_tab.move(5, 80)

        self.ui.image_tab.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.ui.image_tab.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.ui.image_tab.setColumnCount(2)
        self.ui.image_tab.setColumnWidth(0, 100)
        self.ui.image_tab.setColumnWidth(1, 325)
        self.ui.image_tab.horizontalHeader().setStretchLastSection(True)

        headers = ["PREVIEW","PATH"]
        self.ui.image_tab.setHorizontalHeaderLabels(headers)
        self.ui.image_tab.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

        self.ui.select_all_button = QPushButton(self.ui)
        self.ui.select_all_button.resize(75, 30)
        self.ui.select_all_button.move(310, 50)
        self.ui.select_all_button.setText("Select All")

        self.ui.delete_button = QPushButton(self.ui)
        self.ui.delete_button.resize(65,30)
        self.ui.delete_button.move(390, 50)
        self.ui.delete_button.setText("Delete")

        self.ui.process_button = QPushButton(self.ui)
        self.ui.process_button.resize(65, 30)
        self.ui.process_button.move(390, 385)
        self.ui.process_button.setText("Process")

        self.ui.duration_label = QLabel(self.ui)
        self.ui.duration_label.move(460, 60)
        self.ui.duration_label.setText("Duration (sec):")

        self.ui.duration_text = QLineEdit(self.ui)
        self.ui.duration_text.resize(60, 25)
        self.ui.duration_text.move(460, 80)
        self.ui.duration_text.setText(str(self.duration))

        self.ui.size_label = QLabel(self.ui)
        self.ui.size_label.move(460, 110)
        self.ui.size_label.setText("Size (pixel):")

        self.ui.width_label = QLabel(self.ui)
        self.ui.width_label.move(460, 135)
        self.ui.width_label.setText("W")
        self.ui.width_text = QLineEdit(self.ui)
        self.ui.width_text.resize(45, 25)
        self.ui.width_text.move(490, 130)
        self.ui.width_text.setText(str(self.width))

        self.ui.height_label = QLabel(self.ui)
        self.ui.height_label.move(460, 165)
        self.ui.height_label.setText("H")
        self.ui.height_text = QLineEdit(self.ui)
        self.ui.height_text.resize(45, 25)
        self.ui.height_text.move(490, 160)
        self.ui.height_text.setText(str(self.height))

        self.ui.loop_checkbox = QCheckBox(self.ui)
        self.ui.loop_checkbox.move(460, 190)
        self.ui.loop_checkbox.setText("Looping")
        self.ui.loop_checkbox.setChecked(True)

        self.ui.debug_button = QPushButton(self.ui)
        self.ui.debug_button.setText("Debug")
        self.ui.debug_button.move(460, 300)
