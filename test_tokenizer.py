import unittest
from src.tokenizer import tokenize

class TestTokenize(unittest.TestCase):
    def testBooleanToken(self):
        res = tokenize("True")[0]
        self.assertEqual(res[0], "BOOLEAN")
        self.assertEqual(res[1], "True")

        res = tokenize("False")[0]
        self.assertEqual(res[0], "BOOLEAN")
        self.assertEqual(res[1], "False")

        res = tokenize("    True     ")[0]
        self.assertEqual(res[0], "BOOLEAN")
        self.assertEqual(res[1], "True")

        res = tokenize("    True    False ")
        self.assertEqual(res[0][0], "BOOLEAN")
        self.assertEqual(res[0][1], "True")
        self.assertEqual(res[1][0], "BOOLEAN")
        self.assertEqual(res[1][1], "False")

        self.assertRaises(SyntaxError, tokenize, "TrueFalse")


if __name__ == "__main__":
    unittest.main()