from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QImage, QPixmap

def setupUI(app_name : str, url : str) -> QWidget:

        window = QWidget()
        window.setWindowTitle(app_name)

        label = QLabel(window)
        label.setText("Chat")

        print(url)
        # "resources/cat.png"
        pixmap = QPixmap("resources/cat.png")
        label_img = QLabel(window)
        label_img.setPixmap(pixmap)
        window.resize(pixmap.width(), pixmap.height())

        return window
