import cutter

from .plugin import AngrWidget, printMessage, LogLevel

from PySide2.QtWidgets import QAction


class angrCutterPlugin(cutter.CutterPlugin):
    name = 'angr-cutter'
    description = "Angr integration with Cutter's debugger"
    version = '1.0'
    author = 'Yossi Zap'

    def setupPlugin(self):
        pass

    def setupInterface(self, main):
        action = QAction("AngrCutter", main)
        action.setCheckable(True)
        widget = AngrWidget(main, action)
        main.addPluginDockWidget(widget, action)

    def terminate(self):
        pass


def create_cutter_plugin():
    try:
        return angrCutterPlugin()
    except Exception as e:
        printMessage(traceback.format_exc(), LogLevel.ERROR)
