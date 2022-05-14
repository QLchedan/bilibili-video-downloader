# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'video_download.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(121, 61, 51, 17))
        font = QFont()
        font.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        self.label.setFont(font)
        self.quality = QComboBox(Dialog)
        self.quality.setObjectName(u"quality")
        self.quality.setGeometry(QRect(178, 61, 121, 20))
        self.download = QPushButton(Dialog)
        self.download.setObjectName(u"download")
        self.download.setGeometry(QRect(280, 240, 75, 23))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u9009\u62e9\u753b\u8d28:", None))
        self.download.setText(QCoreApplication.translate("Dialog", u"\u4e0b\u8f7d!", None))
    # retranslateUi

