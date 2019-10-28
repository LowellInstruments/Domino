from mat import appdata


def save_session(gui):
    appdata.set_userdata('domino.dat',
                         'output_type',
                         gui.comboBox_output_type.currentText())
    appdata.set_userdata('domino.dat',
                         'meter_model',
                         gui.comboBox_tilt_tables.currentText())
    appdata.set_userdata('domino.dat',
                         'same_directory',
                         gui.radioButton_output_same.isChecked())
    appdata.set_userdata('domino.dat',
                         'output_directory',
                         gui.lineEdit_output_folder.text())

    appdata.set_userdata('domino.dat', 'declination', gui._declination())


def restore_last_session(gui):
    app_data = appdata.get_userdata('domino.dat')
    output_type = app_data.get('output_type', 'Discrete Channels')
    gui.set_combobox(gui.comboBox_output_type, output_type)

    tilt_curve = app_data.get('meter_model', '')
    gui.set_combobox(gui.comboBox_tilt_tables, tilt_curve)

    same_directory = app_data.get('same_directory', True)
    if same_directory:
        gui.radioButton_output_same.setChecked(True)
    else:
        gui.radioButton_output_directory.setChecked(True)
    gui.lineEdit_output_folder.setText(
        app_data.get('output_directory', ''))
    gui.dec_model.declination = str(app_data.get('declination', 0.0))
    appdata.set_userdata('domino.dat', 'custom_cal', None)
