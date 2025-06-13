import re

token_match = [
    ("NEWLINE",   re.compile(r'\n+')), 
    ("BOOLEAN", re.compile(r'\b(True|False)\b')),
    ("IF",        re.compile(r'\bif\b')),                
    ("THEN",      re.compile(r'\bthen\b')),              
    ("ELSE",      re.compile(r'\belse\b')),
    ("OBSERVE",   re.compile(r'\bobserve\b')),           
    ("FLIP",      re.compile(r'\bflip\b')),              
    ("AND",       re.compile(r'\band\b')),               
    ("OR",        re.compile(r'\bor\b')),                
    ("NOT",       re.compile(r'\bnot\b')),               
    ("NUMBER",    re.compile(r'\b\d+(\.\d+)?\b')),        
    ("VAR",     re.compile(r'\b[A-Za-z_]\w*\b')),      # Variables
    ("ASSIGN",    re.compile(r'=')),                     
    ("LPAREN",    re.compile(r'\(')),                  # Parenthesis 
    ("RPAREN",    re.compile(r'\)')),                  
]

def tokenize(program):
    tokens = []
    pos = 0
    size = len(program)
    while pos < size:
        if program[pos] in " \t":
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