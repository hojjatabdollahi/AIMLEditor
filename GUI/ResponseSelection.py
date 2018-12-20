from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, QMainWindow, QWidget, QGridLayout
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from Model.Data import *
from Utils.ErrorMessage import *
from Model.Data import *


class ResponseSelection(QMainWindow):
    def __init__(self, parent=None, tag=None, category=None, editspace=None):
        super().__init__(parent)

        self.tag = tag
        self.editspace = editspace
        self.category = category

        self.initTable()

    def initTable(self):
        self.setWindowTitle("Choose sentence to create a response for")
        self.mainSpace = QWidget()
        self.setCentralWidget(self.mainSpace)
        self.mainSpace.setLayout(QGridLayout())

        # initialize table and dimensions
        self.mainSpace.tableWidget = QTableWidget()
        self.mainSpace.tableWidget.setColumnCount(1)
        # self.mainSpace.tableWidget.setRowCount(len(self.tag.tags))
        self.setRowContent(self.mainSpace.tableWidget)

        # adding table to main widget
        self.mainSpace.layout().addWidget(self.mainSpace.tableWidget, 0, 0)

        # initialize and adding buttons
        self.select = QPushButton("Select this sentence")
        self.mainSpace.layout().addWidget(self.select, 1, 0)

        # click events
        self.select.clicked.connect(self.selectClicked)

        self.show()

    def selectClicked(self):
        print("Select clicked")
        item = self.mainSpace.tableWidget.currentItem()
        itemText = item.text()
        print(itemText)
        self.editspace.childClicked.emit(itemText)
        self.close()

    def setRowContent(self, tableWidget):
        rownum = 0
        tableWidget.setRowCount(len(self.tag.tags))
        sentences = self.editspace.getLastSentence(self.category)
        print(str(sentences))
        for sentence in sentences:
            print("text to append to cell: " + sentence)
            item = QTableWidgetItem()
            item.setText(sentence)
            tableWidget.setItem(rownum, 0, item)
            rownum = rownum + 1
