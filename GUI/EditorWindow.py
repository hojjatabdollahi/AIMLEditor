import os
import json
from PyQt5.QtWidgets import QMainWindow, QLabel, QAction, QMessageBox, QApplication, QFileDialog, QDockWidget, QTextEdit, QHBoxLayout, QVBoxLayout, \
                            QGridLayout, QLineEdit, QWidget, QPushButton
from PyQt5.QtCore import Qt, pyqtSlot
from GUI.EditorWidget import EditorWidget
from GUI.DockerWidget import DockerWidget


class EditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.filename = None
        self.editSpace = None

        self.initUI()


    def createAct(self, name, shortcut, tooltip, callback):
        act = QAction(name, self)
        act.setShortcut(shortcut)
        act.setToolTip(tooltip)
        act.triggered.connect(callback)
        return act

    def initUI(self):
        menubar = self.menuBar()
        
        # initialize Menu
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.createAct('&New', 'Ctrl+N', "Create new graph", self.onFileNew))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAct('&Open', 'Ctrl+O', "Open file", self.onFileOpen))
        fileMenu.addAction(self.createAct('&Save', 'Ctrl+S', "Save file", self.onFileSave))
        fileMenu.addAction(self.createAct('Save &As...', 'Ctrl+Shift+S', "Save file as...", self.onFileSaveAs))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAct('E&xit', 'Ctrl+Q', "Exit application", self.close))

        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction(self.createAct('&Undo', 'Ctrl+Z', "Undo last operation", self.onEditUndo))
        editMenu.addAction(self.createAct('&Redo', 'Ctrl+Shift+Z', "Redo last operation", self.onEditRedo))
        editMenu.addSeparator()
        editMenu.addAction(self.createAct('Cu&t', 'Ctrl+X', "Cut to clipboard", self.onEditCut))
        editMenu.addAction(self.createAct('&Copy', 'Ctrl+C', "Copy to clipboard", self.onEditCopy))
        editMenu.addAction(self.createAct('&Paste', 'Ctrl+V', "Paste from clipboard", self.onEditPaste))
        editMenu.addSeparator()
        editMenu.addAction(self.createAct('&Delete', 'Del', "Delete selected items", self.onEditDelete))
        editMenu.addSeparator()
        editMenu.addAction(self.createAct('&Add a Node', 'Ctrl+A', "Add a new node", self.onEditAdd))

        # Create Widget that contains fields, it get's added to dockable widget, this works, trying to move it into a new class
        # Successfully moved this code into separate class DockerWidget
        # pattern = QLabel('What Ryan Hears:')
        # that = QLabel('That (optional):')
        # template = QLabel('What Ryan Says:')
        # create = QPushButton("Create")
        # patternEdit = QLineEdit()
        # templateEdit = QLineEdit()
        # thatEdit = QLineEdit()
        # editCats = QDockWidget("Edit Category", self)
        # grid = QGridLayout()
        # editCats.setLayout(grid)
        # self.dockedWidget = QWidget(self)
        # editCats.setWidget(self.dockedWidget)
        # self.dockedWidget.setLayout(QGridLayout())
        # self.dockedWidget.layout().addWidget(pattern, 1, 0)
        # self.dockedWidget.layout().addWidget(patternEdit, 1, 1)
        # self.dockedWidget.layout().addWidget(that, 2, 0)
        # self.dockedWidget.layout().addWidget(thatEdit, 2, 1)
        # self.dockedWidget.layout().addWidget(template, 3, 0)
        # self.dockedWidget.layout().addWidget(templateEdit, 3, 1)
        # self.dockedWidget.layout().addWidget(create, 4, 1)
        # self.addDockWidget(Qt.LeftDockWidgetArea, editCats)


        # create dockable widget to have as place to write content in categories
        # Creating docker that can create categories
        docker = None
        docker = DockerWidget(docker)
        self.addDockWidget(Qt.LeftDockWidgetArea, docker)

        # Setting main editing area where Files will be displayed and can be edited
        self.editSpace = QTextEdit(self)
        self.setCentralWidget(self.editSpace)

        # connecting slot for category creation
        self.make_connection(docker)


        # create node editor widget (visualization of categories)
        # nodeeditor = EditorWidget(self)
        # nodeeditor.scene.addHasBeenModifiedListener(self.changeTitle)
        # self.setCentralWidget(nodeeditor)

        # status bar
        self.statusBar().showMessage("")
        self.status_mouse_pos = QLabel("")
        self.statusBar().addPermanentWidget(self.status_mouse_pos)
        # nodeeditor.view.scenePosChanged.connect(self.onScenePosChanged)

        # set window properties
        # self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("Program-R AIML Editor")
        # self.changeTitle()
        self.show()

    # function to make connection with signal in DockerWidget
    def make_connection(self, docker):
        docker.catCreated.connect(self.categoryCreated)

    # slot function for a category being created and displaying on editSpace
    def categoryCreated(self, cat):
        print("made it to slot")
        print(cat)
        self.editSpace.setText(str(cat))

    def changeTitle(self):
        title = "Node Editor - "
        if self.filename is None:
            title += "New"
        else:
            title += os.path.basename(self.filename)

        if self.centralWidget().scene.has_been_modified:
            title += "*"

        self.setWindowTitle(title)


    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def isModified(self):
        return self.centralWidget().scene.has_been_modified

    def maybeSave(self):
        if not self.isModified():
            return True

        res = QMessageBox.warning(self, "About to loose your work?",
                "The document has been modified.\n Do you want to save your changes?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
              )

        if res == QMessageBox.Save:
            return self.onFileSave()
        elif res == QMessageBox.Cancel:
            return False

        return True

    def onCreate(self, docker):
        self.editSpace.setText(str(docker.cat))

    def onScenePosChanged(self, x, y):
        self.status_mouse_pos.setText("Scene Pos: [%d, %d]" % (x, y))

    def onFileNew(self):
        if self.maybeSave():
            self.centralWidget().scene.clear()
            self.filename = None
            self.changeTitle()


    def onFileOpen(self):
        if self.maybeSave():
            fname, filter = QFileDialog.getOpenFileName(self, 'Open graph from file')
            if fname == '':
                return
            if os.path.isfile(fname):
                self.centralWidget().scene.loadFromFile(fname)
                self.filename = fname
                self.changeTitle()

    def onFileSave(self):
        if self.filename is None: return self.onFileSaveAs()
        self.centralWidget().scene.saveToFile(self.filename)
        self.statusBar().showMessage("Successfully saved %s" % self.filename)
        return True

    def onFileSaveAs(self):
        fname, filter = QFileDialog.getSaveFileName(self, 'Save graph to file')
        if fname == '':
            return False
        self.filename = fname
        self.onFileSave()
        return True

    def onEditUndo(self):
        self.centralWidget().scene.history.undo()

    def onEditRedo(self):
        self.centralWidget().scene.history.redo()

    def onEditDelete(self):
        self.centralWidget().scene.grScene.views()[0].deleteSelected()

    def onEditAdd(self):
        widget = self.centralWidget()
        assert isinstance(widget, EditorWidget)
        widget.addNode("new", [0], [0], 0, 0)

    def onEditCut(self):
        data = self.centralWidget().scene.clipboard.serializeSelected(delete=True)
        str_data = json.dumps(data, indent=4)
        QApplication.instance().clipboard().setText(str_data)

    def onEditCopy(self):
        data = self.centralWidget().scene.clipboard.serializeSelected(delete=False)
        str_data = json.dumps(data, indent=4)
        QApplication.instance().clipboard().setText(str_data)

    def onEditPaste(self):
        raw_data = QApplication.instance().clipboard().text()

        try:
            data = json.loads(raw_data)
        except ValueError as e:
            print("Pasting of not valid json data!", e)
            return

        # check if the json data are correct
        if 'nodes' not in data:
            print("JSON does not contain any nodes!")
            return

        self.centralWidget().scene.clipboard.deserializeFromClipboard(data)
