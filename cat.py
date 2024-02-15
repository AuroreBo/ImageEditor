from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTabWidget
from PyQt6.QtGui import QImage, QPixmap, QColor
from PyQt6 import QtCore

import urllib
from urllib import request
from urllib.request import Request, urlopen

import requests
import json

class CatImage:
    """Cat Image class"""
    def __init__(self, name: str, parent: QTabWidget, pos: QtCore.QPoint) -> None:
        # Init QWidget
        super().__init__()

        self.ui = QWidget(parent)
        self.ui.move(pos)

        img_data = self.get_cat_image_data()

        self.setup_ui(img_data)

        # ------------------ UI CALLBACK ------------------
        self.ui.button.clicked.connect(self.change_cat_image)

    def get_cat_url(self) -> str:
        """ Request cat API for image URL. """
        rep = requests.get(f"https://api.thecatapi.com/v1/images/search")
        catimage_dict = json.loads(rep.content)
        cat_url = catimage_dict[0]['url']

        return cat_url

    def get_cat_image_data(self) -> str:
        """ Get data from cat API. """
        url = self.get_cat_url()
        request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(request_site).read()

        return data

    def change_cat_image(self) -> None:
        """ Update pixmap with new cat image. """
        data = self.get_cat_image_data()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.ui.pixmap2 = pixmap.scaledToHeight(350)
        self.ui.label_img.setPixmap(self.ui.pixmap2)
        self.ui.resize(self.ui.pixmap2.width(), self.ui.pixmap2.height())

    def print_pixel(self) -> None:
        """ Get value of every pixel. """
        img = self.ui.pixmap2.toImage()
        for x in range(0, img.width()):
           for y in range(0, img.height()):
               c = img.pixel(x, y)
               colors = QColor(c).getRgbF()
               print("(%s,%s) = %s" % (x, y, colors))

   # def get_pixel(self) -> None:
   #     x = event.pos().x()
   #     y = event.pos().y()
   #
   #     img = self.pixmap2.toImage()

    # ----------------------------------------------------------------
    #  UI
    # ----------------------------------------------------------------

    def setup_ui(self, p_data_img) -> None:
        """ PyQt UI setup """
        self.ui.button = QPushButton(self.ui)
        self.ui.button.setObjectName("button_generate")
        self.ui.button.resize(80, 30)
        self.ui.button.move(0, 0)
        self.ui.button.setText("Generate")

        pixmap = QPixmap()
        pixmap.loadFromData(p_data_img)
        self.ui.pixmap2 = pixmap.scaledToHeight(350)

        self.ui.label_img = QLabel(self.ui)
        self.ui.label_img.setObjectName("cat_image")
        self.ui.label_img.setPixmap(self.ui.pixmap2)
        self.ui.label_img.move(0, 30)
        self.ui.resize(self.ui.pixmap2.width() + 50, self.ui.pixmap2.height() + 50)

