#Subprocess Importer
import sys
import os
from DNNFunctions import DNNFunctions
import time
import pathlib
from extra_keras_datasets import emnist
import argparse

DNNFunctions.loadEMNIST(sys.argv[1])