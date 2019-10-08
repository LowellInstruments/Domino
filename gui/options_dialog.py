from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from gui.options_ui import Ui_Dialog
from mat import appdata
from mat.calibration_factories import make_from_calibration_file


class OptionsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle('File Output Options')
        self.ui.pushButton_save.clicked.connect(self.save)
        self.ui.pushButton_cancel.clicked.connect(self.cancel)
        self.ui.pushButton_browse.clicked.connect(
            self.open_custom_calibration)
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
        self.ui.buttonGroup_calibration.buttonToggled.connect(
            self.calibration_type_changed)
        self.ui.buttonGroup_output_format.buttonToggled.connect(
            self.output_type_changed)
        self.load_saved()

    #PyQt slot
    def output_type_changed(self, val):
        hdf_state = self.ui.radioButton_hdf5.isChecked() is True
        self.ui.comboBox_split.setEnabled(not hdf_state)
        self.ui.label.setEnabled(not hdf_state)
        for button in self.ui.buttonGroup.buttons():
            button.setEnabled(not hdf_state)

    def alert_bad_cal_file(self):
        QMessageBox.warning(self, 'Calibration File Error',
                            'There was an error loading the custom '
                            'calibration file.',
                            QMessageBox.Ok)

    def open_custom_calibration(self):
        file_path = QFileDialog.getOpenFileName(
            self,
            'Open Custom Calibration File',
            '',
            'Custom Calibration File (*.txt)')
        if not file_path[0]:
            return
        try:
            make_from_calibration_file(file_path[0])
            self.ui.lineEdit_custom_cal.setText(file_path[0])
        except ValueError:
            self.alert_bad_cal_file()
            self.ui.lineEdit_custom_cal.setText('')
            self.ui.radioButton_factory_cal.setChecked(True)

    # PyQt slot
    def calibration_type_changed(self):
        state = self.ui.radioButton_custom_cal.isChecked()
        self.ui.lineEdit_custom_cal.setEnabled(state)
        self.ui.pushButton_browse.setEnabled(state)

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
        # calibration = application_data.get('custom_cal', None)
        # if calibration:
        #     self.ui.radioButton_custom_cal.setChecked(True)
        #     self.ui.lineEdit_custom_cal.setText(calibration)

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
        # appdata.set_userdata('domino.dat',
        #                      'custom_cal',
        #                      self.ui.lineEdit_custom_cal.text())
        self.hide()

    def cancel(self):
        self.close()
