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

from interface import setupUI

# __________________________________________________
# Main.
# __________________________________________________
def main() -> None:

    # get url image
    cat_url = "https://cataas.com/cat"

    app = QApplication([])

    app_name = "Image Editor"
    window = setupUI(app_name,cat_url)

    window.show()
    app.exec()



    # display image
    response = requests.get(cat_url)
    img = Image.open(BytesIO(response.content))
    img.show()


if __name__ == "__main__":
    main()