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

            self.find_addr = []
            self.avoid_addr = []

            self.setObjectName("angr_cutter")
            self.setWindowTitle("AngrCutter")

            self.setupUi(self)

            self.viewRegisters = RegistersTable(self)
            self.regTableBox.addWidget(self.viewRegisters)

            self.show()

            self.setupActions()

            self.startButton.clicked.connect(self.startExplore)
            self.startButton.setDisabled(True)
            self.stopButton.setDisabled(True)

            cutter.core().toggleDebugView.connect(self.debugStateChanged)

        except Exception as e:
            print("[angr-cutter]: " + traceback.format_exc())
    
    def setupActions(self):
        findAddrAction = QAction("Angr - set find address", self)
        avoidAddrAction = QAction("Angr - set avoid address", self)

        cutter.core().addContextMenuExtensionAction(
                cutter.CutterCore.ContextMenuType.Disassembly, findAddrAction)
        cutter.core().addContextMenuExtensionAction(
                cutter.CutterCore.ContextMenuType.Disassembly, avoidAddrAction)
        cutter.core().addContextMenuExtensionSeparator(
                cutter.CutterCore.ContextMenuType.Disassembly)

        findAddrAction.triggered.connect(self.setFindAddr)
        avoidAddrAction.triggered.connect(self.setAvoidAddr)

    def setFindAddr(self):
        offset = cutter.core().getOffset()
        if offset in self.avoid_addr or offset in self.find_addr:
            print("[angr-cutter] Address %s was already set" % hex(offset))
            return
        self.find_addr.append(offset)
        self.updateFindAddrLine()

    def setAvoidAddr(self):
        offset = cutter.core().getOffset()
        if offset in self.avoid_addr or offset in self.find_addr:
            print("[angr-cutter] Address %s was already set" % hex(offset))
            return
        self.avoid_addr.append(offset)
        self.updateAvoidAddrLine()

    def updateFindAddrLine(self):
        self.findLine.setText(",".join([hex(addr) for addr in self.find_addr]))

    def updateAvoidAddrLine(self):
        self.avoidLine.setText(",".join([hex(addr) for addr in self.avoid_addr]))

    def startExplore(self):
        if len(self.find_addr) == 0:
            print("[angr-cutter]: You have to set a find address to explore to")
            return
        print("[angr-cutter]: Starting exploration with find (%s) and avoid (%s)" %
                (self.find_addr, self.avoid_addr,))
        self.stateMgr = StateManager()
        self.simMgr = self.stateMgr.simulation_manager()
        self.simMgr.explore(find=self.find_addr, avoid=self.avoid_addr)
        print("[angr-cutter]: Found: " + str(self.simMgr.found[0]))
        conc = self.stateMgr.concretize(self.simMgr.found[0])
        for addr in conc:
            print("0x%x ==> %s" % (addr, repr(conc[addr])))
    
    def debugStateChanged(self):
        if cutter.core().currentlyDebugging:
            disableUi = False
        else:
            del self.stateMgr
            self.stateMgr = None
            disableUi = True

        self.startButton.setDisabled(disableUi)
        self.stopButton.setDisabled(disableUi)
