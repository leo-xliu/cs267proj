import unittest
from src.inference import rejection_sampling, pr
from src.ppl_ast import *

class TestRejectionSampling(unittest.TestCase):
    def test_simple_program(self):
        parsed_program = [Flip(0.5)]
        self.assertAlmostEqual(rejection_sampling(parsed_program, 30000), 0.5, delta=0.01)

    def test_observe_program(self):
        parsed_program = [Assign(Variable("x"), Flip(0.5), Observe(Variable("x"))), Variable("x")]
        self.assertAlmostEqual(rejection_sampling(parsed_program, 30000), 1, delta=0.01)

    # parser implemented
    def test_parser(self):
        program = """
            x = flip(0.01)
            y = if x then flip(0.5) else flip(0.2)
            observe(x or y)
            x
        """
        # 0.01 / 0.01 + 0.99*0.2 = 0.0488
        res = pr(program, debug=False)
        self.assertAlmostEqual(res, 0.01 / (0.01 + 0.99*0.2), delta=0.03)
