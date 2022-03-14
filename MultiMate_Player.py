import json
import platform
import random
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import zipfile
from resources.lib.ytsearch import YoutubeSearch
import resources.pafy_fix.pafy as pafy
from resources.lib.config import config, configfile

try:
    import vlc
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'python-vlc'])
    import vlc

try:
    import youtube_dl
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'youtube_dl'])
    import youtube_dl

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
from resources.gui.gui import *
from resources.lib.console import *
from resources.lib.rpc import rpc


playlist = {}
instance = vlc.Instance()
media = None
mediaplayer = instance.media_player_new()
is_paused = False
timeToSleep = 0
playnext = True
newindex = 0
listplaylist = list()
results = dict()

playerStarted = False


def searchinYTpro():
    global results
    search = uiPSearch.lineEdit.text()
    results = YoutubeSearch(search, max_results=150).to_dict()

    uiPSearch.listWidget.clear()

    for i in range(len(results)):
        item = QtWidgets.QListWidgetItem(results[i]["channel"] + ": " + results[i]["title"])
        item.setCheckState(QtCore.Qt.Unchecked)
        uiPSearch.listWidget.addItem(item)

    return results


def addtoplpro():
    global results
    global playlist
    whichres = list()
    for index in range(uiPSearch.listWidget.count()):
        if uiPSearch.listWidget.item(index).checkState() == QtCore.Qt.Checked:
            whichres.append(index)

    for i in whichres:
        i = int(i)
        url = "https://www.youtube.com" + results[i]["url_suffix"]
        willbesong = dict()
        willbesong['name'] = bytes(results[i]["title"], 'Windows-1251', 'ignore').decode('Windows-1251', 'ignore')
        willbesong['author'] = bytes(results[i]["channel"], 'Windows-1251', 'ignore').decode('Windows-1251', 'ignore')
        willbesong['url'] = url
        playlist[str(len(list(playlist)) + 1)] = willbesong

    playlistfile = open(ui.playlistsComboBox.currentText(), 'w+')
    json.dump(playlist, playlistfile, indent=3, ensure_ascii=False)
    playlistfile.close()

    getplaylist()


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


def addtopl():
    global results
    global playlist
    whichres = ui.foundSongs.currentIndex()

    url = "https://www.youtube.com" + results[whichres]["url_suffix"]

    print(str(len(list(playlist))))
    willbesong = dict()
    willbesong['name'] = bytes(results[whichres]["title"], 'Windows-1251', 'ignore').decode('Windows-1251', 'ignore')
    willbesong['author'] = bytes(results[whichres]["channel"], 'Windows-1251', 'ignore').decode('Windows-1251',
                                                                                                'ignore')
    willbesong['url'] = url
    playlist[str(len(list(playlist)) + 1)] = willbesong

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
    video = None
    while video is None:
        try:
            video = pafy.new(url)
        except:
            print("Cannot create translation link, I will try once more")
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

    playpause()
    ui.timer.stop()
    time.sleep(1)
    if int(mediaplayer.get_length() / 60000) <= 3:
        timeToSleepForUnbug = 0
    else:
        timeToSleepForUnbug = (mediaplayer.get_length() / 60000) / 2.6
    time.sleep(timeToSleepForUnbug)
    ui.timer.start(100)

    mediaplayer.audio_set_volume(ui.volumeDial.value())
    time.sleep(0.5)
    timeToSleep = mediaplayer.get_length() / 1000
    cls()
    ui.nowPlaying.setText(author + " - " + name)
    try:
        if config['showrpc']:
            rpc.update(details="Listening " + author, state=name, large_image="multimate",
                       start=int(time.time()))
    except:
        pass
    print("Playing " + author + " - " + name)


def getplaylist():
    global playlist
    global newindex
    global listplaylist
    newindex = 0
    playlist = readpl(ui.playlistsComboBox.currentText())
    ui.songList.clear()
    listplaylist = list(playlist)
    for item in listplaylist:
        ui.songList.addItem(str(playlist[item]['author'] + " - " + playlist[item]['name']))
    ui.nowPlaying.setPlaceholderText("Click play button or song name...")


def playallpl(index=0):
    global listplaylist
    global newindex
    ui.playpausebutton.clicked.disconnect()
    ui.playpausebutton.clicked.connect(playpause)
    item = listplaylist[index]
    playmusic(playlist[item]['url'], playlist[item]['name'], playlist[item]['author'])
    ui.songList.setCurrentRow(index)
    if newindex < len(listplaylist) - 1:
        newindex = index + 1
    else:
        newindex = 0


