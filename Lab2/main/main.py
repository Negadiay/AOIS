def evaluate_expression(expr, values):
    tokens = []
    i = 0
    n = len(expr)
    while i < n:
        if expr[i] == ' ':
            i += 1
            continue
        if expr[i] >= 'a' and expr[i] <= 'e':
            var = expr[i]
            tokens.append(var)
            i += 1
        elif expr[i] == '-' and i + 1 < n and expr[i+1] == '>':
            tokens.append('->')
            i += 2
        elif expr[i] == '~':
            tokens.append('~')
            i += 1
        else:
            tokens.append(expr[i])
            i += 1
    
    for i in range(len(tokens)):
        if tokens[i] in values:
            tokens[i] = str(values[tokens[i]])
    
    expr = ''.join(tokens)
    
    expr = expr.replace('!', ' not ')
    expr = expr.replace('&', ' and ')
    expr = expr.replace('|', ' or ')
    expr = expr.replace('->', ' <= ')
    expr = expr.replace('~', ' == ')
    
    try:
        return 1 if eval(expr) else 0
    except:
        return 0

def get_variables(expr):
    variables = []
    for c in expr:
        if c >= 'a' and c <= 'e' and c not in variables:
            variables.append(c)
    return sorted(variables)

def generate_truth_table(expr, variables):
    table = []
    n = len(variables)
    
    for i in range(2 ** n):
        combo = []
        for j in range(n):
            combo.append((i >> (n - 1 - j)) & 1)
        
        values = {}
        for var, val in zip(variables, combo):
            values[var] = val
        
        result = evaluate_expression(expr, values)
        table.append((combo, result))
    
    return table

def build_sdnf(table, variables):
    terms = []
    indexes = []
    
    for i in range(len(table)):
        combo, result = table[i]
        if result == 1:
            indexes.append(i)
            term_parts = []
            for j in range(len(variables)):
                if combo[j] == 1:
                    term_parts.append(variables[j])
                else:
                    term_parts.append('¬' + variables[j])
            terms.append('(' + '∧'.join(term_parts) + ')')
    
    return ' ∨ '.join(terms), indexes

def build_sknf(table, variables):
    terms = []
    indexes = []
    
    for i in range(len(table)):
        combo, result = table[i]
        if result == 0:
            indexes.append(i)
            term_parts = []
            for j in range(len(variables)):
                if combo[j] == 0:
                    term_parts.append(variables[j])
                else:
                    term_parts.append('¬' + variables[j])
            terms.append('(' + '∨'.join(term_parts) + ')')
    
    return ' ∧ '.join(terms), indexes

def get_numeric_forms(table):
    sknf_indexes = []
    sdnf_indexes = []
    
    for i in range(len(table)):
        _, result = table[i]
        if result == 0:
            sknf_indexes.append(str(i))
        else:
            sdnf_indexes.append(str(i))
    
    return sknf_indexes, sdnf_indexes

def get_index_form(table):
    binary = ''
    for _, result in table:
        binary += str(result)
    
    decimal = 0
    length = len(binary)
    for i in range(length):
        if binary[i] == '1':
            decimal += 2 ** (length - 1 - i)
    
    binary_padded = binary.zfill(length)
    return decimal, binary_padded

def print_truth_table(table, variables, expr):
    header = ' | '.join(variables) + ' | ' + expr 
    print(header)
    print('-' * len(header))
    
    for combo, result in table:
        row = ' | '.join(str(val) for val in combo) + ' |   ' + str(result)
        print(row)

def main():
    expr = input("Введите логическое выражение (используйте переменные a-e и операции &, |, !, ->, ~): ").strip()
    
    variables = get_variables(expr)
    if not variables:
        print("Не найдено переменных в выражении.")
        return
    
    print("\nПеременные в выражении:", ', '.join(variables))
    
    table = generate_truth_table(expr, variables)
    
    print("\nТаблица истинности:")
    print_truth_table(table, variables, expr)
    
    sdnf, sdnf_indexes = build_sdnf(table, variables)
    sknf, sknf_indexes = build_sknf(table, variables)
    
    print("\nСовершенная дизъюнктивная нормальная форма (СДНФ):")
    print(sdnf if sdnf else "Форма не существует (все результаты 0)")
    
    print("\nСовершенная конъюнктивная нормальная форма (СКНФ):")
    print(sknf if sknf else "Форма не существует (все результаты 1)")
    
    sknf_num, sdnf_num = get_numeric_forms(table)
    print("\nЧисловая форма СКНФ (индексы строк с 0):")
    print(f"({' , '.join(sknf_num)})" if sknf_num else "Нет таких строк")
    
    print("\nЧисловая форма СДНФ (индексы строк с 1):")
    print(f"({' , '.join(sdnf_num)})" if sdnf_num else "Нет таких строк")
    
    decimal, binary = get_index_form(table)
    print("\nИндексная форма функции:")
    print(f"Десятичное: {decimal}")
    print(f"Двоичное: {binary}")

if __name__ == "__main__":
    main()