from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
)
from PyQt5 import QtCore
from gui.container import Container
import sys
from gui._version import __version__
import win32gui


def window_enum_handler(hwnd, resultList):
    if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != '':
        resultList.append((hwnd, win32gui.GetWindowText(hwnd)))


def get_app_list(handles=[]):
    mlst=[]
    win32gui.EnumWindows(window_enum_handler, handles)
    for handle in handles:
        mlst.append(handle)
    return mlst


for handle, name in get_app_list():
    if 'Lowell Instruments - Domino' in name:
        win32gui.ShowWindow(handle, 9)
        # win32gui.ShowWindow(handle, 5)
        win32gui.BringWindowToTop(handle)
        win32gui.RedrawWindow(handle)
        sys.exit()

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

QtCore.QCoreApplication.setOrganizationName('LowellInstruments')
QtCore.QCoreApplication.setOrganizationDomain('lowellinstruments.com')
QtCore.QCoreApplication.setApplicationName('Domino' + '_' + __version__)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()  # create a main window

    ui = Container(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
