# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'listview.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView, QLayout,
    QPushButton, QSizePolicy, QSpacerItem, QTableView,
    QVBoxLayout, QWidget)

class Ui_ListView(object):
    def setupUi(self, ListView):
        if not ListView.objectName():
            ListView.setObjectName(u"ListView")
        ListView.resize(643, 417)
        self.list_widget = QWidget(ListView)
        self.list_widget.setObjectName(u"list_widget")
        self.list_widget.setGeometry(QRect(0, 0, 646, 418))
        self.gridLayout = QGridLayout(self.list_widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.add_button = QPushButton(self.list_widget)
        self.add_button.setObjectName(u"add_button")
        self.add_button.setMinimumSize(QSize(120, 60))

        self.verticalLayout_3.addWidget(self.add_button)

        self.edit_button = QPushButton(self.list_widget)
        self.edit_button.setObjectName(u"edit_button")
        self.edit_button.setMinimumSize(QSize(120, 60))

        self.verticalLayout_3.addWidget(self.edit_button)

        self.delete_button = QPushButton(self.list_widget)
        self.delete_button.setObjectName(u"delete_button")
        self.delete_button.setMinimumSize(QSize(120, 60))

        self.verticalLayout_3.addWidget(self.delete_button)

        self.mark_as_completed_button = QPushButton(self.list_widget)
        self.mark_as_completed_button.setObjectName(u"mark_as_completed_button")
        self.mark_as_completed_button.setMinimumSize(QSize(120, 70))

        self.verticalLayout_3.addWidget(self.mark_as_completed_button)

        self.start_daily_button = QPushButton(self.list_widget)
        self.start_daily_button.setObjectName(u"start_daily_button")
        self.start_daily_button.setMinimumSize(QSize(120, 70))

        self.verticalLayout_3.addWidget(self.start_daily_button)

        self.asr_to_todo_button = QPushButton(self.list_widget)
        self.asr_to_todo_button.setObjectName(u"asr_to_todo_button")
        self.asr_to_todo_button.setMinimumSize(QSize(120, 70))

        self.verticalLayout_3.addWidget(self.asr_to_todo_button)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.history_button = QPushButton(self.list_widget)
        self.history_button.setObjectName(u"history_button")
        self.history_button.setMinimumSize(QSize(120, 60))

        self.verticalLayout_3.addWidget(self.history_button)


        self.gridLayout.addLayout(self.verticalLayout_3, 0, 1, 1, 1)

        self.tableView = QTableView(self.list_widget)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setMinimumSize(QSize(500, 400))

        self.gridLayout.addWidget(self.tableView, 0, 0, 1, 1)


        self.retranslateUi(ListView)

        QMetaObject.connectSlotsByName(ListView)
    # setupUi

    def retranslateUi(self, ListView):
        ListView.setWindowTitle(QCoreApplication.translate("ListView", u"Form", None))
        self.add_button.setText(QCoreApplication.translate("ListView", u"Add Todo", None))
        self.edit_button.setText(QCoreApplication.translate("ListView", u"Edit Todo", None))
        self.delete_button.setText(QCoreApplication.translate("ListView", u"Delete Todo", None))
        self.mark_as_completed_button.setText(QCoreApplication.translate("ListView", u"Mark Todo\n"
"As Completed\n"
"\u2713", None))
        self.start_daily_button.setText(QCoreApplication.translate("ListView", u"Start Daily Todo", None))
        self.asr_to_todo_button.setText(QCoreApplication.translate("ListView", u"Speech-to-todo", None))
        self.history_button.setText(QCoreApplication.translate("ListView", u"History", None))
    # retranslateUi

