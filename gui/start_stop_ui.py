# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer_files/start_stop.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(782, 512)
        Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.gridLayout_3 = QtWidgets.QGridLayout(Frame)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.frame_2 = QtWidgets.QFrame(Frame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_status = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_status.setFont(font)
        self.label_status.setWordWrap(True)
        self.label_status.setObjectName("label_status")
        self.gridLayout_2.addWidget(self.label_status, 1, 1, 1, 1)
        self.label_connected = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_connected.setFont(font)
        self.label_connected.setObjectName("label_connected")
        self.gridLayout_2.addWidget(self.label_connected, 0, 1, 1, 1)
        self.pushButton_connected = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_connected.setMaximumSize(QtCore.QSize(50, 50))
        self.pushButton_connected.setText("")
        self.pushButton_connected.setIconSize(QtCore.QSize(48, 48))
        self.pushButton_connected.setFlat(True)
        self.pushButton_connected.setObjectName("pushButton_connected")
        self.gridLayout_2.addWidget(self.pushButton_connected, 0, 0, 1, 1)
        self.pushButton_status = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_status.setMaximumSize(QtCore.QSize(50, 50))
        self.pushButton_status.setText("")
        self.pushButton_status.setIconSize(QtCore.QSize(48, 48))
        self.pushButton_status.setFlat(True)
        self.pushButton_status.setObjectName("pushButton_status")
        self.gridLayout_2.addWidget(self.pushButton_status, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.line_3 = QtWidgets.QFrame(self.frame_2)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.label_file_size = QtWidgets.QLabel(self.frame_2)
        self.label_file_size.setObjectName("label_file_size")
        self.verticalLayout.addWidget(self.label_file_size)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_sd_free_space = QtWidgets.QLabel(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_sd_free_space.sizePolicy().hasHeightForWidth())
        self.label_sd_free_space.setSizePolicy(sizePolicy)
        self.label_sd_free_space.setLineWidth(0)
        self.label_sd_free_space.setObjectName("label_sd_free_space")
        self.horizontalLayout_4.addWidget(self.label_sd_free_space)
        self.label_sd_total_space = QtWidgets.QLabel(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_sd_total_space.sizePolicy().hasHeightForWidth())
        self.label_sd_total_space.setSizePolicy(sizePolicy)
        self.label_sd_total_space.setLineWidth(0)
        self.label_sd_total_space.setObjectName("label_sd_total_space")
        self.horizontalLayout_4.addWidget(self.label_sd_total_space)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_logger_time = QtWidgets.QLabel(self.frame_2)
        self.label_logger_time.setObjectName("label_logger_time")
        self.horizontalLayout_3.addWidget(self.label_logger_time)
        self.pushButton_sync_clock = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_sync_clock.setObjectName("pushButton_sync_clock")
        self.horizontalLayout_3.addWidget(self.pushButton_sync_clock)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.label_computer_time = QtWidgets.QLabel(self.frame_2)
        self.label_computer_time.setObjectName("label_computer_time")
        self.verticalLayout.addWidget(self.label_computer_time)
        self.line = QtWidgets.QFrame(self.frame_2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.label_serial = QtWidgets.QLabel(self.frame_2)
        self.label_serial.setObjectName("label_serial")
        self.verticalLayout.addWidget(self.label_serial)
        self.label_firmware = QtWidgets.QLabel(self.frame_2)
        self.label_firmware.setObjectName("label_firmware")
        self.verticalLayout.addWidget(self.label_firmware)
        self.label_model = QtWidgets.QLabel(self.frame_2)
        self.label_model.setObjectName("label_model")
        self.verticalLayout.addWidget(self.label_model)
        self.label_deployment = QtWidgets.QLabel(self.frame_2)
        self.label_deployment.setObjectName("label_deployment")
        self.verticalLayout.addWidget(self.label_deployment)
        self.line_2 = QtWidgets.QFrame(self.frame_2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_stop = QtWidgets.QPushButton(self.frame_2)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/icons8-stop-sign-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_stop.setIcon(icon)
        self.pushButton_stop.setIconSize(QtCore.QSize(36, 36))
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.horizontalLayout_2.addWidget(self.pushButton_stop)
        self.pushButton_start = QtWidgets.QPushButton(self.frame_2)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/icons8-go-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_start.setIcon(icon1)
        self.pushButton_start.setIconSize(QtCore.QSize(36, 36))
        self.pushButton_start.setObjectName("pushButton_start")
        self.horizontalLayout_2.addWidget(self.pushButton_start)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout_3.addWidget(self.frame_2, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_table = QtWidgets.QLabel(Frame)
        self.label_table.setObjectName("label_table")
        self.verticalLayout_2.addWidget(self.label_table)
        self.tableWidget = QtWidgets.QTableWidget(Frame)
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget.setAutoScroll(False)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setCornerButtonEnabled(False)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(9)
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
        self.tableWidget.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tableWidget.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tableWidget.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(2, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tableWidget.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(3, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(3, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tableWidget.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(4, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(4, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tableWidget.setItem(5, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(5, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(5, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tableWidget.setItem(6, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(6, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(6, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(7, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tableWidget.setItem(8, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(8, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(8, 2, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(22)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.groupBox = QtWidgets.QGroupBox(Frame)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.labelLoggerSettings = QtWidgets.QLabel(self.groupBox)
        self.labelLoggerSettings.setWordWrap(True)
        self.labelLoggerSettings.setObjectName("labelLoggerSettings")
        self.gridLayout.addWidget(self.labelLoggerSettings, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        self.gridLayout_3.setColumnStretch(0, 1)
        self.gridLayout_3.setColumnStretch(1, 1)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.label_status.setText(_translate("Frame", "Halted"))
        self.label_connected.setText(_translate("Frame", "Not Connected"))
        self.label_file_size.setText(_translate("Frame", "File Size: 487.65 MB"))
        self.label_sd_free_space.setText(_translate("Frame", "SD Card Usage: 0 "))
        self.label_sd_total_space.setText(_translate("Frame", "of 0 GB Available"))
        self.label_logger_time.setText(_translate("Frame", "Device Time: 2018-10-02 11:10:05"))
        self.pushButton_sync_clock.setToolTip(_translate("Frame", "Syncs the device clock to computer clock"))
        self.pushButton_sync_clock.setText(_translate("Frame", "Set Device Clock"))
        self.label_computer_time.setText(_translate("Frame", "Computer Time: 2018-10-02 11:10:17"))
        self.label_serial.setText(_translate("Frame", "Serial Number:"))
        self.label_firmware.setText(_translate("Frame", "Firmware Version:"))
        self.label_model.setText(_translate("Frame", "Model Number:"))
        self.label_deployment.setText(_translate("Frame", "Deployment Number:"))
        self.pushButton_stop.setText(_translate("Frame", "Stop Running"))
        self.pushButton_start.setText(_translate("Frame", "Start Running"))
        self.label_table.setText(_translate("Frame", "Real-time Data"))
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
        item.setText(_translate("Frame", "Pressure"))
        item = self.tableWidget.verticalHeaderItem(8)
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
        item.setText(_translate("Frame", "Accelerometer X (g)"))
        item = self.tableWidget.item(1, 0)
        item.setText(_translate("Frame", "Accelerometer Y (g)"))
        item = self.tableWidget.item(2, 0)
        item.setText(_translate("Frame", "Accelerometer Z (g)"))
        item = self.tableWidget.item(3, 0)
        item.setText(_translate("Frame", "Magnetometer X (mG)"))
        item = self.tableWidget.item(4, 0)
        item.setText(_translate("Frame", "Magnetometer Y (mG)"))
        item = self.tableWidget.item(5, 0)
        item.setText(_translate("Frame", "Magnetometer Z (mG)"))
        item = self.tableWidget.item(6, 0)
        item.setText(_translate("Frame", "Temperature (°C)"))
        item = self.tableWidget.item(7, 0)
        item.setText(_translate("Frame", "Pressure (dbar)"))
        item = self.tableWidget.item(8, 0)
        item.setText(_translate("Frame", "Battery (V)"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.groupBox.setTitle(_translate("Frame", "Current Logger Settings"))
        self.labelLoggerSettings.setText(_translate("Frame", "Sample temperature every 60 seconds. Sample Accelerometer and Magnetomer at 16 Hz for 10 seconds every 60 seconds. "))
from . import icons_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())
