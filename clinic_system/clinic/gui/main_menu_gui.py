from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QStackedLayout
from PyQt6.QtWidgets import QGridLayout, QTableView

from clinic.controller import Controller
from clinic.gui.patient_table_model import PatientTableModel
from clinic.gui.notes_gui import NotesGUI
from clinic.gui.retrieve_patient_window import RetrievePatientWindow
from clinic.gui.patient_options_gui import PatientOptionsGui
class MainMenu(QWidget):
    def __init__(self, controller: Controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.retrieve_patient_window = RetrievePatientWindow(self)
        #self.patient_options_gui = PatientOptionsGui(self.controller, self)
        
        layout = QGridLayout()
        self.setMinimumSize(650, 500)

        # Adding the patient table
        self.patient_table = QTableView()
        self.patient_model = PatientTableModel(self.controller)
        self.patient_table.setModel(self.patient_model)

        # Making all the buttons to access the functions of the clinic
        self.add_patient_button = QPushButton("Add Patient")
        self.search_patient_button = QPushButton("Search Patient")
        self.retrieve_patient_button = QPushButton("Retrieve Patients")
        self.list_patients_button = QPushButton("List Patients")
        self.start_appointment_button = QPushButton("Start Appointment")
        self.log_out_button = QPushButton("Logout")

        # Formatting all these buttons and table to the layout
        layout.addWidget(self.patient_table)
        
        layout.addWidget(self.add_patient_button)
        layout.addWidget(self.search_patient_button)
        layout.addWidget(self.retrieve_patient_button)
        layout.addWidget(self.list_patients_button)
        layout.addWidget(self.start_appointment_button)
        layout.addWidget(self.log_out_button) 

        self.setLayout(layout)

        # Connecting the buttons to their respective windows
        self.add_patient_button.clicked.connect(self.add_patient_clicked)
        self.search_patient_button.clicked.connect(self.search_patient_clicked)
        self.retrieve_patient_button.clicked.connect(self.retrieve_patient_button_clicked)
        self.list_patients_button.clicked.connect(self.list_patient_button_clicked)
        self.start_appointment_button.clicked.connect(self.start_appointment_button_clicked)
        self.log_out_button.clicked.connect(self.logout_button_clicked)

        self.patient_table.doubleClicked.connect(self.show_patient_requested)
    
    def add_patient_clicked(self):
        """
        This function takes the user to the add patient tab
        """
        self.parent.activate_add_patient_tab()

    def retrieve_patient_button_clicked(self):
        if self.retrieve_patient_window.isVisible():
            self.retrieve_patient_window.hide()
        else:
            self.retrieve_patient_window.show()

    def list_patient_button_clicked(self):
        self.patient_model.refresh_data()

    def search_patient_clicked(self):
        """
        This function takes the user into the 
        search patient tab
        """
        self.parent.activate_search_patient_tab()

    def show_patient_requested(self):
        # Store the current patient's index when the user select a row
        index = self.patient_table.selectionModel().currentIndex()
        self.current_patient_code = int(index.sibling(index.row(), 0).data())

        self.patient_options_gui.show_patient(self.current_patient_code)
        self.patient_options_gui.show()

    def start_appointment_button_clicked(self):
        self.note_window = NotesGUI(self.controller, self)  # Pass self as the parent
        self.note_window.show()

    def logout_button_clicked(self):
        """
        This function exits the program if the user
        pushes the logout button
        """
        self.parent.controller.logout()
        self.parent.activate_login_tab()