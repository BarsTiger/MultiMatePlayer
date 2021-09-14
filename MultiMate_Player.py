import threading
import time
from tkinter import *
import sys, subprocess, os
import urllib.parse
import json
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

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(801, 580)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.timeline = QtWidgets.QSlider(self.centralwidget)
        self.timeline.setGeometry(QtCore.QRect(10, 490, 781, 22))
        self.timeline.setPageStep(1)
        self.timeline.setOrientation(QtCore.Qt.Horizontal)
        self.timeline.setObjectName("timeline")
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
        self.playpausePicture.setPixmap(QtGui.QPixmap("D:\\RAZNOE\\prgrming\\PyQtUIs\\../../!программирование/PYSHARM projects/MultiMate Player/resources/MultiMate40x40.png"))
        self.playpausePicture.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.playpausePicture.setObjectName("playpausePicture")
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
        self.prevPicture.setPixmap(QtGui.QPixmap("D:\\RAZNOE\\prgrming\\PyQtUIs\\../../!программирование/PYSHARM projects/MultiMate Player/resources/prev.png"))
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
        self.nextPicture.setPixmap(QtGui.QPixmap("D:\\RAZNOE\\prgrming\\PyQtUIs\\../../!программирование/PYSHARM projects/MultiMate Player/resources/next.png"))
        self.nextPicture.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.nextPicture.setObjectName("nextPicture")
        self.speedBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.speedBox.setGeometry(QtCore.QRect(10, 515, 62, 22))
        self.speedBox.setDecimals(1)
        self.speedBox.setProperty("value", 1.0)
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
        self.VolDialBG.setPixmap(QtGui.QPixmap("D:\\RAZNOE\\prgrming\\PyQtUIs\\../../!программирование/PYSHARM projects/MultiMate Player/resources/MultiMate80x80.png"))
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
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(310, 0, 331, 23))
        self.textEdit.setObjectName("textEdit")
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
        self.restartPlayerButton = QtWidgets.QPushButton(self.centralwidget)
        self.restartPlayerButton.setGeometry(QtCore.QRect(720, 140, 75, 51))
        self.restartPlayerButton.setObjectName("restartPlayerButton")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(310, 70, 401, 381))
        self.textBrowser.setObjectName("textBrowser")
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
        self.textEdit.raise_()
        self.findSongButton.raise_()
        self.foundSongs.raise_()
        self.addThisSongButton.raise_()
        self.mixButton.raise_()
        self.restartPlayerButton.raise_()
        self.textBrowser.raise_()
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

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
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
        self.restartPlayerButton.setText(_translate("MainWindow", "(Re)start \n"
"player \n"
"cycle"))
        self.textBrowser.setPlaceholderText(_translate("MainWindow", "Logs"))

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

def addtopl(playlist, plname):
    search = input("Search MultiFind: ")

    results = YoutubeSearch(search, max_results=10).to_dict()

    for i in range(len(results)):
        print(str(i) + " - " + results[i]["channel"] + ": " + results[i]["title"])

    whichres = int(input("Type here: "))

    url = "https://www.youtube.com" + results[whichres]["url_suffix"]

    print(str(len(list(playlist))))
    willbesong = {}
    willbesong['name'] = results[whichres]["title"]
    willbesong['author'] = results[whichres]["channel"]
    willbesong['url'] = url
    playlist[str(len(list(playlist)))] = willbesong

    print(playlist)

    playlistfile = open(plname, 'w+')
    json.dump(playlist, playlistfile, indent=3, ensure_ascii=False)
    playlistfile.close()


def playmusic(url, name, author):
    video = pafy.new(url)
    best = video.getbestaudio()
    playurl = best.url
    # playurl = url

    mediatoplay = vlc.MediaPlayer(playurl)
    mediatoplay.audio_set_volume(100)
    mediatoplay.play()
    time.sleep(0.5)
    length = mediatoplay.get_length() / 1000
    cls()
    print("Playing " + author + " - " + name)
    time.sleep(length)
    mediatoplay.stop()

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

playlist = {}

def getplaylist():
    global playlist
    playlist = readpl(ui.playlistsComboBox.currentText())
    for item in list(playlist):
        ui.songList.append(str(playlist[item]['author'] + " - " + playlist[item]['name']))

# addtopl(playlist, 'play.list')

for item in list(playlist):
    playmusic(playlist[item]['url'], playlist[item]['name'], playlist[item]['author'])


MainWindow.show()

ui.openPlaylistButton.clicked.connect(getplaylist)


sys.exit(app.exec_())

