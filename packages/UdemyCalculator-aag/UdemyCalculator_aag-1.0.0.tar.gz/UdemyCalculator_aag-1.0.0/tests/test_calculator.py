import unittest
from UdemyCalculator.calculator import Calculator


class TesteCalculator(unittest.TestCase):
    def test_calculate_square_area(self):
        self.assertEqual(Calculator.calculate_square_area(5), 25)

    def test_calculate_triangle_area(self):
        self.assertEqual(Calculator.calculate_triangle_area(10, 5), 25)

    def test_calculate_trapezoid_area(self):
        self.assertEqual(Calculator.calculate_trapezoid_area(10, 5, 5), 37.5)

    def test_squares(self):
        self.assertTrue(Calculator.compare_squares(5, 5))
        self.assertFalse(Calculator.compare_squares(5, 6))


if __name__ == '__main__':
    unittest.main()
