import imp
from statistics import mode
from PyQt5 import QtCore, QtGui, QtWidgets
from customPredicionHub import *
from DNNFunctions import DNNFunctions
from QMainWindow import Window
from threading import *
import numpy as np
from sklearn.metrics import classification_report


class Ui_loadModelUI(object):
    def setupUi(self, loadModelUI):
        loadModelUI.setObjectName("loadModelUI")
        loadModelUI.resize(400, 300)
        self.label = QtWidgets.QLabel(loadModelUI)
        self.label.setGeometry(QtCore.QRect(80, 10, 231, 71))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(loadModelUI)
        self.pushButton.setGeometry(QtCore.QRect(140, 220, 131, 61))
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(loadModelUI)
        self.label_2.setGeometry(QtCore.QRect(90, 190, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.progressBar = QtWidgets.QProgressBar(loadModelUI)
        self.progressBar.setGeometry(QtCore.QRect(50, 130, 331, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")

        self.retranslateUi(loadModelUI)
        QtCore.QMetaObject.connectSlotsByName(loadModelUI)

        self.pushButton.clicked.connect(lambda: Ui_loadModelUI.file_choose(loadModelUI))

    def retranslateUi(self, loadModelUI):
        _translate = QtCore.QCoreApplication.translate
        loadModelUI.setWindowTitle(_translate("loadModelUI", "Form"))
        self.label.setText(_translate("loadModelUI", "Load Model"))
        self.pushButton.setText(_translate("loadModelUI", "Choose Model"))
        self.label_2.setText(_translate("loadModelUI", "Please click to load model"))


    def thread(self):
        print("hre")
        t1 = Thread(target=self.evalmodel)
        t1.start

    def evalmodel(self):
        print("too")
        Y_test = np.argmax(DNNFunctions.test_y, axis=1) # Convert one-hot to index
        y_pred = np.argmax(DNNFunctions.model.predict(DNNFunctions.test_x, verbose=1), axis=-1)
        print(classification_report(Y_test, y_pred))

    def file_choose(loadModelUI):
        model_path = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
        print(model_path)
        if model_path != "":
            if (DNNFunctions.model_load(model_path) == True):
                print(DNNFunctions.loaded_model.name)     
                Ui_loadModelUI.thread(Ui_loadModelUI)          
                # loadModelUI.close()
                # Window.customPredHub(Window)
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('No Model found in directory')
                msg.setWindowTitle("Model Not Found")
                msg.exec_()
            
        

