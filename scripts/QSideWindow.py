from json.tool import main
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic, QtGui
import pathlib

from DNNFunctions import DNNFunctions

class Ui_trainWindow(object):
    def setupUi(self, trainWindow):
        trainWindow.setObjectName("trainWindow")
        trainWindow.resize(400, 301)
        self.comboBox = QComboBox(trainWindow)
        self.comboBox.setGeometry(QtCore.QRect(60, 80, 61, 31))
        font = QtGui.QFont()
        font.setFamily("HP Simplified")
        font.setPointSize(10)
        self.comboBox.setFont(font)
        self.comboBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.spinBox = QSpinBox(trainWindow)
        self.spinBox.setGeometry(QtCore.QRect(170, 80, 61, 31))
        self.spinBox.setObjectName("spinBox")
        self.spinBox_2 = QSpinBox(trainWindow)
        self.spinBox_2.setGeometry(QtCore.QRect(290, 80, 51, 31))
        self.spinBox_2.setObjectName("spinBox_2")
        self.label = QLabel(trainWindow)
        self.label.setGeometry(QtCore.QRect(40, 10, 301, 41))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic")
        font.setPointSize(23)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QLabel(trainWindow)
        self.label_2.setGeometry(QtCore.QRect(160, 50, 71, 20))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QLabel(trainWindow)
        self.label_3.setGeometry(QtCore.QRect(64, 120, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QLabel(trainWindow)
        self.label_4.setGeometry(QtCore.QRect(150, 120, 101, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QLabel(trainWindow)
        self.label_5.setGeometry(QtCore.QRect(280, 120, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QLabel(trainWindow)
        self.label_6.setGeometry(QtCore.QRect(270, 180, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.pushButton = QPushButton(trainWindow)
        self.pushButton.setGeometry(QtCore.QRect(120, 246, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QLineEdit(trainWindow)
        self.lineEdit.setGeometry(QtCore.QRect(52, 200, 301, 20))
        self.lineEdit.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.lineEdit.setAutoFillBackground(False)
        self.lineEdit.setText("")
        self.lineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(trainWindow)
        QtCore.QMetaObject.connectSlotsByName(trainWindow)

    def retranslateUi(self, trainWindow):
        _translate = QtCore.QCoreApplication.translate
        trainWindow.setWindowTitle(_translate("trainWindow", "Form"))
        self.comboBox.setItemText(0, _translate("trainWindow", "Adam"))
        self.comboBox.setItemText(1, _translate("trainWindow", "SGD"))
        self.comboBox.setItemText(2, _translate("trainWindow", "Nadam"))
        self.label.setText(_translate("trainWindow", "Training a model"))
        self.label_2.setText(_translate("trainWindow", "Choose Specs"))
        self.label_3.setText(_translate("trainWindow", "Optimiser"))
        self.label_4.setText(_translate("trainWindow", "Number of Epochs"))
        self.label_5.setText(_translate("trainWindow", "Batch Size"))
        self.label_6.setText(_translate("trainWindow", "Model Name"))
        self.pushButton.setText(_translate("trainWindow", "Train the model"))


class sideWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Train Model:')

        self.spinBox1 = QSpinBox()
        
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




