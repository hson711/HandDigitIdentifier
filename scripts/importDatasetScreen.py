import sys
from PyQt5.QtWidgets import *
import time

TIME_LIMIT = 100
class importDatasetScreen(QMainWindow):
    """
    Simple dialog that consists of a Progress Bar and a Button.
    Clicking on the button results in the start of a timer and
    updates the progress bar.
    """
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Progress Bar')
        self.stop = False
        self.progress = QProgressBar(self)
        self.progress.setGeometry(0, 0, 300, 25)
        self.progress.setMaximum(100)
        self.button = QPushButton('Start', self)
        self.button.move(0, 30)
        self.button.clicked.connect(self.onButtonClick)
        self.button1 = QPushButton('Stop', self)
        self.button1.move(60, 30)
        self.button1.clicked.connect(self.onButtonClick1)
        self.show()

        

    def onButtonClick(self):
        count = 0
        while count < TIME_LIMIT:
            count += 1
            time.sleep(3)
            self.progress.setValue(count)
            if self.stop:
                count = TIME_LIMIT
        if self.stop:
            count = 0
        self.stop = False

    def onButtonClick1(self):
        self.stop = True