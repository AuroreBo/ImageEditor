# __________________________________________________
# Librairies includes.
# __________________________________________________

# _____ Utilities _____
from PIL import Image
from io import BytesIO
import numpy as np
import urllib
import requests
import json

# _____ UI includes _____
from PyQt6.QtWidgets import QApplication, QWidget, QTabWidget

from PyQt6 import QtCore

from interface import MainWindow
from cat import CatImage
from gif_generator import gifGenerator

# __________________________________________________
# Variables.
# __________________________________________________
api_key = "live_BbUk9mOGIFUrRHGQJxGylLmpxWeokjH5KfZwqicmEyja0B1eAX583X3SylYunpVF"
url_api1 = "https://cataas.com/cat"
window_height = 460
window_width = 840

# __________________________________________________
# Func.
# __________________________________________________


# __________________________________________________
# Main.
# __________________________________________________
def main() -> None:

    app = QApplication([])
    app_name = "Gif Generator"

    with open("style/SpyBot.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    window = MainWindow(app_name)
    window.resize(window_width, window_height)

    cat = CatImage("Cat", window, QtCore.QPoint(0, 10))
    gif = gifGenerator("gif", window, QtCore.QPoint(0, 10))

    window.addTab(gif.ui, "Gif Generator")
    window.addTab(cat.ui, "Image Editor")

    window.show()
    app.exec()


if __name__ == "__main__":
    main()