
import sys
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *




LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4


DEBUG = False


class SimpleItem(QtWidgets.QGraphicsItem):
    width = 40
    height = 20
    margin = 10
    penWidth = 2

    def __init__(self, parent=None):
        QtWidgets.QGraphicsItem.__init__(self, parent)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.widgetProxy = QtWidgets.QGraphicsProxyWidget(self)

    def setWidget(self, widget):
        self.widgetProxy.setWidget(widget)
        self.width = self.widgetProxy.geometry().width()
        self.height = self.widgetProxy.geometry().height()
        return self

    def boundingRect(self):
        return QtCore.QRectF(-self.margin - self.penWidth, -self.margin - self.penWidth, self.width + self.penWidth + 2*self.margin, self.height + self.penWidth + 2*self.margin)

    def paint(self, painter, option, widget):
        painter.setPen(QtGui.QPen(QtGui.QColor(
            0, 0, 0), self.penWidth, QtCore.Qt.SolidLine))
        painter.drawRoundedRect(-self.margin, -self.margin,
                                self.width+2*self.margin, self.height+2*self.margin, 5, 5)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        # painter.drawRoundedRect(self.boundingRect, 5, 5)


class TestEclipseItem(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, parent=None):
        QtWidgets.QGraphicsEllipseItem.__init__(self, parent)

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)

        # set move restriction rect for the item
        # self.move_restrict_rect = QtCore.QRectF(20, 20, 200, 200)
        # set item's rectangle
        self.setRect(QtCore.QRectF(0, 0, 50, 100))
        self.widgetProxy = QtWidgets.QGraphicsProxyWidget(self)

    def setWidget(self, widget):
        self.widgetProxy.setWidget(widget)
        self.widgetProxy.setPos(QtCore.QPoint(10, 100))
        return self

    def mouseMoveEvent(self, event):
        # check of mouse moved within the restricted area for the item
        # if self.move_restrict_rect.contains(event.scenePos()):
        QtWidgets.QGraphicsEllipseItem.mouseMoveEvent(self, event)

    # def boundingRect(self):
    #     return QtCore.QRectF(0, 0, 30, 10)

    # def rect(self):
    #     return QtCore.QRectF(50, 50, 50, 50)

    # def paint(self, painter, option, widget):
    #     painter.drawText(QtCore.QPointF(0, 10), "Hiya")
    #     painter.drawRect(self.boundingRect())


