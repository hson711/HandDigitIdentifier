import os
from asyncio.windows_events import NULL
from importlib.resources import path
import pathlib
from traceback import print_list
from typing_extensions import Self
import keras
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Dropout, Flatten, BatchNormalization
import matplotlib.pyplot as plt
import numpy as np
import struct
import random
import gzip
import gzip
from extra_keras_datasets import emnist
from pandas import array
from scipy import io as sio
from PIL.ImageQt import ImageQt 
from PIL import Image
from PyQt5.QtGui import *
from PyQt5 import *
import cv2
import numpy, scipy.io, zipfile
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

    model = NULL
    loaded_model = NULL
    loaded_model_results = NULL
    
    def __init__(self):
        return

    #Rotates Image
    ##NOT CURRENTLY USED
    def rotate(image):
        image = np.fliplr(image)
        image = np.rot90(image)
        return image
    
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
        
    def model_load(model_path):
        try:
            DNNFunctions.loaded_model = load_model(model_path)
            return True
        except IOError as ioe:
            return False
    
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
        
        



#import numpy as np
#>>> import Image
#>>> im = Image.fromarray(np.random.randint(0,256,size=(100,100,3)).astype(np.uint8))
#>>> im.show()
        

    # def save_model(self):
    #     folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')

    #     #need to incorporate user input !!
    #     file_name = "model_test"
    #     self.model.save(folderpath+file_name+'.h')


"""
    (raw_train_x, raw_train_y), (raw_test_x, raw_test_y) = emnist.load_data(type='byclass')

    plt.imshow(raw_train_x[0], cmap='gray')
    plt.colorbar()
    plt.show()

    #Labels used to define the values of the images
    labels = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    # fig, ax = plt.subplots()

    # for x in range(raw_train_x.shape[0]):
    #     ax.clear()
    #     ax.imshow([i for i in 255 - raw_train_x[x]], cmap='gray')
    #     title = 'label = %d = %s' % (raw_train_y[x], labels[raw_train_y[x]])
    #     ax.set_title(title, fontsize=20)
    #     plt.pause(1)

    print('train_x_shape: ', raw_train_x.shape)
    print('train_y_shape: ', raw_train_y.shape)
    print('test_x_shape: ', raw_test_x.shape)
    print('test_y_shape: ', raw_test_y.shape)

    train_x = raw_train_x.reshape(len(raw_train_x), 784)
    test_x = raw_test_x.reshape(len(raw_test_x), 784)

    print('New train_x: ', train_x.shape)
    print('New test_x: ', test_x.shape)


    train_x = train_x.astype('float32')
    test_x = test_x.astype('float32')

    train_x = train_x/255
    test_x = test_x/255


    # plt.imshow(train_x.reshape(len(train_x),28,28)[112358], cmap='gray')
    # plt.colorbar()
    # plt.show()

    train_y = keras.utils.np_utils.to_categorical(raw_train_y)
    test_y = keras.utils.np_utils.to_categorical(raw_test_y)

    print(raw_train_y[4], train_y[4])
    print(train_x.shape)
    print(test_y.shape)

    model = keras.models.Sequential()
    model.add(Dense(16,input_dim = 784, activation='relu'))
    model.add(Dense(32,activation='relu'))
    model.add(Dense(20,activation='relu'))
    model.add(Dense(62,activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


    model.fit(train_x, train_y, epochs=1, batch_size=100)

    # Getting the loss and accuracy percentages    
    # results = model.evaluate(test_x, test_y)
    # print("Loss & Accuracy:")
    # print(results[0]*100, results[1]*100)


    #Checking the prediction of 10 randomly selected values
    random.seed(3131)
    sample = np.arange(raw_test_x.shape[0])
    np.random.shuffle(sample)
    sample = sample[0:10]

    results = np.round(model.predict(test_x[sample], verbose=1), decimals=2)
    resultLabels = np.argmax(results, axis = 1)

    fig = plt.figure(figsize=(15,8))
    for i in range(10):
        fig.add_subplot(2,5,i+1, aspect='equal')
        plt.imshow(raw_test_x[sample[i]], cmap='gray')
        plt.title('Pred: {}'.format(labels[resultLabels[i]]))
    plt.show()
    """