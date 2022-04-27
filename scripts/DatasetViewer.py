import sys
import os
import imghdr
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication
from photoViewerWindow import photoViewerWindow


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
            self.w.showPhoto(fileDir)
        