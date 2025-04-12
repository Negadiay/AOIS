def str_len(s):
    count = 0
    try:
        while True:
            _ = s[count]
            count += 1
    except:
        return count

def str_get(s, i):
    return s[i]

def list_len(lst):
    count = 0
    try:
        while True:
            _ = lst[count]
            count += 1
    except:
        return count

def list_append(lst, val):
    new_lst = []
    i = 0
    while i < list_len(lst):
        new_lst += [lst[i]]
        i += 1
    new_lst += [val]
    return new_lst

def list_contains(lst, val):
    i = 0
    while i < list_len(lst):
        if lst[i] == val:
            return True
        i += 1
    return False

def list_sort(lst):
    n = list_len(lst)
    i = 0
    while i < n:
        j = 0
        while j < n - 1:
            if lst[j] > lst[j + 1]:
                temp = lst[j]
                lst[j] = lst[j + 1]
                lst[j + 1] = temp
            j += 1
        i += 1
    return lst

def list_copy(lst):
    new_lst = []
    i = 0
    while i < list_len(lst):
        new_lst = list_append(new_lst, lst[i])
        i += 1
    return new_lst

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
        elif c in ('!', '&', '|', '~', '(', ')'):
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
    if op == '~':
        return 3
    if op == '&':
        return 2
    if op == '|':
        return 1
    if op == '->':
        return 0
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
        if is_variable(token):
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

def build_sdnf(table, variables):
    terms = []
    indexes = []
    i = 0
    while i < list_len(table):
        row = table[i]
        if row[1] == 1:
            indexes = list_append(indexes, i)
            term = ''
            j = 0
            while j < list_len(variables):
                if row[0][j] == 1:
                    term += variables[j]
                else:
                    term += '¬' + variables[j]
                if j < list_len(variables) - 1:
                    term += '∧'
                j += 1
            terms = list_append(terms, '(' + term + ')')
        i += 1
    return combine_terms(terms, ' ∨ '), indexes

def build_sknf(table, variables):
    terms = []
    indexes = []
    i = 0
    while i < list_len(table):
        row = table[i]
        if row[1] == 0:
            indexes = list_append(indexes, i)
            term = ''
            j = 0
            while j < list_len(variables):
                if row[0][j] == 0:
                    term += variables[j]
                else:
                    term += '¬' + variables[j]
                if j < list_len(variables) - 1:
                    term += '∨'
                j += 1
            terms = list_append(terms, '(' + term + ')')
        i += 1
    return combine_terms(terms, ' ∧ '), indexes

def combine_terms(terms, sep):
    result = ''
    i = 0
    while i < list_len(terms):
        result += terms[i]
        if i < list_len(terms) - 1:
            result += sep
        i += 1
    return result

def get_index_form(table):
    binary = ''
    i = 0
    while i < list_len(table):
        binary += str(table[i][1])
        i += 1
    decimal = 0
    i = 0
    while i < str_len(binary):
        if binary[i] == '1':
            power = str_len(binary) - i - 1
            decimal += 2 ** power
        i += 1
    return decimal, binary

def get_numeric_forms(table):
    sdnf = []
    sknf = []
    i = 0
    while i < list_len(table):
        if table[i][1] == 1:
            sdnf = list_append(sdnf, i)
        else:
            sknf = list_append(sknf, i)
        i += 1
    return sdnf, sknf

def print_table(table, variables, expr):
    header = ''
    i = 0
    while i < list_len(variables):
        header += variables[i]
        if i < list_len(variables) - 1:
            header += ' | '
        i += 1
    header += ' | ' + expr
    print(header)
    print('-' * str_len(header))
    i = 0
    while i < list_len(table):
        row = table[i]
        line = ''
        j = 0
        while j < list_len(row[0]):
            line += str(row[0][j])
            if j < list_len(row[0]) - 1:
                line += ' | '
            j += 1
        line += ' |   ' + str(row[1])
        print(line)
        i += 1

def main(input_expr=None):
    if input_expr is None:
        expr = input("Введите логическое выражение (a-e, ! & | -> ~): ")
    else:
        expr = input_expr
    tokens = tokenize(expr)
    variables = get_variables(tokens)
    postfix = to_postfix(tokens)
    table = generate_table(postfix, variables)

    print("\nТаблица истинности:")
    print_table(table, variables, expr)

    sdnf, sdnf_i = build_sdnf(table, variables)
    sknf, sknf_i = build_sknf(table, variables)

    print("\nСДНФ:", sdnf if sdnf != '' else "Не существует")
    print("СКНФ:", sknf if sknf != '' else "Не существует")

    sdnf_nums, sknf_nums = get_numeric_forms(table)
    print("\nЧисловая форма СДНФ:", sdnf_nums)
    print("Числовая форма СКНФ:", sknf_nums)

    dec, bin_str = get_index_form(table)
    print("\nИндексная форма:")
    print("Десятичное:", dec)
    print("Двоичное:  ", bin_str)

if __name__ == "__main__":
    main()
