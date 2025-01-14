import unittest
from datetime import datetime, timedelta
from clinic.note import Note
from clinic.patient_record import PatientRecord  # Replace with actual module path if needed

class PatientRecordTest(unittest.TestCase):

    def setUp(self):
        self.patient_record = PatientRecord()

    def test_create_note(self):
        # Test creating a note
        note = self.patient_record.create_note("Patient has a fever")
        self.assertEqual(note.code, 1)
        self.assertEqual(note.text, "Patient has a fever")
        self.assertIn(note, self.patient_record.notes)

    def test_search_note_found(self):
        # Test searching for a note that exists
        note = self.patient_record.create_note("Patient needs rest")
        found_note = self.patient_record.search_note(1)
        self.assertEqual(found_note, note)

    def test_search_note_not_found(self):
        # Test searching for a note that does not exist
        self.patient_record.create_note("Patient has a fever")
        result = self.patient_record.search_note(99)
        self.assertIsNone(result)

    def test_retrieve_notes_found(self):
        # Test retrieving notes containing a specific text
        self.patient_record.create_note("Patient has a fever")
        self.patient_record.create_note("Patient needs rest")
        results = self.patient_record.retrieve_notes("fever")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, "Patient has a fever")

    def test_retrieve_notes_not_found(self):
        # Test retrieving notes with text that doesn't match any note
        self.patient_record.create_note("Patient has a fever")
        results = self.patient_record.retrieve_notes("cough")
        self.assertEqual(results, [])

    def test_update_note_found(self):
        # Test updating a note that exists
        note = self.patient_record.create_note("Initial diagnosis")
        success = self.patient_record.update_note(1, "Updated diagnosis")
        self.assertTrue(success)
        self.assertEqual(note.text, "Updated diagnosis")
        # Check timestamp updated to recent time
        delta = timedelta(seconds=1)
        now = datetime.now()
        self.assertTrue(now - delta <= note.timestamp <= now + delta)

    def test_update_note_not_found(self):
        # Test updating a note that does not exist
        success = self.patient_record.update_note(99, "Non-existent note")
        self.assertFalse(success)

    def test_delete_note_found(self):
        # Test deleting a note that exists
        note = self.patient_record.create_note("To be deleted")
        success = self.patient_record.delete_note(1)
        self.assertTrue(success)
        self.assertNotIn(note, self.patient_record.notes)

    def test_delete_note_not_found(self):
        # Test deleting a note that does not exist
        success = self.patient_record.delete_note(99)
        self.assertFalse(success)

    def test_list_notes(self):
        # Test listing notes in reverse order
        note1 = self.patient_record.create_note("First note")
        note2 = self.patient_record.create_note("Second note")
        note3 = self.patient_record.create_note("Third note")
        listed_notes = self.patient_record.list_notes()
        self.assertEqual(listed_notes, [note3, note2, note1])

if __name__ == "__main__":
    unittest.main()