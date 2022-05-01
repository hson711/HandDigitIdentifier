from customPainter import customPainter, ToolbarWindow
import sys
from PyQt5.QtWidgets import *
from DNNFunctions import DNNFunctions

class customPredicionHub(QDialog):

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Choose custom prediction option")
        self.setGeometry(200, 500, 300, 100)
        hbox = QHBoxLayout()
        button1 = QPushButton('Premade Photos')
        button1.clicked.connect(self.on_click1)
        button2 = QPushButton('Custom Photo')
        button2.clicked.connect(self.on_click2)
        hbox.addWidget(button1)
        hbox.addWidget(button2)
        self.setLayout(hbox)
        self.file_load()
    
    def on_click1(self):
        fileNames = QFileDialog.getOpenFileNames(self,("Open Image"), "", ("Image Files (*.png *.jpg *.bmp)"))
        print(fileNames[0])

    def on_click2(self):
        self.customPainterWindow = ToolbarWindow()
        self.customPainterWindow.show()

    def file_load(self):
        model_path = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
        DNNFunctions.model_load(model_path)
        print(DNNFunctions.loaded_model.name)
