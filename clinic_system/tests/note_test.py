import sys
import unittest
from unittest import TestCase
from unittest import main
from clinic.controller import *
from clinic.note import Note

class NoteTest(TestCase):
    def setUp(self):
        self.note = Note(1, "Patient comes with headache and high blood pressure.")
    
    
    def test_create_note(self):
        """
        This is to mainly tests if notes can be created successfully 
        """
        expected_note_1 = Note(1, "Patient comes with headache and high blood pressure.")

        self.assertIsNotNone(expected_note_1, "Created expected note 1 successfully")


    def test_eq_of_note(self):
        """
        This is to test the __eq__ method in the Note class 
        """
        expected_note_1 = Note(1, "Patient comes with headache and high blood pressure.")
        expected_note_1a = Note(1, "Patient comes with headache and high blood pressure.")
        expected_note_2 = Note(2, "Patient complains of a strong headache on the back of neck.")

        self.assertEqual(expected_note_1, expected_note_1a, "These 2 notes are the same and have been created successfully yay")
        self.assertNotEqual(expected_note_1a, expected_note_2, "These 2 notes are not supposed to be equal")


    def test_str_of_note(self):
        """
        This is to test the __str__ method in the Note class 
        """
        expected_note_1 = Note(1, "Patient comes with headache and high blood pressure.")

        self.assertEqual(str(expected_note_1), f"The note's code is 1: Patient comes with headache and high blood pressure. , created at {expected_note_1.timestamp}")

    
    def test_get_note_code(self):
        """
        This is to test the get_code method to see if it returns the correct code
        """
        expected_note_2 = Note(2, "Patient complains of a strong headache on the back of neck.")
        expected_note_3 = Note(3, "Patient says high BP is controlled, 120x80 in general.")

        self.assertEqual(expected_note_3.get_code(), 3, "This note did not have the expected code")
        self.assertNotEqual(self.note.get_code(), expected_note_2.get_code(), "These 2 different notes should not have the same code")

    
    def test_get_text_note(self):
        """
        This is to test the get_text method to see if it returns the correct text
        """
        expected_note_2 = Note(2, "Patient complains of a strong headache on the back of neck.")

        self.assertEqual(expected_note_2.get_text(), "Patient complains of a strong headache on the back of neck.", "This note did not return the correct text")
        self.assertNotEqual(self.note.get_text(), expected_note_2.get_text(), "These 2 notes should not have the same text")

        
if __name__ == '__main__':
	unittest.main()