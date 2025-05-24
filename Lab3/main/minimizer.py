from utils import list_len, list_append, list_contains, list_copy
import re

def build_sdnf(table, variables):
    terms = []
    i = 0
    while i < list_len(table):
        if table[i][1] == 1:
            term = []
            j = 0
            while j < list_len(variables):
                term = list_append(term, (variables[j], table[i][0][j]))
                j = j + 1
            terms = list_append(terms, term)
        i = i + 1
    return terms

def build_sknf(table, variables):
    terms = []
    i = 0
    while i < list_len(table):
        if table[i][1] == 0:
            term = []
            j = 0
            while j < list_len(variables):
                term = list_append(term, (variables[j], table[i][0][j]))
                j = j + 1
            terms = list_append(terms, term)
        i = i + 1
    return terms

def sort_term(term):
    nt = list_copy(term)
    n = list_len(nt)
    i = 0
    while i < n:
        j = 0
        while j < n - 1 - i:
            if nt[j][0] > nt[j + 1][0]:
                temp = nt[j]
                nt[j] = nt[j + 1]
                nt[j + 1] = temp
            j = j + 1
        i = i + 1
    return nt

def terms_equal(t1, t2):
    if list_len(t1) != list_len(t2):
        return False
    st1 = sort_term(t1)
    st2 = sort_term(t2)
    i = 0
    while i < list_len(st1):
        v1, val1 = st1[i]
        v2, val2 = st2[i]
        if v1 != v2 or val1 != val2:
            return False
        i = i + 1
    return True

def remove_duplicates(terms):
    unique = []
    i = 0
    while i < list_len(terms):
        is_dup = False
        j = 0
        while j < list_len(unique):
            if terms_equal(terms[i], unique[j]):
                is_dup = True
                break
            j = j + 1
        if not is_dup:
            unique = list_append(unique, terms[i])
        i = i + 1
    return unique

def can_glue_terms(t1, t2):
    st1 = sort_term(t1)
    st2 = sort_term(t2)
    if list_len(st1) != list_len(st2):
        return False, None
    diff_count = 0
    diff_var = None
    i = 0
    while i < list_len(st1):
        v1, val1 = st1[i]
        v2, val2 = st2[i]
        if v1 != v2:
            return False, None
        if val1 != val2:
            diff_count = diff_count + 1
            diff_var = v1
        i = i + 1
    if diff_count == 1:
        return True, diff_var
    return False, None

def glue_terms(t1, diff_var):
    new_t = []
    st1 = sort_term(t1)
    i = 0
    while i < list_len(st1):
        v, val = st1[i]
        if v != diff_var:
            new_t = list_append(new_t, (v, val))
        i = i + 1
    return new_t

def format_term(term, is_minterm):
    if list_len(term) == 0:
        return "1" if is_minterm else "0"
    literals = []
    t_sorted = sort_term(term)
    i = 0
    while i < list_len(t_sorted):
        v, val = t_sorted[i]
        literal = v if (is_minterm and val == 1) or \
                       (not is_minterm and val == 0) else "!" + v
        literals = list_append(literals, literal)
        i = i + 1
    op = "" if is_minterm else "∨"
    result = ""
    i = 0
    while i < list_len(literals):
        result = result + literals[i]
        if op != "" and i < list_len(literals) - 1:
            result = result + op
        i = i + 1
    return result

def combine_terms(terms_lst, sep):
    if list_len(terms_lst) == 0:
        return "0" if sep == " ∨ " else "1"
    result = ""
    i = 0
    while i < list_len(terms_lst):
        t_str = terms_lst[i]
        if sep == " ∧ " and re.search(r"∨", t_str) and t_str[0] != "(":
            result = result + "(" + t_str + ")"
        else:
            result = result + t_str
        if i < list_len(terms_lst) - 1:
            result = result + sep
        i = i + 1
    return result

def is_covered_by_pi(orig_term, pi_term):
    i = 0
    while i < list_len(pi_term):
        v_p, val_p = pi_term[i]
        found = False
        j = 0
        while j < list_len(orig_term):
            v_o, val_o = orig_term[j]
            if v_p == v_o and val_p == val_o:
                found = True
                break
            j = j + 1
        if not found:
            return False
        i = i + 1
    return True

