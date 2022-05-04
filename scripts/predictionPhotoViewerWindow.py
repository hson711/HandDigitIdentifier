from importlib.resources import path
from PyQt5.QtWidgets import (QWidget, QLabel, QScrollArea, QMainWindow)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from DNNFunctions import DNNFunctions
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
            predictedValue = DNNFunctions.predict(i)
            DNNFunctions.predictedValue = str(predictedValue)
            if not pix.isNull():
                    imageLabel = QLabel(self)
                    imageLabel.setPixmap(pix)
                    tempString = (" Prediction: {}".format(DNNFunctions.predictedValue))
                    accuracy =round(DNNFunctions.loaded_model_results[1]*100,2)
                    tempString2 = (" Accuracy: {}%".format(accuracy))
                    tempString = (tempString + '\n' + tempString2) 
                    predictionLabel = QLabel(tempString,self)
                    if self.j == 2:
                        self.j = 0
                        self.i = self.i + 1
                    self.layout.addWidget(imageLabel,self.i,self.j)
                    self.j = self.j + 1
                    self.z = self.z + 1
                    self.layout.addWidget(predictionLabel,self.i,self.j)
                    self.j = self.j + 1
                    self.z = self.z + 1