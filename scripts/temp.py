import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout

class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle('Handwritten Digit/English Recognizer')
        self._createMenu()

    def openSideWindow(x,y):
        print("1")

    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&File")
        datasetAction = self.menu.addAction('&Train Model')
        datasetAction.triggered.connect(self.openSideWindow)
        self.menu.addAction('&Quit', self.close)
        self.menu = self.menuBar().addMenu("&View")
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())