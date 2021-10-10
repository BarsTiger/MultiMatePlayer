import random
import threading
import time
from tkinter import *
import platform
import sys, subprocess, os
import urllib.parse
import urllib.request
import json
import zipfile
try:
    import vlc
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'python-vlc'])
    import vlc

try:
    import pafy
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pafy'])
    import pafy

try:
    import requests
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'requests'])
    import requests

try:
    from PyQt5 import QtCore, QtGui, QtWidgets
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'PyQt5'])
    from PyQt5 import QtCore, QtGui, QtWidgets

try:
    import psycopg2
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'psycopg2'])
    import psycopg2

try:
    from pypresence import Presence
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pypresence'])
    from pypresence import Presence

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

playlist = {}
instance = vlc.Instance()
media = None
mediaplayer = instance.media_player_new()
is_paused = False
timeToSleep = 0
playnext = True
newindex = 0

rpc = Presence("896669007342633000")
rpc.connect()
rpc.update(details="Just started app", state="Nothing is beeing listened...", large_image="multimate", start=time.time())

class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(801, 580)
        MainWindow.setWindowIcon(QtGui.QIcon('resources/MultiMate.ico'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.timeline = QtWidgets.QSlider(self.centralwidget)
        self.timeline.setGeometry(QtCore.QRect(10, 490, 781, 22))
        self.timeline.setPageStep(1)
        self.timeline.setOrientation(QtCore.Qt.Horizontal)
        self.timeline.setObjectName("timeline")
        self.timeline.setMaximum(1000)

        self.playpausebutton = QtWidgets.QPushButton(self.centralwidget)
        self.playpausebutton.setEnabled(True)
        self.playpausebutton.setGeometry(QtCore.QRect(390, 520, 40, 40))
        font = QtGui.QFont()
        font.setKerning(True)
        self.playpausebutton.setFont(font)
        self.playpausebutton.setStyleSheet("background-color: rgba(10, 0, 0, 0);\n"
                                        "")
        self.playpausebutton.setText("")
        self.playpausebutton.setObjectName("playpausebutton")
        self.playpausePicture = QtWidgets.QLabel(self.centralwidget)
        self.playpausePicture.setGeometry(QtCore.QRect(390, 520, 40, 40))
        self.playpausePicture.setText("")
        self.playpausePicture.setPixmap(QtGui.QPixmap("resources/MultiMate40x40.png"))
        self.playpausePicture.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.playpausePicture.setObjectName("playpausePicture")

        self.hardstopbutton = QtWidgets.QPushButton(self.centralwidget)
        self.hardstopbutton.setEnabled(True)
        self.hardstopbutton.setGeometry(QtCore.QRect(290, 520, 40, 40))
        font = QtGui.QFont()
        font.setKerning(True)
        self.hardstopbutton.setFont(font)
        self.hardstopbutton.setStyleSheet("background-color: rgba(10, 0, 0, 0);\n"
                                           "")
        self.hardstopbutton.setText("")
        self.hardstopbutton.setObjectName("hardstopbutton")
        self.hardstopPicture = QtWidgets.QLabel(self.centralwidget)
        self.hardstopPicture.setGeometry(QtCore.QRect(290, 520, 40, 40))
        self.hardstopPicture.setText("")
        self.hardstopPicture.setPixmap(QtGui.QPixmap("resources/hardstopbutton.png"))
        self.hardstopPicture.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.hardstopPicture.setObjectName("hardstopPicture")

        self.prevbutton = QtWidgets.QPushButton(self.centralwidget)
        self.prevbutton.setEnabled(True)
        self.prevbutton.setGeometry(QtCore.QRect(340, 520, 40, 40))
        font = QtGui.QFont()
        font.setKerning(True)
        self.prevbutton.setFont(font)
        self.prevbutton.setStyleSheet("background-color: rgba(10, 0, 0, 0);\n"
"")
        self.prevbutton.setText("")
        self.prevbutton.setObjectName("prevbutton")
        self.prevPicture = QtWidgets.QLabel(self.centralwidget)
        self.prevPicture.setGeometry(QtCore.QRect(340, 520, 40, 40))
        self.prevPicture.setText("")
        self.prevPicture.setPixmap(QtGui.QPixmap("resources/prev.png"))
        self.prevPicture.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.prevPicture.setObjectName("prevPicture")
        self.nextbutton = QtWidgets.QPushButton(self.centralwidget)
        self.nextbutton.setEnabled(True)
        self.nextbutton.setGeometry(QtCore.QRect(440, 520, 40, 40))
        font = QtGui.QFont()
        font.setKerning(True)
        self.nextbutton.setFont(font)
        self.nextbutton.setStyleSheet("background-color: rgba(10, 0, 0, 0);\n"
"")
        self.nextbutton.setText("")
        self.nextbutton.setObjectName("nextbutton")
        self.nextPicture = QtWidgets.QLabel(self.centralwidget)
        self.nextPicture.setGeometry(QtCore.QRect(440, 520, 40, 40))
        self.nextPicture.setText("")
        self.nextPicture.setPixmap(QtGui.QPixmap("resources/next.png"))
        self.nextPicture.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.nextPicture.setObjectName("nextPicture")

        self.hardplaybutton = QtWidgets.QPushButton(self.centralwidget)
        self.hardplaybutton.setEnabled(True)
        self.hardplaybutton.setGeometry(QtCore.QRect(490, 520, 40, 40))
        font = QtGui.QFont()
        font.setKerning(True)
        self.hardplaybutton.setFont(font)
        self.hardplaybutton.setStyleSheet("background-color: rgba(10, 0, 0, 0);\n"
                                           "")
        self.hardplaybutton.setText("")
        self.hardplaybutton.setObjectName("hardplaybutton")
        self.hardplayPicture = QtWidgets.QLabel(self.centralwidget)
        self.hardplayPicture.setGeometry(QtCore.QRect(490, 520, 40, 40))
        self.hardplayPicture.setText("")
        self.hardplayPicture.setPixmap(QtGui.QPixmap("resources/hardplaybutton.png"))
        self.hardplayPicture.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.hardplayPicture.setObjectName("hardplayPicture")

        self.speedBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.speedBox.setGeometry(QtCore.QRect(10, 515, 62, 22))
        self.speedBox.setDecimals(1)
        self.speedBox.setProperty("value", 1.0)
        self.speedBox.setSingleStep(0.2)
        self.speedBox.setObjectName("speedBox")
        self.timenow = QtWidgets.QTextEdit(self.centralwidget)
        self.timenow.setGeometry(QtCore.QRect(713, 515, 81, 23))
        self.timenow.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.timenow.setObjectName("timenow")
        self.speedTextLabel = QtWidgets.QLabel(self.centralwidget)
        self.speedTextLabel.setGeometry(QtCore.QRect(25, 536, 47, 13))
        self.speedTextLabel.setObjectName("speedTextLabel")
        self.timeTextLabel = QtWidgets.QLabel(self.centralwidget)
        self.timeTextLabel.setGeometry(QtCore.QRect(740, 536, 47, 13))
        self.timeTextLabel.setObjectName("timeTextLabel")
        self.volumeDial = QtWidgets.QDial(self.centralwidget)
        self.volumeDial.setGeometry(QtCore.QRect(719, 0, 81, 81))
        self.volumeDial.setStyleSheet("")
        self.volumeDial.setMinimum(1)
        self.volumeDial.setMaximum(100)
        self.volumeDial.setPageStep(1)
        self.volumeDial.setProperty("value", 100)
        self.volumeDial.setObjectName("volumeDial")
        self.VolDialBG = QtWidgets.QLabel(self.centralwidget)
        self.VolDialBG.setGeometry(QtCore.QRect(720, 0, 81, 81))
        self.VolDialBG.setText("")
        self.VolDialBG.setPixmap(QtGui.QPixmap("resources/MultiMate80x80.png"))
        self.VolDialBG.setObjectName("VolDialBG")
        self.playlistsComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.playlistsComboBox.setGeometry(QtCore.QRect(0, 0, 231, 22))
        self.playlistsComboBox.setCurrentText("")
        self.playlistsComboBox.setDuplicatesEnabled(True)
        self.playlistsComboBox.setObjectName("playlistsComboBox")
        for playlist in os.listdir(os.getcwd()):
            self.playlistsComboBox.addItem(playlist)
        self.nowPlaying = QtWidgets.QTextBrowser(self.centralwidget)
        self.nowPlaying.setGeometry(QtCore.QRect(10, 460, 781, 23))
        self.nowPlaying.setObjectName("nowPlaying")
        self.openPlaylistButton = QtWidgets.QPushButton(self.centralwidget)
        self.openPlaylistButton.setGeometry(QtCore.QRect(230, 0, 75, 23))
        self.openPlaylistButton.setObjectName("openPlaylistButton")
        self.songList = QtWidgets.QTextBrowser(self.centralwidget)
        self.songList.setGeometry(QtCore.QRect(0, 43, 301, 411))
        self.songList.setObjectName("songList")
        self.TextAllSongs = QtWidgets.QTextEdit(self.centralwidget)
        self.TextAllSongs.setGeometry(QtCore.QRect(0, 20, 301, 23))
        self.TextAllSongs.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.TextAllSongs.setObjectName("TextAllSongs")
        self.toFindName = QtWidgets.QTextEdit(self.centralwidget)
        self.toFindName.setGeometry(QtCore.QRect(310, 0, 331, 23))
        self.toFindName.setObjectName("toFindName")
        self.findSongButton = QtWidgets.QPushButton(self.centralwidget)
        self.findSongButton.setGeometry(QtCore.QRect(640, 0, 75, 23))
        self.findSongButton.setObjectName("findSongButton")
        self.foundSongs = QtWidgets.QComboBox(self.centralwidget)
        self.foundSongs.setGeometry(QtCore.QRect(310, 30, 331, 22))
        self.foundSongs.setObjectName("foundSongs")
        self.addThisSongButton = QtWidgets.QPushButton(self.centralwidget)
        self.addThisSongButton.setGeometry(QtCore.QRect(640, 30, 75, 23))
        self.addThisSongButton.setObjectName("addThisSongButton")
        self.mixButton = QtWidgets.QPushButton(self.centralwidget)
        self.mixButton.setGeometry(QtCore.QRect(720, 90, 75, 41))
        self.mixButton.setObjectName("mixButton")

        self.playlistSettingsButton = QtWidgets.QPushButton(self.centralwidget)
        self.playlistSettingsButton.setGeometry(QtCore.QRect(720, 140, 75, 51))
        self.playlistSettingsButton.setObjectName("playlistSettingsButton")

        self.settingsButton = QtWidgets.QPushButton(self.centralwidget)
        self.settingsButton.setGeometry(QtCore.QRect(720, 200, 75, 45))
        self.settingsButton.setObjectName("settingsButton")

        self.extendedFunctButton = QtWidgets.QPushButton(self.centralwidget)
        self.extendedFunctButton.setGeometry(QtCore.QRect(720, 260, 75, 45))
        self.extendedFunctButton.setObjectName("extendedFunctButton")

        if platform.system() == "Darwin": # for MacOS
            self.videoframe = QtWidgets.QMacCocoaViewContainer(self.centralwidget)
        else:
            self.videoframe = QtWidgets.QFrame(self.centralwidget)
        self.videoframe.setGeometry(QtCore.QRect(310, 70, 401, 381))
        self.videoframe.setObjectName("videoframe")
        self.timeline.raise_()
        self.playpausePicture.raise_()
        self.prevPicture.raise_()
        self.nextPicture.raise_()
        self.speedBox.raise_()
        self.nextbutton.raise_()
        self.prevbutton.raise_()
        self.playpausebutton.raise_()
        self.timenow.raise_()
        self.speedTextLabel.raise_()
        self.timeTextLabel.raise_()
        self.VolDialBG.raise_()
        self.volumeDial.raise_()
        self.playlistsComboBox.raise_()
        self.nowPlaying.raise_()
        self.openPlaylistButton.raise_()
        self.songList.raise_()
        self.TextAllSongs.raise_()
        self.toFindName.raise_()
        self.findSongButton.raise_()
        self.foundSongs.raise_()
        self.addThisSongButton.raise_()
        self.mixButton.raise_()
        self.playlistSettingsButton.raise_()
        self.videoframe.raise_()
        self.hardplaybutton.raise_()
        self.hardstopbutton.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 801, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_ui)

    def update_ui(self):
        global mediaplayer
        global playnext
        media_pos = int(mediaplayer.get_position() * 1000)
        if mediaplayer.get_position() > 0.99:
            playallpl(newindex)
        self.timeline.setValue(media_pos)
        self.timenow.setText(str(time.strftime("%M:%S", time.gmtime(int(mediaplayer.get_time()/1000)))) + "/" + str(time.strftime("%M:%S", time.gmtime(int(mediaplayer.get_length()/1000)))))

        if not mediaplayer.is_playing():
            self.timer.stop()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MultiMate Player"))
        self.speedBox.setPrefix(_translate("MainWindow", "x"))
        self.speedTextLabel.setText(_translate("MainWindow", "Speed"))
        self.timeTextLabel.setText(_translate("MainWindow", "Time"))
        self.nowPlaying.setPlaceholderText(_translate("MainWindow", "Nothing here..."))
        self.openPlaylistButton.setText(_translate("MainWindow", "Open playlist"))
        self.songList.setPlaceholderText(_translate("MainWindow", "Nothing here..."))
        self.TextAllSongs.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Songs in playlist</p></body></html>"))
        self.findSongButton.setText(_translate("MainWindow", "Find song"))
        self.addThisSongButton.setText(_translate("MainWindow", "Add this song"))
        self.mixButton.setText(_translate("MainWindow", "Mix"))
        self.playlistSettingsButton.setText(_translate("MainWindow", "Playlist \nsettings"))
        self.settingsButton.setText(_translate("MainWindow", "Settings"))
        self.extendedFunctButton.setText(_translate("MainWindow", "Extended \n functions"))


class Ui_PlaylistSettings(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(160, 97)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 160, 80))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.deletesongButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.deletesongButton.setObjectName("deletesongButton")
        self.verticalLayout.addWidget(self.deletesongButton)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Playlist settings"))
        self.deletesongButton.setText(_translate("MainWindow", "Manage songs in playlist"))

