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
        MainWindow.resize(500, 200)
        MainWindow.setAcceptDrops(True)
        self.lblStatusText = QLabel(MainWindow)
        self.lblStatusText.setObjectName(u"lblStatusText")
        self.lblStatusText.setGeometry(QRect(10, 120, 471, 71))
        self.lblStatusText.setWordWrap(True)
        self.lblStartRegister = QLabel(MainWindow)
        self.lblStartRegister.setObjectName(u"lblStartRegister")
        self.lblStartRegister.setGeometry(QRect(30, 90, 241, 16))
        self.lineStartRegiter = QLineEdit(MainWindow)
        self.lineStartRegiter.setObjectName(u"lineStartRegiter")
        self.lineStartRegiter.setGeometry(QRect(280, 80, 171, 26))
        self.lineStartRegiter.setInputMethodHints(Qt.InputMethodHint.ImhDigitsOnly)
        self.lblMessageQty = QLabel(MainWindow)
        self.lblMessageQty.setObjectName(u"lblMessageQty")
        self.lblMessageQty.setGeometry(QRect(30, 50, 201, 16))
        self.lineMessageQty = QLineEdit(MainWindow)
        self.lineMessageQty.setObjectName(u"lineMessageQty")
        self.lineMessageQty.setGeometry(QRect(280, 40, 171, 26))
        self.lineMessageQty.setInputMethodHints(Qt.InputMethodHint.ImhDigitsOnly)
        self.lblStatusText.raise_()
        self.lblMessageQty.raise_()
        self.lblStartRegister.raise_()
        self.lineMessageQty.raise_()
        self.lineStartRegiter.raise_()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u041b\u043e\u0433\u0433\u0435\u0440\u0430", None))
        self.lblStatusText.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0435\u0440\u0435\u0442\u0430\u0449\u0438\u0442\u0435 \u0441\u044e\u0434\u0430 configuration.json", None))
        self.lblStartRegister.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0430\u0440\u0442\u043e\u0432\u044b\u0439 \u0440\u0435\u0433\u0438\u0441\u0442\u0440 \u0441\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u044b \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0439", None))
        self.lblMessageQty.setText(QCoreApplication.translate("MainWindow", u"\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0439 \u0432 \u043b\u043e\u0433\u0433\u0435\u0440\u0435", None))
    # retranslateUi

