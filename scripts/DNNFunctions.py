import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from asyncio.windows_events import NULL
from importlib.resources import path
import pathlib
from traceback import print_list
import keras
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Dropout, Flatten, BatchNormalization
import numpy as np
from extra_keras_datasets import emnist
from pandas import array
from scipy import io as sio
from PIL.ImageQt import ImageQt 
from PyQt5.QtGui import *
from PyQt5 import *
import cv2
import numpy, zipfile
from PIL.ImageQt import ImageQt
from torchvision.transforms import ToPILImage
from scipy import *
import contextlib
import io

#Class that hold all global variables and functions related to the downloading of data
class DNNFunctions():
    #Initialises that the data isnt loaded
    data_loaded = False    
    #Class Variable
    (raw_train_x, raw_train_y), (raw_test_x, raw_test_y) = (NULL, NULL), (NULL, NULL)
    (train_x, train_y), (test_x, test_y) = (NULL, NULL), (NULL, NULL)
    predictedValue = NULL
    model = NULL
    loaded_model = NULL
    loaded_model_results = NULL


    #Sets up the path to the downloaded file if its downloaded
    w = NULL
    user_home = str(pathlib.Path.home())
    location = user_home + "\.keras\datasets"
    file = 'emnist_matlab.npz'
    pathFile = os.path.join(location, file)\
    #Initializes keys
    keys = {'matlab/emnist-balanced.mat', 'matlab/emnist-byclass.mat', 'matlab/emnist-bymerge.mat', 'matlab/emnist-digits.mat', 'matlab/emnist-letters.mat', 'matlab/emnist-mnist.mat'}
    #If file is downloaded loads keys
    if os.path.isfile(pathFile) == True:
            numpyObject = numpy.load(pathFile)
            keys = numpyObject.keys()
    #Preset labels
    labels = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    
    
    def __init__(self):
        return

    #Function that is passed a string of what class of data set to use and downloads the dataset and activates the target class of data
    def loadEMNIST(string):
        #If file is not downloaded, download and load the by class data
        if os.path.isfile(DNNFunctions.pathFile) == False:
            (DNNFunctions.raw_train_x, DNNFunctions.raw_train_y), (DNNFunctions.raw_test_x, DNNFunctions.raw_test_y) = emnist.load_data(type='byclass')

            #Reshape the dataset to process for the model
            DNNFunctions.train_x = DNNFunctions.raw_train_x.reshape(len(DNNFunctions.raw_train_x), 784)
            DNNFunctions.test_x = DNNFunctions.raw_test_x.reshape(len(DNNFunctions.raw_test_x), 784)

            DNNFunctions.train_x = DNNFunctions.train_x.astype('float32')
            DNNFunctions.test_x = DNNFunctions.test_x.astype('float32')
            DNNFunctions.train_x = DNNFunctions.train_x/255
            DNNFunctions.test_x = DNNFunctions.test_x/255

            DNNFunctions.train_y = keras.utils.np_utils.to_categorical(DNNFunctions.raw_train_y)
            DNNFunctions.test_y = keras.utils.np_utils.to_categorical(DNNFunctions.raw_test_y)

            DNNFunctions.train_x = DNNFunctions.train_x.reshape(-1, 28, 28, 1)
            DNNFunctions.test_x = DNNFunctions.test_x.reshape(-1, 28, 28, 1)

        #if downloaded, open the downloaded data
        else:
            DNNFunctions.openPreDownloadedDataset(string)
        #Set downloaded data to true
        DNNFunctions.data_loaded = True
    
    #Function that deletes the dataset if it exsists on the system
    def clearCache():
        if os.path.isfile(DNNFunctions.pathFile) == True:
            os.remove(DNNFunctions.pathFile)

    #Function opens the predownloaded datafile and loads the class of data desired, specified by the passed string
    def openPreDownloadedDataset(string):
        #Loads the keys of the data
        numpyObject = numpy.load(DNNFunctions.pathFile)
        DNNFunctions.keys = numpyObject.keys()
        DNNFunctions.data_loaded = True
        #Opens zipfile
        with zipfile.ZipFile(DNNFunctions.pathFile, 'r') as opened_zip:
            with opened_zip.open(string, mode = 'r') as dataSetFile:
                #NEED EXPLANATION
                mat = sio.loadmat(dataSetFile)
                data = mat["dataset"]

                input_train = data["train"][0, 0]["images"][0, 0]
                target_train = data["train"][0, 0]["labels"][0, 0].flatten()
                input_test = data["test"][0, 0]["images"][0, 0]
                target_test = data["test"][0, 0]["labels"][0, 0].flatten()

                input_train = input_train.reshape(
                    (input_train.shape[0], 28, 28), order="F"
                )
                input_test = input_test.reshape(
                    (input_test.shape[0], 28, 28), order="F"
                )
                (DNNFunctions.raw_train_x, DNNFunctions.raw_train_y), (DNNFunctions.raw_test_x, DNNFunctions.raw_test_y) = (input_train, target_train), (input_test, target_test)
                
                #Reshape the dataset to process for the model
                DNNFunctions.train_x = DNNFunctions.raw_train_x.reshape(len(DNNFunctions.raw_train_x), 784)
                DNNFunctions.test_x = DNNFunctions.raw_test_x.reshape(len(DNNFunctions.raw_test_x), 784)

                DNNFunctions.train_x = DNNFunctions.train_x.astype('float32')
                DNNFunctions.test_x = DNNFunctions.test_x.astype('float32')
                DNNFunctions.train_x = DNNFunctions.train_x/255
                DNNFunctions.test_x = DNNFunctions.test_x/255

                DNNFunctions.train_y = keras.utils.np_utils.to_categorical(DNNFunctions.raw_train_y)
                DNNFunctions.test_y = keras.utils.np_utils.to_categorical(DNNFunctions.raw_test_y)

                DNNFunctions.train_x = DNNFunctions.train_x.reshape(-1, 28, 28, 1)
                DNNFunctions.test_x = DNNFunctions.test_x.reshape(-1, 28, 28, 1)
        #depending on the chosen class calls the setLabel function
        DNNFunctions.setLabel(string)
        
    #Given a string of the chosen class of data
    def setLabel(string):
        #Depending on chosen class of data sets the labels of the activated dataset to the respect labels
        if string =='matlab/emnist-balanced.mat':
            DNNFunctions.labels = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabdefghnqrt'
        elif string == 'matlab/emnist-bymerge.mat':
            DNNFunctions.labels = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabdefghnqrt'
        elif string == 'matlab/emnist-digits.mat':
            DNNFunctions.labels = '0123456789'
        elif string ==  'matlab/emnist-letters.mat':
            DNNFunctions.labels = 'AABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        elif string ==  'matlab/emnist-mnist.mat':
            DNNFunctions.labels = '0123456789'

                


    def convertCvImage2QtImage(cv_img): #function not used presently
        if len(cv_img.shape)<3:
            frame = cv2.cvtColor(cv_img, cv2.COLOR_GRAY2RGB)
        else:
            frame = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w = cv_img.shape[:2]
        bytesPerLine = 3 * w
        qimage = QImage(frame.data, w, h, bytesPerLine, QImage.Format.Format_RGB888)
        return qimage
    
    #Function converts numpy array to image and is passed a numpy array from the dataset
    def convertNumpyArrayToImage(np1):
        img = ToPILImage()(np1)
        qim = ImageQt(img)
        pix = QPixmap.fromImage(qim)
        return pix

    def convertPILImageToPixmap(pilImage): #function not used presently
        image = QImage(pilImage, pilImage.size[0], pilImage.size[1], QImage.Format_ARGB32)
        pix = QPixmap.fromImage(image)
        return pix

    def make_model():    
        #Create Sequential Model
        DNNFunctions.model = Sequential()
        DNNFunctions.model.add(Conv2D(32, kernel_size=(3, 3), strides=1,activation='relu', input_shape = (28, 28, 1)))
        DNNFunctions.model.add(BatchNormalization())
        DNNFunctions.model.add(Conv2D(32, (3, 3), activation='relu', strides=1))
        DNNFunctions.model.add(BatchNormalization())
        DNNFunctions.model.add(Dropout(0.4))
        DNNFunctions.model.add(Flatten())
        DNNFunctions.model.add(Dropout(0.4))
        DNNFunctions.model.add(Dense(128, activation='relu'))
        DNNFunctions.model.add(Dense(62, activation='softmax'))
        
    #Load model --> takes in model path and returns true if model exists
    def model_load(model_path):
        try:
            DNNFunctions.loaded_model = load_model(model_path)
            return True
        except IOError as ioe:
            return False
    

    #Predict using the loaded model and return the prediction
    def predict(img_path):
        DNNFunctions.model = DNNFunctions.loaded_model
        image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE )

        resized_img = cv2.resize(image, (28, 28))
        resized_img = resized_img/255
        resized_img = np.expand_dims(resized_img, axis=2)
        resized_img = resized_img.reshape(-1,28,28,1)

        with contextlib.redirect_stdout(io.StringIO()):
            results = np.round(DNNFunctions.model.predict(resized_img, verbose=1), decimals=2)
        resultLabels = np.argmax(results, axis = 1)
        return(DNNFunctions.labels[resultLabels[0]])
        
        