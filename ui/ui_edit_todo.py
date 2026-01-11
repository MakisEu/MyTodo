# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edit_todo.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDateTimeEdit, QFormLayout,
    QLabel, QPlainTextEdit, QPushButton, QSizePolicy,
    QWidget)
import rc_assets

class Ui_Edit_Todo(object):
    def setupUi(self, Edit_Todo):
        if not Edit_Todo.objectName():
            Edit_Todo.setObjectName(u"Edit_Todo")
        Edit_Todo.resize(388, 571)
        icon = QIcon()
        icon.addFile(u":/icons/assets/todo_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Edit_Todo.setWindowIcon(icon)
        self.formLayoutWidget = QWidget(Edit_Todo)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 10, 368, 541))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.plainTextEdit_2 = QPlainTextEdit(self.formLayoutWidget)
        self.plainTextEdit_2.setObjectName(u"plainTextEdit_2")
        self.plainTextEdit_2.setMinimumSize(QSize(200, 35))
        self.plainTextEdit_2.setMaximumSize(QSize(200, 30))

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.plainTextEdit_2)

        self.label_5 = QLabel(self.formLayoutWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(120, 60))
        font = QFont()
        font.setPointSize(18)
        self.label_5.setFont(font)
        self.label_5.setMargin(4)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_5)

        self.dateTimeEdit_3 = QDateTimeEdit(self.formLayoutWidget)
        self.dateTimeEdit_3.setObjectName(u"dateTimeEdit_3")
        self.dateTimeEdit_3.setMinimumSize(QSize(120, 35))

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.dateTimeEdit_3)

        self.label_6 = QLabel(self.formLayoutWidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(120, 60))
        self.label_6.setFont(font)
        self.label_6.setMargin(4)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_6)

        self.dateTimeEdit_4 = QDateTimeEdit(self.formLayoutWidget)
        self.dateTimeEdit_4.setObjectName(u"dateTimeEdit_4")
        self.dateTimeEdit_4.setMinimumSize(QSize(120, 35))

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.dateTimeEdit_4)

        self.pushButton_3 = QPushButton(self.formLayoutWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(160, 80))

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.pushButton_3)

        self.pushButton_4 = QPushButton(self.formLayoutWidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setMinimumSize(QSize(160, 80))

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.pushButton_4)

        self.label_4 = QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(120, 60))
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.label_4.setMargin(4)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.comboBoxTags = QComboBox(self.formLayoutWidget)
        self.comboBoxTags.addItem("")
        self.comboBoxTags.addItem("")
        self.comboBoxTags.addItem("")
        self.comboBoxTags.addItem("")
        self.comboBoxTags.addItem("")
        self.comboBoxTags.addItem("")
        self.comboBoxTags.setObjectName(u"comboBoxTags")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.comboBoxTags)

        self.label_7 = QLabel(self.formLayoutWidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(120, 60))
        self.label_7.setFont(font)
        self.label_7.setMargin(4)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_7)


        self.retranslateUi(Edit_Todo)

        QMetaObject.connectSlotsByName(Edit_Todo)
    # setupUi

    def retranslateUi(self, Edit_Todo):
        Edit_Todo.setWindowTitle(QCoreApplication.translate("Edit_Todo", u"Form", None))
        self.label_5.setText(QCoreApplication.translate("Edit_Todo", u"Start date:", None))
        self.dateTimeEdit_3.setDisplayFormat(QCoreApplication.translate("Edit_Todo", u"dd/MM/yyyy hh:mm", None))
        self.label_6.setText(QCoreApplication.translate("Edit_Todo", u"End date:", None))
        self.dateTimeEdit_4.setDisplayFormat(QCoreApplication.translate("Edit_Todo", u"dd/MM/yyyy hh:mm", None))
        self.pushButton_3.setText(QCoreApplication.translate("Edit_Todo", u"Cancel", None))
        self.pushButton_4.setText(QCoreApplication.translate("Edit_Todo", u"Edit Todo", None))
        self.label_4.setText(QCoreApplication.translate("Edit_Todo", u" Name:", None))
        self.comboBoxTags.setItemText(0, QCoreApplication.translate("Edit_Todo", u"None", None))
        self.comboBoxTags.setItemText(1, QCoreApplication.translate("Edit_Todo", u"Productivity", None))
        self.comboBoxTags.setItemText(2, QCoreApplication.translate("Edit_Todo", u"Education", None))
        self.comboBoxTags.setItemText(3, QCoreApplication.translate("Edit_Todo", u"Work", None))
        self.comboBoxTags.setItemText(4, QCoreApplication.translate("Edit_Todo", u"Entertainment", None))
        self.comboBoxTags.setItemText(5, QCoreApplication.translate("Edit_Todo", u"Chore", None))

        self.label_7.setText(QCoreApplication.translate("Edit_Todo", u"Tag:", None))
    # retranslateUi

