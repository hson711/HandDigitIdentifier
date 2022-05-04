#Import Functions
import sys
from tabnanny import verbose
from xmlrpc.client import Boolean
from PyQt5.QtCore import QThread, pyqtSignal, Qt 
from DNNFunctions import *
import subprocess
from subprocess import *
from PyQt5.QtWidgets import *
import pickle
import re
import time

#Threading class to train model and update the stats without lagging UI
class External(QThread):
    update_signal1 = pyqtSignal(str)
    #Update_signal3 takes in the first string of data with eta and uses that to set the maximum value of the progress bar
    update_signal3 = pyqtSignal(str)
    #Close signal is a signal to stop the subprocess and close the window
    closeSignal = pyqtSignal()

    #Cancel signal is when the user clicks cancel
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

            #Get the subprocesser path
            file_path = str(pathlib.Path(__file__).parent.resolve())
            file_loc = file_path+'\SubprocessImporterTrain.py'
            
            self.p = subprocess.Popen([sys.executable, file_loc, self.path], stdout = PIPE)
            #For loop to skip the first few lines of text of the realtime output as its not needed
            for i in range(10):
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
                        #Wait a while to make sure model is saved before closing subprocess
                        time.sleep(7)

                        #Close Subprocess
                        self.running = False
                        self.closeSignal.emit()
                    break
                
                #Output realtime values from the subprocess
                if self.realtime_output:
                   self.realtime_output = self.realtime_output.decode("cp1252")
                   self.update_signal1.emit(self.realtime_output.strip())


     #Stop function is called by the stop button of the gui to stop the subprocess and stop running the thread
    def stop(self):
        self.running = False
        self.p.kill()

