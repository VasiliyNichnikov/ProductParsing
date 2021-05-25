# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_interface.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 450)
        MainWindow.setMinimumSize(QtCore.QSize(400, 450))
        MainWindow.setMaximumSize(QtCore.QSize(400, 450))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.NameProgram = QtWidgets.QLabel(self.centralwidget)
        self.NameProgram.setGeometry(QtCore.QRect(0, 0, 400, 45))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.NameProgram.setFont(font)
        self.NameProgram.setAlignment(QtCore.Qt.AlignCenter)
        self.NameProgram.setObjectName("NameProgram")
        self.PushButton = QtWidgets.QPushButton(self.centralwidget)
        self.PushButton.setGeometry(QtCore.QRect(10, 380, 380, 20))
        self.PushButton.setObjectName("PushButton")
        self.ListWidget = QtWidgets.QListWidget(self.centralwidget)
        self.ListWidget.setGeometry(QtCore.QRect(10, 50, 380, 315))
        self.ListWidget.setObjectName("ListWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.NameProgram.setText(_translate("MainWindow", "ПАРСЕР САЙТОВ"))
        self.PushButton.setText(_translate("MainWindow", "ЗАПУСК ПАРСЕРА"))
