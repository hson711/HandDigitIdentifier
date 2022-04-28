from asyncio.windows_events import NULL
from importlib.resources import path
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
from extra_keras_datasets import emnist


class DNNFunctions():
    
    #Class Variable
    (raw_train_x, raw_train_y), (raw_test_x, raw_test_y) = (NULL, NULL), (NULL, NULL)
    location = "C:/Users/useR/.keras/datasets"
    file = 'emnist_matlab.npz'
    pathFile = os.path.join(location, file)

    def __init__(self):
        return

        
    def rotate(image):
        image = np.fliplr(image)
        image = np.rot90(image)
        return image
    
    def loadEMNIST():
        (DNNFunctions.raw_train_x, DNNFunctions.raw_train_y), (DNNFunctions.raw_test_x, DNNFunctions.raw_test_y) = emnist.load_data(type='byclass')
        plt.imshow(DNNFunctions.raw_train_x[0], cmap='gray')
        plt.colorbar()
        plt.show()
    
    def clearCache():
        if os.path.isfile(DNNFunctions.pathFile) == True:
            os.remove(DNNFunctions.pathFile)



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