from PySide2.QtWidgets import QAbstractItemView, QTableWidgetItem, QMenu, QTableWidget, QHeaderView, QAction, QInputDialog
from PySide2.QtGui import QColor

import cutter

class RegistersTable(QTableWidget):
    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)
        self.parent = parent
        self.symRegs = {}

        self.setShowGrid(False)
        self.verticalHeader().hide()
        self.setColumnCount(2)

        self.setHorizontalHeaderLabels(['Register', 'Value'])
        self.resizeColumnsToContents()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        cutter.core().registersChanged.connect(self.updateContents)

        self.updateContents()

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        row = self.rowAt(event.pos().y())
        reg = self.item(row, 0).text()
        unsetRegAction = QAction("Cancel symbolization", self)
        symRegAction = QAction("Symbolize Register", self)

        if reg in self.symRegs:
            contextMenu.addAction(unsetRegAction)
        else:
            contextMenu.addAction(symRegAction)

        action = contextMenu.exec_(self.viewport().mapToGlobal(event.pos()))

        if action == symRegAction:
            text, ok = QInputDialog.getText(self, "Symbolize register", "Size(bytes):")
            if ok:
                size = int(text)
            else:
                size = 8

            self.symRegs[reg] = size
            self.updateContents()
        elif action == unsetRegAction:
            del self.symRegs[reg]
            self.updateContents()

    def updateContents(self):
        try:
            registers = cutter.cmdj("drj gpr")
        except Exception as e:
            return

        self.setRowCount(0)
        for reg, value in registers.items():
            row_position = self.rowCount()
            self.insertRow(row_position)
            self.setItem(row_position, 0, QTableWidgetItem(reg))
            self.setItem(row_position, 1, QTableWidgetItem(str(value)))

            if reg in self.symRegs:
                # Color symbolic register in light blue
                self.item(row_position, 0).setBackground(QColor(52, 152, 219))
                self.item(row_position, 1).setBackground(QColor(52, 152, 219))
