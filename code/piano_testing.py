import sys
import unittest
from PyQt6.QtWidgets import QApplication
from piano_keyboard import WhiteKey, BlackKey
from piano_staff import Note, StaffWindow

app = QApplication(sys.argv)


class TestCase(unittest.TestCase):
    def test_white_key(self):
        staff = StaffWindow()
        white_key = WhiteKey(0, 0, 40, 200, "C", staff, 112)

        self.assertEqual(white_key.color, "#FFFFFF")
        self.assertEqual(white_key.name, "C")
        self.assertFalse(white_key.label.isVisible())

        del white_key
        del staff

    def test_black_key(self):
        staff = StaffWindow()
        black_key = BlackKey(60, 0, 20, 120, "C#", staff, 112)
        self.assertEqual(black_key.color, "#000000")
        self.assertEqual(black_key.name, "C#")
        self.assertEqual(black_key.staff, staff)

        del staff

    def test_add_note_to_staff(self):
        staff = StaffWindow()
        # testing quarter note
        quarter_note = Note("C", staff, 112, 400)
        staff.add_note_to_staff(quarter_note)
        self.assertEqual(staff.note_counter, 1)
        # testing half note
        half_note = Note("F", staff, 88, 1000)
        staff.add_note_to_staff(half_note)
        self.assertEqual(staff.note_counter, 3)

        del staff


if __name__ == '__main__':
    unittest.main()
    app.quit()
