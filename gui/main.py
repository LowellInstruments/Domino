from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
)
from gui.container import Container
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()  # create a main window
    ui = Container(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
