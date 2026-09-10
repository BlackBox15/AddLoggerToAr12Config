# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'WindowDesign3.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QSizePolicy,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(674, 439)
        MainWindow.setAcceptDrops(True)
        self.lblStatusText = QLabel(MainWindow)
        self.lblStatusText.setObjectName(u"lblStatusText")
        self.lblStatusText.setGeometry(QRect(40, 350, 471, 71))
        font = QFont()
        font.setItalic(True)
        self.lblStatusText.setFont(font)
        self.lblStatusText.setWordWrap(True)
        self.lblStartRegister = QLabel(MainWindow)
        self.lblStartRegister.setObjectName(u"lblStartRegister")
        self.lblStartRegister.setGeometry(QRect(20, 110, 106, 16))
        self.linePortValue = QLineEdit(MainWindow)
        self.linePortValue.setObjectName(u"linePortValue")
        self.linePortValue.setGeometry(QRect(280, 80, 171, 26))
        self.linePortValue.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.linePortValue.setInputMethodHints(Qt.InputMethodHint.ImhDigitsOnly)
        self.lblBufferLength = QLabel(MainWindow)
        self.lblBufferLength.setObjectName(u"lblBufferLength")
        self.lblBufferLength.setGeometry(QRect(20, 140, 84, 16))
        self.lineMessageQty = QLineEdit(MainWindow)
        self.lineMessageQty.setObjectName(u"lineMessageQty")
        self.lineMessageQty.setGeometry(QRect(280, 170, 171, 26))
        self.lineMessageQty.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineMessageQty.setInputMethodHints(Qt.InputMethodHint.ImhDigitsOnly)
        self.lblMessagesQuantity = QLabel(MainWindow)
        self.lblMessagesQuantity.setObjectName(u"lblMessagesQuantity")
        self.lblMessagesQuantity.setGeometry(QRect(20, 170, 136, 16))
        self.lineBufferLength = QLineEdit(MainWindow)
        self.lineBufferLength.setObjectName(u"lineBufferLength")
        self.lineBufferLength.setGeometry(QRect(280, 140, 171, 26))
        self.lineBufferLength.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineBufferLength.setInputMethodHints(Qt.InputMethodHint.ImhDigitsOnly)
        self.lblPortValue = QLabel(MainWindow)
        self.lblPortValue.setObjectName(u"lblPortValue")
        self.lblPortValue.setGeometry(QRect(20, 80, 74, 16))
        self.lineStartRegister = QLineEdit(MainWindow)
        self.lineStartRegister.setObjectName(u"lineStartRegister")
        self.lineStartRegister.setGeometry(QRect(280, 110, 171, 26))
        self.lineStartRegister.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineStartRegister.setInputMethodHints(Qt.InputMethodHint.ImhDigitsOnly)
        self.lblPlcIpAddress = QLabel(MainWindow)
        self.lblPlcIpAddress.setObjectName(u"lblPlcIpAddress")
        self.lblPlcIpAddress.setGeometry(QRect(20, 50, 74, 16))
        self.linePlcIpAddress = QLineEdit(MainWindow)
        self.linePlcIpAddress.setObjectName(u"linePlcIpAddress")
        self.linePlcIpAddress.setGeometry(QRect(280, 50, 171, 26))
        self.linePlcIpAddress.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.linePlcIpAddress.setInputMethodHints(Qt.InputMethodHint.ImhDigitsOnly)
        self.lblStatusText.raise_()
        self.lblBufferLength.raise_()
        self.lblStartRegister.raise_()
        self.lineMessageQty.raise_()
        self.linePortValue.raise_()
        self.lblMessagesQuantity.raise_()
        self.lineBufferLength.raise_()
        self.lblPortValue.raise_()
        self.lineStartRegister.raise_()
        self.lblPlcIpAddress.raise_()
        self.linePlcIpAddress.raise_()
        QWidget.setTabOrder(self.lineStartRegister, self.lineBufferLength)
        QWidget.setTabOrder(self.lineBufferLength, self.lineMessageQty)
        QWidget.setTabOrder(self.lineMessageQty, self.linePlcIpAddress)
        QWidget.setTabOrder(self.linePlcIpAddress, self.linePortValue)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u041b\u043e\u0433\u0433\u0435\u0440\u0430", None))
        self.lblStatusText.setText(QCoreApplication.translate("MainWindow", u"-> \u041f\u0435\u0440\u0435\u0442\u0430\u0449\u0438\u0442\u0435 \u0441\u044e\u0434\u0430 configuration.json", None))
        self.lblStartRegister.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0430\u0440\u0442\u043e\u0432\u044b\u0439 \u0440\u0435\u0433\u0438\u0441\u0442\u0440", None))
        self.lblBufferLength.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0430\u0437\u043c\u0435\u0440 \u0431\u0443\u0444\u0435\u0440\u0430", None))
        self.lblMessagesQuantity.setText(QCoreApplication.translate("MainWindow", u"\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e  \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0439", None))
        self.lblPortValue.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0440\u0442 \u043b\u043e\u0433\u0433\u0435\u0440\u0430", None))
        self.lblPlcIpAddress.setText(QCoreApplication.translate("MainWindow", u"IP \u041f\u041b\u041a", None))
    # retranslateUi

