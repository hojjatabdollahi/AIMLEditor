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
    childClicked = pyqtSignal(Tag)

    def __init__(self, node, parent=None):
        self.node = node
        self.wdg_label = LabelClickable()
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # self.wdg_label = QLabel("Category")
        self.layout.addWidget(self.wdg_label)

        # add child button
        self.addChild = QPushButton("Add child")
        self.layout.addWidget(self.addChild)

        # connecting label to allow signals to be sent to slot
        self.wdg_label.templateLabel.catClicked.connect(self.categoryClicked)
        self.wdg_label.patternLabel.catClicked.connect(self.categoryClicked)
        self.wdg_label.thatLabel.catClicked.connect(self.categoryClicked)
        self.addChild.clicked.connect(self.addChildClicked)

        # self.layout.addWidget(QLabel("What Ryan Hears:"))
        # self.layout.addWidget(QDMTextEdit(""))
        # self.layout.addWidget(QLabel("What Ryan Says:"))
        # self.layout.addWidget(QDMTextEdit(""))

    def addChildClicked(self):
        print("add child clicked")
        self.childClicked.emit(self.node.category) #emitting signal to editor widget

    def setEditingFlag(self, value):
        self.node.scene.grScene.views()[0].editingFlag = value

    def serialize(self):
        return OrderedDict([

        ])

    def deserialize(self, data, hashmap={}, restore_id=True):
        return False

    @pyqtSlot()
    def categoryClicked(self):
        print("slot in ContentWidget")
        print(self.node.category)
        try:
            if self.node.category.id == "":
                print("id is empty string")
                id = QUuid()
                id = id.createUuid()
                id = id.toString()
                self.node.category.id = id
                print(self.node.category.id)
                try:
                    self.catClicked.emit(self.node.category) # emitting signal up to Editor Widget
                    print("signal emitted")
                except Exception as ex:
                    print("exception caught in Content Widget Slot")
                    print(ex)
            else:
                print("id exists")
                print(self.node.category.id)
                try:
                    self.catClicked.emit(self.node.category) # emitting signal up to Editor Widget
                    print("signal emitted")
                except Exception as ex:
                    print("exception caught in Content Widget Slot")
                    print(ex)
        except Exception as ex:
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
