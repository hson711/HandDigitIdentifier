import sys
from xmlrpc.client import Boolean
from PyQt5.QtWidgets import (QApplication, QDialog, QProgressBar, QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import QThread, pyqtSignal
from numpy import NaN, integer
from DNNFunctions import *
import contextlib
import io
import threading
import gevent
import subprocess
from subprocess import *
from PyQt5.QtWidgets import (QApplication, QWidget, QLineEdit, QTextBrowser, QPushButton, QVBoxLayout)

class Thread(QThread):
    update_signal1 = pyqtSignal(str)
    update_signal3 = pyqtSignal(str)
    closeSignal = pyqtSignal()

    def __init__(self, string,  *args, **kwargs):
        super(Thread, self).__init__(*args, **kwargs)
        self.Finished   = False
        self.string = string
        self.running = True

    def run(self):
        while self.running :
            if os.path.isfile(DNNFunctions.pathFile) == False:
                self.p = subprocess.Popen([sys.executable, 'C:\CodingTemp\CS302 Project 1\HandDigitIdentifier\scripts\SubprocessImporter.py', self.string], stdout = PIPE)
                for i in range(5):
                    self.realtime_output = self.p.stdout.readline()
                maxValue = self.realtime_output.decode("cp1252")
                self.update_signal3.emit(maxValue.strip())
                while True:
                    self.realtime_output = self.p.stdout.readline()
                    if self.realtime_output == '' and self.p.poll() is None:
                        DNNFunctions.openPreDownloadedDataset(self.string)
                        self.closeSignal.emit()
                        break

                    if self.realtime_output:
                        self.realtime_output = self.realtime_output.decode("cp1252")
                        self.update_signal1.emit(self.realtime_output.strip())
            else:
                DNNFunctions.openPreDownloadedDataset(self.string)
                print(DNNFunctions.raw_train_y.shape)
            
            #stdout, stderr = p.communicate()
            #time.sleep(1000)
            #DNNFunctions.loadEMNIST(self.string)

    def stop(self):
        self.running = False
        self.p.terminate()

class importDatasetScreen(QDialog):
    maxValue = 1000

    def __init__(self,string):
        super().__init__()
        self.string = string
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Importing')
        self.progress = QProgressBar()
        self.progress.setGeometry(0, 0, 1000, 500)
        self.progress.setMaximum(importDatasetScreen.maxValue)
        self.progress.setValue(0)
        self.savedEMNIST = False

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        self.progress.setStyleSheet("QProgressBar {border: 2px solid grey;border-radius:8px;padding:1px}" "QProgressBar::chunk {background:yellow}")
        self.progress.setStyleSheet("QProgressBar::chunk {background: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 red, stop: 1 white); }")
        self.progress.setTextVisible(False)

        self.button = QPushButton('Start')
        self.button.setStyleSheet('background-color:yellow')
        self.button2 = QPushButton('Stop')
        self.button2.setStyleSheet('background-color:yellow')
        self.button2.setEnabled(False)
        self.button3 = QPushButton('Clear Cache')
        self.button3.setStyleSheet('background-color:yellow')
        self.tb = QTextBrowser()
        self.tb.setAcceptRichText(True)
        self.tb.setOpenExternalLinks(True)

        vbox.addWidget(self.tb)
        vbox.addWidget(self.progress)
        hbox.addWidget(self.button)
        hbox.addWidget(self.button2)
        hbox.addWidget(self.button3)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.button.clicked.connect(self.onButtonClick)
        self.button2.clicked.connect(self.on_stop)
        self.button3.clicked.connect(self.clearCache)
        self.thread2 = Thread(string=(self.string))
        self.thread2.update_signal1.connect(self.downloaded)
        self.thread2.update_signal3.connect(self.setMaximum)
        self.thread2.closeSignal.connect(self.close)

    def onButtonClick(self):
        self.button2.setEnabled(True)
        self.progress.setValue(0)
        self.thread2.running = True
        self.thread2.start()
        self.button.setEnabled(False)
        self.button3.setEnabled(False)

    def update(self, val):
        self.progress.setValue(val)
        

    def on_stop(self):
        self.thread2.stop()
        self.button.setEnabled(True)
        self.button3.setEnabled(True)
        self.button2.setEnabled(False)

    def clearCache(self):
        DNNFunctions.clearCache()

    def downloaded(self,string):
        string = string.strip()
        string = string[-5:]
        string = string.split(":")
        if  string[0].isdigit() and string[1].isdigit():
            min = int(float(string[0]))
            sec = int(float(string[1]))
        else:
            min = 0
            sec = 0
        minSec = min*60
        deductableTime = minSec + sec
        text = ("Time left till data is imported is ", str(min), " mins and ", str(sec), " seconds.\n" )
        text = ("").join(text)
        self.tb.append(text)
        tempMax = self.progress.maximum()
        self.progress.setValue(tempMax-deductableTime)

    def setMaximum(self,value):
        string = value.strip()
        string = string[-5:]
        string = string.split(":")
        if  string[0].isdigit() and string[1].isdigit():
            min = int(string[0]) * 60
            sec = int(string[1])
        else:
            min = 0
            sec = 0
        time = min + sec
        self.progress.setMaximum(time)
        self.progress.setValue(0)
