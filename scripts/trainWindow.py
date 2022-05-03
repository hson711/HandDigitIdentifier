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
class External(QThread):
    update_signal1 = pyqtSignal(str)
    #Update_signal3 takes in the first string of data with eta and uses that to set the maximum value of the progress bar
    update_signal3 = pyqtSignal(str)
    #Close signal is a signal to stop the subprocess and close the window
    closeSignal = pyqtSignal()

    cancelSignal = pyqtSignal()

    #Initialized Thread and setup variables
    #Takes a string input of what dataset class to activate
    def __init__(self, string,  *args, **kwargs):

        super(External, self).__init__(*args, **kwargs)
        self.Finished   = False
        self.string = string
        self.running = True

        self.path = ""

    def run(self):
        while self.running:
            file_path = str(pathlib.Path(__file__).parent.resolve())
            file_loc = file_path+'\SubprocessImporterTrain.py'
            
            self.p = subprocess.Popen([sys.executable, file_loc, self.path], stdout = PIPE)
            #For loop to skip the first few lines of text of the realtime output as its not needed
            for i in range(15):
                self.realtime_output = self.p.stdout.readline()
                print(self.realtime_output.decode("cp1252"))

            #Decodes the bytes of realtime output into a number and feeds that to the update signal to set max value of progress bar
            maxValue = self.realtime_output.decode("cp1252")

            
            self.update_signal3.emit(maxValue.strip())
            
            
            while True:
                self.realtime_output = self.p.stdout.readline()

                if self.p.poll() is not None:
                    print("It finished")
                    
                    #Checks if cancel was clicked
                    if (self.running ==False):
                        self.cancelSignal.emit()
                    else:

                        #Get results from tmp file
                        with open(self.path, 'rb') as f: 
                            results = pickle.load(f)
                        
                        DNNFunctions.loaded_model_results = results
                        self.running = False
                        self.closeSignal.emit()
                    break
               # print(classification_report(Y_test, y_pred)) 

                if self.realtime_output:
                   self.realtime_output = self.realtime_output.decode("cp1252")
                   self.update_signal1.emit(self.realtime_output.strip())


     #Stop function is called by the stop button of the gui to stop the subprocess and stop running the thread
    def stop(self):
        self.running = False
        self.p.terminate()

