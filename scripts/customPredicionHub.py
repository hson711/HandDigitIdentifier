from customPainter import customPainter, ToolbarWindow
import sys
from PyQt5.QtWidgets import *
class customPredicionHub(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Choose custom prediction option")
        self.setGeometry(300, 300, 400, 300)
        button1 = QPushButton('Premade Photos', self)
        button1.move(50,125)
        button1.clicked.connect(self.on_click1)
        button2 = QPushButton('Custom Photo', self)
        button2.move(250,125)
        button2.clicked.connect(self.on_click2)
    
    def on_click1(self):
        fileNames = QFileDialog.getOpenFileNames(self,("Open Image"), "", ("Image Files (*.png *.jpg *.bmp)"))
        print(fileNames[0])

    def on_click2(self):
        self.customPainterWindow = ToolbarWindow()
        self.customPainterWindow.show()
