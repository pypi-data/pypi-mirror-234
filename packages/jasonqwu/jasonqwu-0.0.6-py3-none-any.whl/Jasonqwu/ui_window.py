# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'window.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPlainTextEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_window(object):
    def setupUi(self, window):
        if not window.objectName():
            window.setObjectName(u"window")
        window.resize(638, 486)
        self.widget = QWidget(window)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(9, 9, 258, 250))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.label)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.text_edit = QPlainTextEdit(self.widget)
        self.text_edit.setObjectName(u"text_edit")

        self.verticalLayout.addWidget(self.text_edit)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.button = QPushButton(self.widget)
        self.button.setObjectName(u"button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.button.sizePolicy().hasHeightForWidth())
        self.button.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.button)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(window)

        QMetaObject.connectSlotsByName(window)
    # setupUi

    def retranslateUi(self, window):
        window.setWindowTitle(QCoreApplication.translate("window", u"\u85aa\u8d44\u7edf\u8ba1", None))
        self.label.setText(QCoreApplication.translate("window", u"\u7edf\u8ba1\u6570\u636e", None))
        self.text_edit.setPlaceholderText(QCoreApplication.translate("window", u"\u8bf7\u8f93\u5165\u85aa\u8d44\u8868", None))
        self.button.setText(QCoreApplication.translate("window", u"\u7edf  \u8ba1", None))
    # retranslateUi

