from PyQt5.QtWidgets import QLabel, QDockWidget, QTextEdit, \
                            QGridLayout, QLineEdit, QWidget, QPushButton, QFrame
from PyQt5.QtGui import QTextImageFormat, QTextCursor, QImage, QTextDocument
from Model.Data import *
from PyQt5.QtCore import pyqtSignal, QUrl, pyqtSlot
from GUI.ConditionHTML import *
from GUI.ConditionTableWidget import *
import xml.etree.ElementTree as ET


class DockerWidget(QDockWidget):

    # Adding signal
    catCreated = pyqtSignal(Tag)

    def __init__(self, parent=None):
        super().__init__(parent)
        # initialize the category object
        self.cat = None
        # initialize a pattern object
        self.pattern = None
        # create template object
        self.template = Template()
        # initialize that object
        self.that = None
        # initialize think object
        self.think = None
        # initialize oob object
        self.oob = None
        # initialize robot object
        self.robot = None
        # initialize "create" button
        self.create = None
        # initialize video and image tags
        self.image = None
        self.video = None
        # initialize filename tag
        self.videoFileName = None
        self.imageFileName = None
        # initialize condition and condition item
        self.condition = Condition()
        self.conItem = None
        # initializing table
        self.conditionTableWidget = None
        self.conditionTableHTML = None
        self.conItemsDict = dict()

        self.initDocker()


    def initDocker(self):

        # initializing content inside widget
        self.setWindowTitle("Edit Category")
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        pattern = QLabel('What Ryan Hears (pattern):')
        that = QLabel('That (optional):')
        template = QLabel('What Ryan Says (template):')
        think = QLabel("Think")
        video = QLabel("Video Filename: ")
        image = QLabel("Image Filename: ")

        self.create = QPushButton("Create")
        starTemplate = QPushButton("Add star tag in template")
        setTemplate = QPushButton("Add set tag in template")
        getTemplate = QPushButton("Add get tag in template")
        starThink = QPushButton("Add star tag in think")
        setThink = QPushButton("Add set tag in think")
        getThink = QPushButton("Add get tag in think")
        addCondition = QPushButton("Add a condition to template")
        addGetSent = QPushButton("Add a sentiment check to your template")

        self.patternEdit = QLineEdit()
        self.templateEdit = QTextEdit()
        self.thatEdit = QLineEdit()
        self.thinkEdit = QTextEdit()
        self.videoEdit = QLineEdit()
        self.imageEdit = QLineEdit()

        # Setting layout
        grid = QGridLayout()
        self.setLayout(grid)

        # Create Widget that contains fields, it get's added to dockable widget
        widgetToDock = QWidget()
        self.setWidget(widgetToDock)

        # formatting content in widget
        widgetToDock.setLayout(QGridLayout())
        widgetToDock.layout().addWidget(pattern, 1, 0)
        widgetToDock.layout().addWidget(self.patternEdit, 1, 1)
        widgetToDock.layout().addWidget(that, 2, 0)
        widgetToDock.layout().addWidget(self.thatEdit, 2, 1)
        widgetToDock.layout().addWidget(think, 3, 0)
        widgetToDock.layout().addWidget(self.thinkEdit, 3, 1)
        # widgetToDock.layout().addWidget(starThink, 4, 2)
        # widgetToDock.layout().addWidget(setThink, 4, 1)
        # widgetToDock.layout().addWidget(getThink, 4, 0)
        widgetToDock.layout().addWidget(template, 5, 0)
        widgetToDock.layout().addWidget(self.templateEdit, 5, 1)
        # widgetToDock.layout().addWidget(starTemplate, 6, 2)
        # widgetToDock.layout().addWidget(setTemplate, 6, 1)
        # widgetToDock.layout().addWidget(getTemplate, 6, 0)
        widgetToDock.layout().addWidget(addCondition, 7, 0)
        # widgetToDock.layout().addWidget(addGetSent, 7, 1)
        widgetToDock.layout().addWidget(line, 8, 0, 1, 3)
        widgetToDock.layout().addWidget(video, 10, 0)
        widgetToDock.layout().addWidget(self.videoEdit, 10, 1)
        widgetToDock.layout().addWidget(image, 11, 0)
        widgetToDock.layout().addWidget(self.imageEdit, 11, 1)
        widgetToDock.layout().addWidget(self.create, 12, 1)

        # Click events
        self.create.clicked.connect(self.createClicked)
        addCondition.clicked.connect(self.conditionClicked)
        addGetSent.clicked.connect(self.sentimentClicked)

        # setTemplate.clicked.connect(self.setClickedTemplate)
        # getTemplate.clicked.connect(self.getClickedTemplate)
        # starTemplate.clicked.connect(self.starClickedTemplate)
        # setThink.clicked.connect(self.setClickedThink)
        # getThink.clicked.connect(self.getClickedThink)
        # starThink.clicked.connect(self.starClickedThink)

    # def setClickedTemplate(self):
    #     self.templateEdit.append("<set name=\"myVar\">Value of myVar</set>")
    #
    # def getClickedTemplate(self):
    #     self.templateEdit.append("<get name=\"myVar\" />")
    #
    # def starClickedTemplate(self):
    #     self.templateEdit.append("<star index=\"1\" />")
    #
    # def setClickedThink(self):
    #     self.thinkEdit.append("<set name=\"myVar\">Value of myVar</set>")
    #
    # def getClickedThink(self):
    #     self.thinkEdit.append("<get name=\"myVar\" />")
    #
    # def starClickedThink(self):
    #     self.thinkEdit.append("<star index=\"1\" />")
    #
    def sentimentClicked(self):
        self.thinkEdit.append("<set name=\"data\"> <star /> </set>")
        self.templateEdit.append("<condition name=\"getsentiment\">\n"
                                 "<li value=\"verypositive\"></li>\n"
                                 "<li value=\"positive\"></li>\n"
                                 "<li value=\"neutral\"></li>\n"
                                 "<li value=\"negative\"></li>\n"
                                 "<li value=\"verynegative\"></li>\n"
                                 "</condition>")

    def conditionClicked(self):
        self.conditionTableWidget = ConditionTableWidget()
        # making connection for a signal from ConditionTable creation
        self.conditionTableWidget.conditionCreated.connect(self.conditionCreated)

    def createClicked(self):
        # Initialize tag objects
        self.cat = Category()
        self.pattern = Pattern()
        self.template = Template()
        self.that = That()
        self.think = Think()
        self.oob = Oob()
        self.robot = Robot()
        self.image = Image()
        self.video = Video()
        self.videoFileName = Filename()
        self.imageFileName = Filename()
        self.condition = Condition()
        self.conItem = ConditionItem()

        # getting text from input fields
        patternText = self.patternEdit.text()
        templateText = self.templateEdit.toPlainText()
        templateHTML = self.templateEdit.toHtml()
        thatText = self.thatEdit.text()
        thinkText = self.thinkEdit.toPlainText()
        videoText = self.videoEdit.text()
        imageText = self.imageEdit.text()

        # appending content into cat object
        self.pattern.append(patternText)

        if thinkText != '':
            self.think.append(thinkText)
            self.template.append(self.think)

        #self.template.append(templateText)
        self.cat.append(self.pattern)

        if thatText != '':
            self.that.append(thatText)
            self.cat.append(self.that)

        if videoText != '':
            print("appending video filename")
            self.videoFileName.append(videoText)
            print("appending filename tag to video tag")
            self.video.append(self.videoFileName)
            print("appending video tag to robot tag")
            self.robot.append(self.video)

        if imageText != '':
            self.imageFileName.append(imageText)
            self.image.append(self.imageFileName)
            self.robot.append(self.image)

        # checking for HTML table, if it exits, parse into condition tag object
        if self.conditionTableHTML is not None:
            self.condition.setAttrib(self.conditionTableHTML.getAttrib())
            print("templateHTML: " + templateHTML)
            root = ET.fromstring(templateHTML)
            root = root.find('body')
            tempRoot = root
            newroot = root.findall('*')
            for child in newroot:
                if child.tag == 'table':
                    break
                elif child.tag == 'p':
                    print("child.text: " + child.text)
                    self.template.append(child.text)
                else:
                    print("do nothing")

            root = root.find('table')
            print("root before parsing: " + root.tag)
            self.condition = self.parse(root, self.condition)
            self.template.append(self.condition)
            tempRoot = tempRoot.findall('*')
            shouldAppend = False
            for child in tempRoot:
                if child.tag == 'p':
                    if shouldAppend is True:
                        print("child.text: " + child.text)
                        self.template.append(child.text)
                if child.tag == 'table':
                    shouldAppend = True
        else:
            print("no table exists. append text")
            self.template.append(templateText)

        self.oob.append(self.robot)
        self.template.append(self.oob)
        self.cat.append(self.template)

        # clear contents inside docker widget
        self.patternEdit.clear()
        self.thatEdit.clear()
        self.patternEdit.clear()
        self.thinkEdit.clear()
        self.templateEdit.clear()
        self.videoEdit.clear()
        self.imageEdit.clear()

        # emitting signal
        self.catCreated.emit(self.cat)

        # clearing tag objects
        self.cat = None
        self.pattern = None
        self.that = None
        self.think = None
        self.oob = None
        self.robot = None
        self.image = None
        self.video = None
        self.mediaFileName = None
        # self.condition = None
        self.conItem = None
        self.conditionTableHTML = None

    def parse(self, root, condition, prevChildText=""):
        print("root.tag: " + root.tag)
        flag = 0
        for child in root:
            if child.tag == "tr":
                self.parse(child, condition)
            elif child.tag == "table":
                self.parse(child, condition)
                # print("root.text: " + root.text)
                # print("child.tail: " + child.tail)
            elif child.tag == "td":
                flag = flag + 1
                if flag == 1:
                    prevChildText = child.find('p')
                elif flag == 2:
                    print("second td in row")
                    self.parse(child, condition, prevChildText)
            elif child.tag == "p":
                if child.text is None:
                    print("then most likely span is a child")
                else:
                    conItem = ConditionItem(prevChildText.text)
                    conItem.append(child.text)
                    condition.append(conItem)

        return condition


    @pyqtSlot(Tag, dict)
    def conditionCreated(self, condition, conItems):
        print("made it to slot")
        # saving to model
        self.condition = condition
        self.conItemsDict = conItems

        # creating HTML table to be displayed in template
        self.conditionTableHTML = ConditionHTML(self.condition)

        for k, v in conItems.items():
            # creating instance of ConditionItem
            conItem = ConditionItem(k)
            conItem.append(str(v))
            # appending to Condition Tag object
            self.condition.append(conItem)
            # adding conItems to HTML table in template
            self.conditionTableHTML.appendConItem(k, v)

        print(self.condition)

        # self.template.append(self.condition)
        self.templateEdit.insertHtml(self.conditionTableHTML.table)
