# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'http_client.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QTextBrowser, QVBoxLayout, QWidget)

class Ui_http_client(object):
    def setupUi(self, http_client):
        if not http_client.objectName():
            http_client.setObjectName(u"http_client")
        http_client.resize(565, 530)
        self.layoutWidget = QWidget(http_client)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 0, 535, 510))
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.comboBox = QComboBox(self.layoutWidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout.addWidget(self.comboBox)

        self.lineEdit = QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.layoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.line_3 = QFrame(self.layoutWidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.label)

        self.pushButton_2 = QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton_3 = QPushButton(self.layoutWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy1.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.pushButton_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.headersTable = QTableWidget(self.layoutWidget)
        if (self.headersTable.columnCount() < 2):
            self.headersTable.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.headersTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.headersTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.headersTable.setObjectName(u"headersTable")

        self.verticalLayout_2.addWidget(self.headersTable)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.line = QFrame(self.layoutWidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_3.addWidget(self.line)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 4, -1, -1)
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(-1, 6, -1, -1)
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy2)

        self.horizontalLayout_9.addWidget(self.label_2)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.plainTextEdit = QPlainTextEdit(self.layoutWidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")

        self.verticalLayout.addWidget(self.plainTextEdit)


        self.horizontalLayout_3.addLayout(self.verticalLayout)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.line_2 = QFrame(self.layoutWidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_2)

        self.textBrowser = QTextBrowser(self.layoutWidget)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout_3.addWidget(self.textBrowser)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.buttonClearLog = QPushButton(self.layoutWidget)
        self.buttonClearLog.setObjectName(u"buttonClearLog")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.buttonClearLog.sizePolicy().hasHeightForWidth())
        self.buttonClearLog.setSizePolicy(sizePolicy3)

        self.horizontalLayout_8.addWidget(self.buttonClearLog)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)


        self.retranslateUi(http_client)

        QMetaObject.connectSlotsByName(http_client)
    # setupUi

    def retranslateUi(self, http_client):
        http_client.setWindowTitle(QCoreApplication.translate("http_client", u"HTTP \u63a5\u53e3\u6d4b\u8bd5", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("http_client", u"GET", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("http_client", u"POST", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("http_client", u"PUT", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("http_client", u"DELETE", None))

        self.lineEdit.setPlaceholderText(QCoreApplication.translate("http_client", u"\u8bf7\u8f93\u5165URL", None))
        self.pushButton.setText(QCoreApplication.translate("http_client", u"\u53d1\u9001", None))
        self.label.setText(QCoreApplication.translate("http_client", u"\u6d88\u606f\u5934", None))
        self.pushButton_2.setText(QCoreApplication.translate("http_client", u"+", None))
        self.pushButton_3.setText(QCoreApplication.translate("http_client", u"-", None))
        ___qtablewidgetitem = self.headersTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("http_client", u"\u540d\u79f0", None));
        ___qtablewidgetitem1 = self.headersTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("http_client", u"\u503c", None));
        self.label_2.setText(QCoreApplication.translate("http_client", u"\u6d88\u606f\u4f53", None))
        self.buttonClearLog.setText(QCoreApplication.translate("http_client", u"\u6e05\u9664", None))
    # retranslateUi

