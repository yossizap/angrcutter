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
            self.stateMgr = None
            self.main = parent

            self.find_addr = -1
            self.avoid_addr = -1

            self.setObjectName("angr_cutter")
            self.setWindowTitle("AngrCutter")

            self.setupLayout()
            self.show()

            self.startButton.clicked.connect(self.startExplore)
            self.startButton.setDisabled(True)
            self.stopButton.setDisabled(True)
            self.viewRegisters.setDisabled(True)

            cutter.core().toggleDebugView.connect(self.debugStateChanged)

        except Exception as e:
            print("[angr-cutter]: " + traceback.format_exc())
    
    def setupLayout(self):
        self.setupUi(self)

        self.viewRegisters = RegistersTable(self)
        self.regTableBox.addWidget(self.viewRegisters)

        findAddrAction = QAction("Angr - set find address", self)
        avoidAddrAction = QAction("Angr - set avoid address", self)

        cutter.core().addContextMenuExtensionAction(
                cutter.CutterCore.ContextMenuType.Disassembly, findAddrAction)
        cutter.core().addContextMenuExtensionAction(
                cutter.CutterCore.ContextMenuType.Disassembly, avoidAddrAction)
        cutter.core().addContextMenuExtensionSeparator(
                cutter.CutterCore.ContextMenuType.Disassembly)

        findAddrAction.triggered.connect(self.setfindAddr)
        avoidAddrAction.triggered.connect(self.setAvoidAddr)

    def setfindAddr(self):
        self.find_addr = cutter.core().getOffset()
        self.findLine.setText(hex(self.find_addr))

    def setAvoidAddr(self):
        self.avoid_addr = cutter.core().getOffset()
        self.avoidLine.setText(hex(self.avoid_addr))

    def startExplore(self):
        pass
    
    def debugStateChanged(self):
        if cutter.core().currentlyDebugging:
            disableUi = False
        else:
            del self.stateMgr
            self.stateMgr = None
            disableUi = True

        self.startButton.setDisabled(disableUi)
        self.stopButton.setDisabled(disableUi)
        self.viewRegisters.setDisabled(disableUi)
