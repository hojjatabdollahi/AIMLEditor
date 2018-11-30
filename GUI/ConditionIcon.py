from PyQt5.QtGui import QImage, QPixmap, QTextCursor, QTextImageFormat
from PyQt5.QtWidgets import QLabel
import string

class ConditionIcon():
    def __init__(self):
        super().__init__()
        self.table = ""
        self.initIcon()

    def initIcon(self):
        self.table = "<table border=\"1\">" \
                        "<tr>" \
                            "<th>Condition</th>" \
                            "<th>Variable</th>" \
                        "</tr>" \
                        "<tr>" \
                            "<td></td>" \
                            "<td></td>" \
                        "</tr>" \
                        "<tr>" \
                            "<th>Condition Item Value</th>" \
                            "<th>Response</th>" \
                        "</tr>" \
                        "<tr>" \
                            "<td></td>" \
                            "<td></td>" \
                        "</tr>" \
                     "</table>"

    """
    Appends an additional row to the condition table
    """
    def appendConItem(self):
        print("appending an extra row")
        myStr = "</tr>"
        try:
            print("index of first </tr>: " + str(self.table.rfind(myStr)))
        except Exception as ex:
            print(ex)

        stringIndex = self.table.rfind(myStr) + 5
        conItem = "<tr>" \
                    "<td>blah</td>" \
                    "<td>blah</td>" \
                  "</tr>" \

        self.table = self.table[:stringIndex] + conItem + self.table[stringIndex:]
        print(self.table)
        # self.table = self.table + conItem
