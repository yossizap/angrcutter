from PySide2.QtWidgets import QAction, QInputDialog
import PySide2.QtCore as QtCore

import cutter
from .autogen.angrcutter_ui import Ui_AngrWidget
from .debugger import cutterDebugger
from .regtable import RegistersTable

import os
import traceback
import json
from enum import Enum
from angrdbg import *
import angr

LOG_PREFIX = "[cutter-angr]"


class LogLevel(Enum):
    def __str__(self):
        return str(self.value)

    WARNING = "Warning"
    ERROR = "Error"
    INFO = "Info"


def printMessage(message, level, prefix=LOG_PREFIX):
    print("{prefix} {level}: {message}".format(
        prefix=prefix, level=level, message=message))


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
            printMessage(traceback.format_exc(), LogLevel.ERROR)

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
            printMessage("Address %s was already set" %
                         hex(offset), LogLevel.WARNING)
            return

        text, ok = QInputDialog.getText(
            self, "Symbolize address", "Size(bytes):")
        if ok:
            size = int(text)
        else:
            size = 8

        self.symAddrs[offset] = size
        self.updateSymAddrLine()
        cutter.cmd("ecHi black @ %d" % offset)

    def setFindAddr(self):
        offset = int(self.findAddrAction.data())
        if offset in self.avoidAddrs or offset in self.findAddrs or offset in self.symAddrs:
            printMessage("Address %s was already set" %
                         hex(offset), LogLevel.WARNING)
            return

        self.findAddrs.append(offset)
        self.updateFindAddrLine()
        cutter.cmd("ecHi blue @ %d" % offset)

    def setAvoidAddr(self):
        offset = int(self.avoidAddrAction.data())
        if offset in self.avoidAddrs or offset in self.findAddrs or offset in self.symAddrs:
            printMessage("Address %s was already set" %
                         hex(offset), LogLevel.WARNING)
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
        self.avoidLine.setText(
            ",".join([hex(addr) for addr in self.avoidAddrs]))

    def updateSymAddrLine(self):
        self.symLine.setText(",".join([hex(addr) + '-' + hex(addr + self.symAddrs[addr])
                                       for addr in self.symAddrs]))

    def applySim(self):
        self.stateMgr.to_dbg(self.simMgr.found[0])
        # Synchronize all widgets with the applied memory/register values
        cutter.core().refreshAll.emit()

    def startExplore(self):
        if len(self.findAddrs) == 0:
            printMessage(
                "You have to set a find address to explore to", LogLevel.WARNING)
            return

        self.stateMgr = StateManager()
        self.simMgr = self.stateMgr.simulation_manager()

        # Configure symbolic memory addresses and registers
        for addr in self.symAddrs:
            self.stateMgr.sim(addr, self.symAddrs[addr])
        for reg in self.viewRegisters.symRegs:
            self.stateMgr.sim(
                self.stateMgr[reg], self.viewRegisters.symRegs[reg])

        # Start exploration
        printMessage("Starting exploration with find (%s) and avoid (%s)" %
                     (self.findAddrs, self.avoidAddrs,), LogLevel.INFO)
        printMessage("Symbolics are: " +
                     str(self.stateMgr.symbolics), LogLevel.INFO)
        self.simMgr.explore(find=self.findAddrs, avoid=self.avoidAddrs)

        # Attempt to print the results
        if len(self.simMgr.found):
            printMessage("Found: " + str(self.simMgr.found[0]), LogLevel.INFO)

            conc = self.stateMgr.concretize(self.simMgr.found[0])
            for addr in conc:
                printMessage("0x%x ==> %s" %
                             (addr, repr(conc[addr])), LogLevel.INFO)

            self.applySimButton.setDisabled(False)
        else:
            printMessage("Failed to find a state", LogLevel.ERROR)
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
