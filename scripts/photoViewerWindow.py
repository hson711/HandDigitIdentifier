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
import numpy as np
from statisticsWindow import statisticsWindow

#Class to view photos of the loaded test or train set of data
class photoViewerWindow(QMainWindow):

    #Initializes instance of photoViewerWindow class
    #Takes input of a string of what set to view photos of
    def __init__(self,set):

        super().__init__()
        self.initUI(set)

    #Setup of instances layout and associated variables
    #Takes input of what set to view photos of
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
        self.set = set

        #Initialize toolbar
        toolbar = QMenuBar()

        #Add toolbar actions and connect function to buttons
        filterPhotosAction = QAction("Filter", toolbar)
        toolbar.addAction(filterPhotosAction)
        filterPhotosAction.triggered.connect(self.filterPhotos)

        statisticsAction = QAction("Statistics",toolbar)
        statisticsAction.triggered.connect(self.statistics)
        toolbar.addAction(statisticsAction)

        #Setup layout and attach widgets
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
        self.setWindowTitle('Dataset Viewer')

        self.show()
        self.loadData()

    #Function that is called upon when the scrollbar experiences a value change event
    #Input: New value that the scroll bar has
    def scrolled(self, value):

        #Sets up an area near the bottom of the scrollbar but not at the very bottom to start loading the next photos, so scrolling becomes smoother
        tempValue = (self.scrollBar.maximum())
        maxValue = round(tempValue * 1)
        minValue = round(tempValue * 0.95)

        #If no filter then shows any photo otherwise only shows more filtered photos
        if value >= minValue and value <= maxValue :
            if self.filterText == None:
                self.showPhotoExsisting(self.lengthx, self.datax)
            else:
                self.showMoreFilteredPhotos(self.datax,self.filterText)

    #Function that is called when window is first opened and shows the first 1000 photos of the dataset
    def showPhoto(self, lengthx, datax):

        #Sets up counter placeholder in order to print 1000 photos from original starting point
        temp = self.z
        #Try clause in order to catch running out of photos to not crash code
        try:
            #Loop for self.z data up to self.z(starting self.z) + 1000
            while self.z <= temp + 1000:

                pm1 = DNNFunctions.convertNumpyArrayToImage(datax[self.z])
                if not pm1.isNull():

                    imageLabel = QLabel(self)
                    imageLabel.setPixmap(pm1)
                    #j and i loop to add widgets to grid layout in a series of 32 across
                    if self.j == 32:

                        self.j = 0
                        self.i = self.i + 1
                    #Sets up grid layout so theres no space or tear
                    self.layout.setColumnStretch(self.j,1)
                    self.layout.setRowStretch(self.i,1)
                    self.layout.addWidget(imageLabel,self.i,self.j)
                    #Increments loop variables
                    self.j = self.j + 1
                    self.z = self.z + 1
        #Catching eof clause
        except:
            pass

    #Function is called after filter button is pressed and is passed both the data to view and the filter text to use
    def showMoreFilteredPhotos(self,datax,filter):
        #Temp placeholder of z to only filter through the next 1000 photos, from starting pos
        ##temp = self.z
        temp = self.layout.count()
        #Try clause to catch running out of photos so index doesnt go out of bounds
        try:
            ###IMPROVEMENT: Could be to filter photos until the size of the widget is filled up
            ##while self.z <= temp + 1000:
            while self.layout.count() <= temp + 64:

                #Sets a string variable to be the current photo we are reviewings label
                string = (DNNFunctions.labels[self.datay[self.z]])

                #Compares label to filter and if equal then proceeds to show the photo on the widget
                if (filter.upper() == string.upper()):

                    #This part is the same as above function
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
        except:
            pass
    
    #Function to show more photos when scrolling if there is no filter placed
    #Takes length of dataset and dataset as input
    def showPhotoExsisting(self, lengthx, datax):
        #Sets place holder for self.z to calculate and show the next 32 pictures i.e 1 line
        temp = self.z
        #Try clause to catch index out of bounds when nearing end of dataset
        try:
            #Loops through the next 32 pictures of the dataset and shows them
            while self.z <= temp + 32:
                #Code is the same as previous codes
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
        except:
            pass
    
    #Function is called when filtered text is provided to setup and show the first set of filtered photos
    #Input: photoID = is the dataset array pos of the found filtered photo to print
    def showPhotoSpecific(self, photoID):
        try:
            #Code same as previous functions to convert 1 photo of index photoID
            pm1 = DNNFunctions.convertNumpyArrayToImage(self.datax[photoID])
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
        except:
            pass
    
    #Function is called on instance initialization to setup data depending on string given, either train or test set
    #Input is what test set to save as data
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
        

    #Function is connected to button that allows user input and saves the input as what filter to apply to shown photos
    def filterPhotos(self):
        #Creates a input dialog to enter string
        filterText, done1 = QtWidgets.QInputDialog.getText(self, 'Filtering', 'Enter text to filter:')
        if done1:
            #Calls filtered photo viewer function giving the filter text as input
            self.filteredPhotoViewer(filterText)

    #Function is called by the filter dialog to first clear layout then depending on filtered text take a range of actions
    #Input is the desired filter inputted by user
    def filteredPhotoViewer(self, filterText):
        #Calls the clear layout function that clears the grid layout of the window
        self.clearLayout()
        #If text is blank resets the photo viewer to depcit photos with no filter
        if (filterText == ""):
            self.filterText = None
            self.showPhoto(self.lengthx, self.datax)
            return
        else:
            self.filterText = filterText
        #Initializes variable for while loop
        k = 0
        #Adds filtered photos to the photo viewer until the widget count on the window reaches 700 which is approx 1 page of photos
        while self.layout.count() <= 700:
            string = (DNNFunctions.labels[self.datay[k]])
            #If the filter text is equal to the current photos label then we show that photo on the viewer
            if (filterText.upper() == string.upper()):
                self.showPhotoSpecific(k)
            k = k+1

    #Function is called to clear all widgets within the screens gridlayout
    def clearLayout(self):
        #Clears widgets
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().setParent(None)
        #Resets variables
        self.i = 0
        self.j = 0
        self.z = 0

    #Function is called from connected button to create an array counting how many times each label occurs in the data given and sends that to the statistics window
    def statistics(self):
        countArr = np.bincount(self.datay)
        self.wStatistics = statisticsWindow(countArr)
