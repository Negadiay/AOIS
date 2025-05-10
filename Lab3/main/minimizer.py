from utils import list_len, list_append, list_contains, list_copy

def build_sdnf(table, variables):
    terms = []
    i = 0
    while i < list_len(table):
        row = table[i]
        if row[1] == 1:
            term = []
            j = 0
            while j < list_len(variables):
                term = list_append(term, (variables[j], row[0][j]))
                j += 1
            terms = list_append(terms, term)
        i += 1
    return terms

def build_sknf(table, variables):
    terms = []
    i = 0
    while i < list_len(table):
        row = table[i]
        if row[1] == 0:
            term = []
            j = 0
            while j < list_len(variables):
                term = list_append(term, (variables[j], row[0][j]))
                j += 1
            terms = list_append(terms, term)
        i += 1
    return terms

def term_is_subsumed_by_list(term_to_check, list_of_implicants):
    idx_imp = 0
    while idx_imp < list_len(list_of_implicants):
        implicant = list_of_implicants[idx_imp]
        is_covered_by_this_implicant = True
        idx_lit_imp = 0
        while idx_lit_imp < list_len(implicant):
            var_imp, val_imp = implicant[idx_lit_imp]
            found_match_in_term = False
            idx_lit_term = 0
            while idx_lit_term < list_len(term_to_check):
                var_term, val_term = term_to_check[idx_lit_term]
                if var_imp == var_term:
                    if val_imp == val_term:
                        found_match_in_term = True
                    break 
                idx_lit_term += 1
            if not found_match_in_term:
                is_covered_by_this_implicant = False
                break
            idx_lit_imp += 1
        
        if is_covered_by_this_implicant:
            return True 
        idx_imp += 1
    return False


def can_glue(term1, term2):
    sorted_term1 = list_copy(term1)
    k = 0
    while k < list_len(sorted_term1):
        m = 0
        while m < list_len(sorted_term1) - k - 1:
            if sorted_term1[m][0] > sorted_term1[m+1][0]:
                temp = sorted_term1[m]
                sorted_term1[m] = sorted_term1[m+1]
                sorted_term1[m+1] = temp
            m += 1
        k += 1

    sorted_term2 = list_copy(term2)
    k = 0
    while k < list_len(sorted_term2):
        m = 0
        while m < list_len(sorted_term2) - k - 1:
            if sorted_term2[m][0] > sorted_term2[m+1][0]:
                temp = sorted_term2[m]
                sorted_term2[m] = sorted_term2[m+1]
                sorted_term2[m+1] = temp
            m += 1
        k += 1

    if list_len(sorted_term1) != list_len(sorted_term2):
        return False, None

    differences = 0
    diff_var = None
    i = 0
    while i < list_len(sorted_term1):
        var1, val1 = sorted_term1[i]
        var2, val2 = sorted_term2[i]
        if var1 != var2: 
            return False, None 
        if val1 != val2:
            differences += 1
            diff_var = var1
        i += 1
    return differences == 1, diff_var

def glue_terms(term1, term2, diff_var):
    new_term = []
    i = 0
    term1_sorted_for_glue = list_copy(term1)
    k_s = 0
    while k_s < list_len(term1_sorted_for_glue):
        m_s = 0
        while m_s < list_len(term1_sorted_for_glue) - k_s - 1:
            if term1_sorted_for_glue[m_s][0] > term1_sorted_for_glue[m_s+1][0]:
                temp_s = term1_sorted_for_glue[m_s]
                term1_sorted_for_glue[m_s] = term1_sorted_for_glue[m_s+1]
                term1_sorted_for_glue[m_s+1] = temp_s
            m_s += 1
        k_s += 1

    while i < list_len(term1_sorted_for_glue):
        var, val = term1_sorted_for_glue[i]
        if var != diff_var:
            new_term = list_append(new_term, (var, val))
        i += 1
    return new_term

