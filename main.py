import sys
from PyQt5.QtWidgets import QApplication

from GUI.EditorWindow import EditorWindow
import Utils.Storage as Storage
import xml.etree.ElementTree as ET


# TODO: Add support for Topics to the UI. How should we visualize a Topic?


if __name__ == '__main__':
    app = QApplication(sys.argv)

    wnd = EditorWindow()
    try:
        sys.exit(app.exec_())
    except:
        pass
