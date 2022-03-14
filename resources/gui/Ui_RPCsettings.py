from PyQt5 import QtCore, QtWidgets
from resources.lib.config import config


class Ui_RPCsettings(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(160, 100)
        MainWindow.setMinimumSize(QtCore.QSize(160, 100))
        MainWindow.setMaximumSize(QtCore.QSize(160, 100))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 0, 151, 80))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ShowRPCcheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.ShowRPCcheckBox.setObjectName("ShowRPCcheckBox")
        self.verticalLayout.addWidget(self.ShowRPCcheckBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 160, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.ShowRPCcheckBox.setChecked(config['showrpc'])

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RPC settings"))
        self.ShowRPCcheckBox.setText(_translate("MainWindow", "Show RPC"))