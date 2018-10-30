from collections import OrderedDict
from GUI.Node.Utils.Serializable import Serializable
from PyQt5.QtWidgets import *
from Model.Categories import Category
from PyQt5 import QtCore


class QDMNodeContentWidget(QWidget, Serializable):
    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        if self.node.category is not None:
            self.wdg_label = QLabel(str(self.node.category.id))
            self.layout.addWidget(self.wdg_label)
            self.layout.addWidget(QLabel("Pattern:"))
            self.layout.addWidget(QDMTextEdit(self.node.category.pattern))
            self.layout.addWidget(QLabel("Template:"))
            self.layout.addWidget(QDMTextEdit(self.node.category.template))
        else:
            self.wdg_label = QLabel("Some Title")
            self.layout.addWidget(self.wdg_label)
            self.layout.addWidget(QLabel("Pattern:"))
            self.layout.addWidget(QDMTextEdit(""))
            self.layout.addWidget(QLabel("Template:"))
            self.layout.addWidget(QDMTextEdit(""))

    def setEditingFlag(self, value):
        self.node.scene.grScene.views()[0].editingFlag = value

    def serialize(self):
        return OrderedDict([

        ])

    def deserialize(self, data, hashmap={}):
        return False


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
