# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer_files/setup.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(782, 493)
        Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.gridLayout = QtWidgets.QGridLayout(Frame)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_6 = QtWidgets.QGroupBox(Frame)
        self.groupBox_6.setObjectName("groupBox_6")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_12 = QtWidgets.QLabel(self.groupBox_6)
        self.label_12.setText("")
        self.label_12.setObjectName("label_12")
        self.horizontalLayout.addWidget(self.label_12)
        self.lineEdit_file_name = QtWidgets.QLineEdit(self.groupBox_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_file_name.sizePolicy().hasHeightForWidth())
        self.lineEdit_file_name.setSizePolicy(sizePolicy)
        self.lineEdit_file_name.setMinimumSize(QtCore.QSize(200, 0))
        self.lineEdit_file_name.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lineEdit_file_name.setObjectName("lineEdit_file_name")
        self.horizontalLayout.addWidget(self.lineEdit_file_name)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addWidget(self.groupBox_6, 0, 0, 1, 2)
        self.groupBox = QtWidgets.QGroupBox(Frame)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_4.setVerticalSpacing(12)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.comboBox_temp_interval = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_temp_interval.setObjectName("comboBox_temp_interval")
        self.gridLayout_4.addWidget(self.comboBox_temp_interval, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem1, 2, 0, 1, 1)
        self.checkBox_temperature = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_temperature.setChecked(True)
        self.checkBox_temperature.setObjectName("checkBox_temperature")
        self.gridLayout_4.addWidget(self.checkBox_temperature, 0, 0, 1, 2)
        self.gridLayout_4.setColumnStretch(0, 1)
        self.gridLayout_4.setColumnStretch(1, 1)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(Frame)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.comboBox_start_time = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_start_time.setObjectName("comboBox_start_time")
        self.comboBox_start_time.addItem("")
        self.comboBox_start_time.addItem("")
        self.gridLayout_6.addWidget(self.comboBox_start_time, 0, 0, 1, 1)
        self.dateTimeEdit_start_time = QtWidgets.QDateTimeEdit(self.groupBox_3)
        self.dateTimeEdit_start_time.setEnabled(True)
        self.dateTimeEdit_start_time.setCalendarPopup(True)
        self.dateTimeEdit_start_time.setObjectName("dateTimeEdit_start_time")
        self.gridLayout_6.addWidget(self.dateTimeEdit_start_time, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_3, 3, 0, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(Frame)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.comboBox_end_time = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox_end_time.setObjectName("comboBox_end_time")
        self.comboBox_end_time.addItem("")
        self.comboBox_end_time.addItem("")
        self.gridLayout_7.addWidget(self.comboBox_end_time, 0, 0, 1, 1)
        self.dateTimeEdit_end_time = QtWidgets.QDateTimeEdit(self.groupBox_4)
        self.dateTimeEdit_end_time.setEnabled(True)
        self.dateTimeEdit_end_time.setCalendarPopup(True)
        self.dateTimeEdit_end_time.setObjectName("dateTimeEdit_end_time")
        self.gridLayout_7.addWidget(self.dateTimeEdit_end_time, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_4, 3, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.pushButton_save = QtWidgets.QPushButton(Frame)
        self.pushButton_save.setMinimumSize(QtCore.QSize(125, 0))
        self.pushButton_save.setObjectName("pushButton_save")
        self.horizontalLayout_2.addWidget(self.pushButton_save)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.gridLayout.addLayout(self.horizontalLayout_2, 5, 0, 1, 2)
        self.groupBox_5 = QtWidgets.QGroupBox(Frame)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.label_description = QtWidgets.QLabel(self.groupBox_5)
        self.label_description.setWordWrap(True)
        self.label_description.setObjectName("label_description")
        self.gridLayout_8.addWidget(self.label_description, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_5, 4, 0, 1, 2)
        self.groupBox_7 = QtWidgets.QGroupBox(Frame)
        self.groupBox_7.setObjectName("groupBox_7")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_7)
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBox_led = QtWidgets.QCheckBox(self.groupBox_7)
        self.checkBox_led.setChecked(True)
        self.checkBox_led.setObjectName("checkBox_led")
        self.verticalLayout.addWidget(self.checkBox_led)
        self.gridLayout.addWidget(self.groupBox_7, 2, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Frame)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_5.setVerticalSpacing(12)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.checkBox_accelerometer = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_accelerometer.setChecked(True)
        self.checkBox_accelerometer.setObjectName("checkBox_accelerometer")
        self.gridLayout_5.addWidget(self.checkBox_accelerometer, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_5.addWidget(self.label_6, 2, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_5.addWidget(self.label_7, 1, 0, 1, 1)
        self.checkBox_magnetometer = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_magnetometer.setChecked(True)
        self.checkBox_magnetometer.setObjectName("checkBox_magnetometer")
        self.gridLayout_5.addWidget(self.checkBox_magnetometer, 0, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setObjectName("label_8")
        self.gridLayout_5.addWidget(self.label_8, 3, 0, 1, 1)
        self.comboBox_orient_interval = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_orient_interval.setObjectName("comboBox_orient_interval")
        self.gridLayout_5.addWidget(self.comboBox_orient_interval, 1, 1, 1, 1)
        self.comboBox_orient_burst_rate = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_orient_burst_rate.setObjectName("comboBox_orient_burst_rate")
        self.gridLayout_5.addWidget(self.comboBox_orient_burst_rate, 2, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem4, 5, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(15)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lineEdit_burst_duration = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_burst_duration.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_burst_duration.sizePolicy().hasHeightForWidth())
        self.lineEdit_burst_duration.setSizePolicy(sizePolicy)
        self.lineEdit_burst_duration.setObjectName("lineEdit_burst_duration")
        self.horizontalLayout_3.addWidget(self.lineEdit_burst_duration)
        self.checkBox_continuous = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_continuous.setObjectName("checkBox_continuous")
        self.horizontalLayout_3.addWidget(self.checkBox_continuous)
        self.gridLayout_5.addLayout(self.horizontalLayout_3, 3, 1, 1, 1)
        self.gridLayout_5.setColumnStretch(0, 1)
        self.gridLayout_5.setColumnStretch(1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 1, 1, 2, 1)
        self.gridLayout.setRowStretch(0, 2)
        self.gridLayout.setRowStretch(1, 4)
        self.gridLayout.setRowStretch(2, 3)
        self.gridLayout.setRowStretch(3, 2)
        self.gridLayout.setRowStretch(4, 1)
        self.label_5.setBuddy(self.comboBox_temp_interval)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.groupBox_6.setTitle(_translate("Frame", "Description"))
        self.groupBox.setTitle(_translate("Frame", "Temperature"))
        self.label_5.setText(_translate("Frame", "Sampling Interval:"))
        self.checkBox_temperature.setText(_translate("Frame", "Temperature"))
        self.groupBox_3.setTitle(_translate("Frame", "Start Time"))
        self.comboBox_start_time.setItemText(0, _translate("Frame", "Start Recording Immediately"))
        self.comboBox_start_time.setItemText(1, _translate("Frame", "Start at Time (year-month-day hours:minutes:seconds)"))
        self.dateTimeEdit_start_time.setDisplayFormat(_translate("Frame", "yyyy-MM-dd HH:mm:ss"))
        self.groupBox_4.setTitle(_translate("Frame", "Stop Time"))
        self.comboBox_end_time.setItemText(0, _translate("Frame", "Record Until Stopped"))
        self.comboBox_end_time.setItemText(1, _translate("Frame", "Stop at Time (year-month-day hours:minutes:seconds)"))
        self.dateTimeEdit_end_time.setDisplayFormat(_translate("Frame", "yyyy-MM-dd HH:mm:ss"))
        self.pushButton_save.setText(_translate("Frame", "Save Setup File"))
        self.groupBox_5.setTitle(_translate("Frame", "Summary"))
        self.label_description.setText(_translate("Frame", "Sample temperature every 60 seconds. Sample Accelerometer and Magnetomer at 16 Hz for 10 seconds every 60 seconds. "))
        self.groupBox_7.setTitle(_translate("Frame", "Operational Indicator"))
        self.checkBox_led.setText(_translate("Frame", "Blink LED when running"))
        self.groupBox_2.setTitle(_translate("Frame", "Accelerometer/Magnetometer"))
        self.checkBox_accelerometer.setText(_translate("Frame", "Accelerometer"))
        self.label_6.setText(_translate("Frame", "Burst Rate:"))
        self.label_7.setText(_translate("Frame", "Burst Interval:"))
        self.checkBox_magnetometer.setText(_translate("Frame", "Magnetometer"))
        self.label_8.setText(_translate("Frame", "Burst Duration (seconds):"))
        self.checkBox_continuous.setText(_translate("Frame", "Continuous"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())
