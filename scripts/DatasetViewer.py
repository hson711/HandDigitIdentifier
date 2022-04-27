import sys
import os
import imghdr
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication
from photoViewerWindow import photoViewerWindow
from PIL import Image


class datasetViewer():
    def __init__(self):
        super().__init__()
        dialog = QFileDialog()
        self.folderDir = dialog.getExistingDirectory(None, "Select Folder With Photos To Display")
        self.photoViewer()

    def photoViewer(self):
        self.w = photoViewerWindow()
        for file in os.listdir(self.folderDir):
            fileDir = os.path.join(self.folderDir, file)
            #self.w.convert_to_srgb(fileDir) #this isn't working for some reason
            self.w.showPhoto(fileDir)  