class MainForm(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        scene = QtWidgets.QGraphicsScene(-50, -50, 600, 600)
        # scene.addText("test")
        # ellipseItem = TestEclipseItem()
        # ellipseItem.setWidget(QtWidgets.QLabel("This is a test"))
        # scene.addItem(ellipseItem)
        simpleItem = SimpleItem()
        simpleItem.setWidget(QtWidgets.QLabel("I'm a big fat\n test."))
        simpleItem.setPos(100, 100)
        scene.addItem(simpleItem)
        simpleItem2 = SimpleItem()
        simpleItem2.setWidget(QtWidgets.QLineEdit())
        scene.addItem(simpleItem2)

        node1 = Node(scene, "My Awesome Node 1", inputs=[0,0,0], outputs=[1])
        

        view = QtWidgets.QGraphicsView()
        view.setScene(scene)
        view.setGeometry(QtCore.QRect(0, 0, 400, 200))
        self.setCentralWidget(view)



class QDMGraphicsNode(QGraphicsItem):
    
    handleBottomRight = 8

    handleSize = +8.0
    handleSpace = -4.0

    handleCursors = {
        handleBottomRight: Qt.SizeFDiagCursor
    }

    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node
        self.content = self.node.content

        self._title_color = Qt.white
        self._title_font = QFont("Ubuntu", 10)


        self.width = 260
        self.height = 500
        self.edge_size = 10.0
        self.title_height = 24.0
        self._padding = 4.0

        self._pen_default = QPen(QColor("#7F000000"))
        self._pen_selected = QPen(QColor("#FFFFA637"))

        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#E3212121"))

        # init title
        self.initTitle()
        self.title = self.node.title

        # init sockets
        self.initSockets()

        # init content
        self.initContent()

        self.initUI()
        self.wasMoved = False



        self.handles = {}
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None

        self.updateHandlesPos()

    def handleAt(self, point):
        """
        Returns the resize handle below the given point.
        """
        for k, v, in self.handles.items():
            if v.contains(point):
                return k
        return None
    
    def hoverMoveEvent(self, moveEvent):
        """
        Executed when the mouse moves over the shape (NOT PRESSED).
        """
        if self.isSelected():
            handle = self.handleAt(moveEvent.pos())
            cursor = Qt.ArrowCursor if handle is None else self.handleCursors[handle]
            self.setCursor(cursor)
        super().hoverMoveEvent(moveEvent)

    def hoverLeaveEvent(self, moveEvent):
        """
        Executed when the mouse leaves the shape (NOT PRESSED).
        """
        self.setCursor(Qt.ArrowCursor)
        super().hoverLeaveEvent(moveEvent)
   
    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the item.
        """
        self.handleSelected = self.handleAt(mouseEvent.pos())
        if self.handleSelected:
            self.mousePressPos = mouseEvent.pos()
            self.mousePressRect = self.boundingRect()
        super().mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        # optimize me! just update the selected nodes
        for node in self.scene().scene.nodes:
            if node.grNode.isSelected():
                node.updateConnectedEdges()
        self.wasMoved = True
        
        if self.handleSelected is not None:
            self.interactiveResize(event.pos())





    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

        if self.wasMoved:
            self.wasMoved = False
            self.node.scene.history.storeHistory("Node moved", setModified=True)
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.update()


        

    @property
    def title(self): return self._title
    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)



        # self.content.setGeometry(self.edge_size, self.title_height + self.edge_size,
                                #  self.width - 2*self.edge_size, self.height - 2*self.edge_size-self.title_height)

    def boundingRect(self):
        return QRectF(
            0,
            0,
            self.width,
            self.height
        ).normalized()
        # o = self.handleSize + self.handleSpace
        # return self.rect().adjusted(-o, -o, o, o)

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)

    def updateHandlesPos(self):
        """
        Update current resize handles according to the shape size and position.
        """
        s = self.handleSize
        b = self.boundingRect()
        self.handles[self.handleBottomRight] = QRectF(b.right() - s, b.bottom() - s, s, s)

    def interactiveResize(self, mousePos):
        """
        Perform shape interactive resize.
        """
        offset = self.handleSize + self.handleSpace
        boundingRect = self.boundingRect()
        diff = QPointF(0, 0)

        self.prepareGeometryChange()
        if self.handleSelected == self.handleBottomRight:

            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            print(diff)
            boundingRect.setRight(toX)
            boundingRect.setBottom(toY)
            # rect.setRight(boundingRect.right() - offset)
            self.content.setBottom(boundingRect.bottom() - offset)
            self.content.setRight(boundingRect.right() - offset)
        self.updateHandlesPos()
   
    # def shape(self):
    #     """
    #     Returns the shape of this item as a QPainterPath in local coordinates.
    #     """
    #     path = QPainterPath()
    #     path.addRect(self.boundingRect())
    #     if self.isSelected():
    #         for shape in self.handles.values():
    #             path.addEllipse(shape)
    #     return path

    def initTitle(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.node = self.node
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self._padding, 0)
        self.title_item.setTextWidth(
            self.width
            - 2 * self._padding
        )

    def initContent(self):
        self.grContent = QGraphicsProxyWidget(self)
        self.content.setGeometry(self.edge_size, self.title_height + self.edge_size,
                                 self.width - 2*self.edge_size, self.height - 2*self.edge_size-self.title_height)
        self.grContent.setWidget(self.content)


    def initSockets(self):
        pass



    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0,0, self.width, self.title_height, self.edge_size, self.edge_size)
        path_title.addRect(0, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        path_title.addRect(self.width - self.edge_size, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())


        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(self.width - self.edge_size, self.title_height, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())


        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(255, 0, 0, 255)))
        painter.setPen(QPen(QColor(0, 0, 0, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        for handle, rect in self.handles.items():
            if self.handleSelected is None or handle == self.handleSelected:
                painter.drawEllipse(rect)

class QDMNodeContentWidget(QWidget):
    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        self.wdg_label = QLabel("Some Title")
        self.layout.addWidget(self.wdg_label)
        self.layout.addWidget(QLabel("Pattern:"))
        self.layout.addWidget(QDMTextEdit(""))
        self.layout.addWidget(QLabel("Template:"))
        self.layout.addWidget(QDMTextEdit(""))
        
    def setEditingFlag(self, value):
        self.node.scene.grScene.views()[0].editingFlag = value



class QDMTextEdit(QTextEdit):
    def __init__(self, input):
        super().__init__(input)
        # self.setGeometry(QtCore.QRect(90, 30, 291, 21))

    def focusInEvent(self, event):
        self.parentWidget().setEditingFlag(True)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.parentWidget().setEditingFlag(False)
        super().focusOutEvent(event)


app = QtWidgets.QApplication(sys.argv)

form = MainForm()
form.show()
try:
    sys.exit(app.exec_())
except:
    print("Exited")