class Ui_Settings(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(160, 97)
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

class Ui_Updater(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(160, 97)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Updater"))
        self.updateButton.setText(_translate("MainWindow", "Download newest .py"))

class Ui_DelSongs(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 510)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(0, 0, 300, 461))
        self.listWidget.setObjectName("listWidget")
        self.delButton = QtWidgets.QPushButton(self.centralwidget)
        self.delButton.setGeometry(QtCore.QRect(0, 460, 300, 23))
        self.delButton.setObjectName("delButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 300, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Songs manager"))
        self.delButton.setText(_translate("MainWindow", "Delete selected song"))

class Ui_ProSearch(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(750, 600)
        MainWindow.setMinimumSize(QtCore.QSize(750, 600))
        MainWindow.setMaximumSize(QtCore.QSize(750, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(0, 180, 750, 361))
        self.listWidget.setObjectName("listWidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(160, 70, 440, 30))
        self.lineEdit.setStyleSheet("border-radius:\n"
"    1 px;")
        self.lineEdit.setReadOnly(False)
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(285, 20, 180, 31))
        self.label.setObjectName("label")
        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchButton.setGeometry(QtCore.QRect(300, 110, 150, 30))
        self.searchButton.setObjectName("searchButton")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(300, 550, 150, 31))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 750, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pro search"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Never gonna give you up"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:18pt;\">Advanced search</span></p></body></html>"))
        self.searchButton.setText(_translate("MainWindow", "Search"))
        self.pushButton.setText(_translate("MainWindow", "Add selected"))

    def searchinYT(self):
        global results
        search = self.lineEdit.text()
        results = YoutubeSearch(search, max_results=150).to_dict()

        self.listWidget.clear()

        for i in range(len(results)):
            item = QtWidgets.QListWidgetItem(results[i]["channel"] + ": " + results[i]["title"])
            item.setCheckState(QtCore.Qt.Unchecked)
            self.listWidget.addItem(item)

        return results

    def addtopl(self):
        global results
        global playlist
        whichres = list()
        for index in range(self.listWidget.count()):
            if self.listWidget.item(index).checkState() == QtCore.Qt.Checked:
                whichres.append(index)

        for i in whichres:
            i = int(i)
            url = "https://www.youtube.com" + results[i]["url_suffix"]
            willbesong = {}
            willbesong['name'] = results[i]["title"]
            willbesong['author'] = results[i]["channel"]
            willbesong['url'] = url
            playlist[str(len(list(playlist)))] = willbesong

        playlistfile = open(ui.playlistsComboBox.currentText(), 'w+')
        json.dump(playlist, playlistfile, indent=3, ensure_ascii=False)
        playlistfile.close()

        getplaylist()

