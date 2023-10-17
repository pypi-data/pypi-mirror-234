import unittest
from calculator import Calculator

class TestCalculator(unittest.TestCase):
    '''Tests calulator operators for correct results

    ...

    Attributes
    ----------
    calculator : Class
        creates an instance of the calculator to use for tests

    Methods
    -------
    test_addition_with_memory
        Tests adding numbers to memory
    test_subtraction_with_memory
        Tests subtracting numbers from memory
    test_multiplication_with_memory
        Tests multiplying memory by new number
    test_division_with_memory
        Tests dividing memory by new number
        Tests error message when dividing by 0
    test_nth_root_with_negative_memory
        Tests error message when calculating nth root of negative number
    test_nth_root_with_memory
        Tests new number as nth root of memory
    test_reset_memory
        Tests resetting memory to 0
    '''
    
    def setUp(self):
        self.calculator = Calculator()

    def test_addition_with_memory(self):
        self.assertEqual(self.calculator.add(3), 3)
        self.assertEqual(self.calculator.add(5), 8)

    def test_subtraction_with_memory(self):
        self.assertEqual(self.calculator.subtract(2), -2)
        self.assertEqual(self.calculator.subtract(1), -3)

    def test_multiplication_with_memory(self):
        self.assertEqual(self.calculator.multiply(4), 0)

    def test_division_with_memory(self):
        self.assertEqual(self.calculator.divide(2), 0)
        self.assertEqual(self.calculator.divide(0), "Error! Division by zero.")

    def test_nth_root_with_negative_memory(self):
        self.calculator.memory = -8  # Set initial memory value to -8
        with self.assertRaises(ValueError) as context:
            self.calculator.nth_root(2)  # Attempt to calculate nth root with negative memory
        self.assertEqual(str(context.exception), "Cannot calculate nth root of a negative number.")
    
    def test_nth_root_with_memory(self):
        self.assertEqual(self.calculator.add(9), 9)  # Add positive number to memory
        self.assertEqual(self.calculator.nth_root(2), 3)  # Test nth root with positive memory (memory = 9, 2nd root of 9 is 3)

    def test_reset_memory(self):
        self.assertEqual(self.calculator.add(10), 10)  # Add 10 to memory
        self.assertEqual(self.calculator.reset_memory(), "Memory reset to 0.")  # Reset memory
        self.assertEqual(self.calculator.add(5), 5)  # Test add with reset memory (memory = 0 + 5)

if __name__ == "__main__":
    unittest.main()
