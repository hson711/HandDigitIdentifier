from asyncio.windows_events import NULL
from importlib.resources import path
import pathlib
from traceback import print_list
from typing_extensions import Self
import keras
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
import numpy as np
import struct
import random
import gzip
import os
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



class DNNFunctions():
    data_loaded = False    
    #Class Variable
    (raw_train_x, raw_train_y), (raw_test_x, raw_test_y) = (NULL, NULL), (NULL, NULL)

    w = NULL
    user_home = str(pathlib.Path.home())
    location = user_home + "\.keras\datasets"
    file = 'emnist_matlab.npz'
    pathFile = os.path.join(location, file)
    keys = {'matlab/emnist-balanced.mat', 'matlab/emnist-byclass.mat', 'matlab/emnist-bymerge.mat', 'matlab/emnist-digits.mat', 'matlab/emnist-letters.mat', 'matlab/emnist-mnist.mat'}
    if os.path.isfile(pathFile) == True:
            numpyObject = numpy.load(pathFile)
            keys = numpyObject.keys()

    labels = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    model = NULL
    loaded_model = NULL
    
    def __init__(self):
        return

        
    def rotate(image):
        image = np.fliplr(image)
        image = np.rot90(image)
        return image
    
    def loadEMNIST(string):
        if os.path.isfile(DNNFunctions.pathFile) == False:
            (DNNFunctions.raw_train_x, DNNFunctions.raw_train_y), (DNNFunctions.raw_test_x, DNNFunctions.raw_test_y) = emnist.load_data(type='byclass')
        else:
            DNNFunctions.openPreDownloadedDataset(string)

        DNNFunctions.data_loaded = True
    
    def clearCache():
        if os.path.isfile(DNNFunctions.pathFile) == True:
            os.remove(DNNFunctions.pathFile)

    def openPreDownloadedDataset(string):
        numpyObject = numpy.load(DNNFunctions.pathFile)
        DNNFunctions.keys = numpyObject.keys()
        DNNFunctions.data_loaded = True
        #arrayData = numpyObject[string]
        #mat = scipy.io.loadmat(string)
        #print(mat[0])
        with zipfile.ZipFile(DNNFunctions.pathFile, 'r') as opened_zip:
            with opened_zip.open(string, mode = 'r') as dataSetFile:

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
                #print(DNNFunctions.raw_train_x*255)
                """
                print(DNNFunctions.raw_train_y.shape)
                print(DNNFunctions.raw_test_x.shape)
                print(DNNFunctions.raw_test_y.shape)
                """
                


    def convertCvImage2QtImage(cv_img):
        if len(cv_img.shape)<3:
            frame = cv2.cvtColor(cv_img, cv2.COLOR_GRAY2RGB)
        else:
            frame = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w = cv_img.shape[:2]
        bytesPerLine = 3 * w
        qimage = QImage(frame.data, w, h, bytesPerLine, QImage.Format.Format_RGB888)
        return qimage

    def convertNumpyArrayToImage(np1):
        img = ToPILImage()(np1)
        qim = ImageQt(img)
        pix = QPixmap.fromImage(qim)
        return pix

    def convertPILImageToPixmap(pilImage):
        image = QImage(pilImage, pilImage.size[0], pilImage.size[1], QImage.Format_ARGB32)
        pix = QPixmap.fromImage(image)
        return pix

    def train(chosenOptimiser, chosenEpochs, batchSize, modelName):
        train_x = DNNFunctions.raw_train_x.reshape(len(DNNFunctions.raw_train_x), 784)
        test_x = DNNFunctions.raw_test_x.reshape(len(DNNFunctions.raw_test_x), 784)

        train_x = train_x.astype('float32')
        test_x = test_x.astype('float32')
        train_x = train_x/255
        test_x = test_x/255

        train_y = keras.utils.np_utils.to_categorical(DNNFunctions.raw_train_y)
        test_y = keras.utils.np_utils.to_categorical(DNNFunctions.raw_test_y)

        DNNFunctions.model = keras.models.Sequential()
        DNNFunctions.model.add(Dense(16,input_dim = 784, activation='relu'))
        DNNFunctions.model.add(Dense(32,activation='relu'))
        DNNFunctions.model.add(Dense(20,activation='relu'))
        DNNFunctions.model.add(Dense(62,activation='softmax'))
        DNNFunctions.model._name = modelName
        DNNFunctions.model.compile(loss='categorical_crossentropy', optimizer=chosenOptimiser, metrics=['accuracy'])
        DNNFunctions.model.fit(train_x, train_y, epochs=chosenEpochs, batch_size=batchSize)

    def model_load(model_path):
        try:
            DNNFunctions.loaded_model = load_model(model_path)
            return True
        except IOError as ioe:
            return False


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