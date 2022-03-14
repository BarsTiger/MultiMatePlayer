from PyQt5 import QtCore, QtWidgets


class Ui_ExtendedMenu(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(151, 74)
        MainWindow.setMinimumSize(QtCore.QSize(151, 74))
        MainWindow.setMaximumSize(QtCore.QSize(151, 74))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.prosearchButton = QtWidgets.QPushButton(self.centralwidget)
        self.prosearchButton.setGeometry(QtCore.QRect(0, 0, 150, 50))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.prosearchButton.sizePolicy().hasHeightForWidth())
        self.prosearchButton.setSizePolicy(sizePolicy)
        self.prosearchButton.setMaximumSize(QtCore.QSize(150, 50))
        self.prosearchButton.setObjectName("prosearchButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 151, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Extended functions"))
        self.prosearchButton.setText(_translate("MainWindow", "Pro search"))