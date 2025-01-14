import sys

from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

from clinic.controller import Controller
from clinic.patient import Patient
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.gui.notes_gui import NotesGUI
from clinic.gui.update_patient_gui import UpdatePatientGUI

class PatientOptionsGui(QWidget):
    def __init__(self, controller: Controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        #self.current_patient = None
        self.current_phn = None
        self.update_window = UpdatePatientGUI(self.controller, self, None)

        layout1 = QGridLayout()

        # Adding all the boxes for patient's information
        phn_label = QLabel("PHN")
        self.phn_text = QLineEdit()
        #self.phn_text.setInputMask("0000000000")
        
        name_label = QLabel("Patient's Name")
        self.name_text = QLineEdit()

        bd_label = QLabel("Birthdate")
        self.bd_text = QLineEdit()

        phone_label = QLabel("Phone Number")
        self.phone_text = QLineEdit()

        email_label = QLabel("Email Address")
        self.email_text = QLineEdit()

        address_label = QLabel("Address")
        self.address_text = QLineEdit()

        # Adding the gridbox for the patient field
        layout1.addWidget(phn_label, 0, 0)
        layout1.addWidget(self.phn_text, 0 ,1)
        layout1.addWidget(name_label, 1, 0)
        layout1.addWidget(self.name_text, 1, 1)
        layout1.addWidget(bd_label, 2, 0)
        layout1.addWidget(self.bd_text, 2, 1)
        layout1.addWidget(phone_label, 3, 0)
        layout1.addWidget(self.phone_text, 3, 1)
        layout1.addWidget(email_label, 4, 0)
        layout1.addWidget(self.email_text, 4, 1)
        layout1.addWidget(address_label, 5, 0)
        layout1.addWidget(self.address_text, 5, 1)

        # The buttons layout
        layout2 = QHBoxLayout()

        self.update_button = QPushButton("Update")
        self.delete_button = QPushButton("Delete")
        self.start_appoint_button = QPushButton("Start Appointment")
        layout2.addWidget(self.update_button)
        layout2.addWidget(self.delete_button)
        layout2.addWidget(self.start_appoint_button)

        layout3 = QVBoxLayout()

        top_widget = QWidget()
        top_widget.setLayout(layout1)

        bottom_widget = QWidget()
        bottom_widget.setLayout(layout2)

        layout3.addWidget(top_widget)
        layout3.addWidget(bottom_widget)

        self.setLayout(layout3)

        # Define widget's initial state, first for the Patient's info field and then the buttons
        self.phn_text.setEnabled(True)
        self.name_text.setEnabled(True)
        self.bd_text.setEnabled(True)
        self.phone_text.setEnabled(True)
        self.email_text.setEnabled(True)
        self.address_text.setEnabled(True)

        self.update_button.setEnabled(True)
        self.delete_button.setEnabled(True)
        self.start_appoint_button.setEnabled(True)

        # Handle text change to enable the update button 
        self.phn_text.textChanged.connect(self.patient_text_changed)
        self.name_text.textChanged.connect(self.patient_text_changed)
        self.bd_text.textChanged.connect(self.patient_text_changed)
        self.phone_text.textChanged.connect(self.patient_text_changed)
        self.email_text.textChanged.connect(self.patient_text_changed)
        self.address_text.textChanged.connect(self.patient_text_changed)

        # Connect the buttons clicked signals to the slots/functions below
        self.update_button.clicked.connect(self.update_button_clicked)
        self.delete_button.clicked.connect(self.delete_button_clicked)
        self.start_appoint_button.clicked.connect(self.start_appoint_button_clicked)
    
    def patient_text_changed(self):
        if self.phn_text.text() and self.name_text.text() and self.bd_text.text() \
            and self.phone_text.text() and self.email_text.text() and self.address_text.text():
            self.update_button.setEnabled(True)
        else:
            self.update_button.setEnabled(False)

    def show_patient(self, searched_phn: int):
        patient_found = self.controller.search_patient(searched_phn)
        if (patient_found):
            self.phn_text.setText(str(patient_found.phn))
            #self.current_patient = self.controller.set_current_patient(int(self.phn_text.text()))
            self.current_phn = int(self.phn_text.text())
            self.name_text.setText(patient_found.name)
            self.bd_text.setText(patient_found.birth_date)
            self.phone_text.setText(patient_found.phone)
            self.email_text.setText(patient_found.email)
            self.address_text.setText(patient_found.address)
        else:
            QMessageBox.warning(self.parent, "No Patient", "No Patient with this PHN exist")

    def update_button_clicked(self):
        #self.update_window = UpdatePatientGUI(self.controller, self, self.current_phn)
        if self.update_window.isVisible():
            self.retrieve_patient_window.hide()
        else:
            self.update_window.show()
    def delete_button_clicked(self):
        """
        This function deletes a patient from the 
        collection
        """
        try:
            searched_phn = int(self.phn_text.text())
            self.controller.delete_patient(searched_phn)
            QMessageBox.information(self.parent, "Deleted", "You have deleted this patient")
            self.parent.parent.activate_menu_tab()
        except IllegalOperationException:
            QMessageBox.warning(self.parent, "Illegal Operation", "Please provide a valid PHN")

    def start_appoint_button_clicked(self):
        self.note_window = NotesGUI(self.controller, self)  # Pass self as the parent
        self.note_window.show()