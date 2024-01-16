from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt6.QtGui import QImage, QPixmap, QColor
from PyQt6 import QtCore

import urllib
from urllib import request
from urllib.request import Request, urlopen

import requests
import json

class CatImage(QWidget):
    """Cat Image"""
    def __init__(self, name: str, parent: QWidget, pos: QtCore.QPoint) -> None:
        # Init QWidget
        super().__init__()

        self.setParent(parent)
        self.move(pos)

        url = self.get_cat_url()
        request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(request_site).read()

        # DISPLAY
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(data)
        self.pixmap2 = self.pixmap.scaledToHeight(350)

        self.label_img = QLabel(self)
        self.label_img.setObjectName("cat_image")
        self.label_img.setPixmap(self.pixmap2)
        self.resize(self.pixmap2.width(), self.pixmap2.height())

    def get_cat_url(self) -> str:
        rep = requests.get(f"https://api.thecatapi.com/v1/images/search")
        catimage_dict = json.loads(rep.content)
        cat_url = catimage_dict[0]['url']
        return cat_url

    def change_cat_image(self) -> None:
        url = self.get_cat_url()
        request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(request_site).read()

        self.pixmap = QPixmap()
        self.pixmap.loadFromData(data)
        self.pixmap2 = self.pixmap.scaledToHeight(350)
        self.label_img.setPixmap(self.pixmap2)

        self.parent().resize(self.pixmap2.width(), 400)

        self.print_pixel()

    # def get_pixel(self) -> None:
    #     x = event.pos().x()
    #     y = event.pos().y()
    #
    #     img = self.pixmap2.toImage()
    #


    def print_pixel(self) -> None:
        img = self.pixmap2.toImage()
        for x in range(0, img.width()):
           for y in range(0, img.height()):
               c = img.pixel(x, y)
               colors = QColor(c).getRgbF()
               print("(%s,%s) = %s" % (x, y, colors))