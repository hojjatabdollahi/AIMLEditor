

import sys 
from PyQt5 import QtGui, QtCore, QtWidgets

class MyItem(QtWidgets.QGraphicsItem):
    def __init__(self, parent = None):
        super().__init__(self, parent)


class MyView(QtWidgets.QGraphicsView):
    def __init__(self):
        QtWidgets.QGraphicsView.__init__(self)

        self.setGeometry(QtCore.QRect(100, 100, 600, 250))

        self.scene = QtWidgets.QGraphicsScene(self)
        self.scene.setSceneRect(QtCore.QRectF())

        self.setScene(self.scene)

        for i in range(5):
            self.item = QtWidgets.QGraphicsEllipseItem(i*75, 10, 60, 40)
            self.scene.addItem(self.item)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    view = MyView()
    view.show()
    sys.exit(app.exec_())

