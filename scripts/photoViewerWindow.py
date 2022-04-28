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


class photoViewerWindow(QMainWindow):
    def __init__(self,folderDir):
        super().__init__()
        self.initUI()
        self.folderDir = folderDir
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
        filterPhotosAction.triggered.connect(self.filterPhotos)
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


    def showPhoto(self, photoFileDir):
        pm = QPixmap(photoFileDir)
        if not pm.isNull():
            larger_pm = pm.scaled(400,400)
            imageLabel = QLabel(self)
            imageLabel.setPixmap(larger_pm)
            if self.j == 3:
                self.j = 0
                self.i = self.i + 1
            self.layout.addWidget(imageLabel,self.i,self.j)
            self.j = self.j + 1
    
    
    #taken from https://stackoverflow.com/questions/65463848/pyqt5-fromiccprofile-failed-minimal-tag-size-sanity-error
    def convert_to_srgb(self,file_path):
        '''Convert PIL image to sRGB color space (if possible)'''
        img = Image.open(file_path)
        icc = img.info.get('icc_profile', '')
        if icc:
            io_handle = io.BytesIO(icc)     # virtual file
            src_profile = ImageCms.ImageCmsProfile(io_handle)
            dst_profile = ImageCms.createProfile('sRGB')
            img_conv = ImageCms.profileToProfile(img, src_profile, dst_profile)
            icc_conv = img_conv.info.get('icc_profile','')
        if icc != icc_conv:
            # ICC profile was changed -> save converted file
            img_conv.save(file_path,
                        format = 'JPEG',
                        quality = 50,
                        icc_profile = icc_conv)

    def photoViewer(self):
        for file in os.listdir(self.folderDir):
            fileDir = os.path.join(self.folderDir, file)
            #self.convert_to_srgb(fileDir) #this isn't working for some reason
            self.showPhoto(fileDir)
    
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