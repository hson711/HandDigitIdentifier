import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar

class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle('Handwritten Digit/English Recognizer')
        self._createMenu()

    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&File")
        self.menu.addAction('&Quit', self.close)
        self.menu = self.menuBar().addMenu("&View")
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())