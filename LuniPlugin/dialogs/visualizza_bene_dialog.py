import os

from PyQt5 import uic
from PyQt5 import QtWidgets

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'visualizza_bene_dialog.ui'))


class VisualizzaBeneDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(VisualizzaBeneDialog, self).__init__(parent)
        self.setupUi(self)