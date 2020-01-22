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

        self.infoBox = QVBoxLayout()
        self.infoBox.setObjectName(u"infoBox")
        self.findLabel = QLabel(self.dockWidgetContents)
        self.findLabel.setObjectName(u"findLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.findLabel.sizePolicy().hasHeightForWidth())
        self.findLabel.setSizePolicy(sizePolicy)
        self.findLabel.setMidLineWidth(4)

        self.infoBox.addWidget(self.findLabel)

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

        self.infoBox.addWidget(self.findLine)

        self.avoidLabel = QLabel(self.dockWidgetContents)
        self.avoidLabel.setObjectName(u"avoidLabel")
        sizePolicy.setHeightForWidth(self.avoidLabel.sizePolicy().hasHeightForWidth())
        self.avoidLabel.setSizePolicy(sizePolicy)
        self.avoidLabel.setMidLineWidth(4)

        self.infoBox.addWidget(self.avoidLabel)

        self.avoidLine = QLineEdit(self.dockWidgetContents)
        self.avoidLine.setObjectName(u"avoidLine")
        sizePolicy1.setHeightForWidth(self.avoidLine.sizePolicy().hasHeightForWidth())
        self.avoidLine.setSizePolicy(sizePolicy1)
        self.avoidLine.setFrame(True)
        self.avoidLine.setAlignment(Qt.AlignJustify|Qt.AlignVCenter)
        self.avoidLine.setReadOnly(True)

        self.infoBox.addWidget(self.avoidLine)

        self.symLabel = QLabel(self.dockWidgetContents)
        self.symLabel.setObjectName(u"symLabel")
        sizePolicy.setHeightForWidth(self.symLabel.sizePolicy().hasHeightForWidth())
        self.symLabel.setSizePolicy(sizePolicy)
        self.symLabel.setMidLineWidth(4)

        self.infoBox.addWidget(self.symLabel)

        self.symLine = QLineEdit(self.dockWidgetContents)
        self.symLine.setObjectName(u"symLine")
        sizePolicy1.setHeightForWidth(self.symLine.sizePolicy().hasHeightForWidth())
        self.symLine.setSizePolicy(sizePolicy1)
        self.symLine.setFrame(True)
        self.symLine.setAlignment(Qt.AlignJustify|Qt.AlignVCenter)
        self.symLine.setReadOnly(True)

        self.infoBox.addWidget(self.symLine)

        self.memoryLabel = QLabel(self.dockWidgetContents)
        self.memoryLabel.setObjectName(u"memoryLabel")
        sizePolicy.setHeightForWidth(self.memoryLabel.sizePolicy().hasHeightForWidth())
        self.memoryLabel.setSizePolicy(sizePolicy)
        self.memoryLabel.setMidLineWidth(4)

        self.infoBox.addWidget(self.memoryLabel)

        self.memoryCombo = QComboBox(self.dockWidgetContents)
        self.memoryCombo.addItem("")
        self.memoryCombo.addItem("")
        self.memoryCombo.addItem("")
        self.memoryCombo.addItem("")
        self.memoryCombo.setObjectName(u"memoryCombo")

        self.infoBox.addWidget(self.memoryCombo)

        self.startButton = QPushButton(self.dockWidgetContents)
        self.startButton.setObjectName(u"startButton")

        self.infoBox.addWidget(self.startButton)

        self.stopButton = QPushButton(self.dockWidgetContents)
        self.stopButton.setObjectName(u"stopButton")

        self.infoBox.addWidget(self.stopButton)

        self.applySimButton = QPushButton(self.dockWidgetContents)
        self.applySimButton.setObjectName(u"applySimButton")

        self.infoBox.addWidget(self.applySimButton)

        self.verticalSpacer = QSpacerItem(20, 400, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.infoBox.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.infoBox)


        self.verticalLayout.addLayout(self.horizontalLayout)

        AngrWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(AngrWidget)

        QMetaObject.connectSlotsByName(AngrWidget)
    # setupUi

    def retranslateUi(self, AngrWidget):
        self.findLabel.setText(QCoreApplication.translate("AngrWidget", u"Find addresses:", None))
        self.avoidLabel.setText(QCoreApplication.translate("AngrWidget", u"Avoid addresses:", None))
        self.symLabel.setText(QCoreApplication.translate("AngrWidget", u"Symbolic addresses:", None))
        self.memoryLabel.setText(QCoreApplication.translate("AngrWidget", u"Memory type:", None))
#if QT_CONFIG(tooltip)
        self.memoryLabel.setToolTip(QCoreApplication.translate("AngrWidget", u"The memory type defines how angr gets the memory from the debug session and from the CLE backend", None))
#endif // QT_CONFIG(tooltip)
        self.memoryCombo.setItemText(0, QCoreApplication.translate("AngrWidget", u"CLE Simprocedures", None))
        self.memoryCombo.setItemText(1, QCoreApplication.translate("AngrWidget", u"CLE GOT", None))
        self.memoryCombo.setItemText(2, QCoreApplication.translate("AngrWidget", u"CLE Memory", None))
        self.memoryCombo.setItemText(3, QCoreApplication.translate("AngrWidget", u"Debugger Memory", None))

        self.startButton.setText(QCoreApplication.translate("AngrWidget", u"Start", None))
        self.stopButton.setText(QCoreApplication.translate("AngrWidget", u"Stop", None))
        self.applySimButton.setText(QCoreApplication.translate("AngrWidget", u"Apply simulation results", None))
    # retranslateUi

