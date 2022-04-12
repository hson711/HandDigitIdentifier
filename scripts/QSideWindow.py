import sys
from PyQt5.QtWidgets import QWidget

class sideWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Choose a model:')