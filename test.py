from inference import pr

# not sure if this is how we want our ppl to work 
program = """
    x = flip(0.5)
"""

pr(program)