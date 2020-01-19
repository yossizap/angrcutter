# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'angrcutter.ui'
##
## Created by: Qt User Interface Compiler version 5.14.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

class Ui_AngrWidget(object):
    def setupUi(self, AngrWidget):
        if AngrWidget.objectName():
            AngrWidget.setObjectName(u"AngrWidget")
        AngrWidget.resize(899, 542)
        AngrWidget.setWindowTitle(u"Angr Configuration")
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout2 = QHBoxLayout()
        self.horizontalLayout2.setObjectName(u"horizontalLayout2")
        self.startButton = QPushButton(self.dockWidgetContents)
        self.startButton.setObjectName(u"startButton")

        self.horizontalLayout2.addWidget(self.startButton)

        self.stopButton = QPushButton(self.dockWidgetContents)
        self.stopButton.setObjectName(u"stopButton")

        self.horizontalLayout2.addWidget(self.stopButton)


        self.verticalLayout.addLayout(self.horizontalLayout2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, -1)

        self.verticalLayout.addLayout(self.horizontalLayout)

        AngrWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(AngrWidget)

        QMetaObject.connectSlotsByName(AngrWidget)
    # setupUi

    def retranslateUi(self, AngrWidget):
        self.startButton.setText(QCoreApplication.translate("AngrWidget", u"Start", None))
        self.stopButton.setText(QCoreApplication.translate("AngrWidget", u"Stop", None))
    # retranslateUi

