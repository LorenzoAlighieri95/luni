import os

from PyQt5 import uic
from PyQt5 import QtWidgets

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'select_by_date_dialog.ui'))

class SelectByDateDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(SelectByDateDialog, self).__init__(parent)
        self.setupUi(self)