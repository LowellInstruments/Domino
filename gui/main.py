from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
)
from PyQt5 import QtCore
from gui.container import Container
import sys


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

QtCore.QCoreApplication.setOrganizationName('LowellInstruments')
QtCore.QCoreApplication.setOrganizationDomain('lowellinstruments.com')
QtCore.QCoreApplication.setApplicationName('Domino')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()  # create a main window

    ui = Container(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
