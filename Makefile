all:
	pyside2-uic ui/angrcutter.ui > angrcutter/autogen/angrcutter_ui.py
	pyside2-uic ui/symdialog.ui > angrcutter/autogen/symdialog_ui.py
