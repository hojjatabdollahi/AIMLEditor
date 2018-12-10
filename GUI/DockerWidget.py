from PyQt5.QtWidgets import QLabel, QDockWidget, QTextEdit, \
                            QGridLayout, QLineEdit, QWidget, QPushButton, QFrame
from PyQt5.QtGui import QTextImageFormat, QTextCursor, QImage, QTextDocument
from Model.Data import *
from PyQt5.QtCore import pyqtSignal, QUrl, pyqtSlot, QUuid
from GUI.ConditionHTML import *
from GUI.RandomHTML import *
from GUI.ConditionTableWidget import *
from GUI.RandomTableWidget import *
import xml.etree.ElementTree as ET
from GUI.QLabel_Clickable import *
from GUI.EditorWindow import *

class DockerWidget(QDockWidget):

    # Adding signal
    catCreated = pyqtSignal(Tag)
    catUpdated = pyqtSignal(Tag)

    def __init__(self, window=None, parent=None):
        super().__init__(parent)
        # initialize AIML object
        self.aiml = AIML()
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
        # initializing Condition table
        self.conditionTableWidget = None
        self.conditionTableHTML = None
        self.conItemsDict = dict()
        # initialize Random Table
        self.randomTableWidget = None
        self.randomTableHTML = None
        self.random = Random()
        self.conItemArr = list()

        # window that owns docker. Necessary for sending signals back and forth
        self.window = window

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
        self.update = QPushButton("Update")
        self.cancel = QPushButton("Cancel")
        starTemplate = QPushButton("Add star tag in template")
        setTemplate = QPushButton("Add set tag in template")
        getTemplate = QPushButton("Add get tag in template")
        starThink = QPushButton("Add star tag in think")
        setThink = QPushButton("Add set tag in think")
        getThink = QPushButton("Add get tag in think")
        addCondition = QPushButton("Add a condition to template")
        addGetSent = QPushButton("Add a sentiment check to your template")
        addRandom = QPushButton("Add random responses to template")

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
        widgetToDock.layout().addWidget(template, 5, 0)
        widgetToDock.layout().addWidget(self.templateEdit, 5, 1)
        widgetToDock.layout().addWidget(addCondition, 7, 0)
        widgetToDock.layout().addWidget(addRandom, 7, 1)
        widgetToDock.layout().addWidget(line, 8, 0, 1, 3)
        widgetToDock.layout().addWidget(video, 10, 0)
        widgetToDock.layout().addWidget(self.videoEdit, 10, 1)
        widgetToDock.layout().addWidget(image, 11, 0)
        widgetToDock.layout().addWidget(self.imageEdit, 11, 1)
        widgetToDock.layout().addWidget(self.create, 12, 1)
        widgetToDock.layout().addWidget(self.update, 12, 1)
        widgetToDock.layout().addWidget(self.cancel, 12, 0)

        self.update.setVisible(False)

        # Making connection to incoming signals
        self.window.catClicked.connect(self.categoryClicked)

        # Click events
        self.create.clicked.connect(self.createClicked)
        self.update.clicked.connect(self.updateClicked)
        addCondition.clicked.connect(self.conditionClicked)
        addRandom.clicked.connect(self.randomClicked)
        self.cancel.clicked.connect(self.cancelClicked)

    def cancelClicked(self):
        # clear contents inside docker widget
        self.patternEdit.clear()
        self.thatEdit.clear()
        self.patternEdit.clear()
        self.thinkEdit.clear()
        self.templateEdit.clear()
        self.videoEdit.clear()
        self.imageEdit.clear()

        if self.update.isVisible() is True:
            self.update.setVisible(False)

    @pyqtSlot(Tag)
    def categoryClicked(self, cat):
        print("slot in DockerWidget")
        print(cat)
        root = ET.fromstring(str(cat))
        self.update.setVisible(True)
        self.cat = cat
        try:
            self.parseCategory(root)
        except Exception as ex:
            print("Error populatingFields")
            print(ex)

    def updateClicked(self):
        print("update button clicked")

        # initializing tag objects
        self.cat = Category(self.cat.id)
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
        self.random = Random()

        self.categoryCreation()

        self.aiml.update(self.cat)

        print("updated category\n" + str(self.cat))

        self.catUpdated.emit(self.cat) # emitting signal to EditorWindow
        self.update.setVisible(False)

        # clear contents inside docker widget
        self.patternEdit.clear()
        self.thatEdit.clear()
        self.patternEdit.clear()
        self.thinkEdit.clear()
        self.templateEdit.clear()
        self.videoEdit.clear()
        self.imageEdit.clear()

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
        self.conItem = None
        self.conditionTableHTML = None
        self.randomTableHTML = None

    def parseCategory(self, root):
        print("parsing category")
        for child in root:
            if child.tag == "pattern":
                if child.find("set") is None:
                    self.patternEdit.setText(child.text)
                else:
                    set = child.find("set")
                    self.patternEdit.setText("<"+set.tag+">"+set.text+"</"+set.tag+">")
            if child.tag == "that":
                self.thatEdit.setText(child.text)
            if child.tag == "template":
                if child.findall("*") is not None:
                    print("template contains children")
                    self.templateEdit.append(child.text)
                    self.parseCategory(child)
            if child.tag == "think":
                if child.find("set") is not None:
                    print("think has child tags")
                    self.parseCategory(child)
                else:
                    self.thinkEdit.setText(child.text)
                    self.templateEdit.append(child.tail)
            if child.tag == "set":
                self.templateEdit.setText("<"+set.tag+" "+"name=\""+set.attrib+"\">"+set.text+"</"+set.tag+">")
            if child.tag == "oob":
                print("at oob")
                self.parseCategory(child)
            if child.tag == "robot":
                print("at robot")
                self.parseCategory(child)
            if child.tag == "video":
                print("at video")
                file = child.find("filename")
                self.videoEdit.setText(file.text)
            if child.tag == "image":
                print("at image")
                file = child.find("filename")
                self.imageEdit.setText(file.text)
            if child.tag == "random":
                self.randomTableHTML = RandomHTML()
                responses = child.findall("li")
                for item in responses:
                    self.randomTableHTML.appendConItem(item.text)
                self.templateEdit.insertHtml(self.randomTableHTML.table)
                self.templateEdit.append(child.tail)
            if child.tag == "condition":
                self.conditionTableHTML = ConditionHTML(self.condition)
                responses = child.findall("li")
                for item in responses:
                    self.conditionTableHTML.appendConItem(item.get("value"), item.text)
                self.templateEdit.insertHtml(self.conditionTableHTML.table)
                self.templateEdit.append(child.tail)


    def conditionClicked(self):
        self.conditionTableWidget = ConditionTableWidget()
        # making connection for a signal from ConditionTable creation
        self.conditionTableWidget.conditionCreated.connect(self.conditionCreated)

    def randomClicked(self):
        self.randomTableWidget = RandomTableWidget()
        # making connection for a signal from RandomTable creation
        self.randomTableWidget.randomCreated.connect(self.randomCreated)

    def createClicked(self):
        # Initialize tag objects
        id = QUuid()
        id = id.createUuid()
        id = id.toString()
        self.cat = Category(id)
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
        self.random = Random()

        self.categoryCreation()

        # clear contents inside docker widget
        self.patternEdit.clear()
        self.thatEdit.clear()
        self.patternEdit.clear()
        self.thinkEdit.clear()
        self.templateEdit.clear()
        self.videoEdit.clear()
        self.imageEdit.clear()

        self.aiml.append(self.cat)

        # emitting signal to EditorWindow to be sent to EditorWidget
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
        self.conItem = None
        self.conditionTableHTML = None
        self.randomTableHTML = None

    def parseCondition(self, root, condition, prevChildText=""):
        print("root.tag: " + root.tag)
        flag = 0
        for child in root:
            if child.tag == "tr":
                self.parseCondition(child, condition)
            elif child.tag == "table":
                self.parseCondition(child, condition)
                # print("root.text: " + root.text)
                # print("child.tail: " + child.tail)
            elif child.tag == "td":
                flag = flag + 1
                if flag == 1:
                    prevChildText = child.find('p')
                elif flag == 2:
                    print("second td in row")
                    self.parseCondition(child, condition, prevChildText)
            elif child.tag == "p":
                if child.text is None:
                    print("then most likely span is a child")
                else:
                    conItem = ConditionItem(prevChildText.text)
                    conItem.append(child.text)
                    condition.append(conItem)

        return condition

    def parseRandom(self, root, random):
        for child in root:
            if child.tag == "tr":
                print("child.tag = tr")
                self.parseRandom(child, random)
            elif child.tag == "td":
                print("child.tag = td")
                self.parseRandom(child, random)
            elif child.tag == "p":
                if child.text is None:
                    print("then most likely span is a child")
                else:
                    conItem = ConditionItem()
                    print("Child.text: " + child.text)
                    conItem.append(child.text)
                    random.append(conItem)
                    print(random)
            elif child.tag == "th":
                print("child.tag = th")
                print("do nothing")

        print("parsing done")
        return random


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

    @pyqtSlot(Tag, list)
    def randomCreated(self, random, conItems):
        print("made it to the slot")
        self.random = random
        self.conItemArr = conItems

        # creating HTML table to be displayed in template
        self.randomTableHTML = RandomHTML()

        for item in conItems:
            conItem = ConditionItem()
            conItem.append(str(item))
            self.random.append(conItem)
            self.randomTableHTML.appendConItem(str(item))

        self.templateEdit.insertHtml(self.randomTableHTML.table)

    def categoryCreation(self):
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

        # self.template.append(templateText)
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
        # parse in a way where <p> before and after <table> is appended to template as text
        if self.conditionTableHTML is not None:
            self.condition.setAttrib(self.conditionTableHTML.getAttrib())
            print("templateHTML: " + templateHTML)
            root = ET.fromstring(templateHTML)
            root = root.find('body')
            tempRoot = root
            # appending text before table to template
            newroot = root.findall('*')
            for child in newroot:
                if child.tag == 'table':
                    break
                elif child.tag == 'p':
                    print("child.text: " + child.text)
                    self.template.append(child.text)
                else:
                    print("do nothing")

            # parsing table contents
            root = root.find('table')
            print("root before parsing: " + root.tag)
            self.condition = self.parseCondition(root, self.condition)
            self.template.append(self.condition)

            # appending text after table to template
            tempRoot = tempRoot.findall('*')
            shouldAppend = False
            for child in tempRoot:
                if child.tag == 'p':
                    if shouldAppend is True:
                        print("child.text: " + child.text)
                        self.template.append(child.text)
                if child.tag == 'table':
                    shouldAppend = True
        elif self.randomTableHTML is not None:
            print("templateHTML: " + templateHTML)
            root = ET.fromstring(templateHTML)
            root = root.find('body')
            tempRoot = root
            # appending text before table to template
            newroot = root.findall('*')
            for child in newroot:
                if child.tag == 'table':
                    break
                elif child.tag == 'p':
                    print("child.text: " + child.text)
                    self.template.append(child.text)
                else:
                    print("do nothing")

            # parsing table contents
            root = root.find('table')
            print("root before parsing: " + root.tag)
            print(self.random)
            self.random = self.parseRandom(root, self.random)
            print(self.random)
            self.template.append(self.random)

            # appending text after table to template
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