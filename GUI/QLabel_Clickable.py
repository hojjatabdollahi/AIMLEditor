from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QMessageBox


class QLabelClickable(QLabel):

    # initializing signal for click or double click events
    catClicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super(QLabelClickable, self).__init__(parent)

    def mousePressEvent(self, event):
        self.last = "Click"

    def mouseReleaseEvent(self, even):
        if self.last == "Click":
            QTimer.singleShot(QApplication.instance().doubleClickInterval(), self.performSingleClickAction)
        else:
            # emmit to Editor Widget, Editor Widget sends cat to Window then to Docker
            self.catClicked.emit(self.last)

    def mouseDoubleClickEvent(self, event):
        self.last = "Double Click"

    def performSingleClickAction(self):
        if self.last == "Click":
            # emmit to Editor Widget, Editor Widget sends cat to Window then to Docker
            self.catClicked.emit(self.last)





class LabelClickable(QDialog):
    def __init__(self, parent=None):
        super(LabelClickable, self).__init__(parent)

        self.setWindowTitle("Category")
        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        self.setFixedSize(250, 250)

        self.initUI()

    def initUI(self):
        self.imageLabel = QLabelClickable(self)
        self.imageLabel.setGeometry(0, 0, 250, 250)
        self.imageLabel.setToolTip("Edit category")
        self.imageLabel.setCursor(Qt.PointingHandCursor)

        self.imageLabel.setStyleSheet("QLabel {background-color: white; color: black; border: 1px solid "
                                       "#01DFD7; border-radius: 5px;}")

        # self.imageLabel.setText("Category")
        # self.imageLabel.setAlignment(Qt.AlignCenter)

        # connecting signal from QLabelClickable
        self.imageLabel.catClicked.connect(self.Click)


    def Click(self, action):
        print("clicked label")
        QMessageBox.information(self, "Type of click", "you did: {}".format(action))