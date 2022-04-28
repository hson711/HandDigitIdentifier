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
class customPainter(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.points = QtGui.QPolygon()
        pixmap = QtGui.QPixmap(600,300)
        self.setPixmap(pixmap)
        self.setWindowTitle('Custom Painter')
        pal = self.palette()
        pal.setColor(QPalette.Background, Qt.black)
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        self.show()
    
    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.draw_point(qp)
        qp.end()


    def draw_point(self, qp):
        qp.setPen(QPen(Qt.white,  20))
        qp.drawPoints(self.points)

    def mouseMoveEvent(self, e):
        self.points << e.pos()
        self.update()

    def submitPicture(self):
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(self.winId() )
        screenshot.save('screenshot.png', 'png')


class ToolbarWindow(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Digit Painter')

        layout = QHBoxLayout(self)
        self.setGeometry(300, 300, 400, 300)
        self.widget = customPainter()

        toolbar = QMenuBar()
        paintClearAction = QAction("Submit Picture", toolbar)
        toolbar.addAction(paintClearAction)
        paintClearAction.triggered.connect(self.submitCustomPicture)
        layout.setMenuBar(toolbar)
        layout.addWidget(self.widget)

    def submitCustomPicture(self):
        self.widget.submitPicture()
        self.close()