def build_coverage_matrix(orig_terms, pis):
    cov_matrix = []
    i = 0
    while i < list_len(orig_terms):
        row = []
        j = 0
        while j < list_len(pis):
            row = list_append(row, 1 if is_covered_by_pi(orig_terms[i], pis[j]) else 0)
            j = j + 1
        cov_matrix = list_append(cov_matrix, row)
        i = i + 1
    return cov_matrix

def get_uncovered_indices(num_terms):
    uncovered = []
    i = 0
    while i < num_terms:
        uncovered = list_append(uncovered, i)
        i = i + 1
    return uncovered

def find_essential_pis(pis, cov_matrix, uncovered, selected):
    new_uncovered = list_copy(uncovered)
    made_change = False
    i = 0
    while i < list_len(uncovered):
        t_idx = uncovered[i]
        covering_pis = []
        j = 0
        while j < list_len(pis):
            if cov_matrix[t_idx][j] == 1:
                is_selected = False
                k = 0
                while k < list_len(selected):
                    if terms_equal(pis[j], selected[k]):
                        is_selected = True
                        break
                    k = k + 1
                if not is_selected:
                    covering_pis = list_append(covering_pis, j)
            j = j + 1
        if list_len(covering_pis) == 1:
            selected = list_append(selected, pis[covering_pis[0]])
            made_change = True
            temp_uncovered = []
            k = 0
            while k < list_len(new_uncovered):
                if cov_matrix[new_uncovered[k]][covering_pis[0]] == 0:
                    temp_uncovered = list_append(temp_uncovered, new_uncovered[k])
                k = k + 1
            new_uncovered = temp_uncovered
        i = i + 1
    return selected, new_uncovered, made_change

def find_greedy_pis(pis, cov_matrix, uncovered, selected):
    best_idx = -1
    max_cov = 0
    i = 0
    while i < list_len(pis):
        is_selected = False
        j = 0
        while j < list_len(selected):
            if terms_equal(pis[i], selected[j]):
                is_selected = True
                break
            j = j + 1
        if is_selected:
            i = i + 1
            continue
        curr_cov = 0
        j = 0
        while j < list_len(uncovered):
            if cov_matrix[uncovered[j]][i] == 1:
                curr_cov = curr_cov + 1
            j = j + 1
        if curr_cov > max_cov:
            max_cov = curr_cov
            best_idx = i
        elif curr_cov == max_cov and best_idx != -1:
            if list_len(pis[i]) < list_len(pis[best_idx]):
                best_idx = i
        i = i + 1
    if best_idx != -1 and max_cov > 0:
        selected = list_append(selected, pis[best_idx])
        new_uncovered = []
        i = 0
        while i < list_len(uncovered):
            if cov_matrix[uncovered[i]][best_idx] == 0:
                new_uncovered = list_append(new_uncovered, uncovered[i])
            i = i + 1
        return selected, new_uncovered, True
    return selected, uncovered, False

def perform_quine_mccluskey(terms, is_minterm):
    if list_len(terms) == 0:
        return [], []

    pis = []
    current_terms_group = remove_duplicates(list_copy(terms))
    steps = []
    step_cnt = 0

    while True:
        step_cnt += 1
        next_group = []
        marked_indices = [False] * list_len(current_terms_group)
        any_glued_in_step = False

        i = 0
        while i < list_len(current_terms_group):
            j = i + 1
            while j < list_len(current_terms_group):
                term1 = current_terms_group[i]
                term2 = current_terms_group[j]
                can_glue, diff_var = can_glue_terms(term1, term2)

                if can_glue:
                    glued_term = glue_terms(term1, diff_var)
                    if not list_contains_term(next_group, glued_term):
                        next_group = list_append(next_group, glued_term)
                    marked_indices[i] = True
                    marked_indices[j] = True
                    any_glued_in_step = True
                    steps = list_append(steps,
                        "Шаг " + str(step_cnt) + ": Склеивание " +
                        format_term(term1, is_minterm) + " и " +
                        format_term(term2, is_minterm) + " -> " +
                        format_term(glued_term, is_minterm))
                j += 1
            i += 1
        
        i = 0
        while i < list_len(current_terms_group):
            if not marked_indices[i]:
                if not list_contains_term(pis, current_terms_group[i]):
                    pis = list_append(pis, current_terms_group[i])
            i += 1
        
        if not any_glued_in_step:
            break
        current_terms_group = remove_duplicates(next_group)
    
    return pis, steps

