import sys

from clinic.controller import Controller
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from clinic.gui.patient_options_gui import PatientOptionsGui

class SearchPatientGUI(QWidget):
    def __init__(self, controller: Controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.options_window = PatientOptionsGui(self.controller, self)
        #self.current_patient = None

        layout1 = QGridLayout()

         # Adding all the boxes to search patient
        phn_label = QLabel("PHN")
        self.phn_text = QLineEdit()

        # Adding the labels and item to the layout
        layout1.addWidget(phn_label, 0, 0)
        layout1.addWidget(self.phn_text, 0, 1)

        # Adding the buttons
        self.search_button = QPushButton("Search")
        self.back_button = QPushButton("Back")

        # Adding the buttons to the layout
        layout1.addWidget(self.search_button, 1, 0)
        layout1.addWidget(self.back_button, 1, 1)

        # Connecting the button to it's method
        self.search_button.clicked.connect(self.search_button_clicked)
        self.back_button.clicked.connect(self.back_button_clicked)
        self.setLayout(layout1)
    
    def search_button_clicked(self):
        try:
            searched_phn = int(self.phn_text.text())
            patient_found = self.controller.search_patient(searched_phn)
            #self.options_window = PatientOptionsGUI(self.controller, self, patient_found)
            if (patient_found):
                #self.current_patient = patient_found
                QMessageBox.information(self, "Patient Info", str(patient_found))
                self.show_patient_requested(patient_found)
    
            else:
                QMessageBox.warning(self.parent, "Invalid", "This patient does not exist")
                self.phn_text.setText("")
        except:
            QMessageBox.warning(self.parent, "Illegal input", "Please input a valid phn number")
            self.phn_text.setText("")
    
    def show_patient_requested(self, patint_foun):
        #current_patient_phn = self.current_patient.get_phn()
        self.options_window.show_patient(patint_foun.phn)
        self.options_window.show()

    def back_button_clicked(self):
        self.parent.activate_menu_tab()
