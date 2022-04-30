import sys
from xmlrpc.client import Boolean
from PyQt5.QtWidgets import (QApplication, QDialog, QProgressBar, QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import QThread, pyqtSignal
from DNNFunctions import *
import contextlib
import io
import threading
import gevent
import subprocess
from subprocess import *
import time

class Thread(QThread):
    update_signal1 = pyqtSignal(Boolean) 

    def __init__(self, string,  *args, **kwargs):
        super(Thread, self).__init__(*args, **kwargs)
        self.Finished   = False
        self.string = string
        self.running = True

    def run(self):
        while self.running :
            self.p = subprocess.Popen([sys.executable, 'C:\CodingTemp\CS302 Project 1\HandDigitIdentifier\scripts\SubprocessImporter.py', self.string], stdout = PIPE)
            while True:
                self.realtime_output = self.p.stdout.readline()

                if self.realtime_output == '' and self.p.poll() is not None:
                    break

                if self.realtime_output:
                    print(self.realtime_output.strip(), flush=True)
            if self.p.poll() is None:
                DNNFunctions.openPreDownloadedDataset(self.string)

            #stdout, stderr = p.communicate()
            #time.sleep(1000)
            #DNNFunctions.loadEMNIST(self.string)
            self.update_signal1.emit(True)

    def stop(self):
        self.running = False
        self.p.terminate()

class updateThread(QThread):
    update_signal2 = pyqtSignal(int) 

    def __init__(self, *args, **kwargs):
        super(updateThread, self).__init__(*args, **kwargs)
        self.count   = 0
        self.running = True

    def run(self):
        while self.running and self.count < 1000:
            self.count += 1
            self.update_signal2.emit(self.count)
            QThread.msleep(100)                 

    def stop(self):
        self.running = False


class importDatasetScreen(QDialog):

    def __init__(self,string):
        super().__init__()
        self.string = string
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Importing')
        self.progress = QProgressBar()
        self.progress.setGeometry(0, 0, 1000, 100)
        self.progress.setMaximum(1000)
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
        self.thread1 = updateThread()
        self.thread1.update_signal2.connect(self.update)
        self.thread2.update_signal1.connect(self.downloaded)

    def onButtonClick(self):
        self.button2.setEnabled(True)
        self.progress.setValue(0)
        self.thread2.running = True
        self.thread2.count = 0
        self.thread2.start()
        self.thread1.running = True
        self.thread1.count = 0
        self.thread1.start()
        self.button.setEnabled(False)
        self.button3.setEnabled(False)

    def update(self, val):
        self.progress.setValue(val)
        if val == 1000: self.on_stop()

    def on_stop(self):
        self.thread2.stop()
        self.thread1.stop()
        self.button.setEnabled(True)
        self.button3.setEnabled(True)
        self.button2.setEnabled(False)

    def clearCache(self):
        DNNFunctions.clearCache()

    def downloaded(self):
        return
