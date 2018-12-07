from collections import OrderedDict
from GUI.Node.Utils.Serializable import Serializable
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt, pyqtBoundSignal
from GUI.QLabel_Clickable import *
from Model.Data import *
from GUI.Node.Node import *
from PyQt5 import QtCore


class QDMNodeContentWidget(QWidget, Serializable):

    catClicked = pyqtSignal(Tag)

    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # self.wdg_label = QLabel("Category")
        self.wdg_label = LabelClickable()
        self.layout.addWidget(self.wdg_label)

        # connecting label to allow signals to be sent to slot
        self.wdg_label.imageLabel.catClicked.connect(self.categoryClicked)

        # self.layout.addWidget(QLabel("What Ryan Hears:"))
        # self.layout.addWidget(QDMTextEdit(""))
        # self.layout.addWidget(QLabel("What Ryan Says:"))
        # self.layout.addWidget(QDMTextEdit(""))

    def setEditingFlag(self, value):
        self.node.scene.grScene.views()[0].editingFlag = value

    def serialize(self):
        return OrderedDict([

        ])

    def deserialize(self, data, hashmap={}):
        return False

    @pyqtSlot()
    def categoryClicked(self):
        print("slot in Content Widget")
        try:
            self.catClicked.emit(self.node.category) # emitting signal up to Editor Widget
        except Exception as ex:
            print("exception caught in Content Widget Slot")
            print(ex)


class QDMTextEdit(QTextEdit):
    def __init__(self, input):
        super().__init__(input)
        # self.setGeometry(QtCore.QRect(90, 30, 291, 21))

    def focusInEvent(self, event):
        self.parentWidget().setEditingFlag(True)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.parentWidget().setEditingFlag(False)
        super().focusOutEvent(event)


# class CategoryEditor(QWidget):
#     def __init__(self)
