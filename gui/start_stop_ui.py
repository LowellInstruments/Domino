# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './designer_files/start_stop.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(782, 512)
        Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.gridLayout = QtWidgets.QGridLayout(Frame)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_2 = QtWidgets.QFrame(Frame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_4 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_4.setMaximumSize(QtCore.QSize(50, 50))
        self.pushButton_4.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/icons8-running-rabbit-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon)
        self.pushButton_4.setIconSize(QtCore.QSize(48, 48))
        self.pushButton_4.setFlat(True)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line_3 = QtWidgets.QFrame(self.frame_2)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(self.frame_2)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_6 = QtWidgets.QLabel(self.frame_2)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.pushButton = QtWidgets.QPushButton(self.frame_2)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.label_11 = QtWidgets.QLabel(self.frame_2)
        self.label_11.setObjectName("label_11")
        self.verticalLayout.addWidget(self.label_11)
        self.line = QtWidgets.QFrame(self.frame_2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.label_8 = QtWidgets.QLabel(self.frame_2)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.label_7 = QtWidgets.QLabel(self.frame_2)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.label_9 = QtWidgets.QLabel(self.frame_2)
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
        self.label_10 = QtWidgets.QLabel(self.frame_2)
        self.label_10.setObjectName("label_10")
        self.verticalLayout.addWidget(self.label_10)
        self.line_2 = QtWidgets.QFrame(self.frame_2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame_2)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/icons8-stop-sign-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon1)
        self.pushButton_3.setIconSize(QtCore.QSize(36, 36))
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_2)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/icons8-go-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon2)
        self.pushButton_2.setIconSize(QtCore.QSize(36, 36))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addWidget(self.frame_2, 0, 0, 2, 1)
        self.tableWidget = QtWidgets.QTableWidget(Frame)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setCornerButtonEnabled(False)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(8)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(3, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(5, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(6, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(7, 0, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(22)
        self.gridLayout.addWidget(self.tableWidget, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.label_2.setText(_translate("Frame", "Device is running"))
        self.label.setText(_translate("Frame", "Connected on USB"))
        self.label_3.setText(_translate("Frame", "File Size: 487.65 MB"))
        self.label_4.setText(_translate("Frame", "SD Card Usage: 3.25 of 3.96 GB Available"))
        self.label_5.setText(_translate("Frame", "Battery Status: Good"))
        self.label_6.setText(_translate("Frame", "Logger Time: 2018-10-02 11:10:05"))
        self.pushButton.setText(_translate("Frame", "Set Clock"))
        self.label_11.setText(_translate("Frame", "Computer Time: 2018-10-02 11:10:17"))
        self.label_8.setText(_translate("Frame", "Serial Number: 111A"))
        self.label_7.setText(_translate("Frame", "Firmware Version: 1.8.64"))
        self.label_9.setText(_translate("Frame", "Model Number: MAT-1"))
        self.label_10.setText(_translate("Frame", "Deployment Number"))
        self.pushButton_3.setText(_translate("Frame", "Stop Running"))
        self.pushButton_2.setText(_translate("Frame", "Start Running"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Frame", "Accelerometer X"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("Frame", "Accelerometer Y"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("Frame", "Accelerometer Z"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("Frame", "Magnetometer X"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("Frame", "Magnetometer Y"))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(_translate("Frame", "Magnetometer Z"))
        item = self.tableWidget.verticalHeaderItem(6)
        item.setText(_translate("Frame", "Temperature"))
        item = self.tableWidget.verticalHeaderItem(7)
        item.setText(_translate("Frame", "Battery"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Frame", "Sensor"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Frame", "Enabled"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Frame", "Value"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("Frame", "Accelerometer X"))
        item = self.tableWidget.item(1, 0)
        item.setText(_translate("Frame", "Accelerometer Y"))
        item = self.tableWidget.item(2, 0)
        item.setText(_translate("Frame", "Accelerometer Z"))
        item = self.tableWidget.item(3, 0)
        item.setText(_translate("Frame", "Magnetometer X"))
        item = self.tableWidget.item(4, 0)
        item.setText(_translate("Frame", "Magnetometer Y"))
        item = self.tableWidget.item(5, 0)
        item.setText(_translate("Frame", "Magnetometer Z"))
        item = self.tableWidget.item(6, 0)
        item.setText(_translate("Frame", "Temperature"))
        item = self.tableWidget.item(7, 0)
        item.setText(_translate("Frame", "Battery"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)

from . import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())
