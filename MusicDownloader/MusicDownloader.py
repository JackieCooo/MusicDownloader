# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MusicDownloader.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(931, 636)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 931, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(6)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionSearch = QtWidgets.QAction(MainWindow)
        self.actionSearch.setEnabled(False)
        self.actionSearch.setObjectName("actionSearch")
        self.actionOption = QtWidgets.QAction(MainWindow)
        self.actionOption.setEnabled(False)
        self.actionOption.setObjectName("actionOption")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.toolBar.addAction(self.actionSearch)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionOption)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionQuit)
        self.retranslateUi(MainWindow)
        self.toolBar.actionTriggered['QAction*'].connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        QtWidgets.QMainWindow.show(MainWindow)
        sys.exit(app.exec_())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "搜索"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionSearch.setText(_translate("MainWindow", "搜索"))
        self.actionSearch.setToolTip(_translate("MainWindow", "搜索"))
        self.actionOption.setText(_translate("MainWindow", "设置"))
        self.actionOption.setToolTip(_translate("MainWindow", "设置"))
        self.actionQuit.setText(_translate("MainWindow", "退出"))
        self.actionQuit.setToolTip(_translate("MainWindow", "退出"))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    run = Ui_MainWindow()
    run.setupUi(QtWidgets.QMainWindow())

