import sys
from PyQt5.QtWidgets import (QApplication, QDialog, QProgressBar, QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import QThread, pyqtSignal


class Thread(QThread):
    update_signal = pyqtSignal(int) 

    def __init__(self, *args, **kwargs):
        super(Thread, self).__init__(*args, **kwargs)
        self.count   = 0
        self.running = True

    def run(self):
        while self.running and self.count < 100:
            self.count += 1
            self.update_signal.emit(self.count)
            QThread.msleep(100)                   

    def stop(self):
        self.running = False


class importDatasetScreen(QDialog):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Importing')
        self.progress = QProgressBar()
        self.progress.setGeometry(0, 0, 300, 100)
        self.progress.setMaximum(100)
        self.progress.setValue(0)

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

        vbox.addWidget(self.progress)
        hbox.addWidget(self.button)
        hbox.addWidget(self.button2)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.button.clicked.connect(self.onButtonClick)
        self.button2.clicked.connect(self.on_stop)

        self.thread = Thread()
        self.thread.update_signal.connect(self.update)

    def onButtonClick(self):
        self.button2.setEnabled(True)
        self.progress.setValue(0)
        self.thread.running = True
        self.thread.count = 0
        self.thread.start()
        self.button.setEnabled(False)

    def update(self, val):
        self.progress.setValue(val)
        if val == 100: self.on_stop()

    def on_stop(self):
        self.thread.stop()
        self.button.setEnabled(True)
        self.button2.setEnabled(False)