def playprevsong():
    global newindex
    newindex -= 2
    playallpl(newindex)


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

    generateDeletionList()
    getplaylist()


def mixPlaylist():
    global listplaylist
    try:
        random.shuffle(listplaylist)
        ui.songList.clear()
        for item in listplaylist:
            ui.songList.addItem(str(playlist[item]['author'] + " - " + playlist[item]['name']))
    except:
        pass


def updateAppPy():
    try:
        if config['showrpc']:
            rpc.update(details="Updating", state="Everything needs to be up-to-date", large_image="multimate",
                       start=int(time.time()))
    except:
        pass
    urllib.request.urlretrieve("https://github.com/BarsTiger/MultiMatePlayer/raw/master/resources/resources.zip",
                               'resources/resources.zip')
    with zipfile.ZipFile('resources/resources.zip', 'r') as archfile:
        archfile.extractall("resources")
    if config['mainbuild'] != "MultiMate_Player.exe":
        urllib.request.urlretrieve(
            "https://raw.githubusercontent.com/BarsTiger/MultiMatePlayer/master/MultiMate_Player.py",
            config['mainbuild'])
        subprocess.Popen(sys.executable + ' ' + config['mainbuild'])
    elif config['mainbuild'] == "MultiMate_Player.exe":
        urllib.request.urlretrieve("https://github.com/BarsTiger/MultiMatePlayer/raw/master/MultiMate_Player.exe",
                                   config['mainbuild'])
        subprocess.Popen(config['mainbuild'])
    time.sleep(0.5)
    exit()


def changeRPCinCFG():
    config['showrpc'] = uiRPCSet.ShowRPCcheckBox.isChecked()
    cfgwrite = open(configfile, 'w+')
    json.dump(config, cfgwrite, indent=3)
    cfgwrite.close()


def changeMainBuild():
    config['mainbuild'] = uiMainBuild.listWidget.currentItem().text()
    cfgwrite = open(configfile, 'w+')
    json.dump(config, cfgwrite, indent=3)
    cfgwrite.close()


def update_ui():
    global mediaplayer
    global playnext
    media_pos = int(mediaplayer.get_position() * 1000)
    if mediaplayer.get_position() > 0.99:
        playallpl(newindex)
    ui.timeline.setValue(media_pos)
    ui.timenow.setText(str(time.strftime("%M:%S", time.gmtime(int(mediaplayer.get_time() / 1000)))) + "/" + str(
        time.strftime("%M:%S", time.gmtime(int(mediaplayer.get_length() / 1000)))))

    if not mediaplayer.is_playing():
        ui.timer.stop()


MainWindow.show()
cls()

ui.timer.timeout.connect(update_ui)
ui.openPlaylistButton.clicked.connect(getplaylist)
ui.playpausebutton.clicked.connect(playallpl)
ui.timeline.sliderMoved.connect(set_position)
ui.timeline.sliderPressed.connect(set_position)
ui.nextbutton.clicked.connect(lambda: playallpl(newindex))
ui.prevbutton.clicked.connect(playprevsong)
ui.volumeDial.valueChanged.connect(lambda: mediaplayer.audio_set_volume(ui.volumeDial.value()))
ui.findSongButton.clicked.connect(searchinYT)
ui.addThisSongButton.clicked.connect(addtopl)
ui.speedBox.valueChanged.connect(lambda: mediaplayer.set_rate(ui.speedBox.value()))
ui.playlistSettingsButton.clicked.connect(MainWindowPlSet.show)
ui.mixButton.clicked.connect(mixPlaylist)
ui.settingsButton.clicked.connect(MainWindowSet.show)
ui.extendedFunctButton.clicked.connect(MainWindowExt.show)
ui.songList.itemClicked.connect(lambda: playallpl(ui.songList.currentRow()))

uiPlSet.deletesongButton.clicked.connect(showMainWindowDelS)

uiDelS.delButton.clicked.connect(delSongFromPl)

uiSet.updateButton.clicked.connect(MainWindowUpd.show)
uiSet.appBuildButton.clicked.connect(MainWindowMainBuild.show)
uiSet.RPCButton.clicked.connect(MainWindowRPCSet.show)

uiUpd.updateButton.clicked.connect(updateAppPy)

uiExt.prosearchButton.clicked.connect(MainWindowPSearch.show)

uiPSearch.searchButton.clicked.connect(searchinYTpro)
uiPSearch.pushButton.clicked.connect(addtoplpro)

uiRPCSet.ShowRPCcheckBox.clicked.connect(changeRPCinCFG)

uiMainBuild.pushButton.clicked.connect(changeMainBuild)

sys.exit(app.exec_())
