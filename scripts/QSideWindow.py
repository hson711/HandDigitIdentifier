from json.tool import main
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import pathlib

from DNNFunctions import DNNFunctions


#Created using QTdesigner from the trainWindow.ui


class Ui_trainWindow(object):
    def setupUi(self, trainWindow):
        trainWindow.setObjectName("trainWindow")
        trainWindow.resize(400, 301)
        self.chosenOptimiser = QtWidgets.QComboBox(trainWindow)
        self.chosenOptimiser.setGeometry(QtCore.QRect(50, 80, 81, 31))
        font = QtGui.QFont()
        font.setFamily("HP Simplified")
        font.setPointSize(10)
        self.chosenOptimiser.setFont(font)
        self.chosenOptimiser.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.chosenOptimiser.setEditable(False)
        self.chosenOptimiser.setObjectName("chosenOptimiser")
        self.chosenOptimiser.addItem("")
        self.chosenOptimiser.addItem("")
        self.chosenOptimiser.addItem("")
        self.chosenEpoch = QtWidgets.QSpinBox(trainWindow)
        self.chosenEpoch.setGeometry(QtCore.QRect(170, 80, 61, 31))
        self.chosenEpoch.setMinimum(1)
        self.chosenEpoch.setObjectName("chosenEpoch")
        self.batchSize = QtWidgets.QSpinBox(trainWindow)
        self.batchSize.setGeometry(QtCore.QRect(290, 80, 61, 31))
        self.batchSize.setMinimum(1)
        self.batchSize.setMaximum(1000000)
        self.batchSize.setObjectName("batchSize")
        self.header = QtWidgets.QLabel(trainWindow)
        self.header.setGeometry(QtCore.QRect(40, 10, 301, 41))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic")
        font.setPointSize(23)
        self.header.setFont(font)
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.header.setObjectName("header")
        self.subtext = QtWidgets.QLabel(trainWindow)
        self.subtext.setGeometry(QtCore.QRect(160, 50, 71, 20))
        self.subtext.setAlignment(QtCore.Qt.AlignCenter)
        self.subtext.setObjectName("subtext")
        self.label_3 = QtWidgets.QLabel(trainWindow)
        self.label_3.setGeometry(QtCore.QRect(64, 120, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(trainWindow)
        self.label_4.setGeometry(QtCore.QRect(150, 120, 101, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(trainWindow)
        self.label_5.setGeometry(QtCore.QRect(280, 120, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(trainWindow)
        self.label_6.setGeometry(QtCore.QRect(270, 180, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.pushButton = QtWidgets.QPushButton(trainWindow)
        self.pushButton.setGeometry(QtCore.QRect(120, 246, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(trainWindow)
        self.lineEdit.setGeometry(QtCore.QRect(52, 200, 301, 20))
        self.lineEdit.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.lineEdit.setAutoFillBackground(False)
        self.lineEdit.setText("")
        self.lineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(trainWindow)
        self.pushButton.clicked.connect(lambda: self.train_model(self.chosenOptimiser.currentText().lower(),self.chosenEpoch.value(), self.batchSize.value()))
        QtCore.QMetaObject.connectSlotsByName(trainWindow)

    def retranslateUi(self, trainWindow):
        _translate = QtCore.QCoreApplication.translate
        trainWindow.setWindowTitle(_translate("trainWindow", "Form"))
        self.chosenOptimiser.setItemText(0, _translate("trainWindow", "Adam"))
        self.chosenOptimiser.setItemText(1, _translate("trainWindow", "SGD"))
        self.chosenOptimiser.setItemText(2, _translate("trainWindow", "Nadam"))
        self.header.setText(_translate("trainWindow", "Training a model"))
        self.subtext.setText(_translate("trainWindow", "Choose Specs"))
        self.label_3.setText(_translate("trainWindow", "Optimiser"))
        self.label_4.setText(_translate("trainWindow", "Number of Epochs"))
        self.label_5.setText(_translate("trainWindow", "Batch Size"))
        self.label_6.setText(_translate("trainWindow", "Model Name"))
        self.pushButton.setText(_translate("trainWindow", "Train the model"))



    def train_model(checked,chosenOptimiser, chosenEpoch, batchSize):

        #Note, the argument checked is used due to the functionality of qt5 buttons outputting with object call argument which can be considered as not requried for this function
        print("here")
        print(chosenOptimiser)
        print(chosenEpoch)
        print(batchSize)
        #Can maybe add warning for high epoch

        DNNFunctions.train(chosenOptimiser, chosenEpoch, batchSize)
        print("Training done") #For testing purposes


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




