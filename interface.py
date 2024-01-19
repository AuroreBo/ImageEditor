from PyQt6.QtWidgets import QTabWidget

class MainWindow(QTabWidget):
    """Main window"""
    def __init__(self, name: str) -> None:
        # Init QWidget
        super().__init__()

        self.setWindowTitle(name)

