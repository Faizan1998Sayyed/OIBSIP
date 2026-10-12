"""
Automated Verification Suite for Smart BMI Calculator
Tests logic calculations, boundary classifications, input validation, and SQLite DB CRUD operations.
"""

import os
import unittest
import tempfile
import bmi_logic
import database

class TestBMICalculator(unittest.TestCase):

    def setUp(self):
        # Create a temporary database for testing
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.db_fd) # Close handle so SQLite & Windows can manage/delete it cleanly
        database.init_db(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass

    # 1. Formula & Rounding Tests
    def test_bmi_formula_rounding(self):
        # Weight 70kg, Height 1.75m -> 70 / (1.75^2) = 22.85714... -> 22.86
        bmi = bmi_logic.calculate_bmi(70, 1.75)
        self.assertEqual(bmi, 22.86)

        # Weight 80kg, Height 1.80m -> 80 / (1.80^2) = 24.6913... -> 24.69
        bmi2 = bmi_logic.calculate_bmi(80, 1.80)
        self.assertEqual(bmi2, 24.69)

    # 2. Category Boundary Classification Tests
    def test_category_classifications(self):
        # Underweight (< 18.5)
        cat, bg, fg = bmi_logic.classify_bmi(18.49)
        self.assertEqual(cat, "Underweight")

        # Normal (18.5 - 24.9)
        cat_lower, _, _ = bmi_logic.classify_bmi(18.50)
        self.assertEqual(cat_lower, "Normal")
        cat_upper, _, _ = bmi_logic.classify_bmi(24.90)
        self.assertEqual(cat_upper, "Normal")

        # Overweight (25.0 - 29.9)
        cat_ow_lower, _, _ = bmi_logic.classify_bmi(25.00)
        self.assertEqual(cat_ow_lower, "Overweight")
        cat_ow_upper, _, _ = bmi_logic.classify_bmi(29.90)
        self.assertEqual(cat_ow_upper, "Overweight")

        # Obese (>= 30.0)
        cat_obese, _, _ = bmi_logic.classify_bmi(30.00)
        self.assertEqual(cat_obese, "Obese")

    # 3. Input Validation Tests
    def test_input_validation(self):
        # Empty user name
        valid, err = bmi_logic.validate_inputs("", "70", "1.75")
        self.assertFalse(valid)
        self.assertIn("name", err.lower())

        # Empty weight
        valid, err = bmi_logic.validate_inputs("Faizan", "", "1.75")
        self.assertFalse(valid)
        self.assertIn("weight", err.lower())

        # Empty height
        valid, err = bmi_logic.validate_inputs("Faizan", "70", "")
        self.assertFalse(valid)
        self.assertIn("height", err.lower())

        # Non-numeric weight
        valid, err = bmi_logic.validate_inputs("Faizan", "abc", "1.75")
        self.assertFalse(valid)
        self.assertIn("numeric weight", err.lower())

        # Non-numeric height
        valid, err = bmi_logic.validate_inputs("Faizan", "70", "xyz")
        self.assertFalse(valid)
        self.assertIn("numeric height", err.lower())

        # Zero height
        valid, err = bmi_logic.validate_inputs("Faizan", "70", "0")
        self.assertFalse(valid)
        self.assertIn("greater than zero", err.lower())

        # Negative weight
        valid, err = bmi_logic.validate_inputs("Faizan", "-50", "1.75")
        self.assertFalse(valid)
        self.assertIn("greater than zero", err.lower())

        # Valid inputs
        valid, result = bmi_logic.validate_inputs("  Faizan  ", "70", "1.75")
        self.assertTrue(valid)
        self.assertEqual(result, ("Faizan", 70.0, 1.75))

    # 4. Database CRUD & Multi-User Tests
    def test_database_operations(self):
        # Save records for user Faizan
        s1, m1 = database.save_record("Faizan", 70.0, 1.75, 22.86, "Normal", db_path=self.db_path)
        self.assertTrue(s1)
        s2, m2 = database.save_record("Faizan", 69.0, 1.75, 22.53, "Normal", db_path=self.db_path)
        self.assertTrue(s2)

        # Save record for user Ahmed
        s3, m3 = database.save_record("Ahmed", 90.0, 1.80, 27.78, "Overweight", db_path=self.db_path)
        self.assertTrue(s3)

        # Check unique users
        s_users, users = database.get_unique_users(db_path=self.db_path)
        self.assertTrue(s_users)
        self.assertEqual(sorted(users), ["Ahmed", "Faizan"])

        # Fetch records for Faizan
        s_fz, records_fz = database.get_user_records("Faizan", db_path=self.db_path)
        self.assertTrue(s_fz)
        self.assertEqual(len(records_fz), 2)
        self.assertEqual(records_fz[0]['user_name'], "Faizan")

        # Fetch all records
        s_all, records_all = database.get_all_records(db_path=self.db_path)
        self.assertTrue(s_all)
        self.assertEqual(len(records_all), 3)

if __name__ == "__main__":
    unittest.main()
