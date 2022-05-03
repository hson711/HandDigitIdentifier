#Subprocess Importer
import sys
from tabnanny import verbose
from DNNFunctions import DNNFunctions
import pickle

#Py file that allows calling of a subprocess with system arguments easily
# Y_test = np.argmax(DNNFunctions.test_y, axis=1) # Convert one-hot to index
# y_pred = np.argmax(DNNFunctions.loaded_model.predict(DNNFunctions.test_x, verbose=1), axis=-1)

path = sys.argv[1]

#Creates subprocess to download the dataset while making console output fed to the PIPE
with open(path, 'rb') as f: 
    model_name, chosen_optimiser, chosen_epoch, chosen_batch_size, chosen_train_ratio, train_x, train_y = pickle.load(f)


DNNFunctions.make_model()
#Create Sequential Model
DNNFunctions.model._name = model_name
chosen_train_ratio = 1-(chosen_train_ratio/100)
print("Just")
print(chosen_train_ratio)
print("Maybe")
print(chosen_epoch)

#Complie Model and Fit to train with metrics for accuracy and chosen settings for training
DNNFunctions.model.compile(loss='categorical_crossentropy', optimizer=chosen_optimiser, metrics=['accuracy'])
DNNFunctions.model.fit(train_x, train_y, epochs=chosen_epoch, batch_size=chosen_batch_size, validation_split=chosen_train_ratio, verbose=1)


with open(path, 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump(DNNFunctions.model, f, -1)
