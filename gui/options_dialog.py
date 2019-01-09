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
                               'radioButton_csv': 'csv',
                               'radioButton_hdf5': 'hdf5',
                               'iso8601': 'radioButton_iso8601_time',
                               'legacy': 'radioButton_legacy_time',
                               'elapsed': 'radioButton_elapsed_time',
                               'posix': 'radioButton_posix_time',
                               'csv': 'radioButton_csv',
                               'hdf5': 'radioButton_hdf5'}
        self.load_saved()

    def load_saved(self):
        application_data = appdata.get_userdata('domino.dat')
        time_format = application_data.get('time_format', 'iso8601')
        time_format_button_name = self.button_mapping[time_format]
        getattr(self.ui, time_format_button_name).setChecked(True)
        self.ui.checkBox_average_bursts.setChecked(application_data.get(
            'average_bursts', True))
        output_format = application_data.get('output_format',
                                             'csv')
        output_format_button = self.button_mapping[output_format]
        getattr(self.ui, output_format_button).setChecked(True)
        split_size = application_data.get('split',
                                          'Do not split output files')
        self.ui.comboBox_split.setCurrentText(split_size)

    def save(self):
        button_name = self.ui.buttonGroup.checkedButton().objectName()
        appdata.set_userdata('domino.dat',
                             'time_format',
                             self.button_mapping[button_name])
        appdata.set_userdata('domino.dat',
                             'average_bursts',
                             self.ui.checkBox_average_bursts.isChecked())
        output_button = \
            self.ui.buttonGroup_output_format.checkedButton().objectName()
        appdata.set_userdata('domino.dat',
                             'output_format',
                             self.button_mapping[output_button])
        appdata.set_userdata('domino.dat',
                             'split',
                             self.ui.comboBox_split.currentText())
        self.hide()

    def cancel(self):
        self.close()