class Ui_ExtendedMenu(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(151, 74)
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



class YoutubeSearch:
    def __init__(self, search_terms: str, max_results=None):
        self.search_terms = search_terms
        self.max_results = max_results
        self.videos = self._search()

    def _search(self):
        encoded_search = urllib.parse.quote_plus(self.search_terms)
        BASE_URL = "https://youtube.com"
        url = f"{BASE_URL}/search?q={encoded_search}"
        response = requests.get(url).text
        while "ytInitialData" not in response:
            response = requests.get(url).text
        results = self._parse_html(response)
        if self.max_results is not None and len(results) > self.max_results:
            return results[: self.max_results]
        return results

    def _parse_html(self, response):
        results = []
        start = (
            response.index("ytInitialData")
            + len("ytInitialData")
            + 3
        )
        end = response.index("};", start) + 1
        json_str = response[start:end]
        data = json.loads(json_str)

        videos = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"][
            "sectionListRenderer"
        ]["contents"][0]["itemSectionRenderer"]["contents"]

        for video in videos:
            res = {}
            if "videoRenderer" in video.keys():
                video_data = video.get("videoRenderer", {})
                res["id"] = video_data.get("videoId", None)
                res["thumbnails"] = [thumb.get("url", None) for thumb in video_data.get("thumbnail", {}).get("thumbnails", [{}]) ]
                res["title"] = video_data.get("title", {}).get("runs", [[{}]])[0].get("text", None)
                res["long_desc"] = video_data.get("descriptionSnippet", {}).get("runs", [{}])[0].get("text", None)
                res["channel"] = video_data.get("longBylineText", {}).get("runs", [[{}]])[0].get("text", None)
                res["duration"] = video_data.get("lengthText", {}).get("simpleText", 0)
                res["views"] = video_data.get("viewCountText", {}).get("simpleText", 0)
                res["publish_time"] = video_data.get("publishedTimeText", {}).get("simpleText", 0)
                res["url_suffix"] = video_data.get("navigationEndpoint", {}).get("commandMetadata", {}).get("webCommandMetadata", {}).get("url", None)
                results.append(res)
        return results

    def to_dict(self, clear_cache=True):
        result = self.videos
        if clear_cache:
            self.videos = ""
        return result

    def to_json(self, clear_cache=True):
        result = json.dumps({"videos": self.videos})
        if clear_cache:
            self.videos = ""
        return result

