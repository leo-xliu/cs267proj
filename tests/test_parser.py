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
        ast, _ = self.parse("True\n")
        self.assertEqual(len(ast), 1)
        node = ast[0]
        self.assertEqual(node, True)

        ast, _ = self.parse("False\n")
        self.assertEqual(len(ast), 1)
        node = ast[0]
        self.assertEqual(node, False)

    def test_variable(self):
        ast, _ = self.parse("x\n")
        node = ast[0]
        self.assertIsInstance(node, Variable)
        self.assertEqual(node.name, "x")

    def test_flip(self):
        ast, _ = self.parse("flip(0.25)\n")
        node = ast[0]
        self.assertIsInstance(node, Flip)
        self.assertEqual(node.prob, 0.25)

    def test_conditional(self):
        ast, _ = self.parse("if True then False else True\n")
        node = ast[0]
        self.assertIsInstance(node, Conditional)
        self.assertEqual(node.bool_cond, True)
        self.assertEqual(node.if_path, False)
        self.assertEqual(node.else_path, True)

    def test_boolean_operators(self):
        ast, _ = self.parse("not True and False or x\n")
        node = ast[0]
        self.assertIsInstance(node, Or)
        self.assertIsInstance(node.l_expr, And)
        self.assertIsInstance(node.l_expr.l_expr, Not)
        self.assertEqual(node.l_expr.l_expr.expr, True)
        self.assertEqual(node.l_expr.r_expr, False)
        self.assertIsInstance(node.r_expr, Variable)
        self.assertEqual(node.r_expr.name, "x")

    def test_paren_boolean_expr(self):
        ast, _ = self.parse("(not True) and (False or x)\n")
        node = ast[0]
        self.assertIsInstance(node, And)
        self.assertIsInstance(node.l_expr, Not)
        self.assertIsInstance(node.l_expr.expr, bool)
        self.assertEqual(node.l_expr.expr, True)
        self.assertIsInstance(node.r_expr, Or)
        self.assertIsInstance(node.r_expr.l_expr, bool)
        self.assertIsInstance(node.r_expr.r_expr, Variable)
        self.assertEqual(node.r_expr.l_expr, False)
        self.assertEqual(node.r_expr.r_expr.name, "x")

    def test_observe(self):
        ast, _ = self.parse("observe(x)\n")
        node = ast[0]
        self.assertIsInstance(node, Observe)
        self.assertIsInstance(node.expr, Variable)
        self.assertEqual(node.expr.name, "x")

    def test_assign(self):
        ast, _ = self.parse("x = flip(0.5)\nTrue\n")
        node = ast[0]
        self.assertIsInstance(node, Assign)
        self.assertEqual(node.var_node.name, "x")
        self.assertIsInstance(node.expr, Flip)
        self.assertIsInstance(node.next_expr, bool)
        self.assertEqual(node.next_expr, True)

    def test_full_program(self):
        ast, _ = self.parse("x = True\ny = flip(0.5)\nx = if x then y else False\nobserve(x)\nx and y\n")
        node = ast[0]
        self.assertIsInstance(node, Assign)
        self.assertIsInstance(node.var_node, Variable)
        self.assertEqual(node.var_node.name, "x")
        self.assertEqual(node.expr, True)
        self.assertIsInstance(node.next_expr, Assign)
        self.assertIsInstance(node.next_expr.var_node, Variable)
        self.assertIsInstance(node.next_expr.expr, Flip)
        self.assertEqual(node.next_expr.var_node.name, "y")
        self.assertEqual(node.next_expr.expr.prob, 0.5)
        self.assertIsInstance(node.next_expr.next_expr, Assign)
        self.assertIsInstance(node.next_expr.next_expr.var_node, Variable)
        self.assertEqual(node.next_expr.next_expr.var_node.name, "x")
        self.assertIsInstance(node.next_expr.next_expr.expr, Conditional)
        self.assertIsInstance(node.next_expr.next_expr.expr.bool_cond, Variable)
        self.assertEqual(node.next_expr.next_expr.expr.bool_cond.name, "x")
        self.assertIsInstance(node.next_expr.next_expr.expr.if_path, Variable)
        self.assertEqual(node.next_expr.next_expr.expr.if_path.name, "y")
        self.assertEqual(node.next_expr.next_expr.expr.else_path, False)
        self.assertIsInstance(node.next_expr.next_expr.next_expr, Observe)
        self.assertEqual(node.next_expr.next_expr.next_expr.expr.name, "x")
        node = ast[1]
        self.assertIsInstance(node, And)
        self.assertIsInstance(node.l_expr, Variable)
        self.assertIsInstance(node.r_expr, Variable)
        self.assertEqual(node.l_expr.name, "x")
        self.assertEqual(node.r_expr.name, "y")

if __name__ == "__main__":
    unittest.main()