def format_term(term, is_minterm):
    result_literals = []
    term_to_sort = list_copy(term)
    k = 0
    while k < list_len(term_to_sort):
        m = 0
        while m < list_len(term_to_sort) - k - 1:
            if term_to_sort[m][0] > term_to_sort[m+1][0]:
                temp = term_to_sort[m]
                term_to_sort[m] = term_to_sort[m+1]
                term_to_sort[m+1] = temp
            m += 1
        k += 1
    
    i = 0
    while i < list_len(term_to_sort):
        var, value = term_to_sort[i]
        literal = ""
        if is_minterm:
            if value == 1: literal = var
            else: literal = '!' + var
        else:
            if value == 0: literal = var
            else: literal = '!' + var
        result_literals = list_append(result_literals, literal)
        i += 1

    if not result_literals:
        return "1" if is_minterm else "0" 

    op_inside = '' 
    if not is_minterm: op_inside = '∨' 
    res_str = ""
    l_idx = 0
    while l_idx < list_len(result_literals):
        res_str += result_literals[l_idx]
        if op_inside != '' and l_idx < list_len(result_literals) - 1:
            res_str += op_inside
        l_idx +=1
    return res_str


def combine_terms(terms_list, sep_between_terms):
    result = ''
    if not terms_list:
        if sep_between_terms == ' ∨ ': return "0" 
        if sep_between_terms == ' ∧ ': return "1" 
        return ""

    i = 0
    while i < list_len(terms_list):
        term_str = terms_list[i]
        
        if sep_between_terms == ' ∧ ' and term_str != "0" and term_str != "1":
            needs_paren = False
            op_check_idx = 0
            has_internal_or = False
            while op_check_idx < list_len(term_str):
                if term_str[op_check_idx] == '∨':
                    has_internal_or = True
                    break
                op_check_idx += 1
            
            if has_internal_or: 
                needs_paren = True
            
            if needs_paren:
                 if not (term_str[0] == '(' and term_str[list_len(term_str)-1] == ')'):
                    result += '(' + term_str + ')'
                 else:
                    result += term_str 
            else: 
                result += term_str
        else:
            result += term_str
            
        if i < list_len(terms_list) - 1:
            result += sep_between_terms
        i += 1
    return result

def term_equals(term1, term2):
    if list_len(term1) != list_len(term2):
        return False
    
    sorted_term1 = list_copy(term1)
    k = 0
    while k < list_len(sorted_term1):
        m = 0
        while m < list_len(sorted_term1) - k - 1:
            if sorted_term1[m][0] > sorted_term1[m+1][0]:
                temp = sorted_term1[m]
                sorted_term1[m] = sorted_term1[m+1]
                sorted_term1[m+1] = temp
            m += 1
        k += 1

    sorted_term2 = list_copy(term2)
    k = 0
    while k < list_len(sorted_term2):
        m = 0
        while m < list_len(sorted_term2) - k - 1:
            if sorted_term2[m][0] > sorted_term2[m+1][0]:
                temp = sorted_term2[m]
                sorted_term2[m] = sorted_term2[m+1]
                sorted_term2[m+1] = temp
            m += 1
        k += 1

    i = 0
    while i < list_len(sorted_term1):
        var1, val1 = sorted_term1[i]
        var2, val2 = sorted_term2[i]
        if var1 != var2 or val1 != val2:
            return False
        i += 1
    return True

def remove_duplicates_from_list_of_terms(list_of_terms):
    unique_terms = []
    i = 0
    while i < list_len(list_of_terms):
        current_term = list_of_terms[i]
        is_duplicate = False
        j = 0
        while j < list_len(unique_terms):
            if term_equals(current_term, unique_terms[j]):
                is_duplicate = True
                break
            j += 1
        if not is_duplicate:
            unique_terms = list_append(unique_terms, current_term)
        i += 1
    return unique_terms

