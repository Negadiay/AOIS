from utils import *

def is_variable(c):
    return c == 'a' or c == 'b' or c == 'c' or c == 'd' or c == 'e'

def tokenize(expr):
    tokens = []
    i = 0
    while i < str_len(expr):
        c = str_get(expr, i)
        if c == ' ':
            i += 1
        elif is_variable(c):
            tokens = list_append(tokens, c)
            i += 1
        elif c == '-' and str_get(expr, i + 1) == '>':
            tokens = list_append(tokens, '->')
            i += 2
        elif c == '<' and str_get(expr, i + 1) == '-' and str_get(expr, i + 2) == '>':
            tokens = list_append(tokens, '~')
            i += 3
        elif c in ('!', '&', '|', '(', ')'):
            tokens = list_append(tokens, c)
            i += 1
        else:
            i += 1
    return tokens

def get_variables(tokens):
    vars = []
    i = 0
    while i < list_len(tokens):
        t = tokens[i]
        if is_variable(t) and not list_contains(vars, t):
            vars = list_append(vars, t)
        i += 1
    return list_sort(vars)

def get_precedence(op):
    if op == '!':
        return 4
    if op == '&':
        return 3
    if op == '|':
        return 2
    if op in ('->', '~'):
        return 1
    return -1

def to_postfix(tokens):
    output = []
    stack = []
    i = 0
    while i < list_len(tokens):
        token = tokens[i]
        if is_variable(token):
            output = list_append(output, token)
        elif token == '(':
            stack = list_append(stack, token)
        elif token == ')':
            while list_len(stack) > 0 and stack[list_len(stack) - 1] != '(':
                output = list_append(output, stack[list_len(stack) - 1])
                stack = stack[:list_len(stack) - 1]
            stack = stack[:list_len(stack) - 1]
        else:
            while (list_len(stack) > 0 and stack[list_len(stack) - 1] != '(' and
                   get_precedence(stack[list_len(stack) - 1]) >= get_precedence(token)):
                output = list_append(output, stack[list_len(stack) - 1])
                stack = stack[:list_len(stack) - 1]
            stack = list_append(stack, token)
        i += 1
    while list_len(stack) > 0:
        output = list_append(output, stack[list_len(stack) - 1])
        stack = stack[:list_len(stack) - 1]
    return output