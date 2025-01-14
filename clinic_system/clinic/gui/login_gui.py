import sys

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout
from PyQt6.QtWidgets import QGridLayout

from clinic.controller import Controller
from clinic.exception.invalid_login_exception import InvalidLoginException
#from clinic.gui.clinic_gui import ClinicGUI

class LoginGUI(QWidget):
    def __init__(self, controller: Controller, parent):
        super().__init__()
        #self.setWindowTitle("Login")
        self.parent = parent
        self.controller = controller

        layout = QGridLayout()

        label_username = QLabel("Username")
        self.username_input = QLineEdit()
        label_password = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.button_login = QPushButton("Login")
        self.button_quit = QPushButton("Quit")

        layout.addWidget(label_username, 0, 0)
        layout.addWidget(self.username_input, 0, 1)
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.password_input, 1, 1)
        layout.addWidget(self.button_login, 2, 0)
        layout.addWidget(self.button_quit, 2, 1)

        self.setLayout(layout)

        # Connecting the buttons to their signals
        self.button_login.clicked.connect(self.login_button_clicked)
        self.button_quit.clicked.connect(self.quit_button_clicked)
    

    def login_button_clicked(self):
        """
        This function happens when the login button is clicked.
        It checks if the user inputted a correct username and password.
        If the user was successful in logging in, the window will change
        to the main menu, if not it will throw a warning message
        """
        try:
            # Getting the username and password from user
            user_name = self.username_input.text()
            password = self.password_input.text()

            # Passing the user inputs into controller to see if 
            # it matches the database which will return the correct state
            logged_in_status = self.controller.login(user_name, password)
            if (logged_in_status): # Successful login
                QMessageBox.information(self, "Success", "Welcome to the clinic")
                #self.button_login.clicked.connect(self.toggle_main_menu)
                self.parent.activate_menu_tab()
        except InvalidLoginException:
            QMessageBox.warning(self, "Invalid Login", "Please input the right username and password")
    
        # Set the username and password slot to empty after the user clicked login
        self.username_input.setText("")
        self.password_input.setText("")

        # Changing to the menu


    def quit_button_clicked(self):
        """
        This function happens when the user click on the quit
        button and will exit/terminate the program
        """
        self.parent.exit_program()
        #login_gui.quit()

    
    def toggle_main_menu(self, checked):
        if self.main_menu.isVisible():
            self.main_menu.hide()
        else:
            self.main_menu.show()


# login_gui = QApplication(sys.argv)
# window = LoginGUI()
# window.show()
# login_gui.exec()