def readpl(plname):
    playlistfile = open(plname)
    playlist = json.load(playlistfile)
    playlistfile.close()

    return playlist

def searchinYT():
    global results
    search = ui.toFindName.toPlainText()
    results = YoutubeSearch(search, max_results=10).to_dict()

    ui.foundSongs.clear()

    for i in range(len(results)):
        ui.foundSongs.addItem(results[i]["channel"] + ": " + results[i]["title"])

    return results

results = dict()

def addtopl():
    global results
    global playlist
    whichres = ui.foundSongs.currentIndex()

    url = "https://www.youtube.com" + results[whichres]["url_suffix"]

    print(str(len(list(playlist))))
    willbesong = {}
    willbesong['name'] = results[whichres]["title"]
    willbesong['author'] = results[whichres]["channel"]
    willbesong['url'] = url
    playlist[str(len(list(playlist)))] = willbesong

    playlistfile = open(ui.playlistsComboBox.currentText(), 'w+')
    json.dump(playlist, playlistfile, indent=3, ensure_ascii=False)
    playlistfile.close()

    getplaylist()

def set_position():
    global instance
    global media
    global mediaplayer
    global is_paused
    ui.timer.stop()
    pos = ui.timeline.value()
    mediaplayer.set_position(pos / 1000.0)
    ui.timer.start(100)

