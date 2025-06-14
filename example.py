from src.inference import pr 

program = """
x = flip(0.5)
y = flip(0.8)
z = if x then flip(0.1) else flip(0.3)
observe(x and y or not z)
x
"""

pr(program)