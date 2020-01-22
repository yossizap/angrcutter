from PySide2.QtWidgets import QAction, QInputDialog
import PySide2.QtCore as QtCore

import cutter
from .autogen.angrcutter_ui import Ui_AngrWidget
from .debugger import cutterDebugger
from .regtable import RegistersTable

import os, traceback, json
from angrdbg import *
import angr

class AngrWidget(cutter.CutterDockWidget, Ui_AngrWidget):
    def __init__(self, parent, action):
        try:
            super(AngrWidget, self).__init__(parent, action)
            register_debugger(cutterDebugger())
            self.stateMgr = None
            self.main = parent

            self.findAddrs = []
            self.avoidAddrs = []
            self.symAddrs = {}

            self.setObjectName("angr_cutter")
            self.setWindowTitle("AngrCutter")

            self.setupLayout()
            self.show()

            self.setupActions()

            self.startButton.clicked.connect(self.startExplore)
            self.applySimButton.clicked.connect(self.applySim)
            cutter.core().toggleDebugView.connect(self.debugStateChanged)

        except Exception as e:
            print("[angr-cutter]: " + traceback.format_exc())

    def setupLayout(self):
        self.setupUi(self)

        self.viewRegisters = RegistersTable(self)
        self.regTableBox.addWidget(self.viewRegisters)

        self.startButton.setDisabled(True)
        self.stopButton.setDisabled(True)
        self.applySimButton.setDisabled(True)

        self.memoryCombo.setCurrentIndex(get_memory_type())
        self.memoryCombo.currentIndexChanged.connect(self.setMemoryType)

    def setupActions(self):
        self.findAddrAction = QAction("Angr - find address", self)
        self.avoidAddrAction = QAction("Angr - avoid address", self)
        self.symAddrAction = QAction("Angr - symbolize address", self)
        self.unsetAddrAction = QAction("Angr - unset address", self)

        cutter.core().addContextMenuExtensionAction(
                cutter.CutterCore.ContextMenuType.Disassembly, self.findAddrAction)
        cutter.core().addContextMenuExtensionAction(
                cutter.CutterCore.ContextMenuType.Disassembly, self.avoidAddrAction)
        cutter.core().addContextMenuExtensionAction(
                cutter.CutterCore.ContextMenuType.Disassembly, self.symAddrAction)
        cutter.core().addContextMenuExtensionAction(
                cutter.CutterCore.ContextMenuType.Disassembly, self.unsetAddrAction)
        cutter.core().addContextMenuExtensionSeparator(
                cutter.CutterCore.ContextMenuType.Disassembly)

        cutter.core().addContextMenuExtensionAction(
                cutter.CutterCore.ContextMenuType.Addressable, self.symAddrAction)
        cutter.core().addContextMenuExtensionAction(
                cutter.CutterCore.ContextMenuType.Addressable, self.unsetAddrAction)
        cutter.core().addContextMenuExtensionSeparator(
                cutter.CutterCore.ContextMenuType.Addressable)

        self.findAddrAction.triggered.connect(self.setFindAddr)
        self.avoidAddrAction.triggered.connect(self.setAvoidAddr)
        self.unsetAddrAction.triggered.connect(self.unsetAddr)
        self.symAddrAction.triggered.connect(self.setSymAddr)

    def unsetAddr(self):
        offset = self.unsetAddrAction.data()
        if offset in self.findAddrs:
            self.findAddrs.remove(offset)
            self.updateFindAddrLine()
        if offset in self.avoidAddrs:
            self.avoidAddrs.remove(offset)
            self.updateAvoidAddrLine()
        if offset in self.symAddrs:
            del self.symAddrs[offset]
            self.updateSymAddrLine()
        cutter.cmd("ecH- @ %d" % offset)

    def setSymAddr(self):
        offset = int(self.symAddrAction.data())
        if offset in self.avoidAddrs or offset in self.findAddrs or offset in self.symAddrs:
            print("[angr-cutter] Address %s was already set" % hex(offset))
            return

        text, ok = QInputDialog.getText(self, "Symbolize address", "Size:")
        if ok:
            size = int(text)
        else:
            size = 8

        self.symAddrs[offset] = size
        self.updateSymAddrLine()
        cutter.cmd("ecHi orange @ %d" % offset)

    def setFindAddr(self):
        offset = int(self.findAddrAction.data())
        if offset in self.avoidAddrs or offset in self.findAddrs or offset in self.symAddrs:
            print("[angr-cutter] Address %s was already set" % hex(offset))
            return
        self.findAddrs.append(offset)
        self.updateFindAddrLine()
        cutter.cmd("ecHi blue @ %d" % offset)

    def setAvoidAddr(self):
        offset = int(self.avoidAddrAction.data())
        if offset in self.avoidAddrs or offset in self.findAddrs or offset in self.symAddrs:
            print("[angr-cutter] Address %s was already set" % hex(offset))
            return
        self.avoidAddrs.append(offset)
        self.updateAvoidAddrLine()
        cutter.cmd("ecHi yellow @ %d" % offset)

    def setMemoryType(self):
        set_memory_type(self.memoryCombo.currentIndex())

    def updateFindAddrLine(self):
        self.findLine.setText(",".join([hex(addr) for addr in self.findAddrs]))

    def updateAvoidAddrLine(self):
        self.avoidLine.setText(",".join([hex(addr) for addr in self.avoidAddrs]))

    def updateSymAddrLine(self):
        self.symLine.setText(",".join([hex(addr) + '-' + hex(addr + self.symAddrs[addr])
            for addr in self.symAddrs]))

    def applySim(self):
        self.simMgr.to_dbg(self.simMgr.found[0])

    def startExplore(self):
        if len(self.findAddrs) == 0:
            print("[angr-cutter]: You have to set a find address to explore to")
            return
        print("[angr-cutter]: Starting exploration with find (%s) and avoid (%s)" %
                (self.findAddrs, self.avoidAddrs,))
        self.stateMgr = StateManager()
        self.simMgr = self.stateMgr.simulation_manager()
        for addr in self.symAddrs:
            self.stateMgr.sim(addr, self.symAddrs[addr])
        self.simMgr.explore(find=self.findAddrs, avoid=self.avoidAddrs)

        print("[angr-cutter]: Found: " + str(self.simMgr.found[0]))
        conc = self.stateMgr.concretize(self.simMgr.found[0])
        for addr in conc:
            print("[angr-cutter] 0x%x ==> %s" % (addr, repr(conc[addr])))

        if len(self.simMgr.found):
            self.applySimButton.setDisabled(False)
        else:
            self.applySimButton.setDisabled(True)

        cutter.core().updateSeek()
    
    def debugStateChanged(self):
        if cutter.core().currentlyDebugging:
            disableUi = False
        else:
            del self.stateMgr
            self.stateMgr = None
            disableUi = True
            # applySim can be enabled only after startExplore
            self.applySimButton.setDisabled(True)

        self.startButton.setDisabled(disableUi)
        self.stopButton.setDisabled(disableUi)
