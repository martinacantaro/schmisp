import re
import operator as op

def READ(program:str) -> str:
    r = read_str(program)
    return r

def EVAL(ast, env):
    if ast == []:
        return ast
    elif type(ast) == list:
        if ast[0] == 'def!': 
            s = ast[1] #symbol
            v = eval_ast(ast[2], env) #value
            r = env.set(s, v)
            return r        
        e = eval_ast(ast, env)
        print(e) # debugging
        o = e[0] # the first element is the operator (ie +)
        p = e[1::] # the rest are parameters (ie integers)
        print(p) # debugging
        return o(*p) # passes the parameters to the operator
    else:
        return eval_ast(ast, env)
    return line

def PRINT(line):
    return(pr_str(line))

def rep(program):
    rep = PRINT(EVAL(READ(program), repl_env))
    print(rep)

def read_str(program):
    t = tokenize(program)
    r = Reader(t)
    l = read_form(r)
    return l

r = r'''[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"|;.*|[^\s\[\]{}('"`,;)]*)'''

def tokenize(program:str) -> list:
    tkns = re.split(r, program)
    tkns_list = []
    for t in tkns:
        if t != '':
            tkns_list.append(t) 
    return tkns_list


class Reader:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.length = len(tokens)
    def nex(self):
        self.position += 1
    def peek(self):
        current_token = self.tokens[self.position]
        return current_token
    
def read_form(tokens:Reader):
    tkn = tokens.peek()
    l = []
    if tkn == '(':
        t = read_list(tokens)
    else: 
        t = read_atom(tkn)
    return t

def read_list(tokens):
    result = []
    tokens.nex() # skips the "(" that brought us here
    tkn = tokens.peek()
    while tkn != ')':
        t = read_form(tokens)
        result.append(t)
        tokens.nex()
        tkn = tokens.peek()
    return result

def read_atom(token):
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return str(token)
        
def pr_str(token): # turns the program back into a string
    l = []
    if type(token) == list:
        for i in token:
            l.append(pr_str(i))
        l = ' '.join(l)
        l = '(' + l + ')'
        return l
    else:
        s = str(token)
        return s
    
def eval_ast(ast, env): # ast = abstract syntax tree = mal data type
    if type(ast) == list:
        l = []
        for i in ast:
            i = EVAL(i, env)
            l.append(i)
        return l
    elif type(ast) == str:
        return env.get(ast)
    else:
        return ast

class Env:
    def __init__(self, outer):
        self.outer = outer
        self.data = {}
    def set(self, symbol, mal_value):
        self.data[symbol] = mal_value
    def find(self, symbol):
        if symbol in self.data:
            return self.data
        elif self.outer is not None:
            return self.outer.find(symbol)
    def get(self, symbol):
        env_with_symbol = self.find(symbol)
        value = env_with_symbol[symbol]
        return value #  TODO If no key is found up the outer chain, then throws/raises a "not found" error.
    
repl_env = Env(None)

repl_env.set('+', op.add)
repl_env.set('-', op.sub)
repl_env.set('*', op.mul)
repl_env.set('/', op.truediv)


# ------------ TEST


while True:
    command = input('Write your program or type q to quit:')
    if command != 'q':
        rep(command)
    else:
        break
