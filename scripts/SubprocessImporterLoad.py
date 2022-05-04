#Subprocess Importer
import sys
from DNNFunctions import DNNFunctions
import pickle

#Py file that allows calling of a subprocess with system arguments easily
# Y_test = np.argmax(DNNFunctions.test_y, axis=1) # Convert one-hot to index
# y_pred = np.argmax(DNNFunctions.loaded_model.predict(DNNFunctions.test_x, verbose=1), axis=-1)

#Get the input of the path where temp file is saved
path = sys.argv[1]

#Creates subprocess to download the dataset while making console output fed to the PIPE
with open(path, 'rb') as f: 
    model_path, test_x, test_y = pickle.load(f)

DNNFunctions.model_load(model_path)

#Evaluate the results to get accuracy
DNNFunctions.loaded_model_results = DNNFunctions.loaded_model.evaluate(test_x, test_y)


#Send back results to main process
with open(path, 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump(DNNFunctions.loaded_model_results, f, -1)