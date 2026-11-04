# test_prime.py
import unittest
from prime import is_prime

class TestPrime(unittest.TestCase):
    def setUp(self):
        self.prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
        self.non_prime_numbers = [1, 4, 6, 8, 10, 12, 14, 16, 18, 20]

    def test_prime_numbers(self):
        for number in self.prime_numbers:
            self.assertTrue(
                is_prime(number),
                msg=f"{number} is not recognized as a prime",
            )

    def test_non_prime_numbers(self):
        for number in self.non_prime_numbers:
            self.assertFalse(
                is_prime(number),
                msg=f"{number} is incorrectly recognized as a prime",
            )


if __name__ == "__main__":
    unittest.main()