def playmusic(url, name, author):
    video = pafy.new(url)
    best = video.getbest()
    playurl = best.url

    global instance
    global media
    global mediaplayer
    global is_paused
    global timeToSleep
    global playnext

    playnext = False

    media = instance.media_new(playurl)
    mediaplayer.set_media(media)

    if platform.system() == "Linux":  # for Linux using the X Server
        mediaplayer.set_xwindow(int(ui.videoframe.winId()))
    elif platform.system() == "Windows":  # for Windows
        mediaplayer.set_hwnd(int(ui.videoframe.winId()))
    elif platform.system() == "Darwin":  # for MacOS
        mediaplayer.set_nsobject(int(ui.videoframe.winId()))

    if mediaplayer.is_playing():
        mediaplayer.pause()
        is_paused = True
        ui.timer.stop()
    else:
        mediaplayer.play()
        ui.timer.start(100)
        is_paused = False

    mediaplayer.audio_set_volume(100)
    time.sleep(0.5)
    timeToSleep = mediaplayer.get_length() / 1000
    cls()
    ui.nowPlaying.setText(author + " - " + name)
    rpc.update(details="Listening " + author, state=name, large_image="multimate",
               start=time.time())
    print("Playing " + author + " - " + name)

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

appPlSet = QtWidgets.QApplication(sys.argv)
MainWindowPlSet = QtWidgets.QMainWindow()
uiPlSet = Ui_PlaylistSettings()
uiPlSet.setupUi(MainWindowPlSet)

