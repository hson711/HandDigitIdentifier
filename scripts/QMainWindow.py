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
from PyQt5 import QtCore, QtGui, QtWidgets
from QSideWindow import sideWindow
from DatasetViewer import datasetViewer
from customPredicionHub import customPredicionHub
from importDatasetScreen import importDatasetScreen


class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle('Handwritten Digit/English Recognizer')
        self.setGeometry(300, 300, 400, 300)
        self._createMenu()
        
    def openSideWindow(self, checked):
        self.w = sideWindow()
        self.w.show()

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
        self.importDatasetScreen = importDatasetScreen()
        self.importDatasetScreen.show()
    
    def viewDatasetPhotos(self):
        self.viewDataset = datasetViewer()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())