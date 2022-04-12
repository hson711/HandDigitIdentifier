import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QAction, qApp
from PyQt5 import QtCore, uic
from PyQt5 import QtGui
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QToolBar, QWidget, QMenuBar
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QAction, QStatusBar
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon

class customPainter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.points = QtGui.QPolygon()
        self.clear = False
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Custom Painter')
        self.show()
    
    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_point(qp)
        if self.clear:
            canvas = QtGui.QPixmap(400, 300)
            canvas.fill(QtGui.QColor('#ffffff'))
            print("hi")
            self.clear = False
        qp.end()

    def clearPaint(self):
        self.update()

    def draw_point(self, qp):
        qp.setPen(QPen(Qt.black,  5))
        qp.drawPoints(self.points)

    def mouseMoveEvent(self, e):
        self.points << e.pos()
        self.update()

    def clearPaint(self):
        self.clear = True

class SecondExample(QDialog):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)
        self.setGeometry(300, 300, 400, 300)
        self.widget = customPainter()

        toolbar = QMenuBar()
        paintClearAction = QAction("Clear Paint", toolbar)
        toolbar.addAction(paintClearAction)
        paintClearAction.triggered.connect(self.widget.clearPaint)


        layout.setMenuBar(toolbar)
        layout.addWidget(self.widget)
