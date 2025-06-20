# Unit testing for interpreter
import unittest
from src.ppl_ast import *
from src.ppl_interpreter import Interpreter

# safe to assume only a valid AST is passed (?)

class TestInterpreter(unittest.TestCase):
    def test_eval_flip_method(self):
        self.assertEqual(Interpreter().eval_flip(Flip(1)), True)
        self.assertEqual(Interpreter().eval_flip(Flip(0)), False)

        # Do not need to test for invalid Flip objects since checked in Flip class
        self.assertEqual(type(Interpreter().eval_flip(Flip(0.5))), bool)

    def test_eval_variable(self):
        interpreter = Interpreter()
        interpreter.vars["x"] = True
        interpreter.vars["y"] = False
        self.assertEqual(interpreter.eval_variable(Variable("x")), True)
        self.assertEqual(interpreter.eval_variable(Variable("y")), False)
        
        # Not in dict
        self.assertRaises(NameError, interpreter.eval_variable, Variable("z"))
        self.assertRaises(TypeError, interpreter.eval_variable, "x")

    # Update eval testing to include second expression
    def test_eval_assign_method(self):
        interpreter = Interpreter()
        interpreter.eval_assign(Assign(Variable("x"), Flip(0.5), 
                                       Assign(Variable("y"), True, 
                                              Assign(Variable("z"), False, True))))

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
        self.assertRaises(NotImplementedError, interpreter.eval_assign, Assign(Variable("a"), "to a string", True))

        # Invalid Variable type 
        with self.assertRaises(TypeError):
            interpreter.eval_assign(Assign("a", "to a string", True))

    def test_eval_statement(self):
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
                self.assertEqual(interpreter.eval_statement(expr, True), expected)

        # Test eval_bool failure 
        self.assertRaises(NotImplementedError, interpreter.eval_statement, "string cannot be boolean", True)

    def test_eval_program(self):
        pass        

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

    def test_eval_conditional(self):
        interpreter = Interpreter()
        self.assertEqual(interpreter.eval_conditional(Conditional(True, False, True)), False)
        self.assertEqual(interpreter.eval_conditional(Conditional(False, False, True)), True)

        interpreter.vars["x"] = True
        self.assertEqual(interpreter.eval_conditional(Conditional(Variable("x"), False, True)), False)
        interpreter.vars["y"] = False
        self.assertEqual(interpreter.eval_conditional(Conditional(Variable("y"), False, True)), True)
        self.assertEqual(interpreter.eval_conditional(Conditional(True, Variable("y"), Variable("x"))), False)

        # Nested conditional
        nested_cond = Conditional(True, False, True)
        self.assertEqual(interpreter.eval_conditional(Conditional(True, nested_cond, True)), False)
        self.assertEqual(interpreter.eval_conditional(Conditional(False, True, nested_cond)), False)

        # Support Flips
        self.assertEqual(type(interpreter.eval_conditional(Conditional(Flip(0.5), Flip(0.5), Flip(0.5)))), bool)

        # Support boolean operators
        self.assertEqual(interpreter.eval_conditional(Conditional(Or(True, False), And(True, False), Or(True, False))), False)


    def test_run_method(self):
        ast = [Assign(Variable("x"), True,
                      Assign(Variable("y"), False,
                            Assign(Variable("z"), Flip(1), 
                                   Variable("x"))))]
        self.assertEqual(Interpreter().run(ast), True)

if __name__ == "__main__":
    unittest.main()