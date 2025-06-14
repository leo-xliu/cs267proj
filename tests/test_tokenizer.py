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

        self.assertEqual(res[7][0], "NEWLINE")

        self.assertEqual(res[8][0], "IF")
        self.assertEqual(res[9][0], "VAR")
        self.assertEqual(res[9][1], "x")
        self.assertEqual(res[10][0], "THEN")
        self.assertEqual(res[11][0], "FLIP")
        self.assertEqual(res[12][0], "LPAREN")
        self.assertEqual(res[13][0], "NUMBER")
        self.assertEqual(res[13][1], "0.5")
        self.assertEqual(res[14][0], "RPAREN")
        self.assertEqual(res[15][0], "ELSE")
        self.assertEqual(res[16][0], "VAR")
        self.assertEqual(res[16][1], "y")

        self.assertEqual(res[17][0], "NEWLINE")

        self.assertEqual(res[18][0], "OBSERVE")
        self.assertEqual(res[19][0], "LPAREN")
        self.assertEqual(res[20][0], "VAR")
        self.assertEqual(res[20][1], "x")
        self.assertEqual(res[21][0], "RPAREN")

        self.assertEqual(res[22][0], "NEWLINE")

        self.assertEqual(res[23][0], "VAR")
        self.assertEqual(res[23][1], "x")
        self.assertEqual(res[24][0], "OR")
        self.assertEqual(res[25][0], "VAR")
        self.assertEqual(res[25][1], "y")

        self.assertEqual(res[26][0], "NEWLINE")

        self.assertEqual(res[27][0], "VAR")
        self.assertEqual(res[27][1], "x")
        self.assertEqual(res[28][0], "AND")
        self.assertEqual(res[29][0], "VAR")
        self.assertEqual(res[29][1], "y")

        self.assertEqual(res[30][0], "NEWLINE")

        self.assertEqual(res[31][0], "NOT")
        self.assertEqual(res[32][0], "VAR")
        self.assertEqual(res[32][1], "x")

        self.assertEqual(res[33][0], "NEWLINE")

        self.assertEqual(res[34][0], "VAR")
        self.assertEqual(res[34][1], "x")
        self.assertEqual(res[35][0], "ASSIGN")
        self.assertEqual(res[36][0], "BOOLEAN")
        self.assertEqual(res[36][1], "True")

        self.assertEqual(res[37][0], "NEWLINE")

        self.assertEqual(res[38][0], "VAR")
        self.assertEqual(res[38][1], "x")
        self.assertEqual(res[39][0], "ASSIGN")
        self.assertEqual(res[40][0], "BOOLEAN")
        self.assertEqual(res[40][1], "False")

    def testExampleProgram(self):
        program = """
        S1 = True
        route = flip(0.5)
        S2 = if route then S1 else False
        S3 = if route then False else S2
        S4 = (S2 and not flip(0.01)) or (S3 and not flip(0.001))
        observe(not S4)
        S2
        """
        res = tokenize(program)
        
        self.assertEqual(res[0][0], "NEWLINE")
        self.assertEqual(res[1][0], "VAR")
        self.assertEqual(res[1][1], "S1")
        self.assertEqual(res[2][0], "ASSIGN")
        self.assertEqual(res[3][0], "BOOLEAN")
        self.assertEqual(res[3][1], "True")

        self.assertEqual(res[4][0], "NEWLINE")
        self.assertEqual(res[5][0], "VAR")
        self.assertEqual(res[5][1], "route")
        self.assertEqual(res[6][0], "ASSIGN")
        self.assertEqual(res[7][0], "FLIP")
        self.assertEqual(res[8][0], "LPAREN")
        self.assertEqual(res[9][0], "NUMBER")
        self.assertEqual(res[9][1], "0.5")
        self.assertEqual(res[10][0], "RPAREN")

        # S2 = if route then S1 else False
        self.assertEqual(res[11][0], "NEWLINE")
        self.assertEqual(res[12][0], "VAR")
        self.assertEqual(res[12][1], "S2")
        self.assertEqual(res[13][0], "ASSIGN")
        self.assertEqual(res[14][0], "IF")
        self.assertEqual(res[15][0], "VAR")
        self.assertEqual(res[15][1], "route")
        self.assertEqual(res[16][0], "THEN")
        self.assertEqual(res[17][0], "VAR")
        self.assertEqual(res[17][1], "S1")
        self.assertEqual(res[18][0], "ELSE")
        self.assertEqual(res[19][0], "BOOLEAN")
        self.assertEqual(res[19][1], "False")

        # S3 = if route then False else S2
        self.assertEqual(res[20][0], "NEWLINE")
        self.assertEqual(res[21][0], "VAR")
        self.assertEqual(res[21][1], "S3")
        self.assertEqual(res[22][0], "ASSIGN")
        self.assertEqual(res[23][0], "IF")
        self.assertEqual(res[24][0], "VAR")
        self.assertEqual(res[24][1], "route")
        self.assertEqual(res[25][0], "THEN")
        self.assertEqual(res[26][0], "BOOLEAN")
        self.assertEqual(res[26][1], "False")
        self.assertEqual(res[27][0], "ELSE")
        self.assertEqual(res[28][0], "VAR")
        self.assertEqual(res[28][1], "S2")

        # S4 = (S2 and not flip(0.01)) or (S3 and not flip(0.001))
        self.assertEqual(res[29][0], "NEWLINE")
        self.assertEqual(res[30][0], "VAR")
        self.assertEqual(res[30][1], "S4")
        self.assertEqual(res[31][0], "ASSIGN")
        self.assertEqual(res[32][0], "LPAREN")
        self.assertEqual(res[33][0], "VAR")
        self.assertEqual(res[33][1], "S2")
        self.assertEqual(res[34][0], "AND")
        self.assertEqual(res[35][0], "NOT")
        self.assertEqual(res[36][0], "FLIP")
        self.assertEqual(res[37][0], "LPAREN")
        self.assertEqual(res[38][0], "NUMBER")
        self.assertEqual(res[38][1], "0.01")
        self.assertEqual(res[39][0], "RPAREN")
        self.assertEqual(res[40][0], "RPAREN")
        self.assertEqual(res[41][0], "OR")
        self.assertEqual(res[42][0], "LPAREN")
        self.assertEqual(res[43][0], "VAR")
        self.assertEqual(res[43][1], "S3")
        self.assertEqual(res[44][0], "AND")
        self.assertEqual(res[45][0], "NOT")
        self.assertEqual(res[46][0], "FLIP")
        self.assertEqual(res[47][0], "LPAREN")
        self.assertEqual(res[48][0], "NUMBER")
        self.assertEqual(res[48][1], "0.001")
        self.assertEqual(res[49][0], "RPAREN")
        self.assertEqual(res[50][0], "RPAREN")
        
        # observe(not S4)
        self.assertEqual(res[51][0], "NEWLINE")
        self.assertEqual(res[52][0], "OBSERVE")
        self.assertEqual(res[53][0], "LPAREN")
        self.assertEqual(res[54][0], "NOT")
        self.assertEqual(res[55][0], "VAR")
        self.assertEqual(res[55][1], "S4")
        self.assertEqual(res[56][0], "RPAREN")

        # S2
        self.assertEqual(res[57][0], "NEWLINE")
        self.assertEqual(res[58][0], "VAR")
        self.assertEqual(res[58][1], "S2")
        self.assertEqual(res[59][0], "NEWLINE")
        self.assertEqual(res[60][0], "EOP")

if __name__ == "__main__":
    unittest.main()