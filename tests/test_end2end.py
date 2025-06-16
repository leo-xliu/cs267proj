import unittest
from src.ppl_ast import *
from src.inference import pr

algs = ["rejection_sampling", "importance_sampling", "mcmc"]

class TestInterpreter(unittest.TestCase):
    def test_eval_program0_revised(self):
        program = """
            x = flip(0.6)
            y = if x then flip(0.5) else flip(0.2)
            observe(x or y)
            x
        """
        target = 0.6 / (0.6 + 0.4*0.2)
        for alg in algs:
            res = pr(program, inference=alg, n=10000, debug=False)
            self.assertAlmostEqual(res, target, delta=0.05, msg=f"{alg}: Expected {target:.5f}, but got {res:.5f}")

    def test_eval_program0(self):
        program = """
            x = flip(0.01)
            y = if x then flip(0.5) else flip(0.2)
            observe(x or y)
            x
        """
        target = 0.01 / (0.01 + 0.99*0.2)
        for alg in algs:
            res = pr(program, inference=alg, n=10000, debug=False)
            self.assertAlmostEqual(res, target, delta=0.05, msg=f"{alg}: Expected {target:.5f}, but got {res:.5f}")
    
    def test_eval_program1(self):
        program = """
            x = flip(0.6)
            y = flip(0.3)
            x or y
        """
        target = 0.72
        for alg in algs:
            res = pr(program, inference=alg, n=10000, debug=False)
            self.assertAlmostEqual(res, target, delta=0.05, msg=f"{alg}: Expected {target:.5f}, but got {res:.5f}")

    def test_eval_program2(self):
        program = """
            S1 = True
            route = flip(0.5)
            S2 = if route then S1 else False
            S3 = if route then False else S1
            S4 = (S2 and not flip(0.01)) or (S3 and not flip(0.001))
            observe(not S4)
            S2
        """
        target = (0.5 * 0.01) / (0.5 * (0.01 + 0.001))
        for alg in algs[1:]:
            res = pr(program, inference=alg, n=10000, debug=False)
            self.assertAlmostEqual(res, target, delta=0.05, msg=f"{alg}: Expected {target:.5f}, but got {res:.5f}")

    def test_eval_program3(self):
        # x = True, y = false, z = true  ==> 0.6 * 0.6
        # x = False, y = false, z = true ==> 0.4 * 0.3
        program = """
            x = flip(0.6)
            y = if x then flip(0.4) else flip(0.7)
            z = not y
            z
        """
        target = 0.36 + 0.12
        for alg in algs:
            res = pr(program, inference=alg, n=10000, debug=False)
            self.assertAlmostEqual(res, target, delta=0.05, msg=f"{alg}: Expected {target:.5f}, but got {res:.5f}")

    def test_eval_program4(self):
        program = """
            x = flip(0.6)
            y = if x then flip(0.4) else flip(0.7)
            x = if y then False else x
            x
        """
        target = 0.36
        for alg in algs:
            res = pr(program, inference=alg, n=10000, debug=False)
            self.assertAlmostEqual(res, target, delta=0.05, msg=f"{alg}: Expected {target:.5f}, but got {res:.5f}")
    
    def test_eval_program5(self):
        # 1 - 0.4*0.2 = 1 - 0.08 = 0.92
        program = """
            x = flip(0.6)
            y = flip(0.8)
            observe(x or y)
            x
        """
        target = 0.6 / 0.92
        for alg in algs:
            res = pr(program, inference=alg, n=10000, debug=False)
            self.assertAlmostEqual(res, 0.6 / 0.92, delta=0.05, msg=f"{alg}: Expected {target:.5f}, but got {res:.5f}")

    def test_eval_program6(self):
        # 1 - 0.999 * 0.999 = 0.001999
        program = """
            x = flip(0.001)
            y = flip(0.001)
            observe(x or y)
            x
        """
        for alg in algs:
            res = pr(program, inference=alg, n=10000, debug=False)
            self.assertAlmostEqual(res, 0.001 / 0.001999, delta=0.05, msg=f"{alg}: Expected {0.001 / 0.001999:.5f}, but got {res:.5f}")

    def test_eval_program7(self):
        program = """
            x = flip(0.5)
            y = if x then flip(0.7) else flip(0.4)
            observe(x or y)
            x = if y then flip(0.9) else flip(0.2)
            observe(x)
            x
        """
        target = 1.0
        for alg in algs:
            res = pr(program, inference=alg, n=10000, debug=False)
            self.assertAlmostEqual(res, target, delta=0.05, msg=f"{alg}: Expected {target:.5f}, but got {res:.5f}")

    def test_eval_program8(self):
        program = """
            x = flip(0.5)
            y = if x then flip(0.7) else flip(0.4)
            observe(x or y)
            x = if y then flip(0.9) else flip(0.2)
            x
        """
        target = 0.75
        for alg in algs:
            res = pr(program, inference=alg, n=10000, debug=False)
            self.assertAlmostEqual(res, target, delta=0.05, msg=f"{alg}: Expected {target:.5f}, but got {res:.5f}")

    def test_eval_program9(self):
        program = """
            x = flip(0.5)
            y = if x then flip(0.7) else flip(0.4)
            observe(x or y)
            z = if not y then flip(0.01) else flip(0.01)
            z
        """
        # (x, y, z) = (T, T, T) = 0.5 * 0.7 * 0.01 = 0.0035
        # (x, y, z) = (T, T, F) = 0.5 * 0.7 * 0.99 = 0.3465
        # (x, y, z) = (T, F, T) = 0.5 * 0.3 * 0.01 = 0.0015
        # (x, y, z) = (T, F, F) = 0.5 * 0.3 * 0.99 = 0.1485
        # (x, y, z) = (F, T, T) = 0.5 * 0.4 * 0.01 = 0.002
        # (x, y, z) = (F, T, F) = 0.5 * 0.4 * 0.99 = 0.198
        target = (0.0035 + 0.0015 + 0.002) / (0.0035 + 0.0015 + 0.002 + 0.3465 + 0.1485 + 0.198)
        for alg in algs:
            res = pr(program, inference=alg, n=10000, debug=False)
            self.assertAlmostEqual(res, target, delta=0.05, msg=f"{alg}: Expected {target:.5f}, but got {res:.5f}")

if __name__ == "__main__":
    unittest.main()