# PyPPL
cs267a final project implementing a first-order, discrete PPL on python with monte carlo inference, importance sampling, and mcmc

## Language 
### General Grammar
```bnf
<v>        ::= T | F
<aexp>     ::= x | <v>
<expr>     ::= <aexp>
             | x = <expr> ; <expr>
             | flip(θ)
             | if <expr> then <expr> else <expr>
             | observe(<expr>)
             | <expr> or <expr>
             | not <expr>
             | <expr> and <expr>
```
- **Boolean literals**: `T` and `F`, and **variables** like `x` as atomic expressions.  
- **Sequencing**: `x = expr; expr` evaluates `expr`, binds its result to `x`, then continues with the next expression.  
- **Random sampling**: `flip(θ)` draws a Bernoulli random variable that yields `T` with probability θ (and `F` otherwise); θ must be a number in the interval **[0, 1]**.  
- **Conditional branching**: `if expr then expr else expr` chooses between two sub‐expressions based on the Boolean test `expr`.  
- **Conditioning**: `observe(expr)` restricts execution to runs where `expr` is true, allowing inference algorithms to weight or reject samples.  
- **Logical connectives**: `expr or expr`, `expr and expr`, and `not expr` for disjunction, conjunction, and negation of Boolean values.  

### Syntax
Below are examples of the actual language syntax.
- **Boolean literals**  
 ```python 
True 
False
 ```

- **Variables** 
```python 
x 
y 
```

- **Flips** 
```python
flip(0.5)
flip(1)
```

- **Assignment** 
```python 
x = True 
x
```

- **Conditionals** 
```python
x = True 
if x then flip(0.5) else flip(0.8)
```

- **Conditioning** 
```python
x = Flip(0.5)
observe(x)
```

- **Logical Connectives** 
```python 
x = True
y = False
not x and y or y and x
```

## Testing 

### Unit Testing 
We use Python’s built-in `unittest` framework. See the [unittest docs](https://docs.python.org/3/library/unittest.html) for details.

To run all unit tests from the project root:

```bash
python -m unittest discover
```

## Additional Goal
Build a command-line REPL for our PPL so user can write their probablistic program and inference it directly from the terminal 