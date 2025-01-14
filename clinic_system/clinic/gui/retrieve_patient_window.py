import sys
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton

class RetrievePatientWindow(QWidget):
    """
    This "window" is a QWidget. It's parent is 
    the main menu "window"
    """
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QGridLayout()

        # Creating tge slot for users to insert the phn number
        label_name = QLabel("Patient Name")
        self.user_name_input = QLineEdit()

        # Creating the buttons for user to retrieve or close window
        self.retrieve_button = QPushButton("Retrieve Patients")

        # Adding the widget to the layout
        layout.addWidget(label_name, 0, 0)
        layout.addWidget(self.user_name_input, 0 ,1)
        layout.addWidget(self.retrieve_button, 1, 0)

        self.setLayout(layout)

        # Setting the initial stage of the button
        self.retrieve_button.setEnabled(False)

        # Handle text change to enable/disable the retrieve button
        self.user_name_input.textChanged.connect(self.patient_text_changed)

        # Connecting the button
        self.retrieve_button.clicked.connect(self.retrieve_button_clicked)

    def patient_text_changed(self):
        if self.user_name_input.text():
            self.retrieve_button.setEnabled(True)
        else:
            self.retrieve_button.setEnabled(False)

    def retrieve_button_clicked(self):
        searched_name = self.user_name_input.text()
        self.user_name_input.setText("")
        self.parent.patient_model.refresh_retrieve_data(searched_name)
        self.close()