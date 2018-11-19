from PyQt5.QtWidgets import QMainWindow, QLabel, QDockWidget, QTextEdit, \
                            QGridLayout, QLineEdit, QWidget, QPushButton
from Model.Data import *
from PyQt5.QtCore import pyqtSignal

class DockerWidget(QDockWidget):

    # Adding signal
    catCreated = pyqtSignal(Tag)

    def __init__(self, parent=None):
        super().__init__(parent)
        # create the category object
        self.cat = None
        # create a pattern object
        self.pattern = None
        # create template object
        self.template = None
        # create that object
        self.that = None
        # create think object
        self.think = None
        # create oob object
        self.oob = None
        # create robot object
        self.robot = None
        # initialize "create" button
        self.create = None

        self.initDocker()


    def initDocker(self):

        # initializing content inside widget
        self.setWindowTitle("Edit Category")
        pattern = QLabel('What Ryan Hears:')
        that = QLabel('That (optional):')
        template = QLabel('What Ryan Says:')
        think = QLabel("Think")

        self.create = QPushButton("Create")
        self.star = QPushButton("Add star tag at cursor")
        set = QPushButton("Add set tag at cursor")
        get = QPushButton("Add get tag at cursor")

        self.patternEdit = QLineEdit()
        self.templateEdit = QTextEdit()
        self.thatEdit = QLineEdit()
        self.thinkEdit = QLineEdit()

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
        widgetToDock.layout().addWidget(template, 4, 0)
        widgetToDock.layout().addWidget(self.templateEdit, 4, 1)
        widgetToDock.layout().addWidget(self.star, 6, 0)
        widgetToDock.layout().addWidget(set, 5, 1)
        widgetToDock.layout().addWidget(get, 5, 0)
        widgetToDock.layout().addWidget(self.create, 8, 1)

        # Click events
        self.create.clicked.connect(self.createClicked)
        set.clicked.connect(self.setClicked)
        get.clicked.connect(self.getClicked)
        self.star.clicked.connect(self.starClicked)


    def setClicked(self):
        self.templateEdit.append("<set name=\"myVar\"> Value of myVar</set>")

    def getClicked(self):
        self.templateEdit.append("<get name=\"myVar\" />")

    def starClicked(self):
        self.templateEdit.append("<star index=\"1\" />")

    def createClicked(self):
        # Initialize tag objects
        self.cat = Category()
        self.pattern = Pattern()
        self.template = Template()
        self.that = That()
        self.think = Think()
        self.oob = Oob()
        self.robot = Robot()

        # add some body to the pattern object
        patternText = self.patternEdit.text()
        templateText = self.templateEdit.toPlainText()
        thatText = self.thatEdit.text()
        thinkText = self.thinkEdit.text()

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

        self.oob.append(self.robot)
        self.template.append(self.oob)
        self.cat.append(self.template)


        # print the category (For Debugging)
        print(self.cat)

        # emitting signal
        self.catCreated.emit(self.cat)