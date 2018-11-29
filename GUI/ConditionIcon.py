from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel


class ConditionIcon(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initIcon()

    def initIcon(self):
        icon = QImage('C:/Users/DreamFace/AIMLEditor/GUI/Icons/condition.png')
        image = QLabel()
        #image.setToolTip('<span style="color:#B9B900">%s</span>' % (toolTip))
        image.setPixmap(QPixmap.fromImage(icon))