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

    def testFullProgram(self):
        program = """
        x = flip(0.5)
        if x then flip(0.5) else y
        observe(x)
        x or y
        x and y
        not x
        x = True
        x = False
        """
        res = tokenize(program)
        self.assertEqual(res[0][0], "NEWLINE")
        self.assertEqual(res[1][0], "VAR")
        self.assertEqual(res[1][1], "x")
        self.assertEqual(res[2][0], "ASSIGN")
        self.assertEqual(res[3][0], "FLIP")
        self.assertEqual(res[4][0], "LPAREN")
        self.assertEqual(res[5][0], "NUMBER")
        self.assertEqual(res[5][1], "0.5")
        self.assertEqual(res[6][0], "RPAREN")

if __name__ == "__main__":
    unittest.main()