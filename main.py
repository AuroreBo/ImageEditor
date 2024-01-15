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
# Variables.
# __________________________________________________
api_key = "live_BbUk9mOGIFUrRHGQJxGylLmpxWeokjH5KfZwqicmEyja0B1eAX583X3SylYunpVF"

# __________________________________________________
# Func.
# __________________________________________________
def getCatUrl() -> str:
    rep = requests.get(f"https://api.thecatapi.com/v1/images/search")
    catimage_dict = json.loads(rep.content)
    cat_url = catimage_dict[0]['url']
    return cat_url

# __________________________________________________
# Main.
# __________________________________________________
def main() -> None:

    # get url image
    url_api1 = "https://cataas.com/cat"
    url_api2 = getCatUrl()


    app = QApplication([])
    app_name = "Image Editor"
    window = setupUI(app_name,url_api2)

    window.show()
    app.exec()


    # display image
    # response = requests.get(cat_url)
    # img = Image.open(BytesIO(response.content))
    # img.show()


if __name__ == "__main__":
    main()