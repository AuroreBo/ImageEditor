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
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6 import QtCore

from interface import MainWindow
from cat import CatImage

# __________________________________________________
# Variables.
# __________________________________________________
api_key = "live_BbUk9mOGIFUrRHGQJxGylLmpxWeokjH5KfZwqicmEyja0B1eAX583X3SylYunpVF"
url_api1 = "https://cataas.com/cat"
window_height = 400
window_width = 350

# __________________________________________________
# Func.
# __________________________________________________


# __________________________________________________
# Main.
# __________________________________________________
def main() -> None:

    app = QApplication([])
    app_name = "Image Editor"

    window = MainWindow(app_name)

    cat = CatImage("Cat", window, QtCore.QPoint(0, 50))

    window.button.clicked.connect(cat.change_cat_image)
    cat.print_pixel()

    window.resize(cat.pixmap2.width(),window_height)

    window.show()
    app.exec()

if __name__ == "__main__":
    main()