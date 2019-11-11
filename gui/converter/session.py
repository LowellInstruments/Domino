from PyQt5.QtCore import QSettings


def save_session(gui):
    app_data = {
        'output_type': gui.comboBox_output_type.currentText(),
        'meter_model': gui.comboBox_tilt_tables.currentText(),
        'same_directory': gui.radioButton_output_same.isChecked(),
        'output_directory': gui.lineEdit_output_folder.text(),
        'declination': gui.dec_model.declination_value()
    }
    QSettings().setValue('converter_window', app_data)


def restore_last_session(gui):
    app_data = QSettings().value('converter_window', {}, type=dict)
    output_type = app_data.get('output_type', 'Discrete Channels')
    gui.set_combobox(gui.comboBox_output_type, output_type)
    gui.change_output_type_slot()

    tilt_curve = app_data.get('meter_model', '')
    gui.set_combobox(gui.comboBox_tilt_tables, tilt_curve)

    same_directory = app_data.get('same_directory', True)
    if same_directory:
        gui.radioButton_output_same.setChecked(True)
    else:
        gui.radioButton_output_directory.setChecked(True)
    gui.lineEdit_output_folder.setText(
        app_data.get('output_directory', ''))
    gui.dec_model.declination = app_data.get('declination', 0.0)
    # make sure custom_cal doesn't persist between sessions
    output_options = QSettings().value('output_options')
    if output_options:
        output_options['custom_cal'] = None
        QSettings().setValue('output_options', output_options)