def select_prime_implicants(orig_terms, all_pis):
    if list_len(orig_terms) == 0:
        return []
    
    final_selected_pis = []
    
    if list_len(all_pis) > 0:
        cov_matrix = build_coverage_matrix(orig_terms, all_pis)
        uncovered_indices = get_uncovered_indices(list_len(orig_terms))

        while list_len(uncovered_indices) > 0:
            initial_uncovered_count = list_len(uncovered_indices)
            
            final_selected_pis, uncovered_indices, essential_change = \
                find_essential_pis(all_pis, cov_matrix, uncovered_indices, final_selected_pis)
            
            if not essential_change and list_len(uncovered_indices) > 0:
                final_selected_pis, uncovered_indices, greedy_change = \
                    find_greedy_pis(all_pis, cov_matrix, uncovered_indices, final_selected_pis)
                
                if not greedy_change and list_len(uncovered_indices) > 0:
                    break 
            
            if list_len(uncovered_indices) == initial_uncovered_count and \
               not essential_change and not greedy_change:
                break

    return remove_duplicates(final_selected_pis)


def minimize_terms(terms, is_minterm):
    all_pis, glue_steps = perform_quine_mccluskey(terms, is_minterm)
    minimized_terms = select_prime_implicants(terms, all_pis)
    return minimized_terms, glue_steps

def list_contains_term(lst, term):
    i = 0
    while i < list_len(lst):
        if terms_equal(lst[i], term):
            return True
        i = i + 1
    return False

def minimize_terms_calc_table(terms, is_minterm, orig_terms):
    all_pis, glue_steps = perform_quine_mccluskey(terms, is_minterm)
    sel_imp = select_prime_implicants(orig_terms, all_pis)
    
    cov_table = []
    if list_len(sel_imp) > 0 and list_len(orig_terms) > 0:
        header = ["Терм"]
        i = 0
        while i < list_len(sel_imp):
            header = list_append(header, format_term(sel_imp[i], is_minterm))
            i = i + 1
        cov_table = list_append(cov_table, header)
        i = 0
        while i < list_len(orig_terms):
            row = [format_term(orig_terms[i], is_minterm)]
            j = 0
            while j < list_len(sel_imp):
                row = list_append(row, "X" if is_covered_by_pi(orig_terms[i], sel_imp[j]) else ".")
                j = j + 1
            cov_table = list_append(cov_table, row)
            i = i + 1
    return sel_imp, glue_steps, cov_table

def get_gray_codes(num_bits):
    if num_bits == 0:
        return [""]
    if num_bits == 1:
        return ["0", "1"]
    prev = get_gray_codes(num_bits - 1)
    new_codes = []
    i = 0
    while i < list_len(prev):
        new_codes = list_append(new_codes, "0" + prev[i])
        i = i + 1
    i = list_len(prev) - 1
    while i >= 0:
        new_codes = list_append(new_codes, "1" + prev[i])
        i = i - 1
    return new_codes

def get_kmap_dimensions(n_vars):
    if n_vars == 1:
        return 1, 2, 0, 1
    elif n_vars == 2:
        return 2, 2, 1, 1
    elif n_vars == 3:
        return 2, 4, 1, 2
    elif n_vars == 4:
        return 4, 4, 2, 2
    elif n_vars == 5:
        return 4, 8, 2, 3
    else:
        return None, None, None, None

def fill_kmap_cells(kmap, orig_terms, variables, is_minterm, r_var_cnt, c_var_cnt,
                    gc_rows, gc_cols, fill_val, def_val):
    i = 0
    while i < list_len(orig_terms):
        t = orig_terms[i]
        row_vars_str = ""
        j = 0
        while j < r_var_cnt:
            k = 0
            while k < list_len(t):
                if t[k][0] == variables[j]:
                    row_vars_str = row_vars_str + str(t[k][1])
                    break
                k = k + 1
            j = j + 1

        col_vars_str = ""
        j = 0
        while j < c_var_cnt:
            k = 0
            while k < list_len(t):
                if t[k][0] == variables[r_var_cnt + j]:
                    col_vars_str = col_vars_str + str(t[k][1])
                    break
                k = k + 1
            j = j + 1

        row_idx = -1 if r_var_cnt == 0 else gc_rows.index(row_vars_str) if row_vars_str in gc_rows else -1
        col_idx = gc_cols.index(col_vars_str) if col_vars_str in gc_cols else -1

        if row_idx != -1 and col_idx != -1:
            kmap[row_idx][col_idx] = fill_val
        i = i + 1
    return kmap


