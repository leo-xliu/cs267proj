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
        interpreter.eval_assign(Assign("x", Flip(0.5)))
        interpreter.eval_assign(Assign("y", True))
        interpreter.eval_assign(Assign("z", False))

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
        self.assertRaises(NotImplementedError, interpreter.eval_assign, Assign("a", "to a string"))

    def test_eval_return_method(self):
        interpreter = Interpreter()
        interpreter.vars["x"] = True

        # Check nonexisting variable
        self.assertRaises(NameError, interpreter.eval_return, Return("y"))

        # Check existing variable
        self.assertEqual(interpreter.eval_return(Return("x")), True)

    def test_run_method(self):
        ast = [Assign("x", True), Assign("y", False), Assign("z", Flip(1)), Return("x")]
        self.assertEqual(Interpreter().run(ast), True)


if __name__ == "__main__":
    unittest.main()