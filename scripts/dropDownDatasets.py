from asyncio.windows_events import NULL
from PyQt5.QtWidgets import QComboBox, QMainWindow, QVBoxLayout
from DNNFunctions import DNNFunctions
from importDatasetScreen import importDatasetScreen
import contextlib
from photoViewerWindow import photoViewerWindow

#QMainWindow Class that allows users to choose what specific dataset to use
class dropDownDatasets(QMainWindow):

    #Initializes an instance
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Chose dataset to use')
        self.combobox = QComboBox()

        #Adds the datasets keys to the combobox
        if DNNFunctions.keys != NULL:
            for k in DNNFunctions.keys:
                self.combobox.addItem(k)

        layout = QVBoxLayout()
        layout.addWidget(self.combobox)
        self.setCentralWidget(self.combobox)

        self.combobox.currentTextChanged.connect(self.text_changed)
        self.combobox.activated.connect(self.text_changed)

    #Function that is called when a combobox option is selected
    #It closes the current window and then calls the importDataSets function
    def text_changed(self):
        with contextlib.redirect_stdout(None):
            self.s = self.combobox.currentText()
        self.importDataSets()
        self.close()

    #When called it creates an instance of the importing dataset window and shows it
    def importDataSets(self):
        self.importDatasetScreen = importDatasetScreen(self.s)
        self.importDatasetScreen.show()

#Class that allows the user to select the training or testing set to see photos of
class dropDownPhotoViewer(QMainWindow):

    #Initializing an instance
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Chose dataset to use')
        self.setGeometry(300, 300, 200, 150)

        self.combobox = QComboBox()
        self.combobox.addItem('Train Set')
        self.combobox.addItem('Test Set')

        layout = QVBoxLayout()
        layout.addWidget(self.combobox)
        self.setCentralWidget(self.combobox)

        self.combobox.currentTextChanged.connect(self.text_changed)
        self.combobox.activated.connect(self.text_changed)

    #Function that is called when a combobox option is selected
    #It closes the current window and then calls the photoViewerWindow function
    def text_changed(self):
        with contextlib.redirect_stdout(None):
            self.s = self.combobox.currentText()
        self.photoViewerWindow()
        self.close()
    
    #When called it creates an instance of the photo viewer window and shows it
    def photoViewerWindow(self):
        self.w = photoViewerWindow(self.s)