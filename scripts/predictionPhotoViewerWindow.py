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

    def __init__(self,pathFileArray):

        super().__init__()
        self.initUI(pathFileArray)
        
    def initUI(self,pathFileArray):

        self.baseDir = os.getcwd()
        self.pathFileArray = pathFileArray

        #Counter set-up
        self.i = 0
        self.j = 0
        self.z = 0

        #Layout set-up
        self.layout = QGridLayout()
        self.widget = QWidget()
        self.layout.setSpacing(0)
        self.widget.setLayout(self.layout)

        self.predictShow(self.pathFileArray)
        self.show()

    def predictShow(self,pathFileArray):
        for i in pathFileArray:
            pix = QPixmap(pathFileArray[i])
            predictionText = str(DNNFunctions.predict(pathFileArray[i]))
            if not pix.isNull():
                    imageLabel = QLabel(self, text= predictionText)
                    imageLabel.setPixmap(pix)
                    if self.j == 3:
                        self.j = 0
                        self.i = self.i + 1
                    self.layout.addWidget(imageLabel,self.i,self.j)
                    self.j = self.j + 1
                    self.z = self.z + 1