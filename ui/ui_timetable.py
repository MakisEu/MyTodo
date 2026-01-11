# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'timetable.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QSizePolicy, QTableView,
    QVBoxLayout, QWidget)

class Ui_TimeTable(object):
    def setupUi(self, TimeTable):
        if not TimeTable.objectName():
            TimeTable.setObjectName(u"TimeTable")
        TimeTable.resize(961, 770)
        self.verticalLayoutWidget = QWidget(TimeTable)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 751, 751))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.Table = QTableView(self.verticalLayoutWidget)
        self.Table.setObjectName(u"Table")

        self.verticalLayout.addWidget(self.Table)


        self.retranslateUi(TimeTable)

        QMetaObject.connectSlotsByName(TimeTable)
    # setupUi

    def retranslateUi(self, TimeTable):
        TimeTable.setWindowTitle(QCoreApplication.translate("TimeTable", u"Form", None))
    # retranslateUi

