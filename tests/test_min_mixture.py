import unittest
from src.ppl_ast import *
from src.inference import pr
import matplotlib.pyplot as plt
from src.ppl_parser import Parser
from src.tokenizer import tokenize
from src.inference import markov_chain_monte_carlo_metropolis_hastings

class TestMinMixture(unittest.TestCase):
    # program0 in test_end2end
    def test_min_samples(self):
        program = """
            x = flip(0.01)
            y = if x then flip(0.5) else flip(0.2)
            observe(x or y)
            x
        """
        target = 0.01 / (0.01 + 0.99*0.2)
        nsamples = 10000
        nruns = 25
        mixtures = [0.7, 0.75, 0.8, 0.85, 0.9, 0.935, 0.975, 1]
        avg_delta = {mix: 0.0 for mix in mixtures}

        parser = Parser()
        tokens = tokenize(program)
        parsed_program, nflips = parser.parse(tokens)

        for mix in mixtures:
            for i in range(nruns):
                print(f"mix={mix}, run={i}")
                res = markov_chain_monte_carlo_metropolis_hastings(parsed_program, nsamples, nflips=nflips, mix=mix)
                avg_delta[mix] += abs(target - res)
            avg_delta[mix] /= nruns

        print(f"\navg_delta = {avg_delta}\n")

        plt.figure(figsize=(12,6))

        x_vals = sorted(avg_delta.keys())
        y_vals = [avg_delta[x] for x in x_vals]
        plt.plot(x_vals, y_vals, marker='o')
        # Annotate
        for mix, avg in zip(x_vals, y_vals):
            plt.text(mix, avg * 0.68, f"({mix}, {avg:.4f})", fontsize=8, ha='left', va='center')

        plt.xscale('log')
        # Mixture of local and block updates
        plt.xlabel('Mixture proposal probability')
        plt.ylabel('Average Delta')
        plt.title('Average Delta vs Mixture proposal probability')
        plt.grid(True, which="both", ls="--", linewidth=0.5)
        plt.tight_layout()

        plt.savefig('mixture_avg_delta_plot.png')
        plt.close()

if __name__ == "__main__":
    unittest.main()