from PyQt5.QtWidgets import QLabel, QDockWidget, QTextEdit, \
                            QGridLayout, QLineEdit, QWidget, QPushButton, QFrame
from PyQt5.QtGui import QTextImageFormat, QTextCursor, QImage, QTextDocument
from Model.Data import *
from PyQt5.QtCore import pyqtSignal, QUrl
from GUI.ConditionIcon import *

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
        self.condition = None
        self.conItem = None
        # initializing table
        self.conditionTable = None

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
        self.addConItem = QPushButton("Add li tag to your condition")
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
        widgetToDock.layout().addWidget(addGetSent, 7, 1)
        widgetToDock.layout().addWidget(line, 8, 0, 1, 3)
        widgetToDock.layout().addWidget(self.addConItem, 6, 0)
        widgetToDock.layout().addWidget(video, 10, 0)
        widgetToDock.layout().addWidget(self.videoEdit, 10, 1)
        widgetToDock.layout().addWidget(image, 11, 0)
        widgetToDock.layout().addWidget(self.imageEdit, 11, 1)
        widgetToDock.layout().addWidget(self.create, 12, 1)

        # hiding elements on init
        self.addConItem.setVisible(False)

        # Click events
        self.create.clicked.connect(self.createClicked)
        setTemplate.clicked.connect(self.setClickedTemplate)
        getTemplate.clicked.connect(self.getClickedTemplate)
        starTemplate.clicked.connect(self.starClickedTemplate)
        setThink.clicked.connect(self.setClickedThink)
        getThink.clicked.connect(self.getClickedThink)
        starThink.clicked.connect(self.starClickedThink)
        addCondition.clicked.connect(self.conditionClicked)
        self.addConItem.clicked.connect(self.conItemClicked)
        addGetSent.clicked.connect(self.sentimentClicked)

    def setClickedTemplate(self):
        self.templateEdit.append("<set name=\"myVar\">Value of myVar</set>")

    def getClickedTemplate(self):
        self.templateEdit.append("<get name=\"myVar\" />")

    def starClickedTemplate(self):
        self.templateEdit.append("<star index=\"1\" />")

    def setClickedThink(self):
        self.thinkEdit.append("<set name=\"myVar\">Value of myVar</set>")

    def getClickedThink(self):
        self.thinkEdit.append("<get name=\"myVar\" />")

    def starClickedThink(self):
        self.thinkEdit.append("<star index=\"1\" />")

    def conditionClicked(self):
        self.addConItem.setVisible(True)
        self.conditionTable = ConditionIcon()
        self.templateEdit.insertHtml(self.conditionTable.table)

    def conItemClicked(self):
        self.addConItem.show()
        self.conditionTable.appendConItem()
        self.templateEdit.setHtml(self.conditionTable.table)

    def sentimentClicked(self):
        self.thinkEdit.append("<set name=\"data\"> <star /> </set>")
        self.templateEdit.append("<condition name=\"getsentiment\">\n"
                                 "<li value=\"verypositive\"></li>\n"
                                 "<li value=\"positive\"></li>\n"
                                 "<li value=\"neutral\"></li>\n"
                                 "<li value=\"negative\"></li>\n"
                                 "<li value=\"verynegative\"></li>\n"
                                 "</condition>")

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
        thatText = self.thatEdit.text()
        thinkText = self.thinkEdit.toPlainText()
        videoText = self.videoEdit.text()
        imageText = self.imageEdit.text()

        # appending content into cat object
        self.pattern.append(patternText)

        if thinkText != '':
            self.think.append(thinkText)
            self.template.append(self.think)

        self.template.append(templateText)
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
        self.condition = None
        self.conItem = None