import sys
from PyQt5 import QtWidgets
from resources.gui.Ui_DelSongs import Ui_DelSongs
from resources.gui.Ui_ExtendedMenu import Ui_ExtendedMenu
from resources.gui.Ui_MainBuild import Ui_MainBuild
from resources.gui.Ui_MainWindow import Ui_MainWindow
from resources.gui.Ui_PlaylistSettings import Ui_PlaylistSettings
from resources.gui.Ui_ProSearch import Ui_ProSearch
from resources.gui.Ui_RPCsettings import Ui_RPCsettings
from resources.gui.Ui_Settings import Ui_Settings
from resources.gui.Ui_Updater import Ui_Updater


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

appRPCSet = QtWidgets.QApplication(sys.argv)
MainWindowRPCSet = QtWidgets.QMainWindow()
uiRPCSet = Ui_RPCsettings()
uiRPCSet.setupUi(MainWindowRPCSet)

appMainBuild = QtWidgets.QApplication(sys.argv)
MainWindowMainBuild = QtWidgets.QMainWindow()
uiMainBuild = Ui_MainBuild()
uiMainBuild.setupUi(MainWindowMainBuild)
