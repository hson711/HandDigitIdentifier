from customPainter import customPainter, ToolbarWindow
import sys
from PyQt5.QtWidgets import *
from DNNFunctions import DNNFunctions

## Qdialog Class that gives users the submission option for prediction of custom data
class customPredicionHub(QDialog):

    def __init__(self):
        super().__init__()
        self.initUI()
    
    #Initializes instance
    def initUI(self):

        self.setWindowTitle("Choose custom prediction option")
        self.setGeometry(200, 500, 300, 100)

        hbox = QHBoxLayout()

        button1 = QPushButton('Premade Photos')
        button1.clicked.connect(self.on_click1)

        button2 = QPushButton('Custom Photo')
        button2.clicked.connect(self.on_click2)

        hbox.addWidget(button1)
        hbox.addWidget(button2)

        self.setLayout(hbox)
    
    #Function linked to button1 to select premade photos as the submission option
    def on_click1(self):

        fileNames = QFileDialog.getOpenFileNames(self,("Open Image"), "", ("Image Files (*.png *.jpg *.bmp)"))
        print(fileNames[0])

    #Function linked to button2 to select custom drawn photo as the submission option
    def on_click2(self):
        # self.paint = QDialog()
        # painterUI = Ui_Dialog()
        # painterUI.setupUi(self.paintWindow)
        # self.loadModel.show()

        self.customPainterWindow = ToolbarWindow()
        self.customPainterWindow.show()