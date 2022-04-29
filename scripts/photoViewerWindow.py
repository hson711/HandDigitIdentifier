from asyncio.windows_events import NULL
from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea,QApplication,QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import io
from PIL import Image, ImageCms
import os
from DNNFunctions import DNNFunctions

class photoViewerWindow(QMainWindow):
    def __init__(self,set):
        super().__init__()
        self.initUI()
        self.set = set
        self.photoViewer()

    def initUI(self):
        self.scroll = QScrollArea()
        self.widget = QWidget() 
        self.layout = QGridLayout()
        self.i = 0
        self.j = 0

        toolbar = QMenuBar()
        filterPhotosAction = QAction("Filter", toolbar)
        toolbar.addAction(filterPhotosAction)
        #filterPhotosAction.triggered.connect(self.filterPhotos)
        self.layout.setMenuBar(toolbar)

        self.widget.setLayout(self.layout)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

        self.setGeometry(600, 100, 1200, 1200)
        self.setWindowTitle('Scroll Area Demonstration')
        self.show()


    def showPhoto(self, lengthx, lengthy, datax, datay):
        for i in range(100):
            pm1 = DNNFunctions.convertNumpyArrayToImage(datax[i])
            if not pm1.isNull():
                imageLabel = QLabel(self)
                imageLabel.setPixmap(pm1)
                if self.j == 50:
                    self.j = 0
                    self.i = self.i + 1
                self.layout.addWidget(imageLabel,self.i,self.j)
                self.j = self.j + 1
    
    
    def photoViewer(self):
        if (self.set == 'Train Set'):
            lengthx = len(DNNFunctions.raw_train_x)
            datax = DNNFunctions.raw_train_x
            lengthy = len(DNNFunctions.raw_train_y)
            datay = DNNFunctions.raw_train_y
        else:
            lengthx = len(DNNFunctions.raw_test_x)
            datax = DNNFunctions.raw_test_x
            lengthy = len(DNNFunctions.raw_test_y)
            datay = DNNFunctions.raw_test_y
        self.showPhoto(lengthx, lengthy, datax, datay)
    """
    def filterPhotos(self):
        filterText, done1 = QtWidgets.QInputDialog.getText(self, 'Filtering', 'Enter text to filter:')
        if done1:
            self.filteredPhotoViewer(filterText)

    def filteredPhotoViewer(self, filterText):
        self.clearLayout()
        for file in os.listdir(self.folderDir):
            fileDir = os.path.join(self.folderDir, file)
            fileName = fileDir.split("/")[-1]
            fileName = fileName.split(".")[0]
            fileName = fileName.split('\\')[-1]
            #self.convert_to_srgb(fileDir) #this isn't working for some reason
            if (filterText == ""):
                self.showPhoto(fileDir)
            elif (filterText.upper() in fileName.upper()):
                self.showPhoto(fileDir)
                
    def clearLayout(self):
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().setParent(None)
        self.i = 0
        self.j = 0
        """