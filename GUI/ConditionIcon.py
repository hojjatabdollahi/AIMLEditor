from PyQt5.QtGui import QImage, QPixmap, QTextCursor, QTextImageFormat
from PyQt5.QtWidgets import QLabel


class ConditionIcon(QImage):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initIcon()

    def initIcon(self):
        icon = QPixmap('C:/Users/DreamFace/AIMLEditor/GUI/Icons/condition.png')
        self = icon.toImage()

        # imageFormat = QTextImageFormat()
        # imageFormat.setName('C:/Users/DreamFace/AIMLEditor/GUI/Icons/condition.png')