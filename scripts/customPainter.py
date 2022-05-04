import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QAction, qApp
from PyQt5 import QtCore, uic, QtWidgets
from PyQt5 import QtGui
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QToolBar, QWidget, QMenuBar
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QAction, QStatusBar
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from DNNFunctions import DNNFunctions
import pathlib

#Custom Painter Class allows the user to draw a custom picture which can be used by the Neural Network for predictions
class customPainter(QtWidgets.QLabel):
    
    predicion = ''

    #Initializes Instance of the class
    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):

        #Initializes a Pixmap and Points
        self.points = QtGui.QPolygon()

        pixmap = QtGui.QPixmap(280,280)
        self.setPixmap(pixmap)

        self.setWindowTitle('Custom Painter')

        pal = self.palette()
        pal.setColor(QPalette.Background, Qt.black)

        self.setAutoFillBackground(True)
        self.setPalette(pal)
        self.show()
    
    #Function that begins a painting event and calls the draw points function
    def paintEvent(self, e):

        qp = QtGui.QPainter()

        qp.begin(self)
        self.draw_point(qp)
        qp.end()

    #Function that is given the painter instance and proceeds to draw points at the instances points which are continously updated in real time
    #Also sets pen color to white to replicate dataset imagery
    def draw_point(self, qp):

        qp.setPen(QPen(Qt.white,  20))
        qp.drawPoints(self.points)

    #function that changes the instances points to the position of the mouse and takes mouse event as input
    def mouseMoveEvent(self, e):
        #Sets points to be drawn to mouses position when mouse is clicked
        self.points << e.pos()
        #Updates painter to show the new drawn points
        self.update()

    #Function to take a screenshot of the drawn picture and save it in the folder as screenshot.jpg
    #Then proceeds to call the predict function on the screenshot
    def submitPicture(self):

        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(self.winId() )

        file_path = str(pathlib.Path(__file__).parent.resolve())
        temp_save_loc = file_path+'/../bin/screenshot.jpg'
        screenshot.save(temp_save_loc, 'jpg')
        predictedValue = DNNFunctions.predict(temp_save_loc)
        DNNFunctions.predictedValue = str(predictedValue)
        # ToolbarWindow.label
        # ToolbarWindow.label.setText('Prediction: {}'.format(DNNFunctions.predict(temp_save_loc)))

#ToolbarWindow class exsists to be the parent layout to the painter class so that the painter class has a usable toolbar attached
class ToolbarWindow(QDialog):
    #Initializes instance of ToolbarWindow
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Digit Painter')
        self.label = QLabel('Prediction: ', self)
        self.accuracyLabel = QLabel('Accuracy: ', self)

        layout = QHBoxLayout(self)
        layout2 = QVBoxLayout()

        self.setGeometry(300, 300, 300, 300)
        self.widget = customPainter()

        #Creates a toolbar and toolbar action and connects it to the submit function
        toolbar = QMenuBar()
        submitPicture = QAction("Submit Picture", toolbar)
        toolbar.addAction(submitPicture)
        submitPicture.triggered.connect(self.submitCustomPicture)

        #Sets up layout of the toolbar
        layout.setMenuBar(toolbar)
        layout.addWidget(self.widget)
        layout2.addWidget(self.label)
        layout2.addWidget(self.accuracyLabel)
        layout.addLayout(layout2)

    def submitCustomPicture(self):
        self.widget.submitPicture()
        tempString = ("Prediction: {}".format(DNNFunctions.predictedValue))
        accuracy =DNNFunctions.loaded_model_results[1]*100
        tempString2 = ("Accuracy: {}%".format(accuracy))
        self.label.setText(tempString)
        self.accuracyLabel.setText(tempString2)

        
