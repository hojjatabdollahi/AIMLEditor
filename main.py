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


# from PyQt5 import QtWidgets
# import Utils.AIMLHighlighter as HL
#
# app = QtWidgets.QApplication([])
# editor = QtWidgets.QPlainTextEdit()
# editor.setStyleSheet("""QPlainTextEdit{
# 	font-family:'Consolas';
# 	color: #ccc;
# 	background-color: #2b2b2b;}""")
# highlight = HL.AIMLHIghlighter(editor.document())
# editor.show()
#
# # Load syntax.py into the editor for demo purposes
# # infile = open('Utils/AIMLHighlighter.py', 'r')
# # print("hi")
# # editor.setPlainText(infile.read())
# # print("hey")
# app.exec_()