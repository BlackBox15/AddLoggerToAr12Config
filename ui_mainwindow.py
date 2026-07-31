# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'WindowDesign.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(468, 247)
        self.linePlcName = QLineEdit(Dialog)
        self.linePlcName.setObjectName(u"linePlcName")
        self.linePlcName.setGeometry(QRect(260, 20, 171, 26))
        self.lblMessageQty = QLabel(Dialog)
        self.lblMessageQty.setObjectName(u"lblMessageQty")
        self.lblMessageQty.setGeometry(QRect(10, 60, 191, 16))
        self.lblPlcName = QLabel(Dialog)
        self.lblPlcName.setObjectName(u"lblPlcName")
        self.lblPlcName.setGeometry(QRect(10, 30, 191, 16))
        self.lblStartRegister = QLabel(Dialog)
        self.lblStartRegister.setObjectName(u"lblStartRegister")
        self.lblStartRegister.setGeometry(QRect(10, 90, 241, 16))
        self.lineMessageQty = QLineEdit(Dialog)
        self.lineMessageQty.setObjectName(u"lineMessageQty")
        self.lineMessageQty.setGeometry(QRect(260, 50, 171, 26))
        self.lineMessageQty.setInputMethodHints(Qt.InputMethodHint.ImhDigitsOnly)
        self.lineStartRegiter = QLineEdit(Dialog)
        self.lineStartRegiter.setObjectName(u"lineStartRegiter")
        self.lineStartRegiter.setGeometry(QRect(260, 80, 171, 26))
        self.lineStartRegiter.setInputMethodHints(Qt.InputMethodHint.ImhDigitsOnly)
        self.btnOk = QPushButton(Dialog)
        self.btnOk.setObjectName(u"btnOk")
        self.btnOk.setGeometry(QRect(350, 160, 81, 26))
        self.lblStatusText = QLabel(Dialog)
        self.lblStatusText.setObjectName(u"lblStatusText")
        self.lblStatusText.setGeometry(QRect(20, 140, 281, 71))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.lblMessageQty.setText(QCoreApplication.translate("Dialog", u"\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0439 \u043b\u043e\u0433\u0433\u0435\u0440\u0430", None))
        self.lblPlcName.setText(QCoreApplication.translate("Dialog", u"\u0418\u043c\u044f \u041f\u041b\u041a \u0432 configuration", None))
        self.lblStartRegister.setText(QCoreApplication.translate("Dialog", u"\u0421\u0442\u0430\u0440\u0442\u043e\u0432\u044b\u0439 \u0440\u0435\u0433\u0438\u0441\u0442\u0440 \u0441\u0442\u0440\u0443\u043a\u0440\u0443\u0442\u044b \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0439", None))
        self.btnOk.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.lblStatusText.setText(QCoreApplication.translate("Dialog", u"\u041f\u0435\u0440\u0435\u0442\u0430\u0449\u0438\u0442\u044c configuration.json", None))
    # retranslateUi