#Class is the instance creator of the Train model window
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
        hbox7 = QHBoxLayout()
        hbox8 = QHBoxLayout()
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


        #Set Up input widgets along with their labels
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


        #Set the labels for displaying the training progress
        self.results_epoch_label = QLabel("Epoch: ")
        self.results_epoch_label.setAlignment(Qt.AlignCenter)

        self.results_eta_label = QLabel("ETA for epoch: ")
        self.results_eta_label.setAlignment(Qt.AlignCenter)

        self.results_percent_epoch_label = QLabel("Training Done(total): ")
        self.results_percent_epoch_label.setAlignment(Qt.AlignCenter)

        self.results_percentage_label = QLabel("Training Done(total): ")
        self.results_percentage_label.setAlignment(Qt.AlignCenter)

        self.results_loss_label = QLabel("Loss: ")
        self.results_loss_label.setAlignment(Qt.AlignCenter)

        self.results_acc_label = QLabel("Accuracy: ")
        self.results_acc_label.setAlignment(Qt.AlignCenter)

        self.save_label = QLabel("Save Model: ")
        self.save_label.setAlignment(Qt.AlignRight)
        self.save_check = QCheckBox()

        #Set up labels for validation loss % accuracy to display at the end
        self.val_loss_label = QLabel("Validation Loss: ")
        self.val_loss_label.setAlignment(Qt.AlignCenter)

        self.val_acc_label = QLabel("Validation Loss: ")
        self.val_acc_label.setAlignment(Qt.AlignCenter)

        self.modelName_label = QLabel("Model Name:")
        self.modelName_label.setAlignment(Qt.AlignRight)
        

        #Input widget to input model name
        self.modelName = QLineEdit()
        self.modelName.setLayoutDirection(Qt.RightToLeft)
        self.modelName.setAutoFillBackground(False)
        self.modelName.setText("")
        self.modelName.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter) 


        #Set up buttons
        self.button2 = QPushButton('Cancel Training')
        self.button2.setStyleSheet('background-color:yellow')

        self.button3 = QPushButton('Train new model')
        self.button3.setStyleSheet('background-color:yellow')

        self.button4 = QPushButton('Exit')
        self.button4.setStyleSheet('background-color:yellow')

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
        hbox4.addWidget(self.results_percentage_label)
        hbox4.addWidget(self.results_percent_epoch_label)

        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)

        #Add Model Name
        vbox6.addWidget(self.modelName_label)
        vbox6.addWidget(self.modelName)

        hbox5.addLayout(vbox6)
        vbox.addLayout(hbox5)

        hbox6.addWidget(self.save_label)
        hbox6.addWidget(self.save_check)
        vbox.addLayout(hbox6)

        #Add Validation labels
        hbox8.addWidget(self.val_acc_label)
        hbox8.addWidget(self.val_loss_label)
        vbox.addLayout(hbox8)

        #Add Train Button & set layout
        hbox7.addWidget(self.button)
        hbox7.addWidget(self.button2)
        hbox7.addWidget(self.button3)
        hbox7.addWidget(self.button4)
        vbox.addLayout(hbox7)
        self.setLayout(vbox)

        #Change Value of label if slider is moved
        self.slider.valueChanged[int].connect(self.updateSliderVal)

        #Connects buttons to respective functions
        self.button.clicked.connect(self.onButtonClick)
        self.button2.clicked.connect(self.on_stop)
        self.button3.clicked.connect(self.reset)
        self.button4.clicked.connect(self.close)


        #Set the visibility of the results to false first to display input window
        self.progress.setVisible(False)
        self.results_epoch_label.setVisible(False)
        self.results_eta_label.setVisible(False)
        self.results_percentage_label.setVisible(False)
        self.results_acc_label.setVisible(False)
        self.results_loss_label.setVisible(False)
        self.val_acc_label.setVisible(False)
        self.val_loss_label.setVisible(False)

        self.button2.setVisible(False)
        self.button3.setVisible(False)

        #Creates thead and passes it the dataset class to use
        #Connects the thread signals to respective functions
        self.thread2 = External(string=(DNNFunctions.loaded_model))
        self.thread2.update_signal1.connect(self.update_signal)
        self.thread2.update_signal3.connect(self.setMaximum)
        self.thread2.closeSignal.connect(self.closeSignal)
        self.thread2.cancelSignal.connect(self.cancelSignal)

    # Resets window back into original values
    def reset(self):
        self.label.setText("Train a Model:")
        self.optimiser_label.setVisible(True)
        self.optimiser.setVisible(True)
        self.optimiser.setCurrentIndex(0)
        self.epoch_label.setVisible(True)
        self.epoch.setVisible(True)
        self.epoch.setValue(1)
        self.batch_size_label.setVisible(True)
        self.batch_size.setVisible(True)
        self.batch_size.setValue(1)
        self.slider_label.setVisible(True)
        self.slider.setVisible(True)
        self.slider.setValue(100)
        self.slider_pos.setVisible(True)
        self.slider_pos.setText("Train: 100% & Validate: 0%")
        self.modelName_label.setVisible(True)
        self.modelName.setVisible(True)
        self.modelName.setText("")
        self.save_check.setVisible(True)
        self.save_check.setChecked(False)
        self.save_label.setVisible(True)

        self.progress.setVisible(False)
        self.results_epoch_label.setVisible(False)
        self.results_epoch_label.setText("Epoch: 1/{}".format(self.epoch.value()))
        self.results_eta_label.setVisible(False)
        self.results_eta_label.setText("ETA: ")
        self.results_percentage_label.setText("Training Done(total): ")
        self.results_percentage_label.setVisible(False)
        self.results_percent_epoch_label.setVisible(False)
        self.results_percent_epoch_label.setText("Training Done(epoch): ")
        self.results_acc_label.setVisible(False)
        self.results_loss_label.setVisible(False)
        self.results_acc_label.setText("Training Accuracy: ")
        self.results_loss_label.setText("Training Loss: ")
        self.val_acc_label.setVisible(False)
        self.val_acc_label.setVisible(False)
        self.val_loss_label.setVisible(False)
        self.val_loss_label.setVisible(False)

        self.button.setVisible(True)
        self.button2.setVisible(False)
        self.button3.setVisible(False)
        self.button4.setVisible(True)

    #Updates the position of the slider dynamcally
    def updateSliderVal(self, value):
        self.slider_pos.setText("Train: {}% & Validate: {}%".format(value, 100-value))

    #Resets after subprocess is stopped
    def cancelSignal(self):
        self.reset()

    #On Cancel button pushed
    def on_stop(self):
        #Stops the thread instance
        self.thread2.stop()
        QMessageBox.information(self, "Training Cancelled", "The training has stopped!!")

        #Deletes the temp file
        try:
            file_path = str(pathlib.Path(__file__).parent.resolve())
            file = file_path+"/../bin/temp.pkl"
            os.remove(file)
        except OSError:
            pass
        
    #Function that is passed the realtime output of the download progress to the console
    def update_signal(self,string):
        #Strips the string and organises it into a readable time estimate
        string = string.split()

        try:
            #Get the values of both the current epoch value & max epoch value
            current_val = re.findall(r"(\d+)/", string[0])
            max_val = re.findall(r'%s(\d+)' % '/', string[0])

            #When new epoch starts
            if(string[0] == "Epoch"):
                current_val = re.findall(r"(\d+)/", string[1])
                self.current_epoch = int(current_val[0])
                self.results_epoch_label.setText("Epoch: {}/{}".format(self.current_epoch, self.epoch.value()))
                self.label.setText("Training Model")

            
            else:

                #Check if validation was done for epoch
                if ("val_loss:" in string):
                    self.val_loss_label.setText("Validation Loss: {}".format(string[13]))
                    self.val_acc_label.setText("Validation Accuracy: {}%".format(float(string[16])*100))
                
                #Check if validation is happening
                elif(int(current_val[0]) == int(max_val[0])-1):
                    self.label.setText("Validating Data from epoch. Please Wait....(It might take a while depending on the batch size)")                    
                
                
                #Dynamically Update the values of the GUI
                val = int(current_val[0])+((self.current_epoch-1)*int(max_val[0]))
                percent_total = (val/((int(max_val[0]))*self.epoch.value()))*100
                self.progress.setMaximum((int(max_val[0]))*self.epoch.value())
                self.progress.setValue(val)
                self.results_eta_label.setText("ETA(epoch): {}".format(string[4]))
                self.results_loss_label.setText("Training Loss: {}".format(string[7]))
                self.results_acc_label.setText("Training Accuracy: {}%".format((float(string[10])*100)))
                self.results_percent_epoch_label.setText("Training Done(epoch): {:.2f}%".format((int(current_val[0])/int(max_val[0]))*100))
                self.results_percentage_label.setText("Training Done(total): {:.2f}%".format(percent_total))
                
        except Exception as e:
            #For when subprocess outputs unexpected statements(memory exceeded etc.)
            pass

    #Function which is called when thread is initialized to set the maximum value of the progress bar
    #Input is passed one line of realtime output of the download progress
    def setMaximum(self,value):

        #Set the results to be visible 
        self.label.setText("Training Model:")
        self.progress.setVisible(True)
        self.results_epoch_label.setVisible(True)
        self.results_eta_label.setVisible(True)
        self.results_percentage_label.setVisible(True)
        self.results_percent_epoch_label.setVisible(True)
        self.results_acc_label.setVisible(True)
        self.results_loss_label.setVisible(True)
        
        self.button2.setVisible(True)
        
        #Strips and decodes the passed string into digits
        try:
            #Get values of epoch and other data
            string = value.split()
            self.results_epoch_label.setText("Epoch: 1/{}".format(self.epoch.value()))
            current_val = re.findall(r"(\d+)/", string[0])
            max_val = re.findall(r'%s(\d+)' % '/', string[0])
            self.progress.setMaximum(int(max_val[0]))
            self.progress.setValue(int(current_val[0]))
        except Exception as e:
            #For when subprocess outputs unexpected statements(memory exceeded etc.) 
            pass
    
    #Function is called when thread passes a close signal which implies that the subprocess is finished
    def closeSignal(self):

        #Set Labels to display Results
        self.label.setText("Model Results:")
        self.results_eta_label.setVisible(False)
        self.results_epoch_label.setVisible(False)
        self.results_percent_epoch_label.setVisible(False)
        self.results_percentage_label.setVisible(False)
        self.val_loss_label.setVisible(True)
        self.val_acc_label.setVisible(True)
        self.button2.setVisible(False)
        self.button3.setVisible(True)
        self.button4.setVisible(True)


    #When Train Model is clicked
    def onButtonClick(self):

        #Give user a warning for save file if not checked
        if (self.save_check.isChecked() == True):
            self.open_thread()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Warning: Save Model not checked. Are you sure?")
            msgBox.setWindowTitle("Save Warning")
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Yes:
                self.open_thread()
    
    def open_thread(self):

        #Set file path for a temporary pickle file
        file_path = str(pathlib.Path(__file__).parent.resolve())
        file = file_path+"/../bin/temp.pkl"
        save_loc=""

        #Set model name for path
        if (self.save_check.isChecked() == True):
            if self.modelName.text().strip() == "":
                model_name = "mymodel"
            else:
                model_name = self.modelName.text().strip()
            save_file_path = str(QFileDialog.getExistingDirectory(None, "Select Directory to save model"))
            save_loc = save_file_path+"/"+model_name
        
        with open(file, 'wb') as f:  # Python 3: open(..., 'wb')
            pickle.dump([self.modelName.text(), self.optimiser.currentText().lower(), self.epoch.value(), self.batch_size.value(), self.slider.value(), self.save_check.isChecked(), DNNFunctions.train_x, DNNFunctions.train_y, save_loc], f, -1)

        #Start Thread
        self.thread2.running = True
        self.thread2.path = file
        self.thread2.start()

        #Set labels for input to be not visible
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
        self.save_check.setVisible(False)
        self.save_label.setVisible(False)
        

        self.button.setVisible(False)
        self.button4.setVisible(False)
        self.label.setText("Loading. Please Wait....")
        self.results_percentage_label.setText("Hekekek")
        self.results_percentage_label.setVisible(False)