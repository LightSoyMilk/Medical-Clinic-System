import sys
from PyQt6.QtCore import Qt, QAbstractTableModel

from clinic.controller import Controller
from clinic.patient import Patient

class PatientTableModel(QAbstractTableModel):
    def __init__(self, controller: Controller):
        super().__init__()
        self.controller = controller
        self._data = []
    
    def refresh_data(self):
        """
        This function creates a table model with the 
        existing patient data
        """
        self._data = []
        # Getting the list of patients
        lop = self.controller.list_patients()
        for patient in lop:
            row = [patient.phn, patient.name, patient.birth_date, patient.phone, \
                   patient.email, patient.address]
            self._data.append(row)

        # emitting the layoutChanged signal to alert the QTableView of model changes
        self.layoutChanged.emit()

    def refresh_retrieve_data(self, searched_name: str):
        """
        This function refreshes the table model with
        all the patients containing the searched_name string
        """
        self._data = []
        # Retrieving the filtered list of patients
        lop = self.controller.retrieve_patients(searched_name)
        for patient in lop:
            row = [patient.phn, patient.name, patient.birth_date, patient.phone, \
                   patient.email, patient.address]
            self._data.append(row)

        # emitting the layoutChanged signal to alert the QTableView of model changes
        self.layoutChanged.emit()
        
    def reset(self):
        self._data = []
        # emitting the layoutChanged signal to alert the QTableView of model changes
        self.layoutChanged.emit()

    def data(self, index, role):
        value = self._data[index.row()][index.column()]

        if role == Qt.ItemDataRole.DisplayRole:
            # Perform per-type checks and render accordingly.
            if isinstance(value, float):
                # Render float to 2 dp
                return "%.2f" % value
            if isinstance(value, str):
                # Render strings with quotes
                return '%s' % value
            # Default (anything not captured above: e.g. int)
            return value

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if isinstance(value, int) or isinstance(value, float):
                # Align right, vertical middle.
                return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        if self._data:
            return len(self._data[0])
        else:
            return 0

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        headers = ['PHN', 'Name', 'Birthdate', 'Phone Number', 'Email Address', 'Address']
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return '%s' % headers[section]
        return super().headerData(section, orientation, role)