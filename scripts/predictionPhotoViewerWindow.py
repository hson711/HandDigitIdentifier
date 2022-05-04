from importlib.resources import path
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
import numpy as np

class predictionPhotoViewerWindow(QMainWindow):

    def __init__(self,set):

        super().__init__()
        self.initUI(set)

    def initUI(self,set):

        #Setup of variables
        self.filterText = None
        self.scroll = QScrollArea()
        self.widget = QWidget() 
        self.layout = QGridLayout()
        self.i = 0
        self.j = 0
        self.z = 0
        self.layout.setSpacing(0)
        self.pathFileArray = set


        self.widget.setLayout(self.layout)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.scrollBar = self.scroll.verticalScrollBar()

        self.setCentralWidget(self.scroll)

        self.setGeometry(600, 100, 933, 600)
        self.setFixedSize(933,600)
        self.setWindowTitle('Prediction Dataset Viewer')

        self.predictShow(self.pathFileArray)
        self.show()

    def predictShow(self,pathFileArray):
        for i in pathFileArray:
            pix = QPixmap(i)
            predictionText = str(DNNFunctions.predict(i))
            if not pix.isNull():
                    imageLabel = QLabel(self, text= predictionText)
                    imageLabel.setPixmap(pix)
                    if self.j == 3:
                        self.j = 0
                        self.i = self.i + 1
                    self.layout.addWidget(imageLabel,self.i,self.j)
                    self.j = self.j + 1
                    self.z = self.z + 1