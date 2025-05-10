from parser import tokenize, get_variables, to_postfix
from evaluator import generate_table
from minimizer import build_sdnf, build_sknf, minimize_terms, minimize_terms_calc_table, minimize_terms_karnaugh, format_term, combine_terms
from utils import str_len, list_len, list_append

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

def print_coverage_table(table):
    if not table:
        return
    max_widths = [0] * list_len(table[0])
    for row in table:
        for j in range(list_len(row)):
            max_widths[j] = max(max_widths[j], str_len(str(row[j])))
    
    for i, row in enumerate(table):
        line = ''
        for j in range(list_len(row)):
            cell = str(row[j])
            line += cell + ' ' * (max_widths[j] - str_len(cell) + 1)
            if j < list_len(row) - 1:
                line += '| '
        print(line)
        if i == 0:
            print('-' * str_len(line))

def print_karnaugh_map(kmap):
    if not kmap:
        return
    max_widths = [0] * list_len(kmap[0])
    for row in kmap:
        for j in range(list_len(row)):
            max_widths[j] = max(max_widths[j], str_len(str(row[j])))
    
    for i, row in enumerate(kmap):
        line = ''
        for j in range(list_len(row)):
            cell = str(row[j])
            line += cell + ' ' * (max_widths[j] - str_len(cell) + 1)
            if j < list_len(row) - 1:
                line += '| '
        print(line)
        if i == 0:
            print('-' * str_len(line))

