import re

token_match = [
    ("BOOLEAN", re.compile(r'\b(True|False)\b'))
]

def tokenize(program):
    tokens = []
    pos = 0
    while pos < len(program):
        if program[pos].isspace():
            pos += 1
            continue
        for token_type, token_re in token_match:
            match = token_re.match(program, pos)
            if not match: 
                continue
            if token_type == "BOOLEAN":
                val = match.group(1)
            else:
                val = match.group(0)

            tokens.append((token_type, val))
            pos = match.end()
            break
        else:
            raise SyntaxError(f"Unexpected character {program[pos]!r}")
    return tokens