from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QImage, QPixmap

import urllib
from urllib import request
from urllib.request import Request, urlopen

def setupUI(app_name : str, url : str) -> QWidget:

        window = QWidget()
        window.setWindowTitle(app_name)

        label = QLabel(window)
        label.setText("Chat")

        print(url)

        # "resources/cat.png"
        request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(request_site).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)

        label_img = QLabel(window)
        label_img.setPixmap(pixmap)
        window.resize(pixmap.width(), pixmap.height())

        return window
