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

# _____ Image readers includes _____
from matplotlib import pyplot as plt
from matplotlib import image as mpimg

# _____ UI includes _____
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6 import uic

from interface import Ui

# __________________________________________________
# UI class.
# __________________________________________________
class UI(QWidget):
    def __init__(self):
        super().__init__()

        # loading the ui file with uic module
        uic.loadUi("image_editor.ui", self)

# __________________________________________________
# Main.
# __________________________________________________
def main() -> None:
    #
    app = QApplication([])



    window.show()
    app.exec()

    # get url image
    cat_url = "https://cataas.com/cat"

    # display image
    plt.title("Cat Image")
    plt.xlabel("X pixels scaling")
    plt.ylabel("Y pixels scaling")

    response = requests.get(cat_url)
    img = Image.open(BytesIO(response.content))
    img.show()
    # image = mpimg.imread(img)
    # plt.imshow(image)
    # plt.show()

if __name__ == "__main__":
    main()