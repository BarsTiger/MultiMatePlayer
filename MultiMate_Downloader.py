import sys, subprocess, os
import urllib.request
import zipfile
import time
try:
    from PyQt5 import QtCore, QtGui, QtWidgets
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'PyQt5'])
    from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(170, 115)
        MainWindow.setMinimumSize(QtCore.QSize(170, 115))
        MainWindow.setMaximumSize(QtCore.QSize(170, 115))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.downloaderLabel = QtWidgets.QTextBrowser(self.centralwidget)
        self.downloaderLabel.setGeometry(QtCore.QRect(0, 0, 170, 30))
        self.downloaderLabel.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.downloaderLabel.setObjectName("downloaderLabel")
        self.pyVerSownload = QtWidgets.QPushButton(self.centralwidget)
        self.pyVerSownload.setGeometry(QtCore.QRect(0, 29, 170, 23))
        self.pyVerSownload.setObjectName("pyVerSownload")
        self.pywVerSownload = QtWidgets.QPushButton(self.centralwidget)
        self.pywVerSownload.setGeometry(QtCore.QRect(0, 50, 170, 23))
        self.pywVerSownload.setObjectName("pywVerSownload")
        self.exeVerSownload = QtWidgets.QPushButton(self.centralwidget)
        self.exeVerSownload.setGeometry(QtCore.QRect(0, 70, 170, 23))
        self.exeVerSownload.setObjectName("exeVerSownload")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 170, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Downloader"))
        self.downloaderLabel.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">MultiMate Downloader</span></p></body></html>"))
        self.pyVerSownload.setText(_translate("MainWindow", ".py version (console logs)"))
        self.pywVerSownload.setText(_translate("MainWindow", ".pyw version"))
        self.exeVerSownload.setText(_translate("MainWindow", ".exe version (no Python needed)"))

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

if not os.path.exists('resources'):
    os.mkdir('resources')

if not os.path.isfile("play.list"):
    playlistwrite = open("play.list", 'w+')
    playlistwrite.write("{}")
    playlistwrite.close()

def dlExe():
    urllib.request.urlretrieve("https://github.com/BarsTiger/MultiMatePlayer/raw/master/resources/resources.zip", 'resources/resources.zip')
    with zipfile.ZipFile('resources/resources.zip', 'r') as archfile:
        archfile.extractall("resources")
    os.remove('resources/resources.zip')

    urllib.request.urlretrieve("https://github.com/BarsTiger/MultiMatePlayer/raw/master/MultiMate_Player.exe", "MultiMate_Player.exe")
    subprocess.Popen('MultiMate_Player.exe')

    time.sleep(0.5)
    exit()

def dlPy():
    urllib.request.urlretrieve("https://github.com/BarsTiger/MultiMatePlayer/raw/master/resources/resources.zip", 'resources/resources.zip')
    with zipfile.ZipFile('resources/resources.zip', 'r') as archfile:
        archfile.extractall("resources")
    os.remove('resources/resources.zip')

    urllib.request.urlretrieve("https://raw.githubusercontent.com/BarsTiger/MultiMatePlayer/master/MultiMate_Player.py", "MultiMate_Player.py")
    subprocess.Popen(sys.executable + ' MultiMate_Player.py')

    time.sleep(0.5)
    exit()

def dlPyw():
    urllib.request.urlretrieve("https://github.com/BarsTiger/MultiMatePlayer/raw/master/resources/resources.zip", 'resources/resources.zip')
    with zipfile.ZipFile('resources/resources.zip', 'r') as archfile:
        archfile.extractall("resources")
    os.remove('resources/resources.zip')

    urllib.request.urlretrieve("https://raw.githubusercontent.com/BarsTiger/MultiMatePlayer/master/MultiMate_Player.py", "MultiMate_Player.pyw")
    subprocess.Popen(sys.executable + ' MultiMate_Player.pyw')

    time.sleep(0.5)
    exit()

ui.exeVerSownload.clicked.connect(dlExe)
ui.pyVerSownload.clicked.connect(dlPy)
ui.pywVerSownload.clicked.connect(dlPyw)

sys.exit(app.exec_())