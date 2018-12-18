from PyQt5.QtWidgets import QWidget, QTextEdit, QGraphicsItem,\
    QApplication, QVBoxLayout, QPushButton, QBoxLayout, QMainWindow
from PyQt5.QtGui import QBrush, QPen, QFont, QColor
from PyQt5.QtCore import QFile, Qt, pyqtSlot, pyqtSignal
from Utils.ErrorMessage import *
from Model.Data import *
from GUI.QLabel_Clickable import *

from GUI.Node.Node import Node
from GUI.Node.Scene.Scene import Scene
from GUI.Node.Edge import Edge, EDGE_TYPE_BEZIER
from GUI.Node.QDM.GraphicsView import QDMGraphicsView
from GUI.Node.QDM.GraphicsNode import *
from GUI.Node.Utils.Socket import *


class EditorWidget(QWidget):

    # Adding signal
    catCreated = pyqtSignal(Tag)
    catClicked = pyqtSignal(Tag)
    childClicked = pyqtSignal(str)

    def __init__(self, window, parent=None):
        super().__init__(parent)

        self.stylesheet_filename = 'GUI/style/nodestyle.qss'
        self.loadStylesheet(self.stylesheet_filename)
        self.aiml = AIML()


        self.initUI(window)

    def initUI(self, window):
        self.layout = QBoxLayout(QBoxLayout.LeftToRight)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # crate graphics scene
        self.scene = Scene()
        self.grScene = self.scene.grScene

        ########## making connections to slots ################
        window.catCreated.connect(self.categoryCreated) # connecting signal from Editor Window that is sending created category
        window.catUpdated.connect(self.categoryUpdated) # connecting signal from EditorWindow to update Node


        # self.addNodes()
        # self.addDebugContent()
        # create graphics view
        self.view = QDMGraphicsView(self.scene.grScene, self)
        self.layout.addWidget(self.view)


    def addNodes(self):
        node1 = Node(self.scene, "My Awesome Node 1",
                     inputs=[0, 0, 0], outputs=[1])
        node2 = Node(self.scene, "My Awesome Node 2",
                     inputs=[3, 3, 3], outputs=[1])
        node3 = Node(self.scene, "My Awesome Node 3",
                     inputs=[2, 2, 2], outputs=[1])
        node4 = Node(self.scene, "A Category", inputs=[1, 1], outputs=[2, 2], )
        node1.setPos(-350, -250)
        node2.setPos(-75, 0)
        node3.setPos(200, -150)
        node4.setPos(200, -50)

        edge1 = Edge(
            self.scene, node1.outputs[0], node2.inputs[0], edge_type=EDGE_TYPE_BEZIER)
        edge2 = Edge(
            self.scene, node2.outputs[0], node3.inputs[0], edge_type=EDGE_TYPE_BEZIER)

    def addNode(self, title, inputs, outputs, posx, posy):
        node1 = Node(self.scene, title=title, inputs=inputs, outputs=outputs)
        node1.setPos(posx, posy)

    def updateNode(self, cat):
        try:
            print("updating node in display")
            for node in self.scene.nodes:
                if node.category.id == cat.id:
                    print("found node to update")
                    node.category = cat
                    print(str(node.category))
                    node.content.wdg_label.clear()
                    node.content.wdg_label.displayVisuals(cat)
        except Exception as ex:
            print(ex)

    def addDebugContent(self):
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)

        rect = self.grScene.addRect(-100, -100, 80,
                                    100, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)

        text = self.grScene.addText(
            "This is my Awesome text!", QFont("Ubuntu"))
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))

        widget1 = QPushButton("Hello World")
        proxy1 = self.grScene.addWidget(widget1)
        proxy1.setFlag(QGraphicsItem.ItemIsMovable)
        proxy1.setPos(0, 30)

        widget2 = QTextEdit()
        proxy2 = self.grScene.addWidget(widget2)
        proxy2.setFlag(QGraphicsItem.ItemIsSelectable)
        proxy2.setPos(0, 60)

        line = self.grScene.addLine(-200, -200, 400, -100, outlinePen)
        line.setFlag(QGraphicsItem.ItemIsMovable)
        line.setFlag(QGraphicsItem.ItemIsSelectable)

    def loadStylesheet(self, filename):
        print('STYLE loading:', filename)
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))


    """
    Determine if the condition or random table has text afterwards
    """
    def tableContainsTail(self, template):
        try:
            index = 0
            for tag in template.tags:
                print("Beginning of for loop")
                if isinstance(tag, str) is True:
                    print("found string")
                    continue
                elif tag.type == "condition" or tag.type == "random":
                    print("next item in tags list: " + str(template.tags[index+1]))
                    if isinstance(template.tags[index+1], str) is True:
                        print("returning true")
                        return True
                    else:
                        print("returning false")
                        return False
                index = index + 1
        except Exception as ex:
            print("Exception caught in tableContainsTail!")
            print(ex)
            handleError(ex)

    """
    Function to find the sentence to be used for <that> tag of potential children
    """
    def getLastSentence(self, cat):
        try:
            template = cat.findTag("template")
            if template is None:
                print("Template is empty")
                return
            condition = template.findTag("condition")
            random = template.findTag("random")
            print("Before logic")
            if condition is None and random is None:
                print("no random or condition tag found in template")
                print(str(template))
                tempString = template.findTag("text")
                print(tempString)
                tempArr = tempString.split()
                index = 0
                for word in reversed(tempArr):
                    if "." in word or "?" in word or "!" in word:
                        if index == 0:
                            print("Found last punctuation mark on very first word. Keep searching.")
                            print(word)
                        else:
                            print("Found the start of the last sentence")
                            print(word)
                            arrSize = len(tempArr)
                            start = arrSize - (index)
                            lastSentence = tempArr[start:arrSize]
                            lastSentence = " ".join(lastSentence)
                            print(lastSentence)
                            return lastSentence
                    index = index + 1
                    # print("index: " + str(index))
                print("had trouble finding last sentence")
                return
            else:
                print("template contains either a random or condition tag")
                print(str(template))
                if self.tableContainsTail(template) is True:
                    print("Random or Condition tag has text after")
                    tempString = template.findTag("text", 2)
                    print(tempString)
                    tempArr = tempString.split()
                    index = 0
                    for word in reversed(tempArr):
                        if "." in word or "?" in word or "!" in word:
                            if index == 0:
                                print("Found last punctuation mark on very first word. Keep searching.")
                                print(word)
                            else:
                                print("Found the start of the last sentence")
                                print(word)
                                arrSize = len(tempArr)
                                start = arrSize - (index)
                                lastSentence = tempArr[start:arrSize]
                                lastSentence = " ".join(lastSentence)
                                print(lastSentence)
                                return lastSentence
                        index = index + 1
                else:
                    print("Random or Condition tag is the last thing in the template")
        except Exception as ex:
            print("Exception caught in getLastSentence")
            print(ex)
            handleError(ex)

    """
    Find child nodes in the scene and add edges based off of <that> tags
    """
    def findChildNodes(self, newnode, thatStr):
        for node in self.scene.nodes:
            thatTag = node.category.findTag("that")
            print(str(thatTag))
            if thatTag is None:
                print("no that tag found in category: " + str(node.category))
            elif newnode == node:
                print("looking at node just created. Do nothing")
            else:
                # That tag was found add an edge
                print("that tag was found in category: " + str(node.category))
                parentsocket = Socket(newnode)
                newnode.outputs.append(parentsocket)
                childsocket = Socket(node, position=RIGHT_BOTTOM, socket_type=2)
                node.inputs.append(childsocket)
                edge = Edge(self.scene, parentsocket, childsocket)

    """
    Find parent nodes in the scene and add edges based off of <that> tags
    """
    def findParentNodes(self, newnode):
        try:
            print("looking for parent nodes")
            mythatTag = newnode.category.findTag("that")
            if mythatTag is None:
                print("no that tag so node will not have any parents")
                return
            thatText = mythatTag.findTag("text")
            print("Text of That Tag to look for: " + thatText)
            for node in self.scene.nodes:
                if node == newnode:
                    print("looking at node just created, do nothing")
                else:
                    print("looking at node with category: " + str(node.category))
                    # template = node.category.findTag("template")
                    templateText = self.getLastSentence(node.category)
                    if thatText == templateText:
                        print("Found child node")
                        parentsocket = Socket(node)
                        node.outputs.append(parentsocket)
                        childsocket = Socket(newnode, position=RIGHT_BOTTOM, socket_type=2)
                        newnode.inputs.append(childsocket)
                        edge = Edge(self.scene, parentsocket, childsocket)
        except Exception as ex:
            print(ex)
            handleError(ex)

    # slot function for a category being created and displaying on editSpace
    @pyqtSlot(Tag)
    def categoryCreated(self, cat):
        print("slot in EditorWidget, categoryCreated")
        # print(str(cat))
        # print("category id: " + str(cat.id))
        self.aiml.append(cat)
        thatToCheck = self.getLastSentence(cat)
        title = "Category: " + cat.id
        aNode = Node(self.scene, title, cat)
        aNode.content.wdg_label.displayVisuals(cat)
        self.findChildNodes(aNode, thatToCheck)
        self.findParentNodes(aNode)
        aNode.content.catClicked.connect(self.categoryClicked) # connecting signals coming from Content Widget
        try:
            print("trying to connect addChild button")
            aNode.content.childClicked.connect(self.addChildClicked) # connecting signals coming from Content Widget
        except Exception as ex:
            print(ex)

    @pyqtSlot(Tag)
    def addChildClicked(self, cat):
        print("In slot of editor widget")
        thatStr = self.getLastSentence(cat)
        print(thatStr)
        self.childClicked.emit(thatStr) # emitting to Editor Window

    @pyqtSlot(Tag)
    def categoryUpdated(self, cat):
        print("slot in EditorWidget")
        try:
            updatedCat = self.aiml.update(cat)
            self.updateNode(cat)
            print("display updated")
            print("updated category\n")
            print(str(updatedCat))
        except Exception as ex:
            print("Exception caught trying to update Node in EditorWidget")
            print(ex)

    @pyqtSlot(Tag)
    def categoryClicked(self, cat):
        print("slot in EditorWidget")
        cat = self.aiml.find(cat.id)
        print(cat)
        self.catClicked.emit(cat) # emmitting signal to be sent to EditorWindow