appDelS = QtWidgets.QApplication(sys.argv)
MainWindowDelS = QtWidgets.QMainWindow()
uiDelS = Ui_DelSongs()
uiDelS.setupUi(MainWindowDelS)

appSet = QtWidgets.QApplication(sys.argv)
MainWindowSet = QtWidgets.QMainWindow()
uiSet = Ui_Settings()
uiSet.setupUi(MainWindowSet)

appUpd = QtWidgets.QApplication(sys.argv)
MainWindowUpd = QtWidgets.QMainWindow()
uiUpd = Ui_Updater()
uiUpd.setupUi(MainWindowUpd)

appExt = QtWidgets.QApplication(sys.argv)
MainWindowExt = QtWidgets.QMainWindow()
uiExt = Ui_ExtendedMenu()
uiExt.setupUi(MainWindowExt)

appPSearch = QtWidgets.QApplication(sys.argv)
MainWindowPSearch = QtWidgets.QMainWindow()
uiPSearch = Ui_ProSearch()
uiPSearch.setupUi(MainWindowPSearch)

def getplaylist():
    global playlist
    global newindex
    global listplaylist
    newindex = 0
    playlist = readpl(ui.playlistsComboBox.currentText())
    ui.songList.clear()
    for item in list(playlist):
        ui.songList.append(str(playlist[item]['author'] + " - " + playlist[item]['name']))
    listplaylist = list(playlist)

def playallpl(index=0):
    global listplaylist
    global newindex
    item = listplaylist[index]
    playmusic(playlist[item]['url'], playlist[item]['name'], playlist[item]['author'])
    if newindex < len(listplaylist) - 1:
        newindex += 1
    else:
        newindex = 0

