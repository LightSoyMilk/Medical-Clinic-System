import sys
import unittest
from unittest import TestCase
from unittest import main
from clinic.controller import *
from clinic.patient import Patient

class PatientTest(TestCase):
    def setUp(self):
        self.patient = Patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")


    def test_create_patient(self):
        """
        This function is to test if you can create a Patient variable and also to test
        the __eq__ method in the Patient class
        """
        expected_patient_2 = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
        expected_patient_2a = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
        expected_patient_3 = Patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

        self.assertIsNotNone(expected_patient_2, "Could not create a patient_2")

        self.assertEqual(expected_patient_2, expected_patient_2a, "These 2 patients are supposed to be the same")
        self.assertNotEqual(expected_patient_2a, expected_patient_3, "These 2 patients are different and should not be equal")
        self.assertNotEqual(expected_patient_2, self.patient, "These 2 patients are different and should not be equal")

    
    def test_get_phn(self):
        """
        This function is to test the get phn method in the 
        Patient class
        """
        expected_patient_2 = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")

        self.assertIsNotNone(expected_patient_2.get_phn(), "The patient variable could not use the function")
        self.assertEqual(expected_patient_2.get_phn(), 9790014444, "The function did not return a matching phn")
        self.assertNotEqual(expected_patient_2.get_phn(), self.patient.get_phn(), "The function incorrectly return a phn value")

    
    def test_get_name(self):
        """
        This function is to test the get name function in the 
        Patient class
        """
        expected_patient_3 = Patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

        self.assertIsNotNone(expected_patient_3.get_name(), "The function did not return a valid name string")
        self.assertEqual(self.patient.get_name(), "John Doe", "The function did not return the expected matching name string")
        self.assertNotEqual(expected_patient_3.get_name(), "John Doe", "The function incorrectly return names that did not match")

if __name__ == '__main__':
    unittest.main()