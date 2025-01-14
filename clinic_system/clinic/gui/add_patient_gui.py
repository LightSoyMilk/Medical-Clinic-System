import sys

from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

from clinic.controller import Controller
from clinic.exception.illegal_operation_exception import IllegalOperationException

class AddPatientGUI(QWidget):
    def __init__(self, controller: Controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent

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

        self.clear_button = QPushButton("Clear")
        self.add_button = QPushButton("Add")
        self.close_button = QPushButton("Close")
        layout2.addWidget(self.clear_button)
        layout2.addWidget(self.add_button)
        layout2.addWidget(self.close_button)

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

        self.clear_button.setEnabled(True)
        self.add_button.setEnabled(False)
        self.close_button.setEnabled(True)

        # Handle text change to enable/disable the create/add button 
        self.phn_text.textChanged.connect(self.patient_text_changed)
        self.name_text.textChanged.connect(self.patient_text_changed)
        self.bd_text.textChanged.connect(self.patient_text_changed)
        self.phone_text.textChanged.connect(self.patient_text_changed)
        self.email_text.textChanged.connect(self.patient_text_changed)
        self.address_text.textChanged.connect(self.patient_text_changed)

        # Connect the buttons clicked signals to the slots/functions below
        self.clear_button.clicked.connect(self.clear_button_clicked)
        self.add_button.clicked.connect(self.add_button_clicked)
        self.close_button.clicked.connect(self.close_button_clicked)
    
    def patient_text_changed(self):
        if self.phn_text.text() and self.name_text.text() and self.bd_text.text() \
            and self.phone_text.text() and self.email_text.text() and self.address_text.text():
            self.add_button.setEnabled(True)
        else:
            self.add_button.setEnabled(False)

    def clear_button_clicked(self):
        """
        This function clears all the field for Patient's info
        """
        self.phn_text.setText("")
        self.name_text.setText("")
        self.bd_text.setText("")
        self.phone_text.setText("")
        self.email_text.setText("")
        self.address_text.setText("")

    def add_button_clicked(self):
        """
        This function adds a patient with all the given information given 
        to the collection
        """
        try:
            # Getting all the field the user inputted and converting them to the right type
            phn = int(self.phn_text.text())
            name = self.name_text.text()
            birth_date = self.bd_text.text()
            phone = self.phone_text.text()
            email = self.email_text.text()
            address = self.address_text.text()

            # Creating the patient and telling the user if they were successful or not which then closes the 
            # and go back to the main menu
            new_patient = self.controller.create_patient(phn, name, birth_date, phone, email, address)
            QMessageBox.information(self.parent, "Success", "You have created a new Patient")
            self.close_button_clicked()
        except IllegalOperationException:
            QMessageBox.warning(self.parent, "Illegal Operation", "Cannot create a patient with an existing PHN")
            self.clear_button_clicked()

    def close_button_clicked(self):
        """
        This function clears all the text field and close the 
        add patient tab and take us back to main menu
        """
        self.clear_button_clicked()
        self.parent.activate_menu_tab()