def minimize_terms(terms_to_minimize, is_minterm_type):
    if list_len(terms_to_minimize) == 0:
        return [], []
    
    prime_implicants_found = []
    current_group = list_copy(terms_to_minimize)
    current_group = remove_duplicates_from_list_of_terms(current_group)
    
    log_steps = []
    log_step_counter = 0

    while True:
        log_step_counter += 1
        next_group = []
        is_term_marked = [False] * list_len(current_group)
        any_glued_this_iteration = False

        i = 0
        while i < list_len(current_group):
            j = i + 1
            while j < list_len(current_group):
                can_be_glued, differing_var = can_glue(current_group[i], current_group[j])
                if can_be_glued:
                    glued_result = glue_terms(current_group[i], current_group[j], differing_var)
                    
                    is_newly_glued_duplicate = False
                    k_new_chk = 0
                    while k_new_chk < list_len(next_group):
                        if term_equals(next_group[k_new_chk], glued_result):
                            is_newly_glued_duplicate = True
                            break
                        k_new_chk += 1
                    if not is_newly_glued_duplicate:
                        next_group = list_append(next_group, glued_result)
                    
                    is_term_marked[i] = True
                    is_term_marked[j] = True
                    any_glued_this_iteration = True
                    log_steps = list_append(log_steps,
                        'Шаг ' + str(log_step_counter) + ': Склеивание ' +
                        format_term(current_group[i], is_minterm_type) + ' и ' +
                        format_term(current_group[j], is_minterm_type) + ' -> ' +
                        format_term(glued_result, is_minterm_type)
                    )
                j += 1
            i += 1

        idx_unmarked = 0
        while idx_unmarked < list_len(current_group):
            if not is_term_marked[idx_unmarked]:
                is_unmarked_duplicate_in_pi = False
                k_pi_chk = 0
                while k_pi_chk < list_len(prime_implicants_found):
                    if term_equals(prime_implicants_found[k_pi_chk], current_group[idx_unmarked]):
                        is_unmarked_duplicate_in_pi = True
                        break
                    k_pi_chk += 1
                if not is_unmarked_duplicate_in_pi:
                    prime_implicants_found = list_append(prime_implicants_found, current_group[idx_unmarked])
            idx_unmarked += 1
        
        if not any_glued_this_iteration:
            break 
        
        current_group = remove_duplicates_from_list_of_terms(next_group)
        if not current_group: 
            break

    final_selected_implicants = []
    if list_len(prime_implicants_found) > 0 and list_len(terms_to_minimize) > 0:
        coverage_matrix = []
        i_orig_term_cov = 0
        while i_orig_term_cov < list_len(terms_to_minimize):
            row_cov = []
            j_pi_cov = 0
            while j_pi_cov < list_len(prime_implicants_found):
                pi_for_cov = prime_implicants_found[j_pi_cov]
                orig_for_cov = terms_to_minimize[i_orig_term_cov]
                term_is_covered = True
                k_pi_lit_cov = 0
                while k_pi_lit_cov < list_len(pi_for_cov):
                    var_p_cov, val_p_cov = pi_for_cov[k_pi_lit_cov]
                    match_in_orig = False
                    k_orig_lit_cov = 0
                    while k_orig_lit_cov < list_len(orig_for_cov):
                        var_o_cov, val_o_cov = orig_for_cov[k_orig_lit_cov]
                        if var_p_cov == var_o_cov:
                            if val_p_cov == val_o_cov: match_in_orig = True
                            break 
                        k_orig_lit_cov +=1
                    if not match_in_orig:
                        term_is_covered = False; break
                    k_pi_lit_cov +=1
                row_cov = list_append(row_cov, 1 if term_is_covered else 0)
                j_pi_cov +=1
            coverage_matrix = list_append(coverage_matrix, row_cov)
            i_orig_term_cov +=1

        uncovered_orig_indices = []
        idx_uot_c_init = 0
        while idx_uot_c_init < list_len(terms_to_minimize):
            uncovered_orig_indices = list_append(uncovered_orig_indices, idx_uot_c_init)
            idx_uot_c_init +=1

        while list_len(uncovered_orig_indices) > 0:
            essential_pass_made_change = False
            current_uncovered_after_pass = list_copy(uncovered_orig_indices)
            
            idx_uot_ess_c = 0
            while idx_uot_ess_c < list_len(uncovered_orig_indices):
                ot_real_idx_c = uncovered_orig_indices[idx_uot_ess_c]
                pis_covering_this_ot_c = []
                idx_pi_ess_c = 0
                while idx_pi_ess_c < list_len(prime_implicants_found):
                    if coverage_matrix[ot_real_idx_c][idx_pi_ess_c] == 1:
                        is_sel_ess = False
                        for sel_pi_e_chk in final_selected_implicants:
                            if term_equals(sel_pi_e_chk, prime_implicants_found[idx_pi_ess_c]):
                                is_sel_ess = True; break
                        if not is_sel_ess:
                             pis_covering_this_ot_c = list_append(pis_covering_this_ot_c, idx_pi_ess_c)
                    idx_pi_ess_c +=1
                
                if list_len(pis_covering_this_ot_c) == 1:
                    ess_pi_idx_c = pis_covering_this_ot_c[0]
                    ess_pi_c = prime_implicants_found[ess_pi_idx_c]
                    final_selected_implicants = list_append(final_selected_implicants, ess_pi_c)
                    essential_pass_made_change = True
                    
                    new_uncovered_c = []
                    idx_uot_upd_c = 0
                    while idx_uot_upd_c < list_len(current_uncovered_after_pass):
                        ot_idx_upd_c_val = current_uncovered_after_pass[idx_uot_upd_c]
                        if not (coverage_matrix[ot_idx_upd_c_val][ess_pi_idx_c] == 1) :
                            new_uncovered_c = list_append(new_uncovered_c, ot_idx_upd_c_val)
                        idx_uot_upd_c += 1
                    current_uncovered_after_pass = new_uncovered_c
                idx_uot_ess_c += 1
            uncovered_orig_indices = current_uncovered_after_pass
            
            if not essential_pass_made_change and list_len(uncovered_orig_indices) > 0:
                best_pi_greedy_idx_c = -1
                max_new_cov_greedy_c = 0
                idx_pi_g_c = 0
                while idx_pi_g_c < list_len(prime_implicants_found):
                    is_sel_g = False
                    for sel_g_chk in final_selected_implicants:
                        if term_equals(sel_g_chk, prime_implicants_found[idx_pi_g_c]):
                            is_sel_g = True; break
                    if is_sel_g: idx_pi_g_c +=1; continue

                    curr_pi_new_cov_c = 0
                    idx_uot_g_cov_c = 0
                    while idx_uot_g_cov_c < list_len(uncovered_orig_indices):
                        ot_idx_g_c = uncovered_orig_indices[idx_uot_g_cov_c]
                        if coverage_matrix[ot_idx_g_c][idx_pi_g_c] == 1:
                            curr_pi_new_cov_c +=1
                        idx_uot_g_cov_c +=1
                    
                    if curr_pi_new_cov_c > max_new_cov_greedy_c:
                        max_new_cov_greedy_c = curr_pi_new_cov_c
                        best_pi_greedy_idx_c = idx_pi_g_c
                    elif curr_pi_new_cov_c == max_new_cov_greedy_c and best_pi_greedy_idx_c != -1:
                         if list_len(prime_implicants_found[idx_pi_g_c]) < list_len(prime_implicants_found[best_pi_greedy_idx_c]):
                            best_pi_greedy_idx_c = idx_pi_g_c
                    idx_pi_g_c +=1
                
                if best_pi_greedy_idx_c != -1 and max_new_cov_greedy_c > 0 :
                    best_g_pi = prime_implicants_found[best_pi_greedy_idx_c]
                    final_selected_implicants = list_append(final_selected_implicants, best_g_pi)
                    new_uncovered_list_gc = []
                    idx_uot_upd_gc = 0
                    while idx_uot_upd_gc < list_len(uncovered_orig_indices):
                        ot_idx_upd_gc_val = uncovered_orig_indices[idx_uot_upd_gc]
                        if not (coverage_matrix[ot_idx_upd_gc_val][best_pi_greedy_idx_c] == 1) :
                            new_uncovered_list_gc = list_append(new_uncovered_list_gc, ot_idx_upd_gc_val)
                        idx_uot_upd_gc += 1
                    uncovered_orig_indices = new_uncovered_list_gc
                else: break 
            if not list_len(uncovered_orig_indices) > 0: break
    elif list_len(terms_to_minimize) > 0 and list_len(prime_implicants_found) == 0 :
        final_selected_implicants = list_copy(terms_to_minimize)


    final_selected_implicants = remove_duplicates_from_list_of_terms(final_selected_implicants)
    return final_selected_implicants, log_steps


