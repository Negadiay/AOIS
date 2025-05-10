from utils import list_len, list_append

def apply_op(op, a, b):
    if op == '&':
        return a * b
    if op == '|':
        return a + b - a * b
    if op == '->':
        return 1 if (a == 0 or b == 1) else 0
    if op == '~':
        return 1 if a == b else 0
    return 0

def apply_not(a):
    return 1 - a

def evaluate_postfix(postfix, values):
    stack = []
    i = 0
    while i < list_len(postfix):
        token = postfix[i]
        if token in 'abcde':
            stack = list_append(stack, values[token])
        elif token == '!':
            val = stack[list_len(stack) - 1]
            stack = stack[:list_len(stack) - 1]
            stack = list_append(stack, apply_not(val))
        else:
            b = stack[list_len(stack) - 1]
            stack = stack[:list_len(stack) - 1]
            a = stack[list_len(stack) - 1]
            stack = stack[:list_len(stack) - 1]
            stack = list_append(stack, apply_op(token, a, b))
        i += 1
    return stack[0]

def generate_table(postfix, variables):
    results = []
    total = 1
    for _ in range(list_len(variables)):
        total *= 2
    i = 0
    while i < total:
        combo = []
        j = 0
        while j < list_len(variables):
            shift = list_len(variables) - j - 1
            bit = (i // (2 ** shift)) % 2
            combo = list_append(combo, bit)
            j += 1
        values = {}
        k = 0
        while k < list_len(variables):
            values[variables[k]] = combo[k]
            k += 1
        result = evaluate_postfix(postfix, values)
        results = list_append(results, (combo, result))
        i += 1
    return results