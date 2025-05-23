import unittest
from src.ast import Assign, Return, Flip

class TestASTComponents(unittest.TestCase):
    def test_assign_object_initialization(self):
        pass

    def test_return_object_initialization(self):
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

if __name__ == "__main__":
    unittest.main()
