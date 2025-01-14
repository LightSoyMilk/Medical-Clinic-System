#this would be the PatientRecord file
from clinic.note import Note
from datetime import datetime

from clinic.dao.note_dao_pickle import NoteDAOPICKLE

class PatientRecord:
    def __init__(self, autosave = False, phn = None):
        #self.autocounter = 0
        #self.notes = []
        self.autosave = autosave
        self.phn = phn
        self.note_dao = NoteDAOPICKLE(self.autosave)

    def create_note(self, text: str):
        # self.autocounter += 1
        # new_note = Note(self.autocounter, text) #creates new note
        # self.notes.append(new_note) #adds note to list of notes
        # return new_note
        return self.note_dao.create_note(text)
    
    def search_note(self, code: int):
        # for note in self.notes:
        #     if note.get_code() == code:
        #         return note  # Return the note if found
        # return None  # Return None if no matching note is found
        return self.note_dao.search_note(code)
    
    def retrieve_notes(self, text: str):
        # matches = [note for note in self.notes if text.lower() in note.text.lower()]
        # return matches
        return self.note_dao.retrieve_notes(text)
    
    def update_note(self, code: int, new_text: str):
        # # Search for the note with code
        # for note in self.notes:
        #     if note.code == code:
        #         # Update the note
        #         note.text = new_text
        #         note.timestamp = datetime.now()
        #         return True
        # return False
        return self.note_dao.update_note(code, new_text)
    
    def delete_note(self, code: int):
        # # Search for the note with code
        # for note in self.notes:
        #     if note.code == code:
        #         self.notes.remove(note)  # Remove the note from the list
        #         return True 
        # return False
        return self.note_dao.delete_note(code)
    
    def list_notes(self):
        # lonotes = [] #creates new list to keep original unaltered
        # for note in reversed(self.notes):
        #     lonotes.append(note)
        # return lonotes
        return self.note_dao.list_notes()