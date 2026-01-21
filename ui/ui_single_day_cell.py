# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'single_day_cell.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QScrollArea, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_SingleDayCell(object):
    def setupUi(self, SingleDayCell):
        if not SingleDayCell.objectName():
            SingleDayCell.setObjectName(u"SingleDayCell")
        SingleDayCell.resize(394, 293)
        self.verticalLayoutWidget = QWidget(SingleDayCell)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 391, 291))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.day_label = QLabel(self.verticalLayoutWidget)
        self.day_label.setObjectName(u"day_label")
        self.day_label.setStyleSheet(u"border-bottom: 5px solid black;")

        self.verticalLayout.addWidget(self.day_label, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop)

        self.scrollArea = QScrollArea(self.verticalLayoutWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 387, 263))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(SingleDayCell)

        QMetaObject.connectSlotsByName(SingleDayCell)
    # setupUi

    def retranslateUi(self, SingleDayCell):
        SingleDayCell.setWindowTitle(QCoreApplication.translate("SingleDayCell", u"Form", None))
        self.day_label.setText(QCoreApplication.translate("SingleDayCell", u"TextLabel", None))
    # retranslateUi

