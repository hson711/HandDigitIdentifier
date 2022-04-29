from asyncio.windows_events import NULL
import sys
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from QSideWindow import sideWindow, Ui_trainWindow
from customPredicionHub import customPredicionHub
from dropDownDatasets import dropDownDatasets, dropDownPhotoViewer
from DNNFunctions import DNNFunctions
from importDatasetScreen import importDatasetScreen
from PyQt5.QtWidgets import QMessageBox


class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle('Handwritten Digit/English Recognizer')
        self.setGeometry(300, 300, 400, 300)
        self._createMenu()
        
    def openSideWindow(self, checked):
        if (DNNFunctions.data_loaded != True):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Dataset has not been imported. Please Import dataset to train a model')
            msg.setWindowTitle("No dataset imported")
            msg.exec_()
        else:
            window = QWidget()
            window = uic.loadUi('testing3.ui')
            window.show()

    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&File")
        datasetAction = self.menu.addAction('&Import Dataset')
        datasetAction.triggered.connect(self.importDataset)
        datasetAction = self.menu.addAction('&Train Model')
        datasetAction.triggered.connect(self.openSideWindow)
        self.menu.addAction('&Quit', self.close)
        self.menu = self.menuBar().addMenu("&View")
        datasetAction = self.menu.addAction('&Custom Prediction')
        datasetAction.triggered.connect(self.openCustomPainter)
        self.menu = self.menu.addAction('&View Dataset')
        self.menu.triggered.connect(self.viewDatasetPhotos)


    
    def openCustomPainter(self, checked):
        self.customPredictionHub = customPredicionHub()
        self.customPredictionHub.show()

    def importDataset(self):
        if DNNFunctions.keys != NULL:
            self.dropDownDatasets = dropDownDatasets()
        else:
            self.dropDownDatasets = importDatasetScreen("")
        self.dropDownDatasets.show()
    
    def viewDatasetPhotos(self):
        if (DNNFunctions.data_loaded != True):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Dataset has not been imported. Please Import dataset to view')
            msg.setWindowTitle("No dataset imported")
            msg.exec_()
        else:
            self.viewDataset = dropDownPhotoViewer()
            self.viewDataset.show()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())