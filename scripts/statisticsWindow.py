import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLineEdit, QTextBrowser, QPushButton, QVBoxLayout)
from DNNFunctions import DNNFunctions

class statisticsWindow(QWidget):

    def __init__(self,array):
        super().__init__()
        self.countArr = array
        self.initUI(self.countArr)
        
    
    def initUI(self,array):
        self.tb = QTextBrowser()
        self.tb.setAcceptRichText(True)
        self.tb.setOpenExternalLinks(True)

        for i in range(62):
            self.temp = DNNFunctions.labels[i]
            self.count = array[i]
            text = ("Total occurances of ", str(self.temp), " in dataset is ", str(self.count), ".\n" )
            text = ("").join(text)
            self.tb.append(text)

        vbox = QVBoxLayout()
        vbox.addWidget(self.tb)

        self.setLayout(vbox)

        self.setWindowTitle('Statistics Window')
        self.setGeometry(300, 300, 300, 300)
        self.show()
