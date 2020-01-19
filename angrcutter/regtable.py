from PySide2.QtWidgets import QAbstractItemView, QTableWidgetItem, QMenu, QTableWidget, QHeaderView, QAction

import cutter

class RegistersTable(QTableWidget):
    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)
        self.parent = parent

        self.contextMenu = QMenu(self)
        self.regAction = QAction("Emulate Register", self)
        self.regAction.setCheckable(True)
        self.emulateAction = self.contextMenu.addAction(self.regAction)
        self.setShowGrid(False)
        self.verticalHeader().hide()
        self.setColumnCount(2)

        self.setHorizontalHeaderLabels(['Register', 'Value'])
        self.resizeColumnsToContents()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def contextMenuEvent(self, event):
        action = self.contextMenu.exec_(self.viewport().mapToGlobal(event.pos()))
        if action == self.regAction and cutter.core().currentlyDebugging:
            row = self.rowAt(event.pos().y())
            sm = self.parent.stateManager
            key = sm.sim(sm[self.item(row, 0).text()], 100)

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
