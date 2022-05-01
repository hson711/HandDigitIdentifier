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
        self.chosenEpoch.setGeometry(QtCore.QRect(180, 80, 61, 31))
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
        self.subtext.setGeometry(QtCore.QRect(170, 50, 71, 20))
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
        self.label_4.setGeometry(QtCore.QRect(160, 120, 101, 20))
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
        self.label_6.setGeometry(QtCore.QRect(270, 200, 81, 20))
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
        self.modelName = QtWidgets.QLineEdit(trainWindow)
        self.modelName.setGeometry(QtCore.QRect(52, 220, 301, 20))
        self.modelName.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.modelName.setAutoFillBackground(False)
        self.modelName.setText("")
        self.modelName.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.modelName.setObjectName("modelName")
        self.horizontalSlider = QtWidgets.QSlider(trainWindow)
        self.horizontalSlider.setGeometry(QtCore.QRect(50, 160, 301, 20))
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.horizontalSlider.setTickInterval(10)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.label_7 = QtWidgets.QLabel(trainWindow)
        self.label_7.setGeometry(QtCore.QRect(330, 180, 31, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(trainWindow)
        self.label_8.setGeometry(QtCore.QRect(-40, 180, 191, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(trainWindow)
        self.label_9.setGeometry(QtCore.QRect(100, 140, 201, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(trainWindow)
        self.label_10.setGeometry(QtCore.QRect(350, 160, 41, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")

        self.retranslateUi(trainWindow)
        QtCore.QMetaObject.connectSlotsByName(trainWindow)

        #Choosing the validation ratio
        self.horizontalSlider.valueChanged[int].connect(self.updateSliderVal)

        #Training the Model
        self.pushButton.clicked.connect(lambda: self.train_model(self.chosenOptimiser.currentText().lower(),self.chosenEpoch.value(), self.batchSize.value(), self.modelName.text()))
    

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
        self.label_7.setText(_translate("trainWindow", "100"))
        self.label_8.setText(_translate("trainWindow", "0"))
        self.label_9.setText(_translate("trainWindow", "Split the training dataset for validation (%)"))
        self.label_10.setText(_translate("trainWindow", "0%"))
        
        for k in DNNFunctions.keys:
            print (k)

    def updateSliderVal(self, value):
        self.label_10.setText(QtCore.QCoreApplication.translate("trainWindow", str(value)+"%"))


    def train_model(checked,chosenOptimiser, chosenEpoch, batchSize, modelName):

        #Note, the argument checked is used due to the functionality of qt5 buttons outputting with object call argument which can be considered as not requried for this function
        print("here")
        print(chosenOptimiser)
        print(chosenEpoch)
        print(batchSize)
        #Can maybe add warning for high epoch
        

        DNNFunctions.train(chosenOptimiser, chosenEpoch, batchSize, modelName)
        print("Training done") #For testing purposes

        Ui_trainWindow.save_model_popup(Ui_trainWindow)
    
    
    def save_model_popup(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Would you like to save your model?")
        msgBox.setWindowTitle("QMessageBox Example")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Yes:
            file_path = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
            print(file_path)
            DNNFunctions.model.save(file_path+"/"+DNNFunctions.model.name)
            self.model_saved_success()

    def model_saved_success():
        msg = QMessageBox()
        msg.setText("Save Successful")
        msg.setInformativeText('Your model has been saved successfully ')
        msg.setWindowTitle("Save Successful")
        msg.exec_()
