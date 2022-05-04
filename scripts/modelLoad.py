import imp
import sys
from tabnanny import verbose
from tkinter import Label
from xmlrpc.client import Boolean
from PyQt5.QtWidgets import (QApplication, QDialog, QProgressBar, QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import QThread, pyqtSignal, Qt 
from numpy import NaN, integer
from DNNFunctions import *
import contextlib
import subprocess
from subprocess import *
from PyQt5.QtWidgets import (QApplication, QMessageBox, QPushButton, QVBoxLayout, QFileDialog, QLabel)
import pickle
import re
from customPredicionHub import *

#Threading class to download dataset and update the progress bar without lagging UI
class Thread(QThread):
    update_signal1 = pyqtSignal(str)
    #Update_signal3 takes in the first string of data with eta and uses that to set the maximum value of the progress bar
    update_signal3 = pyqtSignal(str)
    #Close signal is a signal to stop the subprocess and close the window
    closeSignal = pyqtSignal()

    cancelSignal = pyqtSignal()

    #Initialized Thread and setup variables
    #Takes a string input of what dataset class to activate
    def __init__(self, string,  *args, **kwargs):

        super(Thread, self).__init__(*args, **kwargs)
        self.Finished   = False
        self.string = string
        self.running = True
        self.path = ""

    def run(self):
        while self.running:
            file_path = str(pathlib.Path(__file__).parent.resolve())
            file_loc = file_path+'\SubprocessImporterLoad.py'
            
            self.p = subprocess.Popen([sys.executable, file_loc, self.path], stdout = PIPE)
            #For loop to skip the first few lines of text of the realtime output as its not needed
            for i in range(5):
                self.realtime_output = self.p.stdout.readline()

            #Decodes the bytes of realtime output into a number and feeds that to the update signal to set max value of progress bar
            maxValue = self.realtime_output.decode("cp1252")

            
            self.update_signal3.emit(maxValue.strip())
            
            
            while True:
                self.realtime_output = self.p.stdout.readline()

                if self.p.poll() is not None:
                    
                    #Checks if cancel was clicked
                    if (self.running ==False):
                        self.cancelSignal.emit()
                    else:

                        #Get results from tmp file
                        with open(self.path, 'rb') as f: 
                            results = pickle.load(f)
                        
                        DNNFunctions.loaded_model_results = results
                        self.running = False
                        self.p.kill()
                        self.closeSignal.emit()
                    break

                if self.realtime_output:
                   self.realtime_output = self.realtime_output.decode("cp1252")
                   self.update_signal1.emit(self.realtime_output.strip())


     #Stop function is called by the stop button of the gui to stop the subprocess and stop running the thread
    def stop(self):
        self.running = False
        self.p.kil()

#Class is the instance creator of the load model window
class modelLoad(QDialog):
    #Sets a base maxValue to set up progress bar
    maxValue = 1000

    #Initializes an instance of the window
    #Input: The string of the dataset class to use
    def __init__(self):

        super().__init__()
    
        self.initUI()

    #Initializes look of gui and connections
    def initUI(self):

        self.setWindowTitle('Load Model')
        #Sets up progressbar
        self.progress = QProgressBar()
        self.progress.setGeometry(0, 0, 1000, 500)
        self.progress.setMaximum(modelLoad.maxValue)
        self.progress.setValue(0)

        self.savedEMNIST = False

        #Initializes layout
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        self.label = QLabel('Load Model')
        self.label.setAlignment(Qt.AlignCenter)

        #Sets color theme of progress bar and buttons
        self.progress.setStyleSheet("QProgressBar {border: 2px solid grey;border-radius:8px;padding:1px}" "QProgressBar::chunk {background:yellow}")
        self.progress.setStyleSheet("QProgressBar::chunk {background: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 red, stop: 1 white); }")
        self.progress.setTextVisible(False)

        #Sets up buttons
        self.button = QPushButton('Load Model')
        self.button.setStyleSheet('background-color:yellow')

        self.button2 = QPushButton('Cancel')
        self.button2.setStyleSheet('background-color:yellow')
        #Set enabled false so you can only click stop button after its been started
        self.button2.setEnabled(False)

        #Adds widgets to layout
        vbox.addWidget(self.label)
        vbox.addWidget(self.progress)
        hbox.addWidget(self.button)
        hbox.addWidget(self.button2)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        #Connects buttons to respective functions
        self.button.clicked.connect(self.onButtonClick)
        self.button2.clicked.connect(self.on_stop)

        self.progress.setVisible(False)

        #Creates thead and passes it the dataset class to use
        #Connects the thread signals to respective functions
        self.thread2 = Thread(string=(DNNFunctions.loaded_model))
        self.thread2.update_signal1.connect(self.downloaded)
        self.thread2.update_signal3.connect(self.setMaximum)
        self.thread2.closeSignal.connect(self.closeSignal)
        self.thread2.cancelSignal.connect(self.cancelSignal)

    def cancelSignal(self):
        self.label.setText("Load Model")
        self.progress.setVisible(False)

    #On stop button pushed
    def on_stop(self):
        #Stops the thread instance
        self.thread2.stop()
        #Enables start and clear cache button and disables stop button
        self.button.setEnabled(True)
        self.button2.setEnabled(False)

    #Function that is passed the realtime output of the download progress to the console
    def downloaded(self,string):
        #Strips the string and organises it into a readable time estimate
        string = string.split()
        try:
            current_val = re.findall(r"(\d+)/", string[0])
            max_val = re.findall(r'%s(\d+)' % '/', string[0])
            self.progress.setValue(int(current_val[0]))
            if (int(current_val[0]) != int(max_val[0])):
                loaded = (int(current_val[0])/int(max_val[0]))*100
                self.label.setText("{:.1f}% Loaded  | ETA: {}".format(loaded, string[4]))
        except Exception as e:
            pass


    #Function which is called when thread is initialized to set the maximum value of the progress bar
    #Input is passed one line of realtime output of the download progress
    def setMaximum(self,value):
        #Strips and decodes the passed string into digits
        try:
            string = value.split()
            current_val = re.findall(r"(\d+)/", string[0])
            max_val = re.findall(r'%s(\d+)' % '/', string[0])
            self.progress.setMaximum(int(max_val[0]))
            self.progress.setValue(int(current_val[0]))

            loaded_val = (int(current_val[0])/int(max_val[0]))*100
            self.label.setText("{:.1f}% Loaded  | ETA: {}".format(loaded_val), string[4])
        except Exception as e:
            pass
    
    #Function is called when thread passes a close signal which closes the import dataset window
    def closeSignal(self):
        QMessageBox.information(self, "Load Successful", "Model Loaded Successfully!")
        self.customPredictionHub = customPredicionHub()
        self.customPredictionHub.show()
        self.close()

    
    #When button clicked, run this
    def onButtonClick(self):

        #Select Directory for load
        model_path = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
        if model_path != "":

            #Check if model exists
            if (DNNFunctions.model_load(model_path) == True):
                #Set up tempfile
                file_path = str(pathlib.Path(__file__).parent.resolve())
                file = file_path+"/objs.pkl"

                #Reshape values to send to subprocess
                DNNFunctions.test_x = DNNFunctions.raw_test_x.reshape(len(DNNFunctions.raw_test_x), 784)
                DNNFunctions.test_x = DNNFunctions.test_x.astype('float32')
                DNNFunctions.test_x = DNNFunctions.test_x/255
                DNNFunctions.test_y = keras.utils.np_utils.to_categorical(DNNFunctions.raw_test_y)
                DNNFunctions.test_x = DNNFunctions.test_x.reshape(-1, 28, 28, 1)


                with open(file, 'wb') as f: 
                    pickle.dump([model_path, DNNFunctions.test_x, DNNFunctions.test_y], f, -1)   

                 #Enables stop button
                self.button2.setEnabled(True)
                self.label.setText("Loading....Please Wait")
                self.progress.setVisible(True)
                #Resets progress bar 
                self.progress.setValue(0)
                #Starts the thread object
                self.thread2.running = True
                self.thread2.path = file
                self.thread2.start()
                #Disables start button and clear cache button
                self.button.setEnabled(False)    
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('No Model found in directory')
                msg.setWindowTitle("Model Not Found")
                msg.exec_()    