def minimize_terms_calc_table(terms, is_minterm, original_terms_for_coverage):
    selected_implicants, glue_steps = minimize_terms(terms, is_minterm) 
    
    
    coverage_table_output = []
    if list_len(selected_implicants) > 0 and list_len(original_terms_for_coverage) > 0:
        header_row = ['Терм']
        idx_h_pi = 0
        while idx_h_pi < list_len(selected_implicants): 
            header_row = list_append(header_row, format_term(selected_implicants[idx_h_pi], is_minterm))
            idx_h_pi +=1
        coverage_table_output = list_append(coverage_table_output, header_row)

        idx_ot_row = 0
        while idx_ot_row < list_len(original_terms_for_coverage):
            current_row_data = [format_term(original_terms_for_coverage[idx_ot_row], is_minterm)]
            idx_pi_col = 0
            while idx_pi_col < list_len(selected_implicants): 
                pi_term_ct = selected_implicants[idx_pi_col]
                orig_term_ct = original_terms_for_coverage[idx_ot_row]
                covers_ct = True 
                k_pi_lit_ct = 0
                while k_pi_lit_ct < list_len(pi_term_ct): 
                    var_p_ct, val_p_ct = pi_term_ct[k_pi_lit_ct]
                    found_in_orig_ct = False
                    k_orig_lit_ct = 0
                    while k_orig_lit_ct < list_len(orig_term_ct): 
                        var_o_ct, val_o_ct = orig_term_ct[k_orig_lit_ct]
                        if var_p_ct == var_o_ct: 
                            if val_p_ct == val_o_ct: 
                                found_in_orig_ct = True
                            break 
                        k_orig_lit_ct +=1
                    if not found_in_orig_ct: 
                        covers_ct = False
                        break
                    k_pi_lit_ct +=1
                current_row_data = list_append(current_row_data, 'X' if covers_ct else '.')
                idx_pi_col +=1
            coverage_table_output = list_append(coverage_table_output, current_row_data)
            idx_ot_row +=1
            
    return selected_implicants, glue_steps, coverage_table_output


