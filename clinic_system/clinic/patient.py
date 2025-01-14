#this would be the Patient file
#from where import Note, patientrecord

from clinic.patient_record import PatientRecord
class Patient:
    def __init__(self, phn: int, name: str, birth_date: str, phone: str, email: str, address: str, autosave = False):
        self.phn = phn 
        self.name = name 
        self.birth_date = birth_date 
        self.phone = phone 
        self.email = email 
        self.address = address 
        self.autosave = autosave

        self.patient_record = PatientRecord(self.autosave, self.phn) #add autosave
        

    def __eq__(self, other):
        return (self.phn == other.phn and self.name == other.name and self.birth_date == other.birth_date \
        and self.phone == other.phone and self.email == other.email and self.address == other.address)
    
    def __str__(self):
        return "The phn of the patient is %d , with name %s, born on %s, whose cell phone number is %s, and email at %s, living at %s" % \
        (self.phn, self.name, self.birth_date, self.phone, self.email, self.address)

    def get_phn(self) -> int:
        return (self.phn)
    
    def get_name(self) -> str:
        return (self.name)
    
    def create_note(self, text: str):
        return self.patient_record.create_note(text)
    
    def search_note(self, code: int):
        return self.patient_record.search_note(code)
    
    def retrieve_notes(self, text):
        return self.patient_record.retrieve_notes(text)
    
    def update_note(self, code: int, new_text: str):
        return self.patient_record.update_note(code, new_text)
    
    def delete_note(self, code: int) -> bool:
        return self.patient_record.delete_note(code)
    
    def list_notes(self):
        return self.patient_record.list_notes()