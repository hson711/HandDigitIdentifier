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

#Threading class to download dataset and update the progress bar without lagging UI
class Thread(QThread):
    #Updatesignal1 sends a signal with a string of each line of realtime output of the download process to print to the gui
    update_signal1 = pyqtSignal(str)
    #Update_signal3 takes in the first string of data with eta and uses that to set the maximum value of the progress bar
    update_signal3 = pyqtSignal(str)
    #Close signal is a signal to stop the subprocess and close the window
    closeSignal = pyqtSignal()

    #Initialized Thread and setup variables
    #Takes a string input of what dataset class to activate
    def __init__(self, string,  *args, **kwargs):

        super(Thread, self).__init__(*args, **kwargs)
        self.Finished   = False
        self.string = string
        self.running = True

    #Threads main function
    def run(self):
        while self.running :
            #If data is not downloaded
            if os.path.isfile(DNNFunctions.pathFile) == False:
                #Creates subprocess to download the dataset while making console output fed to the PIPE
                self.p = subprocess.Popen([sys.executable, 'C:\CodingTemp\CS302 Project 1\HandDigitIdentifier\scripts\SubprocessImporter.py', self.string], stdout = PIPE)
                #For loop to skip the first few lines of text of the realtime output as its not needed
                for i in range(5):
                    self.realtime_output = self.p.stdout.readline()
                #Decodes the bytes of realtime output into a number and feeds that to the update signal to set max value of progress bar
                maxValue = self.realtime_output.decode("cp1252")
                self.update_signal3.emit(maxValue.strip())
                #While loop to print out realtime output to gui
                while True:
                    self.realtime_output = self.p.stdout.readline()
                    #If subprocess is finished
                    if self.p.poll() is not None:
                        #Loads the downloaded dataset
                        if self.Finished == False:
                            DNNFunctions.openPreDownloadedDataset(self.string)
                        #Stops the while loop and closes the window and subprocess
                        self.running = False
                        self.closeSignal.emit()
                        break

                    #If self.realtime_output is not none then sends that through update signal 1 to be printed to gui
                    if self.realtime_output:
                        self.realtime_output = self.realtime_output.decode("cp1252")
                        self.update_signal1.emit(self.realtime_output.strip())

            #Else if data is downloaded, load it and close window and subprocess
            else:
                DNNFunctions.openPreDownloadedDataset(self.string)
                self.closeSignal.emit()
                self.running = False

    #Stop function is called by the stop button of the gui to stop the subprocess and stop running the thread
    def stop(self):
        self.running = False
        self.p.terminate()

#Class is the instance creator of the import datascreen window
class importDatasetScreen(QDialog):
    #Sets a base maxValue to set up progress bar
    maxValue = 1000

    #Initializes an instance of the window
    #Input: The string of the dataset class to use
    def __init__(self,string):

        super().__init__()
        self.string = string

        self.initUI()

    #Initializes look of gui and connections
    def initUI(self):

        self.setWindowTitle('Importing')
        #Sets up progressbar
        self.progress = QProgressBar()
        self.progress.setGeometry(0, 0, 1000, 500)
        self.progress.setMaximum(importDatasetScreen.maxValue)
        self.progress.setValue(0)

        self.savedEMNIST = False

        #Initializes layout
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        #Sets color theme of progress bar and buttons
        self.progress.setStyleSheet("QProgressBar {border: 2px solid grey;border-radius:8px;padding:1px}" "QProgressBar::chunk {background:yellow}")
        self.progress.setStyleSheet("QProgressBar::chunk {background: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 red, stop: 1 white); }")
        self.progress.setTextVisible(False)

        #Sets up buttons
        self.button = QPushButton('Start')
        self.button.setStyleSheet('background-color:yellow')

        self.button2 = QPushButton('Stop')
        self.button2.setStyleSheet('background-color:yellow')
        #Set enabled false so you can only click stop button after its been started
        self.button2.setEnabled(False)

        self.button3 = QPushButton('Clear Cache')
        self.button3.setStyleSheet('background-color:yellow')

        #Sets up text browser to display downloading data progress
        self.tb = QTextBrowser()
        self.tb.setAcceptRichText(True)
        self.tb.setOpenExternalLinks(True)

        #Adds widgets to layout
        vbox.addWidget(self.tb)
        vbox.addWidget(self.progress)
        hbox.addWidget(self.button)
        hbox.addWidget(self.button2)
        hbox.addWidget(self.button3)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        #Connects buttons to respective functions
        self.button.clicked.connect(self.onButtonClick)
        self.button2.clicked.connect(self.on_stop)
        self.button3.clicked.connect(self.clearCache)

        #Creates thead and passes it the dataset class to use
        #Connects the thread signals to respective functions
        self.thread2 = Thread(string=(self.string))
        self.thread2.update_signal1.connect(self.downloaded)
        self.thread2.update_signal3.connect(self.setMaximum)
        self.thread2.closeSignal.connect(self.closeSignal)

    #Start button clicked
    def onButtonClick(self):
        #Enables stop button
        self.button2.setEnabled(True)
        #Resets progress bar 
        self.progress.setValue(0)
        #Starts the thread object
        self.thread2.running = True
        self.thread2.start()
        #Disables start button and clear cache button
        self.button.setEnabled(False)
        self.button3.setEnabled(False)

    ###REDUNDANT CODE###
    """#Is passed the value of (eta at start minus time left)
    def update(self, val):
        #Sets progress bar to be value
        self.progress.setValue(val)"""
        
    #On stop button pushed
    def on_stop(self):
        #Stops the thread instance
        self.thread2.Finished = True
        self.thread2.p.terminate()
        self.thread2.stop()
        #Enables start and clear cache button and disables stop button
        self.button.setEnabled(True)
        self.button3.setEnabled(True)
        self.button2.setEnabled(False)

    #Function that deletes the dataset file off of the system
    def clearCache(self):
        DNNFunctions.clearCache()

    #Function that is passed the realtime output of the download progress to the console
    def downloaded(self,string):
        #Strips the string and organises it into a readable time estimate
        string = string.strip()
        string = string[-5:]
        string = string.split(":")
        #Checks to see if the string passed is a viable integer otherwise eta left is 0
        if  string[0].isdigit() and string[1].isdigit():
            min = int(float(string[0]))
            sec = int(float(string[1]))
        else:
            min = 0
            sec = 0

        minSec = min*60
        #Sets up deductable time to set the progress bar value
        deductableTime = minSec + sec
        #Sets the text equal to the found min and sec and then appends to the text viewer on the gui
        text = ("Time left till data is imported is ", str(min), " mins and ", str(sec), " seconds.\n" )
        text = ("").join(text)
        self.tb.append(text)
        #Sets the progress bar to the starting eta minus by time left
        tempMax = self.progress.maximum()
        self.progress.setValue(tempMax-deductableTime)

    #Function which is called when thread is initialized to set the maximum value of the progress bar
    #Input is passed one line of realtime output of the download progress
    def setMaximum(self,value):
        #Strips and decodes the passed string into digits
        string = value.strip()
        string = string[-5:]
        string = string.split(":")
        #If the resulting data is viable convert it into mins * 60 and seconds
        if  string[0].isdigit() and string[1].isdigit():
            min = int(string[0]) * 60
            sec = int(string[1])
        else:
            min = 0
            sec = 0
        #Set maximum progress bar value to time left and reset progress bar
        time = min + sec
        self.progress.setMaximum(time)
        self.progress.setValue(0)
    
    #Function is called when thread passes a close signal which closes the import dataset window
    def closeSignal(self):
        self.close()