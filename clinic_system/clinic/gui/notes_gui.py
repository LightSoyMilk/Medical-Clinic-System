from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QInputDialog
)

class NotesGUI(QMainWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller  # Save controller reference

        self.setWindowTitle("Patient Notes")
        self.setMinimumSize(600, 400)

        #controller.set_current_patient(123)

        # Central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # QPlainTextEdit for listing and retrieving notes
        self.notes_display = QPlainTextEdit()
        self.notes_display.setReadOnly(True)  # Ensure it is not editable

        # Add note button
        self.add_note_button = QPushButton("Add Note")
        self.add_note_button.clicked.connect(self.add_note)

        # Delete note button
        self.delete_note_button = QPushButton("Delete Note")
        self.delete_note_button.clicked.connect(self.delete_note)

        #Update note button
        self.update_note_button = QPushButton("Update Note")
        self.update_note_button.clicked.connect(self.update_note)

        #Retreive notes button
        self.retrieve_notes_button = QPushButton("Retrieve Notes")
        self.retrieve_notes_button.clicked.connect(self.retrieve_notes)

        #reset button   
        self.reset_button = QPushButton("Reset Button")
        self.reset_button.clicked.connect(self.reset_button_button)

        #Exit notes button
        self.exit_button = QPushButton("Exit")  # Exit button
        self.exit_button.clicked.connect(self.close_notes_menu)

        # Add components to layout
        layout.addWidget(self.notes_display)
        layout.addWidget(self.add_note_button)
        layout.addWidget(self.delete_note_button)
        layout.addWidget(self.update_note_button)
        layout.addWidget(self.retrieve_notes_button)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.exit_button)
        

        # Set central widget
        self.setCentralWidget(central_widget)

        # Refresh the notes display
        self.refresh_notes_display()

    def refresh_notes_display(self):
        """
        Fetch notes from the controller and display them in the QPlainTextEdit.
        """
        notes = self.controller.list_notes()
        self.notes_display.clear()
        for note in notes:
            # Format each note (assuming notes have 'code' and 'text' attributes)
            self.notes_display.appendPlainText(f"Note Code: \
                {note.get_code()}\n{note.get_text()}\n")

    def add_note(self):
        """
        Opens a dialog for adding a new note and updates the notes display.
        """
        text, ok = QInputDialog.getText(self, "Add Note", "Enter your note:")
        if ok and text.strip():
            self.controller.create_note(text.strip())
            QMessageBox.information(self, "Success", "Note added successfully!")
            self.refresh_notes_display()

    def delete_note(self):
        """
        Prompts the user for the note code to delete and removes the note if it exists.
        """
        code, ok = QInputDialog.getInt(self, "Delete Note", "Enter the note code to delete:")
        if ok:
            # Attempt to delete the note using the controller
            success = self.controller.delete_note(code)
            if success:
                QMessageBox.information(self, "Success", f"Note with code {code} deleted successfully!")
                self.refresh_notes_display()
            else:
                QMessageBox.warning(self, "Warning", f"Note with code {code} not found.")

    def update_note(self):
        """
        Prompts the user for the note code to update and the new text.
        Updates the note if it exists and refreshes the display.
        """
        # Prompt the user for the note code
        code, ok_code = QInputDialog.getInt(self, "Update Note", "Enter the note code to update:")
        if not ok_code:
            return

        # Prompt the user for the new text
        new_text, ok_text = QInputDialog.getText(self, "Update Note", "Enter the new text for the note:")
        if not ok_text or not new_text.strip():
            QMessageBox.warning(self, "Warning", "New text cannot be empty.")
            return

        # Attempt to update the note using the controller
        success = self.controller.update_note(code, new_text.strip())
        if success:
            QMessageBox.information(self, "Success", f"Note with code {code} updated successfully!")
            self.refresh_notes_display()
        else:
            QMessageBox.warning(self, "Warning", f"Note with code {code} not found.")

    def retrieve_notes(self):
        """
        Prompts the user for a search string and displays matching notes in the QPlainTextEdit.
        """
        #tuple of string text and a bool for the ok button true/false if pressed
        search_string, ok = QInputDialog.getText(self, "Retrieve Notes", "Enter search string:")
        if not ok or not search_string.strip():
            QMessageBox.warning(self, "Warning", "Search string cannot be empty.")
            return

        # Retrieve matching notes from the controller
        matches = self.controller.retrieve_notes(search_string.strip())
        self.notes_display.clear()

        if matches:
            # Display matching notes in the QPlainTextEdit
            for note in matches:
                self.notes_display.appendPlainText(f"Note Code: {note.get_code()}\n{note.get_text()}\n")
        else:
            QMessageBox.information(self, "No Matches", "No notes found containing the search string.")

    def reset_button_button(self):
        self.refresh_notes_display()




    def close_notes_menu(self):
        self.close()