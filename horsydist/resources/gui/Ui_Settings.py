from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Settings(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(160, 100)
        MainWindow.setMinimumSize(QtCore.QSize(160, 100))
        MainWindow.setMaximumSize(QtCore.QSize(160, 100))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 160, 80))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.updateButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.updateButton.setObjectName("updateButton")
        self.verticalLayout.addWidget(self.updateButton)

        self.appBuildButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.appBuildButton.setObjectName("appBuildButton")
        self.verticalLayout.addWidget(self.appBuildButton)

        self.RPCButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.RPCButton.setObjectName("RPCButton")
        self.verticalLayout.addWidget(self.RPCButton)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 160, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Settings"))
        self.updateButton.setText(_translate("MainWindow", "Upgrade player"))
        self.appBuildButton.setText(_translate("MainWindow", "Choose main build"))
        self.RPCButton.setText(_translate("MainWindow", "Discord RPC settings"))
