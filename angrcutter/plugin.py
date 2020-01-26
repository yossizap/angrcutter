from PySide2.QtWidgets import QAction
import PySide2.QtCore as QtCore

import cutter
from .autogen.angrcutter_ui import Ui_AngrWidget
from .debugger import cutterDebugger
from .regtable import RegistersTable
from .symdialog import SymAddrDialog

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
            cutter.core().refreshAll.connect(self.refreshAll)

        except Exception as e:
            print("[angr-cutter]: " + traceback.format_exc())

    def refreshAll(self):
        # Update baddr in refreshall since it happens after analysis and file changes
        self.baddr = int(cutter.cmd("e bin.baddr").strip('\n'), 16)

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

        dialog = SymAddrDialog()
        dialog.exec_()
        size = dialog.getSize()

        self.symAddrs[offset] = size
        self.updateSymAddrLine()
        cutter.cmd("ecHi black @ %d" % offset)

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

    def update(self):
        self.updateFindAddrLine()
        self.updateAvoidAddrLine()
        self.updateSymAddrLine()

    def updateFindAddrLine(self):
        self.findLine.setText(",".join([hex(addr) for addr in self.findAddrs]))

    def updateAvoidAddrLine(self):
        self.avoidLine.setText(",".join([hex(addr) for addr in self.avoidAddrs]))

    def updateSymAddrLine(self):
        self.symLine.setText(",".join([hex(addr) + '-' + hex(addr + self.symAddrs[addr])
            for addr in self.symAddrs]))

    def applySim(self):
        self.stateMgr.to_dbg(self.simMgr.found[0])
        # Synchronize all widgets with the applied memory/register values
        cutter.core().refreshAll.emit()

    def startExplore(self):
        if len(self.findAddrs) == 0:
            print("[angr-cutter]: You have to set a find address to explore to")
            return

        self.stateMgr = StateManager()
        self.simMgr = self.stateMgr.simulation_manager()

        # Configure symbolic memory addresses and registers
        for addr in self.symAddrs:
            self.stateMgr.sim(addr, self.symAddrs[addr])
        for reg in self.viewRegisters.symRegs:
            self.stateMgr.sim(self.stateMgr[reg], self.viewRegisters.symRegs[reg])

        # Start exploration
        print("[angr-cutter]: Starting exploration with find (%s) and avoid (%s)" %
                (self.findAddrs, self.avoidAddrs,))
        print("[angr-cutter]: Symbolics are: " + str(self.stateMgr.symbolics))
        self.simMgr.explore(find=self.findAddrs, avoid=self.avoidAddrs)

        # Attempt to print the results
        if len(self.simMgr.found):
            print("[angr-cutter]: Found: " + str(self.simMgr.found[0]))

            conc = self.stateMgr.concretize(self.simMgr.found[0])
            for addr in conc:
                print("[angr-cutter] 0x%x ==> %s" % (addr, repr(conc[addr])))

            self.applySimButton.setDisabled(False)
        else:
            print("[angr-cutter]: Failed to find a state")
            self.applySimButton.setDisabled(True)

        # Synchronize displays
        cutter.core().refreshAll.emit()
    
    def debugStateChanged(self):
        # Calculate the diff based on the previous baddr
        baddr = int(cutter.cmd("e bin.baddr").strip('\n'), 16)
        diff = baddr - self.baddr
        self.baddr = baddr

        if cutter.core().currentlyDebugging:
            disableUi = False
        else:
            del self.stateMgr
            self.stateMgr = None
            disableUi = True
            # applySim can be enabled only after startExplore
            self.applySimButton.setDisabled(True)
 
        # Enable exploration action when in debug mode
        self.startButton.setDisabled(disableUi)
        self.stopButton.setDisabled(disableUi)

        # Rebase addresses
        tmp = []
        for addr in self.findAddrs:
            tmp.append(addr + diff)
        self.findAddrs = tmp

        tmp = []
        for addr in self.avoidAddrs:
            tmp.append(addr + diff)
        self.avoidAddrs = tmp
 
        tmp = {}
        for addr in self.symAddrs:
            tmp[addr + diff] = self.symAddrs[addr]
        self.symAddrs = tmp

        self.update()
