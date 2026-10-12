"""
Automated Test Suite for Cryptographically Secure Random Password Generator
"""

import unittest
import generator_logic

class TestPasswordGenerator(unittest.TestCase):

    # 1. Validation Tests
    def test_minimum_length_validation(self):
        success, result = generator_logic.generate_password(length=7)
        self.assertFalse(success)
        self.assertIn("at least 8 characters", result)

    def test_minimum_pools_validation(self):
        # Only 1 pool selected
        success, result = generator_logic.generate_password(length=12, use_upper=True, use_lower=False, use_digits=False, use_symbols=False)
        self.assertFalse(success)
        self.assertIn("at least 2 character types", result)

    # 2. Diversity Rule Enforcement Test
    def test_guaranteed_diversity_enforcement(self):
        for _ in range(20):
            success, pwd = generator_logic.generate_password(
                length=10, use_upper=True, use_lower=True, use_digits=True, use_symbols=True
            )
            self.assertTrue(success)
            self.assertTrue(any(c.isupper() for c in pwd), "Must contain at least 1 uppercase letter")
            self.assertTrue(any(c.islower() for c in pwd), "Must contain at least 1 lowercase letter")
            self.assertTrue(any(c.isdigit() for c in pwd), "Must contain at least 1 digit")
            self.assertTrue(any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in pwd), "Must contain at least 1 symbol")

    # 3. Ambiguous Characters Exclusion Test
    def test_exclude_ambiguous_characters(self):
        ambiguous_set = set("0Oo1lI|")
        for _ in range(20):
            success, pwd = generator_logic.generate_password(
                length=16, use_upper=True, use_lower=True, use_digits=True, use_symbols=True, exclude_ambiguous=True
            )
            self.assertTrue(success)
            for char in pwd:
                self.assertNotIn(char, ambiguous_set, f"Ambiguous character '{char}' found in generated password!")

    # 4. Strength Evaluation Tests
    def test_strength_evaluation(self):
        # Short / weak
        s1 = generator_logic.calculate_strength("a1B!", use_upper=True, use_lower=True, use_digits=True, use_symbols=True)
        self.assertIn("Weak", s1['label'])

        # Medium (entropy between 40 and 60)
        s2 = generator_logic.calculate_strength("aB34567890", use_upper=True, use_lower=True, use_digits=True, use_symbols=False)
        self.assertIn("Medium", s2['label'])

        # Strong / Very Strong
        s3 = generator_logic.calculate_strength("K9#mP2$vX8@nL4!z", use_upper=True, use_lower=True, use_digits=True, use_symbols=True)
        self.assertIn("Very Strong", s3['label'])

if __name__ == "__main__":
    unittest.main()
