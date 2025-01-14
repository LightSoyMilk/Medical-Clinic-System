from clinic.dao.patient_dao import PatientDAO
from clinic.patient import Patient
import json
from json import JSONEncoder, JSONDecoder
from clinic.dao.patient_encoder import PatientEncoder
from clinic.dao.patient_decoder import PatientDecoder

class PatientDAOJSON(PatientDAO):
    def __init__(self, autosave = False):
        """
        This is the constructor for PatientDAOJson. It has an autosave field to know whether 
        the file would be working with files or a built in list to handle the collection of patients
        """
        self.autosave = autosave
        self.lop = []

        self.filename = 'clinic/patients.json'
        if self.autosave:
            try: 
                with open(self.filename, 'r') as file:
                    for line in file:
                        patient = json.loads(line.strip(), cls=PatientDecoder)
                        self.lop.append(patient)
            except:
                self.lop = [] #if there is an error when opening the file, it will default to the list collection
        else:
            self.lop = [] 
        

    def create_patient(self, given_patient: Patient) -> Patient:
        """
        This function takes in a given Patient Object created in Controller
        then add it to the list of patients collection (lop). If autosave is on
        then after the Patient object is created, it will be dumped/written in the 
        json file as a Json object
        """
        self.lop.append(given_patient)
        # Handling files
        if self.autosave:
            with open(self.filename, 'w') as file:
                for patient in self.lop:
                    json_str = json.dumps(patient, cls=PatientEncoder)
                    file.write(json_str + '\n')
        return given_patient
    

    def search_patient(self, searched_phn: int) -> Patient:
        """
        This function takes in a Personal Health Number as a parameter and goes through the
        list of patients(lop) to see if the PHN is in it or not. If yes it will return the patient
        and if not, it will return nothing
        """
        for patient in range(0, len(self.lop)): # for each patient in lop, we'll loop through the entire list
            if(self.lop[patient].get_phn() == searched_phn): #found matched phn then return that patient
                return self.lop[patient]
        return None #if we do not find the patient
    

    def retrieve_patients(self, searched_name: str) -> list[Patient]:
        """
        This function takes in a string(searched_name) and goes through the entire list of patients(lop)
        and append all patients that have the matching name to a list and then return that list
        """
        lo_patient_matched = []
        for patient in range(0, len(self.lop)): #looping through each patient in lop
            if (searched_name in self.lop[patient].get_name()): # if the current patient has a matching name, append it to the lo_patient_matched
                lo_patient_matched.append(self.lop[patient])
        return lo_patient_matched
    
 
    def update_patient(self, searched_phn: int, given_patient: Patient) -> bool:
        """
        This function takes in a searched PHN and a Patient object that is already updated with
        all the input fields provided in Controller. The function will then find the unupdated
        patient and replace that patient in the list with the newly updated Patient object.
        If we are working with a Json file then after updating our list of patients, each patient
        will be written into the Json file as Json objects 
        """
        # The input phn is unused 
        old_patient = self.search_patient(searched_phn)
        old_patient = given_patient
        if self.autosave:
            with open(self.filename, 'w') as file:
                for patient in self.lop:
                    json_str = json.dumps(patient, cls=PatientEncoder)
                    file.write(json_str + '\n')
        return True
    

    def delete_patient(self, searched_phn: int) -> bool:
        """
        This function takes in a Personal Health Number(phn) and see if there is a matching
        patient with the same phn. If so, the patient will be deleted from the list of patients(lop) and 
        after deleting the Patient, the entire list of patients (lop) will be dumped one by one as Json objects
        in the Json file
        """
        for patient in range(0, len(self.lop)):
            if (self.lop[patient].get_phn() == searched_phn): #while looping through the list of patient if we find a match in phn
                self.lop.remove(self.lop[patient]) #remove that patient from the list
                #self.current_patient = None #sets current patient to none. Assuming current patient was the one that was deleted
                if self.autosave:
                    with open(self.filename, 'w') as file:
                        for patient in self.lop:
                            json_str = json.dumps(patient, cls=PatientEncoder)
                            file.write(json_str + '\n')
                return True
        return False
    

    def list_patients(self) -> list[Patient]:
        """
        This function takes no argument and will return all patients in 
        the current list of patients(lop) as a list containing Patients
        """
        temp_lop = []
        for patient in range(0, len(self.lop)):
            temp_lop.append(self.lop[patient])
        return temp_lop