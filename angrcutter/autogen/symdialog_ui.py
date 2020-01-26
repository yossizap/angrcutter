# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'symdialog.ui'
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

class Ui_SymAddrDialog(object):
    def setupUi(self, SymAddrDialog):
        if SymAddrDialog.objectName():
            SymAddrDialog.setObjectName(u"SymAddrDialog")
        SymAddrDialog.setWindowModality(Qt.NonModal)
        SymAddrDialog.resize(320, 370)
        SymAddrDialog.setWindowTitle(u"Symbolic address configuration")
        self.gridLayoutWidget = QWidget(SymAddrDialog)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 301, 311))
        self.verticalLayout_2 = QVBoxLayout(self.gridLayoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.sizeText = QLabel(self.gridLayoutWidget)
        self.sizeText.setObjectName(u"sizeText")

        self.verticalLayout_2.addWidget(self.sizeText)

        self.sizeEdit = QLineEdit(self.gridLayoutWidget)
        self.sizeEdit.setObjectName(u"sizeEdit")
        self.sizeEdit.setMaximumSize(QSize(382, 16777215))
        self.sizeEdit.setInputMask(u"")
        self.sizeEdit.setText(u"")
        self.sizeEdit.setFrame(False)
        self.sizeEdit.setPlaceholderText(u"")

        self.verticalLayout_2.addWidget(self.sizeEdit)

        self.condLabel = QLabel(self.gridLayoutWidget)
        self.condLabel.setObjectName(u"condLabel")

        self.verticalLayout_2.addWidget(self.condLabel)

        self.textEdit = QTextEdit(self.gridLayoutWidget)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout_2.addWidget(self.textEdit)

        self.verticalLayoutWidget = QWidget(SymAddrDialog)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 330, 301, 35))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonBox = QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(SymAddrDialog)
        self.buttonBox.accepted.connect(SymAddrDialog.accept)
        self.buttonBox.rejected.connect(SymAddrDialog.reject)

        QMetaObject.connectSlotsByName(SymAddrDialog)
    # setupUi

    def retranslateUi(self, SymAddrDialog):
        self.sizeText.setText(QCoreApplication.translate("SymAddrDialog", u"Size(bytes):", None))
        self.condLabel.setText(QCoreApplication.translate("SymAddrDialog", u"Condition:", None))
    # retranslateUi

