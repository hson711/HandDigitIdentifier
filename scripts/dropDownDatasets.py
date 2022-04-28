from PyQt5.QtWidgets import QComboBox, QMainWindow, QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
import sys
from DNNFunctions import DNNFunctions
from importDatasetScreen import importDatasetScreen
import contextlib
from photoViewerWindow import photoViewerWindow

class dropDownDatasets(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Chose dataset to use')
        self.combobox = QComboBox()
        for k in DNNFunctions.keys:
            self.combobox.addItem(k)
        
        layout = QVBoxLayout()
        layout.addWidget(self.combobox)
        self.setCentralWidget(self.combobox)

        self.combobox.currentTextChanged.connect(self.text_changed)
        self.combobox.activated.connect(self.text_changed)

    def text_changed(self):
        with contextlib.redirect_stdout(None):
            self.s = self.combobox.currentText()
        self.importDataSets()
        self.close()

    def importDataSets(self):
        self.importDatasetScreen = importDatasetScreen(self.s)
        self.importDatasetScreen.show()

class dropDownPhotoViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Chose dataset to use')
        self.setGeometry(300, 300, 200, 150)

        self.combobox = QComboBox()
        self.combobox.addItem('Train Set')
        self.combobox.addItem('Test Set')

        layout = QVBoxLayout()
        layout.addWidget(self.combobox)
        self.setCentralWidget(self.combobox)

        self.combobox.currentTextChanged.connect(self.text_changed)
        self.combobox.activated.connect(self.text_changed)

    def text_changed(self):
        with contextlib.redirect_stdout(None):
            self.s = self.combobox.currentText()
        self.photoViewerWindow()
        self.close()
    
    def photoViewerWindow(self):
        self.w = photoViewerWindow(self.s)