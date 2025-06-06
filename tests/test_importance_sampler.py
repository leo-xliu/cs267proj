# Unit testing for importance sampling
import unittest
from src.ppl_ast import *
from src.inference import importance_sampling_inference

class TestInterpreter(unittest.TestCase):

    def test_eval_program1(self):
        parsed_program = [
            Assign(Variable("x"), Flip(0.6)),
            Assign(Variable("y"), Flip(0.3)),
            Return(Or(Variable("x"), Variable("y")))
        ]
        res = importance_sampling_inference(parsed_program, 10000)
        self.assertAlmostEqual(res, 0.72, places=2)

    def test_eval_program2(self):
        parsed_program = [
            Assign(Variable("x"), Flip(0.6)),
            Assign(Variable("y"), Or(Variable("x"), Flip(0.7))),
            Return(Or(Variable("x"), Variable("y")))
        ]
        res = importance_sampling_inference(parsed_program, 10000)
        self.assertAlmostEqual(res, 0.88, places=2)

    def test_eval_program3(self):
        # x = True, y = false, z = true  ==> 0.6 * 0.6
        # x = False, y = false, z = true ==> 0.4 * 0.3
        parsed_program = [
            Assign(Variable("x"), Flip(0.6)),
            Conditional(Variable("x"), Assign(Variable("y"), Flip(0.4)), Assign(Variable("y"), Flip(0.7))),
            Assign(Variable("z"), Not(Variable("y"))),
            Return(Variable("z"))
        ]
        res = importance_sampling_inference(parsed_program, 10000)
        self.assertAlmostEqual(res, 0.36 + 0.12, places=2)

if __name__ == "__main__":
    unittest.main()