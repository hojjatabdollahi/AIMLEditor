from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt

class ConditionTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initTable()


    def initTable(self):
        self.setWindowTitle("Edit Condition")
        # initialize table and dimensions 3x3 to start
        self.tableWidget = QTableWidget
        self.tableWidget.setRowCount(self, 3)
        self.tableWidget.setColumnCount(self, 3)

        # initializing labels for the table
        self.tableWidget.setVerticalHeaderLabels(self, ["Condition", "ConditionItem", "ConditionItem"])
        self.tableWidget.setHorizontalHeaderLabels(self, ["Variable Name", "Value of Variable", "Response (Only for Condition Items)"])


        # initialize contents in table
        # self.tableWidget.setItem(0,0, QTableWidgetItem(self, "Condition"))
        # self.tableWidget.setItem(1, 0, QTableWidgetItem(self, "ConditionItem"))
        # self.tableWidget.setItem(2, 0, QTableWidgetItem(self, "ConditionItem"))

        self.show()
