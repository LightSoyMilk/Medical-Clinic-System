from pickle import load, dump
import pickle

from clinic.dao.note_dao import NoteDAO
from clinic.note import Note
from datetime import datetime

class NoteDAOPICKLE(NoteDAO):

    def __init__(self, autosave = False, phn = None):
        self.autosave = autosave
        #self.filename = str(phn) + '.data'
        self.autocounter = 0
        self.notes = []

        self.filename = 'clinic/records/'+str(phn)+'.dat'
        if self.autosave:
            try:
                with open(self.filename, "rb") as file:
                    self.notes = pickle.load(file)
                    self.autocounter = self.notes[-1].get_code()
            except:
                self.notes = []
        else:
                self.notes = []

    def search_note(self, code: int) -> Note:
        """
        Searches for a note in the patient's record by its unique code.
        """
        for note in self.notes:
            if note.get_code() == code:
                return note  # Return the note if found
        return None  # Return None if no matching note is found
    
    
    def create_note(self, text: str) -> Note:
        '''
        The user creates a new note for the current patients record, storing the
        notes code as the auto-incremented counter from the patient record,
        and also storing the notes details and current timestamp.
        '''
        self.autocounter += 1
        new_note = Note(self.autocounter, text) #creates new note
        self.notes.append(new_note) #adds note to list of notes
        if self.autosave:
            with open(self.filename, 'wb') as file:
                pickle.dump(self.notes, file)
        return new_note
    
    
    def retrieve_notes(self, search_string: str):
        '''
        The user searches the current patients record by text, and retrieves a
        list of notes that have the searched text inside the note
        '''
        matches = [note for note in self.notes if search_string.lower() in note.text.lower()]
        return matches
    

    def update_note(self, code: int, new_text: str):
        '''
        The user selects a note by code in the current patients record,
        retrieves the notes details and timestamp, updates the details, and
        changes the timestamp to the current timestamp.
        '''
        # Search for the note with code
        for note in self.notes:
            if note.code == code:
                # Update the note
                note.text = new_text
                note.timestamp = datetime.now()
                if self.autosave:
                    with open(self.filename, 'wb') as file:
                        pickle.dump(self.notes, file)
                return True
        return False
    

    def delete_note(self, code: int):
        '''
        The user selects a note by code in the current patients record, and
        deletes the note
        '''
        # Search for the note with code
        for note in self.notes:
            if note.code == code:
                self.notes.remove(note)  # Remove the note from the list
                if self.autosave:
                    with open(self.filename, 'wb') as file:
                        dump(self.notes, file)
                return True 
        return False
    

    def list_notes(self):
        '''
        The user lists the full patient record with all the notes, from the last
        created note to the first created note
        '''
        lonotes = [] #creates new list to keep original unaltered
        for note in reversed(self.notes):
            lonotes.append(note)
        return lonotes