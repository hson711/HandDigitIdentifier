#Subprocess Importer
import sys
import os
from DNNFunctions import DNNFunctions
import time
import pathlib
from extra_keras_datasets import emnist
import argparse

#Py file that allows calling of a subprocess with system arguments easily
DNNFunctions.loadEMNIST(sys.argv[1])