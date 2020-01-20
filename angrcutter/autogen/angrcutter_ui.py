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
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, -1)
        self.regTableBox = QVBoxLayout()
        self.regTableBox.setObjectName(u"regTableBox")

        self.horizontalLayout.addLayout(self.regTableBox)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout.setHorizontalSpacing(8)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setContentsMargins(-1, -1, 0, -1)
        self.findLabel = QLabel(self.dockWidgetContents)
        self.findLabel.setObjectName(u"findLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.findLabel.sizePolicy().hasHeightForWidth())
        self.findLabel.setSizePolicy(sizePolicy)
        self.findLabel.setMidLineWidth(4)

        self.gridLayout.addWidget(self.findLabel, 0, 0, 1, 1)

        self.findLine = QLineEdit(self.dockWidgetContents)
        self.findLine.setObjectName(u"findLine")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.findLine.sizePolicy().hasHeightForWidth())
        self.findLine.setSizePolicy(sizePolicy1)
        self.findLine.setFrame(True)
        self.findLine.setAlignment(Qt.AlignJustify|Qt.AlignVCenter)
        self.findLine.setReadOnly(True)

        self.gridLayout.addWidget(self.findLine, 0, 1, 1, 1)

        self.avoidLabel = QLabel(self.dockWidgetContents)
        self.avoidLabel.setObjectName(u"avoidLabel")
        sizePolicy.setHeightForWidth(self.avoidLabel.sizePolicy().hasHeightForWidth())
        self.avoidLabel.setSizePolicy(sizePolicy)
        self.avoidLabel.setMidLineWidth(4)

        self.gridLayout.addWidget(self.avoidLabel, 1, 0, 1, 1)

        self.avoidLine = QLineEdit(self.dockWidgetContents)
        self.avoidLine.setObjectName(u"avoidLine")
        sizePolicy1.setHeightForWidth(self.avoidLine.sizePolicy().hasHeightForWidth())
        self.avoidLine.setSizePolicy(sizePolicy1)
        self.avoidLine.setFrame(True)
        self.avoidLine.setAlignment(Qt.AlignJustify|Qt.AlignVCenter)
        self.avoidLine.setReadOnly(True)

        self.gridLayout.addWidget(self.avoidLine, 1, 1, 1, 1)

        self.startButton = QPushButton(self.dockWidgetContents)
        self.startButton.setObjectName(u"startButton")

        self.gridLayout.addWidget(self.startButton, 2, 0, 1, 1)

        self.stopButton = QPushButton(self.dockWidgetContents)
        self.stopButton.setObjectName(u"stopButton")

        self.gridLayout.addWidget(self.stopButton, 3, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 400, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 4, 0, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout)


        self.verticalLayout.addLayout(self.horizontalLayout)

        AngrWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(AngrWidget)

        QMetaObject.connectSlotsByName(AngrWidget)
    # setupUi

    def retranslateUi(self, AngrWidget):
        self.findLabel.setText(QCoreApplication.translate("AngrWidget", u"Find address:", None))
        self.avoidLabel.setText(QCoreApplication.translate("AngrWidget", u"Avoid address:", None))
        self.startButton.setText(QCoreApplication.translate("AngrWidget", u"Start", None))
        self.stopButton.setText(QCoreApplication.translate("AngrWidget", u"Stop", None))
    # retranslateUi

