# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'history.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QApplication, QLayout, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import rc_assets

class Ui_History(object):
    def setupUi(self, History):
        if not History.objectName():
            History.setObjectName(u"History")
        History.resize(474, 604)
        icon = QIcon()
        icon.addFile(u":/icons/assets/todo_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        History.setWindowIcon(icon)
        self.verticalLayoutWidget = QWidget(History)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(9, 9, 451, 581))
        self.vboxLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.vboxLayout.setObjectName(u"vboxLayout")
        self.vboxLayout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.vboxLayout.setContentsMargins(0, 0, 0, 0)
        self.listWidget = QListWidget(self.verticalLayoutWidget)
        self.listWidget.setObjectName(u"listWidget")

        self.vboxLayout.addWidget(self.listWidget)

        self.verticalSpacer = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.vboxLayout.addItem(self.verticalSpacer)

        self.pushButton = QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(120, 60))

        self.vboxLayout.addWidget(self.pushButton)


        self.retranslateUi(History)

        QMetaObject.connectSlotsByName(History)
    # setupUi

    def retranslateUi(self, History):
        History.setWindowTitle(QCoreApplication.translate("History", u"Form", None))
        self.pushButton.setText(QCoreApplication.translate("History", u"Clear Old History", None))
    # retranslateUi

