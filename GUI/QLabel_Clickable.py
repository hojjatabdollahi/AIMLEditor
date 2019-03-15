from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QMessageBox, QScrollArea, QVBoxLayout, QWidget
import xml.etree.ElementTree as ET
from Model.Data import *
from Utils.ErrorMessage import *


class QLabelClickable(QLabel):

    # initializing signal for click or double click events
    catClicked = pyqtSignal()

    def __init__(self, parent=None):
        super(QLabelClickable, self).__init__(parent)
        self.labelFont = QFont("Sanserif", 13)
        self.setFont(self.labelFont)

        self.setAlignment(Qt.AlignTop)

    def mousePressEvent(self, event):
        self.last = "Click"

    def mouseReleaseEvent(self, even):
        if self.last == "Click":
            QTimer.singleShot(QApplication.instance().doubleClickInterval(), self.performSingleClickAction)
        else:
            # emmit to Editor Widget, Editor Widget sends cat to Window then to Docker
            print("label clicked")
            self.catClicked.emit()

    def mouseDoubleClickEvent(self, event):
        self.last = "Double Click"

    def performSingleClickAction(self):
        if self.last == "Click":
            # emmit to Editor Widget, Editor Widget sends cat to Window then to Docker
            print("label clicked")
            self.catClicked.emit()


class LabelClickable(QWidget):
    def __init__(self, parent=None):
        super(LabelClickable, self).__init__(parent)

        self.setWindowTitle("Category")
        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        self.setFixedSize(350, 450)

        self.templateText = ""
        self.patternText = ""

        self.initUI()

    def initUI(self):
        self.patternLabel = QLabelClickable(self)
        self.patternLabel.setGeometry(0, 0, 350, 50)
        self.patternLabel.setCursor(Qt.PointingHandCursor)
        self.patternLabel.setStyleSheet("QLabel {background-color: black; color: white; border: 1px solid "
                                         "#01DFD7; border-radius: 5px;}")

        self.thatLabel = QLabelClickable(self)
        self.thatLabel.setGeometry(0, 60, 350, 50)
        self.thatLabel.setCursor(Qt.PointingHandCursor)
        self.thatLabel.setStyleSheet("QLabel {background-color: black; color: white; border: 1px solid "
                                         "#01DFD7; border-radius: 5px;}")

        self.templateLabel = QLabelClickable(self)
        self.templateLabel.setGeometry(0, 120, 350, 270)
        self.templateLabel.setToolTip("Edit category")
        self.templateLabel.setCursor(Qt.PointingHandCursor)
        self.templateLabel.setStyleSheet("QLabel {background-color: black; color: white; border: 1px solid "
                                         "#01DFD7; border-radius: 5px;}")

        # Making labels scrollable
        layout = QVBoxLayout()
        # patternArea = QScrollArea()
        # patternArea.setWidget(self.patternLabel)
        # thatArea = QScrollArea()
        # thatArea.setWidget(self.thatLabel)
        templateArea = QScrollArea()
        # templateArea.setMinimumSize(350, 270)
        templateArea.setMaximumSize(350, 270)
        templateArea.setWidget(self.templateLabel)

        # layout.addWidget(patternArea)
        # layout.addWidget(thatArea)
        layout.addWidget(self.patternLabel)
        layout.addWidget(self.thatLabel)
        layout.addWidget(templateArea)

        self.setLayout(layout)

        # templateFont = QFont("Sans", 9)
        # self.templateLabel.setFont(templateFont)

    def displayVisuals(self, category):
        try:
            self.clear()
            template = category.findTag("template")
            pattern = category.findTag("pattern")
            that = category.findTag("that")

            # print("creating visuals for the label")
            # root = ET.fromstring(str(category))
            # self.template = Template()
            # self.pattern = Pattern()
            # self.condition = Condition()
            # self.random = Random()
            # self.that = That()
            #
            # self.templateText = []
            # self.patternText = []
            # self.thatText = []
            #
            # self.templateText = self.parseTree(root)
            #
            # templateStr = ""
            # patternStr = ""
            # thatStr = ""
            #
            # # Converting list elements into a continuous string
            # templateStr = templateStr.join(self.templateText)
            # patternStr = patternStr.join(self.patternText)
            # thatStr = thatStr.join(self.thatText)

            # adding text to appropriate fields

            self.patternLabel.setText(pattern.getContents())
            if that is not None:
                self.thatLabel.setText(that.getContents())
            self.templateLabel.setText(template.getContents())

            # making sure tags don't have unnecessary attributes
            category.attrib = []
        except Exception as ex:
            print("exception caught in display visuals!")
            print(ex)
            handleError(ex)

    # def parseTree(self, root):
    #     # print("parsing through category tree to get desired text")
    #     for child in root:
    #         if child.tag == "template":
    #             if child.findall("*") is None:
    #                 if child.text is None:
    #                     # print("child.text is None")
    #                     # print("child.text for template: " + str(child.text))
    #                     self.templateText.append("")
    #                     self.template.attrib = []
    #                 else:
    #                     # print("child.text for template: " + child.text)
    #                     self.templateText.append(child.text)
    #                     self.template.attrib = []
    #             else:
    #                 self.templateText.append(child.text)
    #                 self.parseTree(child)
    #         elif child.tag == "pattern":
    #             if child.text is None:
    #                 # print("child.text is None")
    #                 # print("child.text for pattern: " + str(child.text))
    #                 self.patternText.append("")
    #                 self.pattern.attrib = []
    #             else:
    #                 # print("child.text for pattern: " + child.text)
    #                 self.patternText.append(child.text)
    #                 self.pattern.attrib = []
    #         elif child.tag == "condition":
    #             self.parseTree(child)
    #             self.condition.attrib = child.attrib
    #             self.templateText.append(str(self.condition))
    #             self.templateText.append(child.tail)
    #         elif child.tag == "random":
    #             self.parseTree(child)
    #             self.templateText.append(str(self.random))
    #             self.templateText.append(child.tail)
    #         elif child.tag == "think":
    #             think = Think()
    #             if child.find("*") is None:
    #                 print("No children think tag")
    #                 think.append(child.text)
    #                 self.templateText.append(str(think))
    #                 self.templateText.append(child.tail)
    #             else:
    #                 print("think has children")
    #                 setArr = child.findall("set")
    #                 for set in setArr:
    #                     star = set.find("star")
    #                     setTag = Set()
    #                     setTag.attrib = set.attrib
    #                     if star is not None:
    #                         setTag.append("<"+str(star.tag)+"/>")
    #                     else:
    #                         setTag.append(set.text)
    #                     think.append(setTag)
    #                     self.templateText.append(str(think))
    #                 self.templateText.append(child.tail)
    #         elif child.tag == "li":
    #             print("child.attrib: " + str(child.attrib))
    #             if child.attrib == {}:
    #                 # print("LI TAG IS FOR RANDOM!!!")
    #                 conItem = ConditionItem()
    #                 conItem.append(child.text)
    #                 self.random.append(conItem)
    #             else:
    #                 # print("LI TAG IS FOR CONDITION!!!")
    #                 conItem = ConditionItem()
    #                 conItem.append(child.text)
    #                 conItem.attrib = child.attrib
    #                 self.condition.append(conItem)
    #         elif child.tag == "that":
    #             self.thatText.append(child.text)
    #         else:
    #             print("do nothing")
    #
    #     return self.templateText

    def clear(self):
        self.templateLabel.clear()
        self.patternLabel.clear()
        self.thatLabel.clear()
