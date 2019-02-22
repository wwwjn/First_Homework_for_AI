# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtGui import QIcon

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        self.setWindowIcon(QIcon(":/carroticon.ico"))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(620, 110, 130, 50))
        self.pushButton.setDefault(False)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(750, 330, 251, 201))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/1.png"))
        self.label.setObjectName("label")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(820, 110, 130, 50))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(580, 180, 501, 421))
        self.label_2.setMinimumSize(QtCore.QSize(501, 421))
        self.label_2.setLineWidth(10)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/hungry.png"))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setIndent(8)
        self.label_2.setOpenExternalLinks(False)
        self.label_2.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(-10, -40, 1321, 661))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(":/background.png"))
        self.label_3.setObjectName("label_3")
        self.label_3.raise_()
        self.pushButton.raise_()
        self.label.raise_()

        self.pushButton_2.raise_()
        self.label_2.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        #self.pushButton.clicked.connect(MainWindow.hide)
        self.pushButton_2.clicked.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Find Carrot!"))
        self.pushButton.setText(_translate("MainWindow", "Start Game"))

        self.pushButton_2.setText(_translate("MainWindow", "Exit"))
import resource


if __name__=="__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget=QtWidgets.QMainWindow()
    First= Ui_MainWindow()
    First.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())