#Class is the instance creator of the import datascreen window
class trainWindow(QDialog):
    #Sets a base maxValue to set up progress bar
    maxValue = 1000
    current_epoch = 1
    total_epoch = 1
    #Initializes an instance of the window
    #Input: The string of the dataset class to use
    def __init__(self):

        super().__init__()
    
        self.initUI()

    #Initializes look of gui and connections
    def initUI(self):

        self.setWindowTitle('Train Model')
        #Sets up progressbar
        self.progress = QProgressBar()
        self.progress.setGeometry(0, 0, 1000, 500)
        self.progress.setMaximum(trainWindow.maxValue)
        self.progress.setValue(0)

        self.savedEMNIST = False

        #Initializes layout
        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        hbox5 = QHBoxLayout()
        hbox6 = QHBoxLayout()
        vbox2 = QVBoxLayout()
        vbox3 = QVBoxLayout()
        vbox4 = QVBoxLayout()
        vbox5 = QVBoxLayout()
        vbox6 = QVBoxLayout()

        self.label = QLabel('Train Model')
        self.label.setAlignment(Qt.AlignCenter)

       
        #Sets up buttons
        self.button = QPushButton('Train Model')
        self.button.setStyleSheet('background-color:yellow')

        self.optimiser_label = QLabel("Choose DNN:")
        self.label.setAlignment(Qt.AlignCenter)
        self.optimiser = QComboBox()
        self.optimiser.addItems(["Adam", "SGD", "Nadam"])

        self.epoch_label = QLabel("Number of Epochs:")
        self.epoch_label.setAlignment(Qt.AlignCenter)

        self.epoch = QSpinBox()
        self.epoch.setMinimum(1)
        
        self.batch_size_label =QLabel("Batch Size:")
        self.batch_size_label.setAlignment(Qt.AlignCenter)

        self.batch_size = QSpinBox()
        self.batch_size.setMinimum(1)
        self.batch_size.setMaximum(1000000)


        self.slider_label = QLabel("Choose Train/Validation Percentage")
        self.slider_label.setAlignment(Qt.AlignCenter)

        self.slider = QSlider()
        self.slider.setMaximum(100)
        self.slider.setValue(100)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(10)

        self.slider_pos = QLabel("Train: 100% & Validate: 0%")
        self.slider_pos.setAlignment(Qt.AlignCenter)



        #Sets color theme of progress bar and buttons
        self.progress.setStyleSheet("QProgressBar {border: 2px solid grey;border-radius:8px;padding:1px}" "QProgressBar::chunk {background:yellow}")
        self.progress.setStyleSheet("QProgressBar::chunk {background: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 red, stop: 1 white); }")
        self.progress.setTextVisible(False)

        self.results_epoch_label = QLabel("Epoch: ")
        self.results_epoch_label.setAlignment(Qt.AlignCenter)

        self.results_eta_label = QLabel("ETA for epoch: ")
        self.results_eta_label.setAlignment(Qt.AlignCenter)

        self.results_percent_epoch_label = QLabel("Percent Done(total): ")
        self.results_percent_epoch_label.setAlignment(Qt.AlignCenter)

        self.results_percent_label = QLabel("Percent Done(total): ")
        self.results_percent_label.setAlignment(Qt.AlignCenter)

        self.results_loss_label = QLabel("Loss: ")
        self.results_loss_label.setAlignment(Qt.AlignCenter)

        self.results_acc_label = QLabel("Accuracy: ")
        self.results_acc_label.setAlignment(Qt.AlignCenter)


        self.tbox = QTextBrowser()
        self.tbox.setAcceptRichText(True)
        self.tbox.setOpenExternalLinks(True)

        self.modelName_label = QLabel("Model Name:")
        self.modelName_label.setAlignment(Qt.AlignRight)
        
        self.modelName = QLineEdit()
        self.modelName.setLayoutDirection(Qt.RightToLeft)
        self.modelName.setAutoFillBackground(False)
        self.modelName.setText("")
        self.modelName.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter) 


        self.button2 = QPushButton('Cancel')
        self.button2.setStyleSheet('background-color:yellow')
        #Set enabled false so you can only click stop button after its been started
        self.button2.setEnabled(False)

        #Adds widgets to layout
        vbox.addWidget(self.label)

        #Add the choices widgets into one layer
        vbox2.addWidget(self.optimiser_label)
        vbox2.addWidget(self.optimiser)
        vbox3.addWidget(self.epoch_label)
        vbox3.addWidget(self.epoch)
        vbox4.addWidget(self.batch_size_label)
        vbox4.addWidget(self.batch_size)
        hbox1.addLayout(vbox2)
        hbox1.addLayout(vbox3)
        hbox1.addLayout(vbox4)
        vbox.addLayout(hbox1)
        
        #Add Slider
        vbox5.addWidget(self.slider_label)
        vbox5.addWidget(self.slider)
        vbox5.addWidget(self.slider_pos)
        hbox2.addLayout(vbox5)
        vbox.addLayout(hbox2)

        #Add Progress Bar
        vbox.addWidget(self.progress)
        
        #Add Results label
        hbox3.addWidget(self.results_epoch_label)
        hbox3.addWidget(self.results_eta_label)
        hbox3.addWidget(self.results_loss_label)
        hbox3.addWidget(self.results_acc_label)
        hbox4.addWidget(self.results_percent_label)
        hbox4.addWidget(self.results_percent_epoch_label)

        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)

        #Add Model Name
        vbox6.addWidget(self.modelName_label)
        vbox6.addWidget(self.modelName)

        hbox5.addLayout(vbox6)
        vbox.addLayout(hbox5)

        #Add Train Button & set layout
        hbox6.addWidget(self.button)
        hbox6.addWidget(self.button2)
        vbox.addLayout(hbox6)
        self.setLayout(vbox)

        #Change Value of label if slider is moved
        self.slider.valueChanged[int].connect(self.updateSliderVal)

        #Connects buttons to respective functions
        self.button.clicked.connect(self.onButtonClick)
        self.button2.clicked.connect(self.on_stop)

        self.progress.setVisible(False)
        self.results_epoch_label.setVisible(False)
        self.results_eta_label.setVisible(False)
        self.results_percent_label.setVisible(False)
        self.results_acc_label.setVisible(False)
        self.results_loss_label.setVisible(False)

        #Creates thead and passes it the dataset class to use
        #Connects the thread signals to respective functions
        self.thread2 = External(string=(DNNFunctions.loaded_model))
        self.thread2.update_signal1.connect(self.downloaded)
        self.thread2.update_signal3.connect(self.setMaximum)
        self.thread2.closeSignal.connect(self.closeSignal)
        self.thread2.cancelSignal.connect(self.cancelSignal)

    def updateSliderVal(self, value):
        self.slider_pos.setText("Train: {}% & Validate: {}%".format(value, 100-value))


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
        print(string)
        string = string.split()

        try:
            if(string[0] == "Epoch"):
                print("Epock thing here")
                current_val = re.findall(r"(\d+)/", string[1])
                self.current_epoch = int(current_val)
                self.results_epoch_label.setText("Epoch: {}/{}".format(self.current_epoch, self.epoch.value()))
            else:
                if ("val_loss:" in string):
                    self.tbox.append("Epoch: {}/{}\n".format(self.current_epoch,self.epoch.value()))
                    self.tbox.append("Training Loss: {} | Training Accuracy: {}% | Validation Loss: {} | Validation Accuracy: {}%".format(string[7],float(string[10])*100,string[13],float(string[16]))*100)
                current_val = re.findall(r"(\d+)/", string[0])
                max_val = re.findall(r'%s(\d+)' % '/', string[0])                
                val = int(current_val[0])+((self.current_epoch-1)*int(max_val[0]))
                self.progress.setMaximum((int(max_val[0]))*self.epoch.value())
                self.progress.setValue(val)
                self.results_eta_label.setText("ETA: {}".format(string[4]))
                self.results_loss_label.setText("Loss: {}".format(string[7]))
                self.results_acc_label.setText("Accuracy: {}%".format((float(string[10])*100)))
                self.results_percent_epoch_label.setText("Percent Done(epoch): {:.2f}%".format((int(current_val[0])/int(max_val[0]))*100))
                self.results_percent_label.setText("Percent Done(total): {:.2f}%".format((val/(int(max_val[0]))*self.epoch.value())*100))
                

        except Exception as e:
            print("Except jadj")
            print(e)
        # try:
        #     current_val = re.findall(r"(\d+)/", string[0])
        #     max_val = re.findall(r'%s(\d+)' % '/', string[0])
        #     self.progress.setValue(int(current_val[0]))
        #     if (int(current_val[0]) != int(max_val[0])):
        #         loaded = (int(current_val[0])/int(max_val[0]))*100
        #         self.label.setText("{:.1f}% Loaded  | ETA: {}".format(loaded, string[4]))
        # except Exception as e:
        #     print(e)
        #     pass


    #Function which is called when thread is initialized to set the maximum value of the progress bar
    #Input is passed one line of realtime output of the download progress
    def setMaximum(self,value):
        print(value)
        #Strips and decodes the passed string into digits
        try:
            string = value.split()
            self.results_epoch_label.setText("Epoch: 1/{}".format(self.epoch.value()))
            current_val = re.findall(r"(\d+)/", string[0])
            max_val = re.findall(r'%s(\d+)' % '/', string[0])
            self.progress.setMaximum(int(max_val[0]))
            self.progress.setValue(int(current_val[0]))
            loaded_val = (int(current_val[0])/int(max_val[0]))*100
        except Exception as e:
            print("max exception")
            print(e)
            pass
    
    #Function is called when thread passes a close signal which closes the import dataset window
    def closeSignal(self):
        QMessageBox.information(self, "Load Successful", "Model Loaded Successfully!")
        self.customPredictionHub = customPredicionHub()
        self.customPredictionHub.show()
        self.close()

    
    def onButtonClick(self):
        file_path = str(pathlib.Path(__file__).parent.resolve())
        file = file_path+"/../bin/temp.pkl"
        print ("Sending: {} | {} | {} | {} | {}".format(self.modelName.text(), self.optimiser.currentText().lower(),self.epoch.value(), self.batch_size.value(), self.slider.value()))
        with open(file, 'wb') as f:  # Python 3: open(..., 'wb')
            pickle.dump([self.modelName.text(), self.optimiser.currentText().lower(), self.epoch.value(), self.batch_size.value(), self.slider.value(), DNNFunctions.train_x, DNNFunctions.train_y], f, -1)


        self.thread2.running
        self.thread2.path = file
        self.thread2.start()

        self.label.setText("Training Model:")
        self.optimiser_label.setVisible(False)
        self.optimiser.setVisible(False)
        self.epoch_label.setVisible(False)
        self.epoch.setVisible(False)
        self.batch_size_label.setVisible(False)
        self.batch_size.setVisible(False)
        self.slider_label.setVisible(False)
        self.slider.setVisible(False)
        self.slider_pos.setVisible(False)
        self.modelName_label.setVisible(False)
        self.modelName.setVisible(False)

        self.progress.setVisible(True)
        self.results_epoch_label.setVisible(True)
        self.results_eta_label.setVisible(True)
        self.results_percent_label.setVisible(True)
        self.results_acc_label.setVisible(True)
        self.results_loss_label.setVisible(True)

        self.button.setEnabled(False)

        # model_path = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
        # if model_path != "":
        #     if (DNNFunctions.model_load(model_path) == True):
        #         file_path = str(pathlib.Path(__file__).parent.resolve())
        #         file = file_path+"/objs.pkl"

        #         DNNFunctions.test_x = DNNFunctions.raw_test_x.reshape(len(DNNFunctions.raw_test_x), 784)
        #         DNNFunctions.test_x = DNNFunctions.test_x.astype('float32')
        #         DNNFunctions.test_x = DNNFunctions.test_x/255
        #         DNNFunctions.test_y = keras.utils.np_utils.to_categorical(DNNFunctions.raw_test_y)
        #         DNNFunctions.test_x = DNNFunctions.test_x.reshape(-1, 28, 28, 1)


        #         with open(file, 'wb') as f:  # Python 3: open(..., 'wb')
        #             pickle.dump([model_path, DNNFunctions.test_x, DNNFunctions.test_y], f, -1)   

        #          #Enables stop button
        #         self.button2.setEnabled(True)
        #         self.label.setText("Loading....Please Wait")
        #         self.progress.setVisible(True)
        #         #Resets progress bar 
        #         self.progress.setValue(0)
        #         #Starts the thread object
        #         self.thread2.running = True
        #         self.thread2.path = file
        #         self.thread2.start()
        #         #Disables start button and clear cache button
        #         self.button.setEnabled(False)    
        #     else:
        #         msg = QMessageBox()
        #         msg.setIcon(QMessageBox.Critical)
        #         msg.setText("Error")
        #         msg.setInformativeText('No Model found in directory')
        #         msg.setWindowTitle("Model Not Found")
        #         msg.exec_()    