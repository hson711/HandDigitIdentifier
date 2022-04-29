from asyncio.windows_events import NULL
from pickle import TRUE
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
import threading

class photoViewerWindow(QMainWindow):
    def __init__(self,set):
        super().__init__()
        self.initUI(set)

    def initUI(self,set):
        self.scroll = QScrollArea()
        self.widget = QWidget() 
        self.layout = QGridLayout()
        self.i = 0
        self.j = 0
        self.z = 0
        self.layout.setSpacing(0)
        self.set = set

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
        self.scrollBar = self.scroll.verticalScrollBar()
        self.scrollBar.valueChanged.connect(self.scrolled)

        self.setCentralWidget(self.scroll)

        self.setGeometry(600, 100, 933, 600)
        self.setFixedSize(933,600)
        self.setWindowTitle('Scroll Area Demonstration')
        self.show()
        self.loadData()

    
    def scrolled(self, value):
        tempValue = (self.scrollBar.maximum())
        maxValue = round(tempValue * 1)
        minValue = round(tempValue * 0.95)
        halfValue = round(tempValue * 0.5)
        if value >= minValue and value <= maxValue :
            self.showPhotoExsisting(self.lengthx, self.datax)


    def showPhoto(self, lengthx, datax):
        temp = self.z
        while self.z <= temp + 1000:
            pm1 = DNNFunctions.convertNumpyArrayToImage(datax[self.z])
            if not pm1.isNull():
                imageLabel = QLabel(self)
                imageLabel.setPixmap(pm1)
                if self.j == 32:
                    self.j = 0
                    self.i = self.i + 1
                self.layout.setColumnStretch(self.j,1)
                self.layout.setRowStretch(self.i,1)
                self.layout.addWidget(imageLabel,self.i,self.j)
                self.j = self.j + 1
                self.z = self.z + 1
    
    def showPhotoExsisting(self, lengthx, datax):
        datax = DNNFunctions.raw_train_x
        temp = self.z
        while self.z <= temp + 32:
            pm1 = DNNFunctions.convertNumpyArrayToImage(datax[self.z])
            if not pm1.isNull():
                imageLabel = QLabel(self)
                imageLabel.setPixmap(pm1)
                if self.j == 32:
                    self.j = 0
                    self.i = self.i + 1
                self.layout.setColumnStretch(self.j,1)
                self.layout.setRowStretch(self.i,1)
                self.layout.addWidget(imageLabel,self.i,self.j)
                self.j = self.j + 1
                self.z = self.z + 1
    
    def loadData(self):
        if (self.set == 'Train Set'):
            self.lengthx = len(DNNFunctions.raw_train_x)
            self.datax = DNNFunctions.raw_train_x
            self.lengthy = len(DNNFunctions.raw_train_y)
            self.datay = DNNFunctions.raw_train_y
        else:
            self.lengthx = len(DNNFunctions.raw_test_x)
            self.datax = DNNFunctions.raw_test_x
            self.lengthy = len(DNNFunctions.raw_test_y)
            self.datay = DNNFunctions.raw_test_y
        self.showPhoto(self.lengthx, self.datax)
        

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