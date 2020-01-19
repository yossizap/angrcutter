from PySide2.QtWidgets import QAction
import PySide2.QtCore as QtCore

import cutter
from .autogen.angrcutter_ui import Ui_AngrWidget
from .debugger import cutterDebugger
from .regtable import RegistersTable

import os, traceback, json
from angrdbg import *

class AngrWidget(cutter.CutterDockWidget, Ui_AngrWidget):
    def __init__(self, parent, action):
        try:
            super(AngrWidget, self).__init__(parent, action)
            register_debugger(cutterDebugger())
            self.stateManager = None
            self.main = parent

            self.setObjectName("angr_cutter")
            self.setWindowTitle("AngrCutter")

            self.setupLayout()
            self.show()

            cutter.core().toggleDebugView.connect(self.debugStateChanged)

        except Exception as e:
            print("[angr-cutter]: " + traceback.format_exc())
    
    def setupLayout(self):
        self.setupUi(self)

        self.viewRegisters = RegistersTable(self)
        self.horizontalLayout.addWidget(self.viewRegisters)

        self.disassemblyWidget = cutter.DisassemblyWidget(None)

        self.disassemblyWidget.setObjectName("angr_disasm")
        self.disassemblyWidget.setPreviewMode(True)
        self.disassemblyWidget.setWindowTitle("Disassembly View")
        self.disassemblyWidget.setMinimumSize(QtCore.QSize(500, 500))
        self.horizontalLayout.addWidget(self.disassemblyWidget)

        finalAddrAction = QAction("Angr - set final address", self)
        finalAddrAction.setCheckable(True)
        avoidAddrAction = QAction("Angr - set avoid address", self)
        avoidAddrAction.setCheckable(True)
        cutter.core().addContextMenuAction(cutter.CutterCore.ContextMenuType.Disassembly, finalAddrAction)
        cutter.core().addContextMenuAction(cutter.CutterCore.ContextMenuType.Disassembly, avoidAddrAction)

        cutter.core().registersChanged.connect(self.updateContents)

        self.updateContents()

    def updateContents(self):
        self.viewRegisters.updateContents()
    
    def debugStateChanged(self):
        if cutter.core().currentlyDebugging:
            self.stateManager = StateManager()
        else:
            del self.stateManager
            self.stateManager = None
