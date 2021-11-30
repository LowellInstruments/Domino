# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer_files/setup.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
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
        self.gridLayout = QtWidgets.QGridLayout(Frame)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_5 = QtWidgets.QGroupBox(Frame)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.label_description = QtWidgets.QLabel(self.groupBox_5)
        self.label_description.setWordWrap(True)
        self.label_description.setObjectName("label_description")
        self.gridLayout_8.addWidget(self.label_description, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_5, 5, 0, 1, 2)
        self.groupBox_3 = QtWidgets.QGroupBox(Frame)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.comboBox_start_time = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_start_time.setObjectName("comboBox_start_time")
        self.comboBox_start_time.addItem("")
        self.comboBox_start_time.addItem("")
        self.comboBox_start_time.addItem("")
        self.comboBox_start_time.addItem("")
        self.comboBox_start_time.addItem("")
        self.gridLayout_6.addWidget(self.comboBox_start_time, 0, 0, 1, 1)
        self.dateTimeEdit_start_time = QtWidgets.QDateTimeEdit(self.groupBox_3)
        self.dateTimeEdit_start_time.setEnabled(True)
        self.dateTimeEdit_start_time.setCalendarPopup(True)
        self.dateTimeEdit_start_time.setObjectName("dateTimeEdit_start_time")
        self.gridLayout_6.addWidget(self.dateTimeEdit_start_time, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_3, 4, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_save = QtWidgets.QPushButton(Frame)
        self.pushButton_save.setMinimumSize(QtCore.QSize(125, 0))
        self.pushButton_save.setObjectName("pushButton_save")
        self.horizontalLayout_2.addWidget(self.pushButton_save)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout_2, 6, 0, 1, 2)
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
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem2, 5, 0, 1, 1)
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
        self.gridLayout.addWidget(self.groupBox_2, 2, 1, 2, 1)
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
        self.gridLayout.addWidget(self.groupBox_4, 4, 1, 1, 1)
        self.groupBox_7 = QtWidgets.QGroupBox(Frame)
        self.groupBox_7.setObjectName("groupBox_7")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_7)
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBox_led = QtWidgets.QCheckBox(self.groupBox_7)
        self.checkBox_led.setChecked(True)
        self.checkBox_led.setObjectName("checkBox_led")
        self.verticalLayout.addWidget(self.checkBox_led)
        self.gridLayout.addWidget(self.groupBox_7, 3, 0, 1, 1)
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
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.gridLayout.addWidget(self.groupBox_6, 1, 0, 1, 2)
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
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem4, 2, 0, 1, 1)
        self.checkBox_temperature = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_temperature.setChecked(True)
        self.checkBox_temperature.setObjectName("checkBox_temperature")
        self.gridLayout_4.addWidget(self.checkBox_temperature, 0, 0, 1, 2)
        self.gridLayout_4.setColumnStretch(0, 1)
        self.gridLayout_4.setColumnStretch(1, 1)
        self.gridLayout.addWidget(self.groupBox, 2, 0, 1, 1)
        self.groupBox_8 = QtWidgets.QGroupBox(Frame)
        self.groupBox_8.setObjectName("groupBox_8")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_8)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.pushButton_unlock = QtWidgets.QPushButton(self.groupBox_8)
        self.pushButton_unlock.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/icons8-padlock-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_unlock.setIcon(icon)
        self.pushButton_unlock.setIconSize(QtCore.QSize(24, 24))
        self.pushButton_unlock.setFlat(True)
        self.pushButton_unlock.setObjectName("pushButton_unlock")
        self.horizontalLayout_6.addWidget(self.pushButton_unlock)
        self.pushButton_save_2 = QtWidgets.QPushButton(self.groupBox_8)
        self.pushButton_save_2.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/icons8-save-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_save_2.setIcon(icon1)
        self.pushButton_save_2.setIconSize(QtCore.QSize(24, 24))
        self.pushButton_save_2.setFlat(True)
        self.pushButton_save_2.setObjectName("pushButton_save_2")
        self.horizontalLayout_6.addWidget(self.pushButton_save_2)
        self.pushButton_delete = QtWidgets.QPushButton(self.groupBox_8)
        self.pushButton_delete.setWhatsThis("")
        self.pushButton_delete.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/icons8-delete-bin-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_delete.setIcon(icon2)
        self.pushButton_delete.setIconSize(QtCore.QSize(24, 24))
        self.pushButton_delete.setFlat(True)
        self.pushButton_delete.setObjectName("pushButton_delete")
        self.horizontalLayout_6.addWidget(self.pushButton_delete)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem5)
        self.gridLayout_2.addLayout(self.horizontalLayout_6, 0, 1, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.comboBox = QtWidgets.QComboBox(self.groupBox_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout_5.addWidget(self.comboBox)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_8)
        self.lineEdit.setEnabled(True)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 1, 0, 1, 2)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 1)
        self.gridLayout.addWidget(self.groupBox_8, 0, 0, 1, 2)
        self.label_5.setBuddy(self.comboBox_temp_interval)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.groupBox_5.setTitle(_translate("Frame", "Summary"))
        self.label_description.setText(_translate("Frame", "Sample temperature every 60 seconds. Sample Accelerometer and Magnetomer at 16 Hz for 10 seconds every 60 seconds. "))
        self.groupBox_3.setTitle(_translate("Frame", "Start Time"))
        self.comboBox_start_time.setItemText(0, _translate("Frame", "Start Recording Immediately"))
        self.comboBox_start_time.setItemText(1, _translate("Frame", "Start on Next Minute"))
        self.comboBox_start_time.setItemText(2, _translate("Frame", "Start on Next Quarter Hour"))
        self.comboBox_start_time.setItemText(3, _translate("Frame", "Start on Next Hour"))
        self.comboBox_start_time.setItemText(4, _translate("Frame", "Start at Time (year-month-day hours:minutes:seconds)"))
        self.dateTimeEdit_start_time.setDisplayFormat(_translate("Frame", "yyyy-MM-dd HH:mm:ss"))
        self.pushButton_save.setText(_translate("Frame", "Save Setup File"))
        self.groupBox_2.setTitle(_translate("Frame", "Accelerometer/Magnetometer"))
        self.checkBox_accelerometer.setText(_translate("Frame", "Accelerometer"))
        self.label_6.setText(_translate("Frame", "Burst Rate:"))
        self.label_7.setText(_translate("Frame", "Burst Interval:"))
        self.checkBox_magnetometer.setText(_translate("Frame", "Magnetometer"))
        self.label_8.setText(_translate("Frame", "Burst Duration (seconds):"))
        self.checkBox_continuous.setText(_translate("Frame", "Continuous"))
        self.groupBox_4.setTitle(_translate("Frame", "Stop Time"))
        self.comboBox_end_time.setItemText(0, _translate("Frame", "Record Until Stopped"))
        self.comboBox_end_time.setItemText(1, _translate("Frame", "Stop at Time (year-month-day hours:minutes:seconds)"))
        self.dateTimeEdit_end_time.setDisplayFormat(_translate("Frame", "yyyy-MM-dd HH:mm:ss"))
        self.groupBox_7.setTitle(_translate("Frame", "Operational Indicator"))
        self.checkBox_led.setText(_translate("Frame", "Blink LED when running"))
        self.groupBox_6.setTitle(_translate("Frame", "Data Filename (appended to serial number)"))
        self.lineEdit_file_name.setToolTip(_translate("Frame", "Allowable characters: Upper/lower case letters, digits, space, hyphen, underscore"))
        self.groupBox.setTitle(_translate("Frame", "Temperature"))
        self.label_5.setText(_translate("Frame", "Sampling Interval:"))
        self.checkBox_temperature.setText(_translate("Frame", "Temperature"))
        self.groupBox_8.setTitle(_translate("Frame", "Presets"))
        self.pushButton_unlock.setToolTip(_translate("Frame", "Duplicate and edit this preset"))
        self.pushButton_save_2.setToolTip(_translate("Frame", "Save as custom presets"))
        self.pushButton_delete.setToolTip(_translate("Frame", "Delete this custom preset"))
        self.comboBox.setItemText(0, _translate("Frame", "Current meter - Typical"))
        self.comboBox.setItemText(1, _translate("Frame", "Current meter - Swells"))
        self.comboBox.setItemText(2, _translate("Frame", "Continuous - Low Rate"))
        self.comboBox.setItemText(3, _translate("Frame", "Continuous - High Rate"))
        self.lineEdit.setToolTip(_translate("Frame", "Description of preset"))
        self.lineEdit.setText(_translate("Frame", "Commonly used settings for current meters in most environments. 12 month battery life"))
from . import icons_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())
