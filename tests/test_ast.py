import unittest
from src.ppl_ast import *

class TestASTComponents(unittest.TestCase):
    def test_assign_object_initialization(self):
        pass

    def test_flip_object_initialization(self):
        # Assigning valid probabilities
        self.assertEqual(Flip(0.5).prob, 0.5)
        self.assertEqual(Flip(0).prob, 0)
        self.assertEqual(Flip(1).prob, 1)

        # Invalid probabilities 
        self.assertRaises(TypeError, Flip, "string")
        self.assertRaises(ValueError, Flip, 100)
        self.assertRaises(ValueError, Flip, -0.5)

    def test_or_object_initialization(self):
        pass

    def test_and_object_initialization(self):
        pass

    def test_not_object_initialization(self):
        pass

    def test_variable_initialization(self):
        pass

    def test_observe_initialization(self):
        pass

    def test_conditional_initialization(self):
        pass

if __name__ == "__main__":
    unittest.main()
