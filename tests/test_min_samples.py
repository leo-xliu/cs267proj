# import unittest
# from src.ppl_ast import *
# from src.inference import pr
# import matplotlib.pyplot as plt

# algs = ["rejection_sampling", "importance_sampling", "mcmc"]

# class TestMinSamples(unittest.TestCase):
#     # how many samples needed to estimate the target probability
#     def test_min_samples(self):
#         program = """
#             x = flip(0.001)
#             y = flip(0.001)
#             observe(x or y)
#             x
#         """
#         target = 0.001 / 0.001999
#         nsamples_list = [1000, 10000, 50000, 100000, 500000]
#         nruns = 10
#         avg_delta = {alg: {nsample: 0.0 for nsample in nsamples_list} for alg in algs}

#         for alg in algs:
#             # try different samples of n
#             for nsamples in nsamples_list:
#                 # take average across 10 runs
#                 for i in range(nruns):
#                     print(f"alg={alg}, nsamples={nsamples}, run={i}")
#                     res = pr(program, inference=alg, n=nsamples, debug=False)
#                     avg_delta[alg][nsamples] += abs(target - res)
#                 avg_delta[alg][nsamples] /= nruns

#         print(f"\navg_delta = {avg_delta}\n")

#         plt.figure(figsize=(12,6))

#         for alg, samples_dict in avg_delta.items():
#             nsamples = sorted(samples_dict.keys())
#             deltas = [samples_dict[n] for n in nsamples]
#             plt.plot(nsamples, deltas, marker='o', label=alg)

#             for x, y in zip(nsamples, deltas):
#                 plt.text(x * 1.05, y * 1.05, f"{y:.4f}", fontsize=8, ha='left', va='center')

#         plt.xscale('log')
#         plt.xlabel('Number of Samples (log scale)')
#         plt.ylabel('Average Delta')
#         plt.title('Average Delta vs Number of Samples for different Inference Algorithms')
#         plt.legend()
#         plt.grid(True, which="both", ls="--", linewidth=0.5)
#         plt.tight_layout()

#         plt.savefig('avg_delta_plot.png')
#         plt.close()

# if __name__ == "__main__":
#     unittest.main()