def main():
    expr = input("Введите логическое выражение (a-e, ! & | -> ~): ")
    try:
        tokens = tokenize(expr)
        variables = get_variables(tokens)
        if list_len(variables) > 5:
            print("Ошибка: Максимум 5 переменных (a-e)")
            return
        if list_len(variables) == 0:
            print("Ошибка: Нет переменных в выражении")
            return
        postfix = to_postfix(tokens)
        table = generate_table(postfix, variables)

        print("\nТаблица истинности:")
        print_table(table, variables, expr)

        # Исходные СДНФ и СКНФ
        sdnf_terms = build_sdnf(table, variables)
        sdnf_initial = combine_terms([format_term(t, True) for t in sdnf_terms], ' ∨ ')
        print("\nИсходная СДНФ:", sdnf_initial if sdnf_initial != '' else "0")
        
        sknf_terms = build_sknf(table, variables)
        sknf_initial = combine_terms([format_term(t, False) for t in sknf_terms], ' ∧ ')
        print("Исходная СКНФ:", sknf_initial if sknf_initial != '' else "1")

        # Минимизация СДНФ (Расчётный метод)
        min_sdnf, sdnf_steps = minimize_terms(sdnf_terms, True)
        print("\nМинимизация СДНФ (Расчётный метод):")
        if list_len(sdnf_terms) == 0:
            print("СДНФ пустая (функция всегда 0)")
        else:
            print("Стадии склеивания:")
            if list_len(sdnf_steps) == 0:
                print("Склеивание не требуется")
            i = 0
            while i < list_len(sdnf_steps):
                print(sdnf_steps[i])
                i += 1
            sdnf_result = combine_terms([format_term(t, True) for t in min_sdnf], ' ∨ ')
            print("Минимизированная СДНФ:", sdnf_result if sdnf_result != '' else "0")

        # Минимизация СКНФ (Расчётный метод)
        min_sknf, sknf_steps = minimize_terms(sknf_terms, False)
        print("\nМинимизация СКНФ (Расчётный метод):")
        if list_len(sknf_terms) == 0:
            print("СКНФ пустая (функция всегда 1)")
        else:
            print("Стадии склеивания:")
            if list_len(sknf_steps) == 0:
                print("Склеивание не требуется")
            i = 0
            while i < list_len(sknf_steps):
                print(sknf_steps[i])
                i += 1
            sknf_result = combine_terms([format_term(t, False) for t in min_sknf], ' ∧ ')
            print("Минимизированная СКНФ:", sknf_result if sknf_result != '' else "1")

        # Минимизация СДНФ (Расчётно-табличный метод)
        min_sdnf_calc, sdnf_calc_steps, sdnf_calc_table = minimize_terms_calc_table(sdnf_terms, True, sdnf_terms)
        print("\nМинимизация СДНФ (Расчётно-табличный метод):")
        if list_len(sdnf_terms) == 0:
            print("СДНФ пустая (функция всегда 0)")
        else:
            print("Стадии склеивания:")
            if list_len(sdnf_calc_steps) == 0:
                print("Склеивание не требуется")
            i = 0
            while i < list_len(sdnf_calc_steps):
                print(sdnf_calc_steps[i])
                i += 1
            print("\nТаблица покрытия:")
            print_coverage_table(sdnf_calc_table)
            sdnf_calc_result = combine_terms([format_term(t, True) for t in min_sdnf_calc], ' ∨ ')
            print("Минимизированная СДНФ:", sdnf_calc_result if sdnf_calc_result != '' else "0")

        # Минимизация СКНФ (Расчётно-табличный метод)
        min_sknf_calc, sknf_calc_steps, sknf_calc_table = minimize_terms_calc_table(sknf_terms, False, sknf_terms)
        print("\nМинимизация СКНФ (Расчётно-табличный метод):")
        if list_len(sknf_terms) == 0:
            print("СКНФ пустая (функция всегда 1)")
        else:
            print("Стадии склеивания:")
            if list_len(sknf_calc_steps) == 0:
                print("Склеивание не требуется")
            i = 0
            while i < list_len(sknf_calc_steps):
                print(sknf_calc_steps[i])
                i += 1
            print("\nТаблица покрытия:")
            print_coverage_table(sknf_calc_table)
            sknf_calc_result = combine_terms([format_term(t, False) for t in min_sknf_calc], ' ∧ ')
            print("Минимизированная СКНФ:", sknf_calc_result if sknf_calc_result != '' else "1")

        # Минимизация СДНФ (Карта Карно)
        min_sdnf_kmap, sdnf_kmap_steps, sdnf_kmap_table = minimize_terms_karnaugh(sdnf_terms, True, variables)
        print("\nМинимизация СДНФ (Карта Карно):")
        if list_len(sdnf_terms) == 0:
            print("СДНФ пустая (функция всегда 0)")
        elif list_len(sdnf_kmap_table) == 1 and 'Карта Карно' in sdnf_kmap_table[0]:
            print(sdnf_kmap_table[0])
        else:
            print("Стадии склеивания:")
            if list_len(sdnf_kmap_steps) == 0:
                print("Склеивание не требуется")
            i = 0
            while i < list_len(sdnf_kmap_steps):
                print(sdnf_kmap_steps[i])
                i += 1
            print("\nКарта Карно:")
            print_karnaugh_map(sdnf_kmap_table)
            sdnf_kmap_result = combine_terms([format_term(t, True) for t in min_sdnf_kmap], ' ∨ ')
            print("Минимизированная СДНФ:", sdnf_kmap_result if sdnf_kmap_result != '' else "0")

        # Минимизация СКНФ (Карта Карно)
        min_sknf_kmap, sknf_kmap_steps, sknf_kmap_table = minimize_terms_karnaugh(sknf_terms, False, variables)
        print("\nМинимизация СКНФ (Карта Карно):")
        if list_len(sknf_terms) == 0:
            print("СКНФ пустая (функция всегда 1)")
        elif list_len(sknf_kmap_table) == 1 and 'Карта Карно' in sknf_kmap_table[0]:
            print(sknf_kmap_table[0])
        else:
            print("Стадии склеивания:")
            if list_len(sknf_kmap_steps) == 0:
                print("Склеивание не требуется")
            i = 0
            while i < list_len(sknf_kmap_steps):
                print(sknf_kmap_steps[i])
                i += 1
            print("\nКарта Карно:")
            print_karnaugh_map(sknf_kmap_table)
            sknf_kmap_result = combine_terms([format_term(t, False) for t in min_sknf_kmap], ' ∧ ')
            print("Минимизированная СКНФ:", sknf_kmap_result if sknf_kmap_result != '' else "1")
    
    except Exception as e:
        print("Ошибка:", str(e))

if __name__ == "__main__":
    main()