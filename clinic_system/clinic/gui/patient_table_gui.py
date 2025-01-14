import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PyQt6.QtWidgets import QPushButton, QTableView, QWidget

from clinic.controller import Controller
from clinic.patient import Patient
from clinic.gui.patient_table_model import PatientTableModel

class PatientTableGUI(QWidget):
    def __init__(self, controller: Controller, parent):
        super().__init__()
