from PySide2.QtWidgets import QDialog

from .autogen.symdialog_ui import Ui_SymAddrDialog

class SymAddrDialog(QDialog, Ui_SymAddrDialog):
    def __init__(self, parent=None):
        super(SymAddrDialog, self).__init__(parent)
        self.setupUi(self)
        self.sizeEdit.setText("8")

    def getSize(self):
        return int(self.sizeEdit.text())
