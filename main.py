
import requests
import json
from PIL import Image
import numpy as np
import urllib


from matplotlib import pyplot as plt
from matplotlib import image as mpimg

# from PyQt5.QtWidgets import QApplication, QWidget

def getCatImage():
    rep = requests.get("https://api.thecatapi.com/v1/images/search")
    return rep.content

if __name__ == '__main__':

    #get image
    catimage_dict = json.loads(getCatImage())
    cat_url = catimage_dict[0]['url']

    #display image
    plt.title("Cat Image")
    plt.xlabel("X pixels scaling")
    plt.ylabel("Y pixels scaling")

    np.array(Image.open(urllib.request.urlopen(cat_url)))
    image = mpimg.imread(cat_url)
    #plt.imshow(image)
    #plt.show()
