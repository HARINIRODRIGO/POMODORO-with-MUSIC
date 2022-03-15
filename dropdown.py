# importing libraries
from PyQt5.QtWidgets import *
# from PyQt5 import QtCore, QtGui
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
import sys


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        # setting title
        self.label = QLabel(self)
        self.spin = QSpinBox(self)
        self.setWindowTitle("Python ")

        # setting geometry
        self.setGeometry(20, 20, 200, 200)

        # calling method
        self.ui_components()

        # showing all the widgets
        self.show()

    # method for widgets
    def ui_components(self):
        # creating spin box

        # setting geometry to spin box
        self.spin.setGeometry(50, 50, 50, 40)
        # adding action to the spin box
        self.spin.valueChanged.connect(self.show_result)

        # creating label show result

        # setting geometry
        self.label.setGeometry(50, 100, 100, 40)

    # method called by spin box
    def show_result(self):
        # getting current value
        value = self.spin.value()

        # setting value of spin box to the label
        self.label.setText("Value : " + str(value))


# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

window.show()

# start the app
sys.exit(App.exec())