def playnextsong():
    global newindex
    playallpl(newindex)

def playprevsong():
    global newindex
    newindex -= 2
    playallpl(newindex)

def stopandclear():
    mediaplayer.set_media(None)

def playpause():
    global is_paused
    if mediaplayer.is_playing():
        mediaplayer.pause()
        is_paused = True
        ui.timer.stop()
    else:
        mediaplayer.play()
        ui.timer.start(100)
        is_paused = False

def changevolume():
    mediaplayer.audio_set_volume(ui.volumeDial.value())

def changespeed():
    mediaplayer.set_rate(ui.speedBox.value())

def addtofoundsongs():
    ui.toFindName.toPlainText()

def generateDeletionList():
    global playlist
    songList = []
    for item in list(playlist):
        songList.append(str(playlist[item]['author'] + " - " + playlist[item]['name']))
    uiDelS.listWidget.clear()
    uiDelS.listWidget.addItems(songList)

def showMainWindowDelS():
    generateDeletionList()
    MainWindowDelS.show()

def delSongFromPl():
    global playlist
    indextodel = uiDelS.listWidget.selectedIndexes()[0].row()
    toDelID = list(playlist)[indextodel]
    playlist.pop(toDelID)
    playlistfile = open(ui.playlistsComboBox.currentText(), 'w+')
    json.dump(playlist, playlistfile, indent=3, ensure_ascii=False)
    playlistfile.close()

    getplaylist()

def mixPlaylist():
    global listplaylist
    try:
        random.shuffle(listplaylist)
        print("Mixed!")
    except:
        pass

def updateAppPy():
    rpc.update(details="Updating", state="Everything needs to be up-to-date", large_image="multimate",
               start=time.time())
    urllib.request.urlretrieve("https://github.com/BarsTiger/MultiMatePlayer/raw/master/resources/resources.zip", 'resources/resources.zip')
    with zipfile.ZipFile('resources/resources.zip', 'r') as archfile:
        archfile.extractall("resources")
    os.remove('resources/resources.zip')
    urllib.request.urlretrieve("https://raw.githubusercontent.com/BarsTiger/MultiMatePlayer/master/MultiMate_Player.py", 'MultiMate_Player.py')
    subprocess.Popen(sys.executable + ' MultiMate_Player.py')
    time.sleep(0.5)
    exit()

MainWindow.show()
cls()

ui.openPlaylistButton.clicked.connect(getplaylist)
ui.hardplaybutton.clicked.connect(playallpl)
ui.timeline.sliderMoved.connect(set_position)
ui.timeline.sliderPressed.connect(set_position)
ui.nextbutton.clicked.connect(playnextsong)
ui.prevbutton.clicked.connect(playprevsong)
ui.hardstopbutton.clicked.connect(stopandclear)
ui.playpausebutton.clicked.connect(playpause)
ui.volumeDial.valueChanged.connect(changevolume)
ui.findSongButton.clicked.connect(searchinYT)
ui.addThisSongButton.clicked.connect(addtopl)
ui.speedBox.valueChanged.connect(changespeed)
ui.playlistSettingsButton.clicked.connect(MainWindowPlSet.show)
ui.mixButton.clicked.connect(mixPlaylist)
ui.settingsButton.clicked.connect(MainWindowSet.show)
ui.extendedFunctButton.clicked.connect(MainWindowExt.show)

uiPlSet.deletesongButton.clicked.connect(showMainWindowDelS)

uiDelS.delButton.clicked.connect(delSongFromPl)

uiSet.updateButton.clicked.connect(MainWindowUpd.show)

uiUpd.updateButton.clicked.connect(updateAppPy)

uiExt.prosearchButton.clicked.connect(MainWindowPSearch.show)

uiPSearch.searchButton.clicked.connect(uiPSearch.searchinYT)
uiPSearch.pushButton.clicked.connect(uiPSearch.addtopl)

sys.exit(app.exec_())
