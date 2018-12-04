from PyQt5.QtGui import QImage, QPixmap, QTextCursor, QTextImageFormat
from PyQt5.QtWidgets import QLabel
import string

class ConditionHTML():
    def __init__(self, condition):
        super().__init__()
        self.table = ""
        self.condition = condition
        self.initIcon(condition)

    def initIcon(self, condition):
        self.table = "<table border=\"1\">" \
                        "<tr>" \
                            "<th colspan=\"2\">Condition</th>" \
                        "</tr>" \
                        "<tr>" \
                            "<td colspan=\"2\">{0}</td>" \
                        "</tr>" \
                        "<tr>" \
                            "<th>Condition Item Value</th>" \
                            "<th>Response</th>" \
                        "</tr>" \
                     "</table>".format(str(condition.attrib["name"]))

    """
    Appends an additional row to the end of condition table
    """
    def appendConItem(self, k, v):
        print("appending an extra row")
        myStr = "</tr>"
        stringIndex = self.table.rfind(myStr) + 5 # looking for last occurrence of </tr> and placing cursor after it
        conItem = "<tr>" \
                    "<td>{0}</td>" \
                    "<td>{1}</td>" \
                  "</tr>".format(k, v)

        self.table = self.table[:stringIndex] + conItem + self.table[stringIndex:]

    def getAttrib(self):
        return self.condition.attrib