from PyQt5.QtWidgets import QDialog
from gui.progress_ui import Ui_Dialog
from time import sleep


class ProgressDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle('File Conversion Progress')
        self.ui.label_status.setText('')

    def update_progress(self, percent, overall_percent):
        self.ui.progressBar_file.setValue(percent)
        self.ui.progressBar_total.setValue(overall_percent)
        if percent == 100:
            sleep(0.5)

    def update_status(self, filename, i, total_files):
        self.ui.progressBar_file.setValue(0)
        self.ui.label_status.setText(
            'Converting {} - File {} of {}'.format(filename, i, total_files))

    def conversion_complete(self):
        self.close()

    def click_cancel(self):
        self.ui.label_status.setText('Canceling conversion...')
        self.ui.pushButton.setEnabled(False)
