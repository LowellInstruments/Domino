from PyQt5 import QtGui, QtWidgets, QtCore
from gui.container_ui import Ui_MainWindow
from gui.start_stop_ui import Ui_Frame as StartStopFrame
from gui.converter_ui import Ui_Frame as ConverterFrame
from gui.setup import SetupFrame
import sys


class Container(Ui_MainWindow):
    def __init__(self, window):
        self.window = window
        self.setupUi(window)
        self.converter_frame = ConverterFrame()
        self.converter_frame.setupUi(self.frame_convert)
        self.setup_frame = SetupFrame()
        self.setup_frame.setupUi(self.frame_setup_file)
        self.start_stop_frame = StartStopFrame()
        self.start_stop_frame.setupUi(self.frame_start_stop)
        self.pushButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton1.setGeometry(QtCore.QRect(740, 5, 48, 48))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/icons8-menu-48.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton1.setIcon(icon)
        self.pushButton1.setIconSize(QtCore.QSize(36, 36))
        self.pushButton1.setFlat(True)
        self.pushButton1.setObjectName('Preferences')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()  # create a main window
    ui = Container(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