def get_gray_codes(num_bits):
    if num_bits == 0: return [""] 
    if num_bits == 1: return ["0", "1"]
    
    prev_codes = get_gray_codes(num_bits - 1)
    new_codes = []
    i = 0
    while i < list_len(prev_codes):
        new_codes = list_append(new_codes, "0" + prev_codes[i])
        i += 1
    i = list_len(prev_codes) - 1
    while i >= 0:
        new_codes = list_append(new_codes, "1" + prev_codes[i])
        i -= 1
    return new_codes

def get_kmap_layout_and_fill(original_terms, variables, is_minterm):
    n_vars = list_len(variables)
    fill_value = 1 if is_minterm else 0
    default_value = 0 if is_minterm else 1

    rows_kmap, cols_kmap = 0, 0
    row_var_count, col_var_count = 0, 0

    if n_vars == 1: rows_kmap, cols_kmap, row_var_count, col_var_count = 1, 2, 0, 1
    elif n_vars == 2: rows_kmap, cols_kmap, row_var_count, col_var_count = 2, 2, 1, 1
    elif n_vars == 3: rows_kmap, cols_kmap, row_var_count, col_var_count = 2, 4, 1, 2
    elif n_vars == 4: rows_kmap, cols_kmap, row_var_count, col_var_count = 4, 4, 2, 2
    elif n_vars == 5: rows_kmap, cols_kmap, row_var_count, col_var_count = 4, 8, 2, 3
    else: return None, None, None, None

    kmap = []
    r_idx = 0
    while r_idx < rows_kmap:
        col_list = []
        c_idx = 0
        while c_idx < cols_kmap:
            col_list = list_append(col_list, default_value)
            c_idx += 1
        kmap = list_append(kmap, col_list)
        r_idx += 1
    
    gray_codes_for_rows = get_gray_codes(row_var_count)
    gray_codes_for_cols = get_gray_codes(col_var_count)

    idx_term = 0
    while idx_term < list_len(original_terms):
        term = original_terms[idx_term]
        term_values_dict = {}
        idx_lit = 0
        while idx_lit < list_len(term):
            var_name, var_val = term[idx_lit]
            term_values_dict[var_name] = var_val
            idx_lit +=1

        row_k, col_k = -1, -1
        row_vars_str_val = ""
        col_vars_str_val = ""

        var_map_idx = 0
        while var_map_idx < row_var_count: 
            row_vars_str_val += str(term_values_dict[variables[var_map_idx]])
            var_map_idx += 1
        
        var_map_idx = 0
        while var_map_idx < col_var_count: 
            col_vars_str_val += str(term_values_dict[variables[row_var_count + var_map_idx]])
            var_map_idx += 1

        if row_var_count == 0: row_k = 0
        else:
            r_gc_idx = 0
            while r_gc_idx < list_len(gray_codes_for_rows):
                if gray_codes_for_rows[r_gc_idx] == row_vars_str_val:
                    row_k = r_gc_idx; break
                r_gc_idx += 1
        
        c_gc_idx = 0
        while c_gc_idx < list_len(gray_codes_for_cols):
            if gray_codes_for_cols[c_gc_idx] == col_vars_str_val:
                col_k = c_gc_idx; break
            c_gc_idx += 1

        if row_k != -1 and col_k != -1:
            kmap[row_k][col_k] = fill_value
        idx_term += 1
    
    kmap_params_for_output = (gray_codes_for_rows, gray_codes_for_cols, row_var_count, col_var_count, variables)
    return kmap, kmap_params_for_output, rows_kmap, cols_kmap