def get_kmap_fill_data(orig_terms, variables, is_minterm):
    n_vars = list_len(variables)
    fill_val = 1 if is_minterm else 0
    def_val = 0 if is_minterm else 1

    r_kmap, c_kmap, r_var_cnt, c_var_cnt = get_kmap_dimensions(n_vars)
    if r_kmap is None:
        return None, None, None, None

    kmap = []
    i = 0
    while i < r_kmap:
        row = []
        j = 0
        while j < c_kmap:
            row = list_append(row, def_val)
            j = j + 1
        kmap = list_append(kmap, row)
        i = i + 1

    gc_rows = get_gray_codes(r_var_cnt)
    gc_cols = get_gray_codes(c_var_cnt)

    kmap = fill_kmap_cells(kmap, orig_terms, variables, is_minterm, r_var_cnt, c_var_cnt,
                           gc_rows, gc_cols, fill_val, def_val)
    
    kmap_params = (gc_rows, gc_cols, r_var_cnt, c_var_cnt, variables)
    return kmap, kmap_params, r_kmap, c_kmap

def _get_row_label(r_idx, r_var_cnt, gc_rows, all_vars):
    if r_var_cnt == 0 and list_len(all_vars) == 1:
        return ""
    if r_var_cnt > 0:
        row_vars_str = ""
        k = 0
        while k < r_var_cnt:
            row_vars_str += all_vars[k]
            k += 1
        return row_vars_str + "=" + gc_rows[r_idx]
    return ""

def _get_col_label(c_idx, c_var_cnt, gc_cols, all_vars, r_var_cnt):
    col_vars_str = ""
    j = 0
    while j < c_var_cnt:
        col_vars_str += all_vars[r_var_cnt + j]
        j += 1
    if list_len(col_vars_str) > 0:
        return col_vars_str + "=" + gc_cols[c_idx]
    return gc_cols[c_idx]

def format_kmap_for_print(kmap, kmap_params):
    gc_rows, gc_cols, r_var_cnt, c_var_cnt, all_vars = kmap_params
    kmap_out = []

    if list_len(all_vars) > 0 and list_len(kmap) > 0:
        header = [""]
        i = 0
        while i < list_len(gc_cols):
            header = list_append(header, _get_col_label(i, c_var_cnt, gc_cols, all_vars, r_var_cnt))
            i = i + 1
        kmap_out = list_append(kmap_out, header)

        i = 0
        while i < list_len(kmap):
            row_label = _get_row_label(i, r_var_cnt, gc_rows, all_vars)
            row = [row_label]
            j = 0
            while j < list_len(kmap[i]):
                row = list_append(row, str(kmap[i][j]))
                j = j + 1
            kmap_out = list_append(kmap_out, row)
            i = i + 1
    return kmap_out

def minimize_terms_karnaugh(orig_terms, is_minterm, variables):
    if list_len(orig_terms) == 0:
        return [], [], [["Карта Карно: нет термов для минимизации."]]
    if list_len(variables) == 0:
        return [], [], [["Карта Карно: нет переменных."]]
    if list_len(variables) > 5:
        return [], [], [["Карта Карно: Поддерживается до 5 переменных."]]

    kmap_data, kmap_params, _, _ = get_kmap_fill_data(orig_terms, variables, is_minterm)
    if kmap_data is None:
        return [], [], [["Карта Карно: Ошибка инициализации карты."]]

    minimized_implicants, glue_steps = minimize_terms(orig_terms, is_minterm)
    
    kmap_formatted_for_print = format_kmap_for_print(kmap_data, kmap_params)
    
    return minimized_implicants, glue_steps, kmap_formatted_for_print
