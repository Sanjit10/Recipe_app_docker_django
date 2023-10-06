"""
    Sample test file
"""

from django.test import SimpleTestCase

from app import calc

class CalcTests(SimpleTestCase):

    def test_add_numbers(self):
        """Test that two numbers are added together"""
        self.assertEqual(calc.add(3, 8), 11)
    
    def test_subtract_numbers(jpani_bhaye_hunchha):
        """Test that values are subtracted and returned"""
        jpani_bhaye_hunchha.assertEqual(calc.subtract(5, 11), 6)
        