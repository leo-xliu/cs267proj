# Unit testing for interpreter
import unittest
from src.ppl_ast import *
from src.ppl_interpreter import Interpreter

# safe to assume only a valid AST is passed (?)

class TestInterpreter(unittest.TestCase):
    def test_eval_flip_method(self):
        # Do not need to test for invalid Flip objects since checked in Flip class
        self.assertEqual(type(Interpreter().eval_flip(Flip(0.5))), bool)

    def test_eval_assign_method(self):
        interpreter = Interpreter()
        interpreter.eval_assign(Assign(Variable("x"), Flip(0.5)))
        interpreter.eval_assign(Assign(Variable("y"), True))
        interpreter.eval_assign(Assign(Variable("z"), False))

        # Check existence of x
        self.assertIn("x", interpreter.vars)
        self.assertIn("y", interpreter.vars)
        self.assertIn("z", interpreter.vars)

        # Check that assigning a flip results in a boolean
        # Cannot determine actual value since eval_flip uses random
        self.assertEqual(type(interpreter.vars["x"]), bool)
        self.assertEqual(interpreter.vars["y"], True)
        self.assertEqual(interpreter.vars["z"], False)

        # Invalid Assignment 
        self.assertRaises(NotImplementedError, interpreter.eval_assign, Assign(Variable("a"), "to a string"))

        # Invalid Variable type 
        self.assertRaises(TypeError, interpreter.eval_assign, Assign("a", "to a string"))

    def test_eval_variable(self):
        pass

    def test_eval_return_method(self):
        interpreter = Interpreter()
        interpreter.vars["x"] = True

        # Check nonexisting variable
        self.assertRaises(NameError, interpreter.eval_return, Return(Variable("y")))

        # Check existing variable
        self.assertEqual(interpreter.eval_return(Return(Variable("x"))), True)

    def test_eval_or_basic(self):
        interpreter = Interpreter()
        cases = [
            (False, False, False), 
            (False, True, True),
            (True, False, True),
            (True, True, True),
        ]

        for l_expr, r_expr, expected in cases:
            with self.subTest(l_expr=l_expr, r_expr=r_expr):
                self.assertEqual(interpreter.eval_or(Or(l_expr, r_expr)), expected)

    def test_eval_and_basic(self):
        interpreter = Interpreter()
        cases = [
            (False, False, False), 
            (False, True, False),
            (True, False, False),
            (True, True, True),
        ]

        for l_expr, r_expr, expected in cases:
            with self.subTest(l_expr=l_expr, r_expr=r_expr):
                self.assertEqual(interpreter.eval_and(And(l_expr, r_expr)), expected)

    def test_eval_not_basic(self):
        interpreter = Interpreter()
        cases = [
            (False, True), 
            (True, False),
        ]

        for expr, expected in cases:
            with self.subTest(expr=expr):
                self.assertEqual(interpreter.eval_not(Not(expr)), expected)

    def test_eval_bool(self):
        interpreter = Interpreter()

        # Add test cases here 
        cases = [
            (Flip(1), True),
            (Flip(0), False),
            (True, True),
            (False, False),
            (Or(False, False), False),
            (Or(False, True), True),
            (Or(True, False), True),
            (Or(True, True), True),
            (And(False, False), False),
            (And(False, True), False),
            (And(True, False), False),
            (And(True, True), True),
            (Not(True), False),
            (Not(False), True),
        ]

        for expr, expected in cases:
            with self.subTest(expr=expr):
                self.assertEqual(interpreter.eval_bool(expr), expected)

        # Test eval_bool failure 
        self.assertRaises(NotImplementedError, interpreter.eval_bool, "string cannot be boolean")

    def test_eval_or_complex(self):
        interpreter = Interpreter()
        cases = [
            (Or(True, False), Or(False, True), True), 
            (Or(False, False), Or(False, False), False),
            (And(True, False), And(True, True), True),
            (And(True, False), And(True, False), False),
            (And(True, False), Or(True, False), True),
            (And(False, False), Or(False, False), False),
            (Not(True), Not(False), True),
            (Not(True), Not(True), False),
            (And(Not(False), True), Or(Not(True), False), True),
        ]

        for l_expr, r_expr, expected in cases:
            with self.subTest(l_expr=l_expr, r_expr=r_expr):
                self.assertEqual(interpreter.eval_or(Or(l_expr, r_expr)), expected)

        # Expression uses Flip
        self.assertEqual(type(interpreter.eval_or(Or(Flip(0.1), Flip(0.9)))), bool)


    def test_eval_and_complex(self):
        interpreter = Interpreter()
        cases = [
            (Or(True, False), Or(False, True), True), 
            (Or(False, False), Or(False, False), False),
            (And(True, False), And(True, True), False),
            (And(True, False), And(True, False), False),
            (And(True, False), Or(True, False), False),
            (And(False, False), Or(False, False), False),
            (Not(True), Not(False), False),
            (Not(True), Not(True), False),
            (And(Not(False), True), Or(Not(True), False), False),
        ]

        for l_expr, r_expr, expected in cases:
            with self.subTest(l_expr=l_expr, r_expr=r_expr):
                self.assertEqual(interpreter.eval_and(And(l_expr, r_expr)), expected)

        # Expression uses Flip
        self.assertEqual(type(interpreter.eval_and(And(Flip(0.1), Flip(0.9)))), bool)

    def test_eval_not_complex(self):
        interpreter = Interpreter()
        cases = [
            (Not(Not(Not(True))), True),
            (And(True, True), False),
            (And(True, False), True),
            (Or(True, False), False),
            (Or(False, False), True),
        ]

        for expr, expected in cases:
            with self.subTest(expr=expr):
                self.assertEqual(interpreter.eval_not(Not(expr)), expected)

        # Expression uses Flip
        self.assertEqual(type(interpreter.eval_not(Not(Flip(0.1)))), bool)

    def test_run_method(self):
        ast = [Assign(Variable("x"), True), Assign(Variable("y"), False), Assign(Variable("z"), Flip(1)), Return(Variable("x"))]
        self.assertEqual(Interpreter().run(ast), True)


if __name__ == "__main__":
    unittest.main()