import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLineEdit, QTextBrowser, QPushButton, QVBoxLayout)
from DNNFunctions import DNNFunctions

#Class to create a QWidget window that tells you basic statistics of the loaded dataset in the photo viewer
class statisticsWindow(QWidget):

    #Initializes instance and sets basic variables
    #Input: is the bincount array that was created right before calling this function, which holds data on how many times each label occurs in the dataset
    def __init__(self,array):

        super().__init__()
        self.countArr = array
        self.initUI(self.countArr)
        
    #Initialize the text viewer
    #Input is the array that was passed on initialization
    def initUI(self,array):
        self.tb = QTextBrowser()
        self.tb.setAcceptRichText(True)
        self.tb.setOpenExternalLinks(True)

        #For loop that for the length of the data labels prints out the label and how many times it occurs
        for i in range(len(DNNFunctions.labels)):

            self.temp = DNNFunctions.labels[i]

            try:
                self.count = array[i]
                text = ("Total occurances of ", str(self.temp), " in dataset is ", str(self.count), ".\n" )
                text = ("").join(text)
                self.tb.append(text)

            except:
                self.count = 0

        #Sets up layout and geometry
        vbox = QVBoxLayout()
        vbox.addWidget(self.tb)

        self.setLayout(vbox)

        self.setWindowTitle('Statistics Window')
        self.setGeometry(300, 300, 300, 300)
        self.show()
