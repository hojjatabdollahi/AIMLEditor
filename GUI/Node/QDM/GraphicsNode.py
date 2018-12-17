from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Model.Data import *

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

        self._title_color = Qt.green
        self._title_font = QFont("Ubuntu", 10)

        self.rect = QRectF(
            0,
            0,
            430,
            540
        )
        self.edge_size = 10.0
        self.title_height = 35.0
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
        self.handle = QRectF(self.rect.right() - self.handleSize,
                             self.rect.bottom() - self.handleSize, self.handleSize, self.handleSize)

    def boundingRect(self):
        return self.rect

    def hoverMoveEvent(self, moveEvent):
        """
        Executed when the mouse moves over the shape (NOT PRESSED).
        """
        if self.isSelected():
            handle = None
            if self.handle.contains(moveEvent.pos()):
                handle = "k"  # something not None
            cursor = Qt.ArrowCursor if handle is None else Qt.SizeFDiagCursor
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

        if self.handle.contains(mouseEvent.pos()):
            self.handleSelected = "Bottom Right"
        if self.handleSelected:
            self.mousePressPos = mouseEvent.pos()
            self.mousePressRect = self.rect
        super().mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, event):
        # optimize me! just update the selected nodes
        for node in self.scene().scene.nodes:
            if node.grNode.isSelected():
                node.updateConnectedEdges()
        self.wasMoved = True

        if self.handleSelected is not None:
            self.interactiveResize(event.pos())
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        print("mouse released")
        try:
            super().mouseReleaseEvent(event)

            if self.wasMoved:
                self.wasMoved = False
                self.node.scene.history.storeHistory(
                    "Node moved", setModified=True)
            self.handleSelected = None
            self.mousePressPos = None
            self.mousePressRect = None
            self.update()
        except Exception as ex:
            print(ex)

    @property
    def title(self): return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    @property
    def width(self): return self.rect.width()

    @width.setter
    def width(self, value):
        self.rect.setWidth(value)

    @property
    def height(self): return self.rect.height()

    @height.setter
    def height(self, value):
        self.rect.setheight(value)

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)

    def interactiveResize(self, mousePos):
        """
        Perform shape interactive resize.
        """
        rect = QRectF(self.rect)
        self.prepareGeometryChange()
        if self.handleSelected:
            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            rect.setRight(toX)
            rect.setBottom(toY)
            self.rect = rect
            self.setContentGeo()
            self.node.updateSocketPos()
            # self.setRect(self.rect)

        self.handle = QRectF(self.rect.right() - self.handleSize,
                             self.rect.bottom() - self.handleSize, self.handleSize, self.handleSize)

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
                                 self.rect.width() - 2*self.edge_size, self.rect.height() - 2*self.edge_size-self.title_height)
        self.grContent.setWidget(self.content)

    def setContentGeo(self):
        self.content.setGeometry(self.edge_size, self.title_height + self.edge_size,
                                 self.rect.width() - 2*self.edge_size, self.rect.height() - 2*self.edge_size-self.title_height)

    def initSockets(self):
        pass

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0, 0, self.rect.width(
        ), self.title_height, self.edge_size, self.edge_size)
        path_title.addRect(0, self.title_height -
                           self.edge_size, self.edge_size, self.edge_size)
        path_title.addRect(self.rect.width() - self.edge_size, self.title_height -
                           self.edge_size, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.rect.width(),
                                    self.rect.height() - self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(0, self.title_height,
                             self.edge_size, self.edge_size)
        path_content.addRect(self.rect.width() - self.edge_size,
                             self.title_height, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(
            0, 0, self.rect.width(), self.rect.height(), self.edge_size, self.edge_size)
        painter.setPen(self._pen_default if not self.isSelected()
                       else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(255, 0, 0, 255)))
        painter.setPen(QPen(QColor(0, 0, 0, 255), 1.0,
                            Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawEllipse(self.handle)