def format_kmap_for_print(kmap_matrix, kmap_params):
    gray_codes_for_rows, gray_codes_for_cols, row_var_count, col_var_count, variables = kmap_params
    
    kmap_output_table = []
    n_vars = list_len(variables)

    if n_vars > 0 and list_len(kmap_matrix) > 0:
        header_print_row = [""] 
        idx_col_h = 0
        while idx_col_h < list_len(gray_codes_for_cols):
            gc_col = gray_codes_for_cols[idx_col_h]
            label_col = ""
            current_col_vars = []
            idx_cv = 0
            while idx_cv < col_var_count:
                current_col_vars = list_append(current_col_vars, variables[row_var_count + idx_cv])
                idx_cv +=1
            
            l_cv_str = ""
            idx_lcv =0
            while idx_lcv < list_len(current_col_vars):
                l_cv_str += current_col_vars[idx_lcv]
                idx_lcv+=1
            if list_len(l_cv_str)>0 : label_col = l_cv_str + "=" + gc_col
            else: label_col = gc_col 

            header_print_row = list_append(header_print_row, label_col)
            idx_col_h += 1
        kmap_output_table = list_append(kmap_output_table, header_print_row)

        idx_row_p = 0
        while idx_row_p < list_len(kmap_matrix): 
            current_print_row = []
            label_row = ""
            if row_var_count > 0:
                gc_row = gray_codes_for_rows[idx_row_p]
                current_row_vars = []
                idx_rv = 0
                while idx_rv < row_var_count:
                    current_row_vars = list_append(current_row_vars, variables[idx_rv])
                    idx_rv +=1
                l_rv_str = ""
                idx_lrv =0
                while idx_lrv < list_len(current_row_vars):
                    l_rv_str += current_row_vars[idx_lrv]
                    idx_lrv +=1
                label_row = l_rv_str + "=" + gc_row
            elif n_vars == 1: 
                 label_row = ""


            current_print_row = list_append(current_print_row, label_row)
            
            idx_col_p = 0
            while idx_col_p < list_len(kmap_matrix[idx_row_p]):
                current_print_row = list_append(current_print_row, str(kmap_matrix[idx_row_p][idx_col_p]))
                idx_col_p +=1
            kmap_output_table = list_append(kmap_output_table, current_print_row)
            idx_row_p +=1
    return kmap_output_table

def minimize_terms_karnaugh(original_terms, is_minterm, variables):
    if list_len(original_terms) == 0:
        return [], [], [['Карта Карно: нет термов для минимизации.']]
    n_vars = list_len(variables)
    if n_vars == 0: return [], [], [['Карта Карно: нет переменных.']]
    if n_vars > 5: return [], [], [['Карта Карно: Поддерживается до 5 переменных.']]

    kmap_fill_data = get_kmap_layout_and_fill(original_terms, variables, is_minterm)
    if kmap_fill_data[0] is None:
        return [], [], [['Карта Карно: Ошибка инициализации карты.']]
    
    filled_kmap, kmap_params_out, _, _ = kmap_fill_data
    kmap_output_for_print = format_kmap_for_print(filled_kmap, kmap_params_out)
    
    minimized_selected_implicants, minimization_log_steps, _ = \
        minimize_terms_calc_table(original_terms, is_minterm, original_terms)
        

    return minimized_selected_implicants, minimization_log_steps, kmap_output_for_print