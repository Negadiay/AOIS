import pytest
from minimizer import (
    build_sdnf, build_sknf, term_is_subsumed_by_list, can_glue, glue_terms,
    format_term, combine_terms, term_equals, remove_duplicates_from_list_of_terms,
    minimize_terms, minimize_terms_calc_table, get_gray_codes,
    get_kmap_layout_and_fill, format_kmap_for_print, minimize_terms_karnaugh
)
from utils import list_append, list_copy

def test_build_sdnf():
    table = [([0, 0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 0)]
    variables = ["a", "b"]
    sdnf = build_sdnf(table, variables)
    expected = [[("a", 0), ("b", 1)], [("a", 1), ("b", 0)]]
    assert len(sdnf) == len(expected)
    for term, exp_term in zip(sdnf, expected):
        assert term == exp_term

def test_build_sknf():
    table = [([0, 0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 0)]
    variables = ["a", "b"]
    sknf = build_sknf(table, variables)
    expected = [[("a", 0), ("b", 0)], [("a", 1), ("b", 1)]]
    assert len(sknf) == len(expected)
    for term, exp_term in zip(sknf, expected):
        assert term == exp_term

def test_term_is_subsumed_by_list():
    term = [("a", 1), ("b", 0), ("c", 1)]
    implicants = [[("a", 1), ("c", 1)]]
    assert term_is_subsumed_by_list(term, implicants) == True
    implicants = [[("a", 1), ("b", 1)]]
    assert term_is_subsumed_by_list(term, implicants) == False

def test_glue_terms():
    term1 = [("a", 1), ("b", 0)]
    term2 = [("a", 1), ("b", 1)]
    result = glue_terms(term1, term2, "b")
    assert result == [("a", 1)]
    term1 = [("a", 1), ("b", 0)]
    term2 = [("a", 0), ("b", 0)]
    result = glue_terms(term1, term2, "a")
    assert result == [("b", 0)]



def test_term_equals():
    term1 = [("a", 1), ("b", 0)]
    term2 = [("b", 0), ("a", 1)]
    assert term_equals(term1, term2) == True
    term2 = [("a", 1), ("b", 1)]
    assert term_equals(term1, term2) == False

def test_remove_duplicates_from_list_of_terms():
    terms = [[("a", 1), ("b", 0)], [("b", 0), ("a", 1)], [("a", 1), ("b", 1)]]
    result = remove_duplicates_from_list_of_terms(terms)
    expected = [[("a", 1), ("b", 0)], [("a", 1), ("b", 1)]]
    assert len(result) == len(expected)
    for term in result:
        assert term in expected

def test_minimize_terms():
    terms = [[("a", 0), ("b", 0)], [("a", 0), ("b", 1)]]
    min_terms, steps = minimize_terms(terms, True)
    assert min_terms == [[("a", 0)]]
    assert len(steps) > 0
    terms = []
    min_terms, steps = minimize_terms(terms, True)
    assert min_terms == []
    assert steps == []

def test_minimize_terms_calc_table():
    terms = [[("a", 0), ("b", 0)], [("a", 0), ("b", 1)]]
    min_terms, steps, table = minimize_terms_calc_table(terms, True, terms)
    assert min_terms == [[("a", 0)]]
    assert len(table) > 0
    assert table[0][0] == "Терм"
    terms = []
    min_terms, steps, table = minimize_terms_calc_table(terms, True, terms)
    assert min_terms == []
    assert table == []

def test_get_gray_codes():
    assert get_gray_codes(0) == [""]
    assert get_gray_codes(1) == ["0", "1"]
    assert get_gray_codes(2) == ["00", "01", "11", "10"]
    assert get_gray_codes(3) == ["000", "001", "011", "010", "110", "111", "101", "100"]

def test_get_kmap_layout_and_fill():
    terms = [[("a", 0), ("b", 1)], [("a", 1), ("b", 0)]]
    variables = ["a", "b"]
    kmap, params, rows, cols = get_kmap_layout_and_fill(terms, variables, True)
    assert rows == 2
    assert cols == 2
    assert kmap[0][1] == 1
    assert kmap[1][0] == 1
    assert kmap[0][0] == 0
    assert kmap[1][1] == 0

def test_format_kmap_for_print():
    kmap = [[0, 1], [1, 0]]
    params = (["0", "1"], ["0", "1"], 1, 1, ["a", "b"])
    table = format_kmap_for_print(kmap, params)
    assert len(table) == 3
    assert table[0][0] == ""
    assert "b=0" in table[0] or "b=1" in table[0]
    assert table[1][1] == "0" or table[1][1] == "1"

def test_minimize_terms_karnaugh():
    terms = [[("a", 0), ("b", 0)], [("a", 0), ("b", 1)]]
    variables = ["a", "b"]
    min_terms, steps, table = minimize_terms_karnaugh(terms, True, variables)
    assert min_terms == [[("a", 0)]]
    assert len(table) > 0
    terms = []
    min_terms, steps, table = minimize_terms_karnaugh(terms, True, [])
    assert table == [['Карта Карно: нет термов для минимизации.']]