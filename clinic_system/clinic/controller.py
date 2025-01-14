#this would be the controller file

#importing files and libraries
#import unittest
import hashlib
from clinic.note import Note
from clinic.patient import Patient
from clinic.patient_record import PatientRecord

from clinic.dao.patient_dao import PatientDAO
from clinic.dao.patient_dao_json import PatientDAOJSON

USER_NAME = 0
PASSWORD_HASH = 1

from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException


"""
Hardcoded variables/lists
"""
class Controller:
    def __init__(self, autosave = False):
        self.autosave = autosave
        self.logged_in = False
        self.dou = {"user": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92", \
                    "ali": "6394ffec21517605c1b426d43e6fa7eb0cff606ded9c2956821c2c36bfee2810", \
                        "kala": "e5268ad137eec951a48a5e5da52558c7727aaa537c8b308b5e403e6b434e036e"} #dict[str, str], encoded within memory
        if self.autosave:
            try:
                self.dou = self.load_user()
            except FileNotFoundError:
                pass

        self.patient_dao = PatientDAOJSON(self.autosave) #JSON file to handle collection

        self.current_patient = None


    def load_user(self):
        users = {}
        user_file = open("clinic/users.txt", "r")

        for line in user_file:
            stripped_line = line.strip()
            user_info_list = stripped_line.split(",")
            #print(user_info_list)
            users[user_info_list[USER_NAME]] = user_info_list[PASSWORD_HASH] # Creating a new dictionary entry with d[new_key] = new_value

        user_file.close()
        return users
    

    def get_password_hash(self, password):
        # Learn a bit about password hashes by reading this code
        encoded_password = password.encode('utf-8')     # Convert the password to bytes
        hash_object = hashlib.sha256(encoded_password)      # Choose a hashing algorithm (e.g., SHA-256)
        hex_dig = hash_object.hexdigest()       # Get the hexadecimal digest of the hashed password
        return hex_dig

    def login(self, user_name: str, user_pass: str) -> bool:
        """
        This function checks for the user input and see if the user name and
        the provided password matches with what is in the list of users record
        and returns a bool reflecting the match and sets the state of logged in
        to True
        """
        password_hash = self.get_password_hash(user_pass)
        if (self.logged_in == True):
            raise DuplicateLoginException()
        elif (user_name in self.dou and password_hash == self.dou[user_name]):
            self.logged_in = True
            return True
        else:
            raise InvalidLoginException()
        

    def logout(self) -> bool:
        """
        This function sets the state of logged in to False and return
        the bool matching the success state of logging out
        """
        if(self.logged_in == False):
            raise InvalidLogoutException()
        else:
            self.logged_in = False
            return True

    
    def create_patient(self, phn: int, name: str, birth_date: str, phone: str, email: str, address: str) -> Patient:
        """
        This function creates a new patient with all the required field given in the parameters 
        and then delegate the collection system to the JSON class
        """
        if (self.logged_in == False):
            raise IllegalAccessException()
        elif (self.search_patient(phn)): # handling the case where there is an existing phn, do we break or do we update the patient?
            raise IllegalOperationException()
        else:
            new_patient = Patient(phn, name, birth_date, phone, email, address, self.autosave) #add self.autosave at the end
            return self.patient_dao.create_patient(new_patient)
    

    def search_patient(self, searched_phn: int) -> Patient:
        """
        This function takes in a Personal Health Number as a parameter and goes through the
        list of patients(lop) to see if the PHN is in it or not. If yes it will return the patient
        and if not, it will return nothing
        """
        if (self.logged_in == False):
            raise IllegalAccessException()
        return self.patient_dao.search_patient(searched_phn)
    

    def retrieve_patients(self, searched_name: str) -> list[Patient]:
        """
        This function takes in a string(searched_name) and goes through the entire list of patients(lop)
        and append all patients that have the matching name to a list and then return that list
        """
        if (self.logged_in == False):
            raise IllegalAccessException() #if logged_in is False then we raise exception
        return self.patient_dao.retrieve_patients(searched_name) # return the list of patients with matching name
    

    def update_patient(self, searched_phn: int, input_phn: int, input_name: str, \
                       input_birth_date: str, input_phone: str, input_email: str, input_address: str) -> bool: 
        """
        This function takes in a searching Personal Health Number and see if that patient exists in the system.
        If so, proceed to update that patient with the input field.
        In case that the inputted phn collides with another patient's phn then we do not update that patient.
        """
        if (self.logged_in == False):
            raise IllegalAccessException()

        if (not self.search_patient(searched_phn)): # if patient is not in the system then returns false
            raise IllegalOperationException()

        if (self.current_patient is not None and self.search_patient(searched_phn) == self.current_patient): # cannot update the current patient 
            raise IllegalOperationException()

        if (searched_phn != input_phn):  # if there is a new patient number
            if (self.search_patient(input_phn)): #check if the new phn already exists
                raise IllegalOperationException()
        # The input phn is unused 
        found_patient = self.search_patient(searched_phn)
        found_patient.phn = input_phn
        found_patient.name = input_name
        found_patient.birth_date = input_birth_date
        found_patient.phone = input_phone
        found_patient.email = input_email
        found_patient.address = input_address
        return self.patient_dao.update_patient(searched_phn, found_patient)


    def delete_patient(self, searched_phn: int) -> bool:
        """
        This function takes in a Personal Health Number(phn) and see if there is a matching
        patient with the same phn. If so, the patient will be deleted from the list of patients(lop)
        """
        if (self.logged_in == False):
            raise IllegalAccessException()
        if (self.get_current_patient() is not None and self.search_patient(searched_phn) == self.current_patient): #cannot delete the current selected patient
            raise IllegalOperationException()
        if (self.search_patient(searched_phn) is None): # if there is no matching phn in the collection raise an Exception
            raise IllegalOperationException()
        
        return self.patient_dao.delete_patient(searched_phn)
        
    
    def list_patients(self) -> list[Patient]:
        """
        This function takes no argument and will return all patients in 
        the current list of patients(lop) 
        """
        if (self.logged_in == False): 
            raise IllegalAccessException()
        return self.patient_dao.list_patients()
        

    def set_current_patient(self, phn: int) -> None:
        """
        This funciton will set the current patient to the patient in the 
        list of patients with the same phn. The current patient will still 
        be None if the phn does not exist
        """
        if (self.logged_in == False):
            raise IllegalAccessException()
        if (self.search_patient(phn) is None): #If there is not a matching patient in the collection, you cannot set the current patient to it
            raise IllegalOperationException()
        self.current_patient = self.search_patient(phn) 


    def get_current_patient(self) -> Patient:
        """
        This will return the current patient if the user is logged in
        else it will return None
        """
        if (self.logged_in == False):
            raise IllegalAccessException()
        return self.current_patient
    

    def unset_current_patient(self) -> None:
        """
        This function will set current patient to None if the user is 
        logged in
        """
        if (self.logged_in == False):
            raise IllegalAccessException()
        self.current_patient = None


    def create_note(self, text: str):
        """
        The user creates a new note for the current patients record, storing the
        notes code as the auto-incremented counter from the patient record,
        and also storing the notes details and current timestamp
        """
        if (self.logged_in == False):
            raise IllegalAccessException()
        if (self.current_patient is None):
            raise NoCurrentPatientException()
        else: 
            return self.current_patient.create_note(text)
    
    def search_note(self, key):
        """
        This method searches the note based on the key (number)
        provided
        """
        if (self.logged_in == False):
            raise IllegalAccessException()
        if (self.current_patient is None): #Cannot do search note without a valid current patient
            raise NoCurrentPatientException()
        return self.current_patient.search_note(key)
    
    def retrieve_notes(self, text):
        """
        The user searches the current patients record by text, and retrieves a
        list of notes that have the searched text inside the note.
        """
        if (self.logged_in == False):
            raise IllegalAccessException()
        if (self.current_patient is None):
            raise NoCurrentPatientException()
        return self.current_patient.retrieve_notes(text)
    
    def update_note(self, code: int, new_text: str):
        """
        The user selects a note by code in the current patients record,
        retrieves the notes details and timestamp, updates the details, and
        changes the timestamp to the current timestamp
        """
        if (self.logged_in == False):
            raise IllegalAccessException()
        if (self.current_patient is None):
            raise NoCurrentPatientException()
        return self.current_patient.update_note(code, new_text)
    
    def delete_note(self, code: int):
        """
        The user selects a note by code in the current patients record, and
        deletes the note
        """
        if (self.logged_in == False):
            raise IllegalAccessException()
        if (self.current_patient is None):
            raise NoCurrentPatientException()
        return self.current_patient.delete_note(code)
    
    def list_notes(self):
        """
        The user lists the full patient record with all the notes, from the last
        created note to the first created note.
        """
        if (self.logged_in == False):
            raise IllegalAccessException()
        if (self.current_patient is None):
            raise NoCurrentPatientException()
        return self.current_patient.list_notes()