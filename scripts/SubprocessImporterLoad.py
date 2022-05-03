#Subprocess Importer
import sys
import os
from tabnanny import verbose
from DNNFunctions import DNNFunctions
import time
import pathlib
from extra_keras_datasets import emnist
import argparse
import numpy as np
import pickle

#Py file that allows calling of a subprocess with system arguments easily
# Y_test = np.argmax(DNNFunctions.test_y, axis=1) # Convert one-hot to index
# y_pred = np.argmax(DNNFunctions.loaded_model.predict(DNNFunctions.test_x, verbose=1), axis=-1)

path = sys.argv[1]

#Creates subprocess to download the dataset while making console output fed to the PIPE
with open(path, 'rb') as f: 
    model_path, test_x, test_y = pickle.load(f)

DNNFunctions.model_load(model_path)

DNNFunctions.loaded_model_results = DNNFunctions.loaded_model.evaluate(test_x, test_y)

with open(path, 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump(DNNFunctions.loaded_model_results, f, -1)