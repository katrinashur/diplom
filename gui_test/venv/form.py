# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(424, 307)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.experimentPath = QtWidgets.QLineEdit(self.centralwidget)
        self.experimentPath.setObjectName("experimentPath")
        self.horizontalLayout_2.addWidget(self.experimentPath)
        self.openDirectory = QtWidgets.QPushButton(self.centralwidget)
        self.openDirectory.setObjectName("openDirectory")
        self.horizontalLayout_2.addWidget(self.openDirectory)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.start = QtWidgets.QPushButton(self.centralwidget)
        self.start.setObjectName("start")
        self.horizontalLayout.addWidget(self.start)
        self.stop = QtWidgets.QPushButton(self.centralwidget)
        self.stop.setObjectName("stop")
        self.horizontalLayout.addWidget(self.stop)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 1)
        self.experimenName = QtWidgets.QLineEdit(self.centralwidget)
        self.experimenName.setObjectName("experimenName")
        self.gridLayout.addWidget(self.experimenName, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.test_button = QtWidgets.QPushButton(self.centralwidget)
        self.test_button.setObjectName("test_button")
        self.verticalLayout.addWidget(self.test_button)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 424, 26))
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
        self.label_2.setText(_translate("MainWindow", "Выберите папку для сохранения результатов эксперимента"))
        self.openDirectory.setText(_translate("MainWindow", "Открыть"))
        self.start.setText(_translate("MainWindow", "Начать эксперимент"))
        self.stop.setText(_translate("MainWindow", "Закончить эксперимент"))
        self.label.setText(_translate("MainWindow", "Введите название эксперимента"))
        self.test_button.setText(_translate("MainWindow", "Обработать картинку"))
