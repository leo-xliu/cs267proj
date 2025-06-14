# Unit testing for parser
import unittest
from src.ppl_parser import Parser
from src.tokenizer import tokenize
from src.ppl_ast import *

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()
        
    def parse(self, src: str):
        tokens = tokenize(src)
        return self.parser.parse(tokens)

    def test_boolean(self):
        ast = self.parse("True\n")
        self.assertEqual(len(ast), 1)
        node = ast[0]
        self.assertEqual(node, True)

        ast = self.parse("False\n")
        self.assertEqual(len(ast), 1)
        node = ast[0]
        self.assertEqual(node, False)

    def test_variable(self):
        ast = self.parse("x\n")
        node = ast[0]
        self.assertIsInstance(node, Variable)
        self.assertEqual(node.name, "x")



if __name__ == "__main__":
    unittest.main()