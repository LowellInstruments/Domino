from PyQt5.QtWidgets import QDialog
from gui.options_ui import Ui_Dialog
from mat import appdata


class OptionsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle('File Output Options')
        self.ui.pushButton_save.clicked.connect(self.save)
        self.ui.pushButton_cancel.clicked.connect(self.cancel)
        self.button_mapping = {'radioButton_iso8601_time': 'iso8601',
                               'radioButton_legacy_time': 'legacy',
                               'radioButton_elapsed_time': 'elapsed',
                               'radioButton_posix_time': 'posix',
                               'iso8601': 'radioButton_iso8601_time',
                               'legacy': 'radioButton_legacy_time',
                               'elapsed': 'radioButton_elapsed_time',
                               'posix': 'radioButton_posix_time'}
        self.load_saved()

    def load_saved(self):
        application_data = appdata.get_userdata('converter-1.dat')
        time_format = application_data.get('time_format', 'iso8601')
        time_format_button_name = self.button_mapping[time_format]
        getattr(self.ui, time_format_button_name).setChecked(True)
        self.ui.checkBox_average_bursts.setChecked(application_data.get(
            'average_bursts', True))
        self.ui.checkBox_declination.setChecked(application_data.get(
            'is_declination', True))
        self.ui.lineEdit_declination.setText(application_data.get(
            'declination', '0'))

    def save(self):
        button_name = self.ui.buttonGroup.checkedButton().objectName()
        appdata.set_userdata('converter-1.dat',
                             'time_format',
                             self.button_mapping[button_name])
        appdata.set_userdata('converter-1.dat',
                             'average_bursts',
                             self.ui.checkBox_average_bursts.isChecked())
        appdata.set_userdata('converter-1.dat',
                             'is_declination',
                             self.ui.checkBox_declination.isChecked())
        appdata.set_userdata('converter-1.dat',
                             'declination',
                             self.ui.lineEdit_declination.text())
        self.hide()

    def cancel(self):
        self.close()
