from PyQt5.QtWidgets import QErrorMessage

def handleError(error):
    em = QErrorMessage.qtHandler()
    em.showMessage(str(error))
