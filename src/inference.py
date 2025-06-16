from src.ppl_parser import Parser
from src.tokenizer import tokenize
from src.ppl_interpreter import Interpreter, ObserveReject, InferenceMode

INFERENCE_ALGORITHM = {
    "rejection_sampling": lambda parsed_program, n, nflips: rejection_sampling(parsed_program, n, nflips), 
    "importance_sampling": lambda parsed_program, n, nflips: importance_sampling_inference(parsed_program, n, nflips),
    "mcmc": lambda parsed_program, n, nflips: markov_chain_monte_carlo_metropolis_hastings(parsed_program, n, nflips),
    # add other inference algorithms here
}

def pr(program, inference="rejection_sampling", n=10000, debug=False):
    parser = Parser()
    tokens = tokenize(program)
    parsed_program, nflips = parser.parse(tokens)
    return pr_helper(parsed_program, nflips, inference, n, debug)
    

def pr_helper(parsed_program, nflips, inference, n, debug):
    if debug:
        print(f"nflips = {nflips}\n")
    prob_true = INFERENCE_ALGORITHM[inference](parsed_program, n, nflips)
    print(f"True ==> {prob_true:.4f},  False ==> {1-prob_true:.4f}")
    return prob_true
    
def rejection_sampling(parsed_program, n, nflips=0):
    # simple monte carlo inference by actually running program n times 
    true = 0 
    rejects = 0
    for _ in range(n):
        interpreter = Interpreter(mode=InferenceMode.REJECTION)
        try: 
            res = interpreter.run(parsed_program)
        except ObserveReject:
            rejects += 1
            continue
        if res:
            true += 1
    return true / (n - rejects) if rejects < n else 0.0

def importance_sampling_inference(parsed_program, n, nflips=0):
    num, den = 0.0, 0.0
    for _ in range(n):
        interp = Interpreter(mode=InferenceMode.IMPORTANCE)
        res, w = interp.run(parsed_program)
        num += (1 if res else 0) * w
        den += w
    return num/den

def markov_chain_monte_carlo_metropolis_hastings(parsed_program, n, nflips=0, mix=0.8):
    burn_in = int(n * 0.1)
    true, kept = 0, 0

    interp = Interpreter(mode=InferenceMode.MCMC, nflips=nflips, mix=mix)
    curr_res, curr_weight = interp.run(parsed_program)

    for i in range(burn_in + n):
        curr_res, curr_weight = interp.run(parsed_program)

        if i >= burn_in and curr_weight > 0:
            kept += 1
            if curr_res:
                true += 1

    return true / kept if kept else 0.0
            
