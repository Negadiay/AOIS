import pytest
from minimizer import (
    build_sdnf, build_sknf, sort_term, terms_equal, remove_duplicates,
    can_glue_terms, glue_terms, format_term, combine_terms, is_covered_by_pi,
    build_coverage_matrix, get_uncovered_indices, find_essential_pis,
    find_greedy_pis, minimize_terms, minimize_terms_calc_table,
    get_gray_codes, get_kmap_dimensions, fill_kmap_cells,
    get_kmap_fill_data, format_kmap_for_print, minimize_terms_karnaugh
)

# Mock utils.py functions to avoid dependency on actual implementation
def mock_list_len(lst):
    return len(lst)

def mock_list_append(lst, val):
    return lst + [val]

def mock_list_contains(lst, val):
    return val in lst

def mock_list_copy(lst):
    return lst[:]

# Fixture to mock utils functions
@pytest.fixture(autouse=True)
def mock_utils(monkeypatch):
    monkeypatch.setattr("minimizer.list_len", mock_list_len)
    monkeypatch.setattr("minimizer.list_append", mock_list_append)
    monkeypatch.setattr("minimizer.list_contains", mock_list_contains)
    monkeypatch.setattr("minimizer.list_copy", mock_list_copy)

def test_build_sdnf():
    table = [([0, 0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 0)]
    variables = ['a', 'b']
    result = build_sdnf(table, variables)
    expected = [[('a', 0), ('b', 1)], [('a', 1), ('b', 0)]]
    assert all(any(terms_equal(r, e) for e in expected) for r in result)
    assert len(result) == len(expected)

def test_build_sknf():
    table = [([0, 0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 0)]
    variables = ['a', 'b']
    result = build_sknf(table, variables)
    expected = [[('a', 0), ('b', 0)], [('a', 1), ('b', 1)]]
    assert all(any(terms_equal(r, e) for e in expected) for r in result)
    assert len(result) == len(expected)

def test_sort_term():
    term = [('b', 1), ('a', 0)]
    result = sort_term(term)
    expected = [('a', 0), ('b', 1)]
    assert result == expected

def test_terms_equal():
    t1 = [('a', 0), ('b', 1)]
    t2 = [('b', 1), ('a', 0)]
    t3 = [('a', 0), ('b', 0)]
    assert terms_equal(t1, t2)
    assert not terms_equal(t1, t3)

def test_remove_duplicates():
    terms = [[('a', 0), ('b', 1)], [('b', 1), ('a', 0)], [('a', 1), ('b', 0)]]
    result = remove_duplicates(terms)
    expected = [[('a', 0), ('b', 1)], [('a', 1), ('b', 0)]]
    assert all(any(terms_equal(r, e) for e in expected) for r in result)
    assert len(result) == len(expected)

def test_glue_terms():
    t1 = [('a', 0), ('b', 1)]
    result = glue_terms(t1, 'b')
    expected = [('a', 0)]
    assert terms_equal(result, expected)

def test_is_covered_by_pi():
    orig = [('a', 1), ('b', 0), ('c', 1)]
    pi = [('a', 1), ('c', 1)]
    assert is_covered_by_pi(orig, pi)
    pi = [('a', 0), ('c', 1)]
    assert not is_covered_by_pi(orig, pi)

def test_build_coverage_matrix():
    orig_terms = [[('a', 0), ('b', 1)], [('a', 1), ('b', 0)]]
    pis = [[('a', 0)], [('b', 0)]]
    result = build_coverage_matrix(orig_terms, pis)
    expected = [[1, 0], [0, 1]]
    assert result == expected

def test_get_uncovered_indices():
    assert get_uncovered_indices(3) == [0, 1, 2]

def test_find_essential_pis():
    pis = [[('a', 0)], [('b', 0)]]
    cov_matrix = [[1, 0], [0, 1]]
    uncovered = [0, 1]
    selected = []
    result, new_uncovered, changed = find_essential_pis(pis, cov_matrix, uncovered, selected)
    expected = [[('a', 0)], [('b', 0)]]
    assert all(any(terms_equal(r, e) for e in expected) for r in result)
    assert new_uncovered == []
    assert changed

def test_minimize_terms_sdnf():
    terms = [[('a', 0), ('b', 1)], [('a', 1), ('b', 0)]]
    min_terms, steps = minimize_terms(terms, True)
    expected = [[('a', 0), ('b', 1)], [('a', 1), ('b', 0)]]
    assert all(any(terms_equal(r, e) for e in expected) for r in min_terms)
    assert steps == []

def test_minimize_terms_empty():
    min_terms, steps = minimize_terms([], True)
    assert min_terms == []
    assert steps == []

def test_get_gray_codes():
    assert get_gray_codes(0) == [""]
    assert get_gray_codes(1) == ["0", "1"]
    assert get_gray_codes(2) == ["00", "01", "11", "10"]

def test_get_kmap_dimensions():
    assert get_kmap_dimensions(1) == (1, 2, 0, 1)
    assert get_kmap_dimensions(3) == (2, 4, 1, 2)
    assert get_kmap_dimensions(6) == (None, None, None, None)

def test_fill_kmap_cells():
    kmap = [[0, 0], [0, 0]]
    terms = [[('a', 0), ('b', 1)]]
    variables = ['a', 'b']
    gc_rows = ["0", "1"]
    gc_cols = ["0", "1"]
    kmap = fill_kmap_cells(kmap, terms, variables, True, 1, 1, gc_rows, gc_cols, 1, 0)
    assert kmap == [[0, 1], [0, 0]]

def test_get_kmap_fill_data():
    terms = [[('a', 0), ('b', 1)]]
    variables = ['a', 'b']
    kmap, params, r, c = get_kmap_fill_data(terms, variables, True)
    assert kmap == [[0, 1], [0, 0]]
    assert params[0] == ["0", "1"]
    assert params[1] == ["0", "1"]
    assert r == 2
    assert c == 2

def test_format_kmap_for_print():
    kmap = [[0, 1], [0, 0]]
    params = (["0", "1"], ["0", "1"], 1, 1, ['a', 'b'])
    result = format_kmap_for_print(kmap, params)
    expected = [["", "b=0", "b=1"], ["a=0", "0", "1"], ["a=1", "0", "0"]]
    assert result == expected

def test_minimize_terms_karnaugh():
    terms = [[('a', 0), ('b', 1)]]
    variables = ['a', 'b']
    min_terms, steps, kmap = minimize_terms_karnaugh(terms, True, variables)
    assert terms_equal(min_terms[0], [('a', 0), ('b', 1)])
    assert kmap[0] == ["", "b=0", "b=1"]
    assert kmap[1][1:] == ["0", "1"]

def test_minimize_terms_karnaugh_empty():
    result = minimize_terms_karnaugh([], True, [])
    assert result == ([], [], [["Карта Карно: нет термов для минимизации."]])

