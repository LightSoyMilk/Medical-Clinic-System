import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedLayout, QWidget

from clinic.gui.login_gui import LoginGUI
from clinic.controller import Controller
from clinic.gui.main_menu_gui import MainMenu
from clinic.gui.add_patient_gui import AddPatientGUI
from clinic.gui.search_patient_gui import SearchPatientGUI

class ClinicGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        # Continue here with your code!
        self.controller = Controller(autosave = True)
        self.stacklayout = QStackedLayout()

        self.setWindowTitle("Victoria Walk-in Clinic")
        self.setMaximumSize(400, 300)

        self.login_tab = LoginGUI(self.controller, self)
        self.stacklayout.addWidget(self.login_tab)

        
        self.main_menu_tab = MainMenu(self.controller, self)
        self.stacklayout.addWidget(self.main_menu_tab)

        self.add_patient_tab = AddPatientGUI(self.controller, self)
        self.stacklayout.addWidget(self.add_patient_tab)

        self.search_patient_tab = SearchPatientGUI(self.controller, self)
        self.stacklayout.addWidget(self.search_patient_tab)

        # self.patient_options_tab = PatientOptionsGUI(self.controller, self)
        # self.stacklayout.addWidget(self.patient_options_tab)

        self.stacklayout.setCurrentIndex(0)
        widget = QWidget()
        widget.setLayout(self.stacklayout)
        self.setCentralWidget(widget)

    def exit_program(self):
        """
        This function exits the program upon being
        triggered
        """
        self.close()
    def activate_login_tab(self):
        self.stacklayout.setCurrentIndex(0)

    def activate_menu_tab(self):
        self.stacklayout.setCurrentIndex(1)
        self.main_menu_tab.patient_model.refresh_data()

    def activate_add_patient_tab(self):
        self.stacklayout.setCurrentIndex(2)

    def activate_search_patient_tab(self):
        self.stacklayout.setCurrentIndex(3)
    
    # def activate_options_tab(self):
    #     self.stacklayout.setCurrentIndex(4)



def main():
    app = QApplication(sys.argv)
    window = ClinicGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
