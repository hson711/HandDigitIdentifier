#Subprocess Importer
import sys
from tabnanny import verbose
from DNNFunctions import DNNFunctions
import pickle
from PyQt5.QtWidgets import QFileDialog, QMessageBox

#Py file that allows calling of a subprocess with system arguments easily
# Y_test = np.argmax(DNNFunctions.test_y, axis=1) # Convert one-hot to index
# y_pred = np.argmax(DNNFunctions.loaded_model.predict(DNNFunctions.test_x, verbose=1), axis=-1)

path = sys.argv[1]

#Creates subprocess to download the dataset while making console output fed to the PIPE
with open(path, 'rb') as f: 
    model_name, chosen_optimiser, chosen_epoch, chosen_batch_size, chosen_train_ratio, save_check, train_x, train_y, save_loc = pickle.load(f)



#Create Sequential Model to train
DNNFunctions.make_model()

DNNFunctions.model._name = model_name.strip()
chosen_train_ratio = 1-(chosen_train_ratio/100)


#Complie Model and Fit to train with metrics for accuracy and chosen settings for training
DNNFunctions.model.compile(loss='categorical_crossentropy', optimizer=chosen_optimiser, metrics=['accuracy'])
DNNFunctions.model.fit(train_x, train_y, epochs=chosen_epoch, batch_size=chosen_batch_size, validation_split=chosen_train_ratio, verbose=1)


#Save if button checked
if(save_check):
    DNNFunctions.model.save(save_loc)



