from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, QMainWindow, QWidget, QGridLayout
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from Model.Data import *
from Utils.ErrorMessage import *

class RandomTableWidget(QMainWindow):

    # initializing signal for creating condition
    randomCreated = pyqtSignal(Tag, list)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.header = ["Random Response", "Random Response"]
        self.conItemArr = list()

        self.initTable()

    def initTable(self):
        self.setWindowTitle("Edit Random")
        self.mainSpace = QWidget()
        self.setCentralWidget(self.mainSpace)
        self.mainSpace.setLayout(QGridLayout())

        # initialize table and dimensions 3x3 to start
        self.mainSpace.tableWidget = QTableWidget()
        self.mainSpace.tableWidget.setRowCount(2)
        self.mainSpace.tableWidget.setColumnCount(1)

        # initializing labels for the table
        self.mainSpace.tableWidget.setVerticalHeaderLabels(self.header)

        # adding table to main widget
        self.mainSpace.layout().addWidget(self.mainSpace.tableWidget, 0, 0)

        # initialize contents in widget window
        self.create = QPushButton("Create")
        self.addRow = QPushButton("Add Row")
        self.delRow = QPushButton("Delete Row")
        self.mainSpace.layout().addWidget(self.create, 1, 0)
        self.mainSpace.layout().addWidget(self.addRow, 1, 1)
        self.mainSpace.layout().addWidget(self.delRow, 1, 2)

        # click events
        self.addRow.clicked.connect(self.addRowClicked)
        self.delRow.clicked.connect(self.delRowClicked)
        self.create.clicked.connect(self.createClicked)

        self.show()

    def addRowClicked(self):
        self.mainSpace.tableWidget.insertRow(1)
        self.header.insert(1, "Random Response")
        self.mainSpace.tableWidget.setVerticalHeaderLabels(self.header)

    def delRowClicked(self):
        row = self.mainSpace.tableWidget.currentRow()
        self.mainSpace.tableWidget.removeRow(row)
        self.header.pop()
        self.mainSpace.tableWidget.setVerticalHeaderLabels(self.header)

    def createClicked(self):
        self.random = Random()
        print(self.random)

        try:
            # storing condition items in a dictionary(k, v) where k = value of condition variable, and v = response
            allRows = self.mainSpace.tableWidget.rowCount()
            for row in range(0, allRows):
                self.conItemArr.append(self.mainSpace.tableWidget.item(row, 0).text())
                print(self.mainSpace.tableWidget.item(row, 0).text())
        except Exception as ex:
            handleError(ex)
            print(ex)

        # emmitting signal
        self.randomCreated.emit(self.random, self.conItemArr)
        print("signal emitted")

        # closing window
        self.close()