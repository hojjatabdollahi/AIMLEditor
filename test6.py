import sys
from PyQt5.QtWidgets import QApplication
import os
import json
from PyQt5.QtWidgets import QMainWindow, QLabel, QAction, QMessageBox, QApplication, QFileDialog
from PyQt5.QtWidgets import QWidget, QTextEdit, QGraphicsItem,\
    QApplication, QVBoxLayout, QPushButton
from PyQt5.QtGui import QBrush, QPen, QFont, QColor
from PyQt5.QtCore import QFile, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# TODO: Align the title
# TODO: Figure out how to limit the size of the widget (limit the size of the text box)
# TODO: Probably I will need some sort of scrollbar
# TODO: The UI should be produced on the fly using the input data:
#       based on the input type, I can come up with the proper widget to set the data
#       I can use "@" and create some annotation that says if the field is read only or editable
#       I can also add some sort of min-max value too.
# TODO: Add a testing framework. Pytest?!


class Item():
    # TODO: Input should change to dictionary instead of  these two,
    #       based on the input we generate the UI (Number of data in dict and their lable)
    def __init__(self, template=None, pattern=None):
        self.widget = QWidget()
        self.template = template
        self.pattern = pattern
        self.grid_layout = QGridLayout(self.widget)
        self.grid_layout.setContentsMargins(2, 2, 2, 2)
        self.widget.setLayout(self.grid_layout)

    def get_widget(self):
        offset = 0
        if self.pattern is not None:
            self.grid_layout.addWidget(QLabel("Pattern:"), offset, 0)
            self.grid_layout.addWidget(QTextEdit(self.pattern), offset, 1)
            offset += 1
        if self.template is not None:
            self.grid_layout.addWidget(QLabel("Template:"), offset, 0)
            self.grid_layout.addWidget(QTextEdit(self.template), offset, 1)
            offset += 1
        return self.widget


class HojjatWidget(QWidget):
    def __init__(self, parent=None, text=""):
        super().__init__(parent)
        self.widgets = []
        self.initUI(text)

    def append(self, widget):
        self.layout.addWidget(widget)

    def add_item(self, item):
        self.layout.addWidget(item.get_widget())

    def initUI(self, text):
        # _____________________
        # |       title       |
        # ---------------------
        # | Pattern:          |
        # |                   |
        # |                   |
        # | Template:         |
        # |                   |
        # |                   |
        # |                   |
        # ---------------------
        #

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        if text != "":
            self.layout.addWidget(QLabel(text),  Qt.AlignRight)
        self.setLayout(self.layout)


class EditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.filename = None
        self.initUI()

    def initUI(self):
        # create node editor widget
        item1 = Item(pattern="hello", template="hi, how are you?")
        w1 = HojjatWidget(self, "Title 1")
        w1.add_item(item1)
        w2 = HojjatWidget(self, "2")
        w2.add_item(Item(pattern="Doing well", template="Oh, that's so nice."))

        w3 = HojjatWidget(self)
        w3.append(w1)
        w3.append(w2)
        self.setCentralWidget(w3)

        # set window properties
        self.setGeometry(200, 200, 800, 600)
        # self.changeTitle()
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    wnd = EditorWindow()
    try:
        sys.exit(app.exec_())
    except:
        pass
