from json.tool import main
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic, QtGui
import pathlib

from DNNFunctions import DNNFunctions

class Ui_trainWindow(object):
    def setupUi(self, trainWindow):
        super().__init__()
        trainWindow.setObjectName("trainWindow")
        trainWindow.resize(400, 300)
        self.comboBox = QComboBox(trainWindow)
        self.comboBox.setGeometry(QtCore.QRect(40, 60, 53, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.spinBox = QSpinBox(trainWindow)
        self.spinBox.setGeometry(QtCore.QRect(140, 60, 42, 22))
        self.spinBox.setObjectName("spinBox")
        self.spinBox_2 = QSpinBox(trainWindow)
        self.spinBox_2.setGeometry(QtCore.QRect(240, 60, 42, 22))
        self.spinBox_2.setObjectName("spinBox_2")
        self.commandLinkButton = QCommandLinkButton(trainWindow)
        self.commandLinkButton.setGeometry(QtCore.QRect(130, 160, 167, 41))
        self.commandLinkButton.setObjectName("commandLinkButton")

        self.retranslateUi(trainWindow)
        QtCore.QMetaObject.connectSlotsByName(trainWindow)

    def retranslateUi(self, trainWindow):
        _translate = QtCore.QCoreApplication.translate
        trainWindow.setWindowTitle(_translate("trainWindow", "Form"))
        self.comboBox.setItemText(0, _translate("trainWindow", "adma"))
        self.comboBox.setItemText(1, _translate("trainWindow", "sfg"))
        self.comboBox.setItemText(2, _translate("trainWindow", "nadam"))
        self.commandLinkButton.setText(_translate("trainWindow", "CommandLinkButton"))

class sideWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Train Model:')

        # self.spinBox1 = QSpinBox()
        
        # self.spinBox2 = QSpinBox()

        # self.combobox1 = QComboBox()
        # self.combobox1.addItems(['Adam', 'SFG'])

        # mainLayout = QVBoxLayout()
        # mainLayout.addWidget(self.combobox1, 0, 0)
        # self.setLayout(mainLayout)

        #uic('test.ui',self)

        #SpinBox
        epochSelection = 2

        #Spinbox
        batchSizeSelection = 100

        #Combobox (possible options: adam,sfg,nadam etc.)
        chosenOptimiser = 'adam'

        self.process.start('python',['-u','QSideWindow.py'])
        DNNFunctions.train(epochSelection,batchSizeSelection,chosenOptimiser)

        
        
        # results = DNNFunctions.model.evaluate(DNNFunctions.raw_test_x, DNNFunctions.raw_test_y, batch_size=128)
        # output = "test loss: {}, test acc: {}".format(results[0], results[1]) 
        # self.label = QLabel(output)




