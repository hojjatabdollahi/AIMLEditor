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


class EditorWidget(QWidget):

    # Adding signal
    catCreated = pyqtSignal(Tag)
    catClicked = pyqtSignal(Tag)

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

        # create a Node for signaling purposes
        # self.tempNode = Node(self.scene, "Temp")

        ########## making connections to slots ################
        window.catCreated.connect(self.categoryCreated) # connecting signal from Editor Window that is sending created category
        # TODO: make a connection from scene for incoming signals from Nodes
        # self.scene.catClicked.connect(self.categoryClicked)

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


    # slot function for a category being created and displaying on editSpace
    @pyqtSlot(Tag)
    def categoryCreated(self, cat):
        print("slot in EditorWidget")
        # print(str(cat))
        self.aiml.append(cat)
        print("category id: " + str(cat.id))
        try:
            aNode = Node(self.scene, "Category", cat)
            aNode.content.wdg_label.imageLabel.setText(str(cat))
            """ 
            this line is throwing error: Node cannot be converted to PyQt5.QtCore.QObject in this context
            try connecting signal through scene rather than node
            """
            # aNode.catClicked.connect(self.categoryClicked)
        except Exception as ex:
            print(ex)

    @pyqtSlot(Tag)
    def categoryClicked(self, cat):
        print("slot in EditorWidget")
        cat = self.aiml.find(cat.id)
        self.catClicked.emmit(cat) # emmitting signal to be sent to EditorWindow