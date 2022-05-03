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
from QSideWindow import Ui_trainWindow
from customPredicionHub import customPredicionHub
from dropDownDatasets import dropDownDatasets, dropDownPhotoViewer
from DNNFunctions import DNNFunctions
from importDatasetScreen import importDatasetScreen
from PyQt5.QtWidgets import QMessageBox
from loadModel import *
from modelLoad import modelLoad
from trainWindow import *

#Class that creates the main menu window
class Window(QMainWindow):

    #Main Window Initializer Function
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Handwritten Digit/English Recognizer')
        self.setGeometry(300, 300, 400, 300)
        self._createMenu()
        
    
    #Input: Main Window Instance
    #Output:Dataset Training Window
    #Function called upon by main window toolbar to access a new window to train installed dataset
    def openSideWindow(self):

        if (DNNFunctions.data_loaded != True):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Dataset has not been imported. Please Import dataset to train a model')
            msg.setWindowTitle("No dataset imported")
            msg.exec_()
        else:
            self.trainWindow = trainWindow()
            self.trainWindow.show()
            # self.trainWindow = QWidget()
            # trainUi = Ui_trainWindow()
            # trainUi.setupUi(self.trainWindow)
            # self.trainWindow.show()

    #Input: Main Window Instance
    #Output: Main Window Toolbar and connections
    #Function called upon by main window instance to set the toolbar and initialize its connections to functions
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


    #Input: Main Window Instance
    #Output: Custom Painter Menu Window
    #Function called upon to create a new window to predict custom dataset
    def openCustomPainter(self):
        if (DNNFunctions.data_loaded != True):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Dataset has not been imported. Please Import dataset to view')
            msg.setWindowTitle("No dataset imported")
            msg.exec_()
        else:
            self.modelLoad = modelLoad()
            self.modelLoad.show()
        
        
    #Input: Main Window Instance
    #Output: dropDownDatasets Window/ Import Dataset Screen
    #Function that checks if the data is downloaded and if it is already downloaded opens up a screen to ask what specific data set to use, otherwise just opens the downloading
    #data screen menu
    def importDataset(self):

        if DNNFunctions.keys != NULL:
            self.dropDownDatasets = dropDownDatasets()
        else:
            self.dropDownDatasets = importDatasetScreen("")

        self.dropDownDatasets.show()
    
    #Input: Main Window Instance
    #Output: Error Message/ Drop Down Photo Viewer Instance
    #A function that checks if dataset is loaded, if not displays an error, otherwise it opens a dataset viewer screen
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
    
    #Input: Main Window Instance
    #Output: Custom Prediction Hub Instance
    #Function that when called opens the custom prediction hub window
    ## CURRENTLY UNUSED ##
    def customPredHub(self):
        self.customPredictionHub = customPredicionHub()
        self.customPredictionHub.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())