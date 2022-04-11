import keras
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
import numpy as np
import struct
import random
import gzip


def read_idx(filename):
    with gzip.open(filename, 'rb') as f:
        z, dtype, dim = struct.unpack('>HBB', f.read(4))
        
        shape = tuple(struct.unpack('>I', f.read(4))[0] for d in range(dim))
        
        #Check values of files
        # print("Dimensions: ", dim)
        # print("Shape: ", shape)

        return np.frombuffer(f.read(), dtype=np.uint8).reshape(shape)

def load_emnist():
    train_images = dnld_path + 'emnist-byclass-train-images-idx3-ubyte.gz'
    train_labels = dnld_path + 'emnist-byclass-train-labels-idx1-ubyte.gz'
    test_images = dnld_path + 'emnist-byclass-test-images-idx3-ubyte.gz'
    test_labels = dnld_path + 'emnist-byclass-test-labels-idx1-ubyte.gz'

    train_x = read_idx(train_images)
    train_y = read_idx(train_labels)
    test_x = read_idx(test_images)
    test_y = read_idx(test_labels)

    return (train_x, train_y, test_x, test_y)

if __name__ == '__main__':

    #Set the path where the .gz files are located
    proj_path = r'C:/Users/Hemanth/OneDrive - The University of Auckland/UNI-Hemanth/2022/COMPSYS 302/Project1 tests/data/'
    dnld_path = proj_path + r'datafiles/'


    raw_train_x, raw_train_y, raw_test_x, raw_test_y = load_emnist()

    # plt.imshow(raw_train_x[112358].T, cmap='gray')
    # plt.colorbar()
    # plt.show()


    #Labels used to define the values of the images
    labels = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    # fig, ax = plt.subplots()

    # for x in range(raw_train_x.shape[0]):
    #     ax.clear()
    #     ax.imshow([i for i in 255 - raw_train_x[x].T], cmap='gray')
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


    # plt.imshow(train_x.reshape(len(train_x),28,28)[112358].T, cmap='gray')
    # plt.colorbar()
    # plt.show()

    n_cat = len(labels)

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
        plt.imshow(raw_test_x[sample[i]].T, cmap='gray')
        plt.title('Pred: {}'.format(labels[resultLabels[i]]))
    plt.show()