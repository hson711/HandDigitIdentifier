import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication
class datasetViewer():
    def __init__(self):
        super().__init__()
        dialog = QFileDialog()
        self._folder_path = dialog.getExistingDirectory(None, "Select Folder With Photos To Display")
        print(self._folder_path)