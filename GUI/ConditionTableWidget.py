from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, QMainWindow, QWidget, QGridLayout
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from Model.Data import *
from Utils.ErrorMessage import *


class ConditionTableWidget(QMainWindow):

    # initializing signal for creating condition
    conditionCreated = pyqtSignal(Tag, dict)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.headers = ["Condition", "Condition Item", "Condition Item"]

        # initialize aiml tag objects
        self.condition = None
        self.conItem = None

        self.conItemDict = dict()

        self.initTable()


    def initTable(self):
        self.setWindowTitle("Edit Condition")
        self.mainSpace = QWidget()
        self.setCentralWidget(self.mainSpace)
        self.mainSpace.setLayout(QGridLayout())

        # initialize table and dimensions 3x3 to start
        self.mainSpace.tableWidget = QTableWidget()
        self.mainSpace.tableWidget.setRowCount(2)
        self.mainSpace.tableWidget.setColumnCount(2)

        # disabling cell (0, 1)
        disabled = QTableWidgetItem()
        disabled.setBackground(QColor(0, 0, 0))
        self.mainSpace.tableWidget.setItem(0, 1, disabled)
        disabled.setFlags(Qt.ItemIsEditable)

        # initializing labels for the table
        self.mainSpace.tableWidget.setVerticalHeaderLabels(self.headers)
        self.mainSpace.tableWidget.setHorizontalHeaderLabels(["Variable Name/Value", "Response"])

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
        self.headers.insert(1, "Condition Item")
        self.mainSpace.tableWidget.setVerticalHeaderLabels(self.headers)

    def delRowClicked(self):
        row = self.mainSpace.tableWidget.currentRow()
        self.mainSpace.tableWidget.removeRow(row)
        self.headers.pop()
        self.mainSpace.tableWidget.setVerticalHeaderLabels(self.headers)
        # resetting disabled cell just incase first row was deleted
        disabled = QTableWidgetItem()
        disabled.setBackground(QColor(0, 0, 0))
        self.mainSpace.tableWidget.setItem(0, 1, disabled)
        disabled.setFlags(Qt.ItemIsEditable)

    def createClicked(self):
        try:
            self.condition = Condition(self.mainSpace.tableWidget.item(0, 0).text())
            print(self.condition)

            # storing condition items in a dictionary(k, v) where k = value of condition variable, and v = response
            allRows = self.mainSpace.tableWidget.rowCount()
            for row in range(1, allRows):
                self.conItemDict[self.mainSpace.tableWidget.item(row, 0).text()] = self.mainSpace.tableWidget.item(row, 1).text()
                print(self.mainSpace.tableWidget.item(row, 0).text())

            # emmitting signal
            self.conditionCreated.emit(self.condition, self.conItemDict)

            # closing window
            self.close()
        except Exception as ex:
            print("exception caught!")
            handleError(ex)
            print(ex)
