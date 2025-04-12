import pytest
from main import (
    str_len, str_get, list_len, list_append, list_contains,
    list_sort, is_variable, tokenize, get_variables,
    get_precedence, to_postfix, apply_op, apply_not,
    evaluate_postfix, generate_table, build_sdnf,
    build_sknf, combine_terms, get_index_form,
    get_numeric_forms, main
)

# Test basic string operations
def test_str_operations():
    assert str_len("") == 0
    assert str_len("abc") == 3
    assert str_get("abc", 1) == 'b'
    with pytest.raises(IndexError):
        str_get("abc", 5)

# Test list operations
def test_list_operations():
    assert list_len([]) == 0
    assert list_len([1, 2, 3]) == 3
    
    lst = []
    lst = list_append(lst, 1)
    assert lst == [1]
    lst = list_append(lst, 2)
    assert lst == [1, 2]
    
    assert list_contains([1, 2, 3], 2) is True
    assert list_contains([1, 2, 3], 4) is False
    
    assert list_sort([3, 1, 2]) == [1, 2, 3]
    assert list_sort(['c', 'a', 'b']) == ['a', 'b', 'c']

# Test variable detection
def test_is_variable():
    assert is_variable('a') is True
    assert is_variable('b') is True
    assert is_variable('e') is True
    assert is_variable('f') is False
    assert is_variable('!') is False
    assert is_variable(' ') is False

# Test tokenizer
def test_tokenize():
    assert tokenize("") == []
    assert tokenize("a & b") == ['a', '&', 'b']
    assert tokenize("a -> b") == ['a', '->', 'b']
    assert tokenize("!(a | b)") == ['!', '(', 'a', '|', 'b', ')']
    assert tokenize("a ~ b") == ['a', '~', 'b']
    assert tokenize("  a  b  ") == ['a', 'b']  # Test spaces
    assert tokenize("a & (b | c)") == ['a', '&', '(', 'b', '|', 'c', ')']

# Test variable extraction
def test_get_variables():
    assert get_variables([]) == []
    assert get_variables(['a', '&', 'b']) == ['a', 'b']
    assert get_variables(['a', '->', 'b', '&', 'c']) == ['a', 'b', 'c']
    assert get_variables(['!', 'a']) == ['a']
    assert get_variables(['(', 'a', '|', 'b', ')']) == ['a', 'b']

# Test operator precedence
def test_get_precedence():
    assert get_precedence('!') == 4
    assert get_precedence('~') == 3
    assert get_precedence('&') == 2
    assert get_precedence('|') == 1
    assert get_precedence('->') == 0
    assert get_precedence('(') == -1
    assert get_precedence(')') == -1
    assert get_precedence('a') == -1

# Test postfix conversion
def test_to_postfix():
    assert to_postfix(['a']) == ['a']
    assert to_postfix(['a', '&', 'b']) == ['a', 'b', '&']
    assert to_postfix(['!', 'a']) == ['a', '!']
    assert to_postfix(['a', '->', 'b', '&', 'c']) == ['a', 'b', 'c', '&', '->']
    assert to_postfix(['(', 'a', '|', 'b', ')', '&', 'c']) == ['a', 'b', '|', 'c', '&']
    assert to_postfix(['a', '~', 'b']) == ['a', 'b', '~']

# Test operator application
def test_apply_operations():
    assert apply_op('&', 1, 1) == 1
    assert apply_op('&', 1, 0) == 0
    assert apply_op('|', 1, 0) == 1
    assert apply_op('|', 0, 0) == 0
    assert apply_op('->', 1, 1) == 1
    assert apply_op('->', 1, 0) == 0
    assert apply_op('->', 0, 1) == 1
    assert apply_op('~', 1, 1) == 1
    assert apply_op('~', 1, 0) == 0
    assert apply_not(1) == 0
    assert apply_not(0) == 1

# Test postfix evaluation
def test_evaluate_postfix():
    assert evaluate_postfix(['a'], {'a': 1}) == 1
    assert evaluate_postfix(['a', 'b', '&'], {'a': 1, 'b': 1}) == 1
    assert evaluate_postfix(['a', 'b', '&'], {'a': 1, 'b': 0}) == 0
    assert evaluate_postfix(['a', '!'], {'a': 1}) == 0
    assert evaluate_postfix(['a', 'b', '|'], {'a': 0, 'b': 0}) == 0
    assert evaluate_postfix(['a', 'b', '->'], {'a': 0, 'b': 1}) == 1

# Test table generation
def test_generate_table():
    # Test with one variable
    table = generate_table(['a'], ['a'])
    assert len(table) == 2
    assert ([0], 0) in table
    assert ([1], 1) in table

    # Test with two variables
    table = generate_table(['a', 'b', '&'], ['a', 'b'])
    assert len(table) == 4
    assert ([0, 0], 0) in table
    assert ([0, 1], 0) in table
    assert ([1, 0], 0) in table
    assert ([1, 1], 1) in table

# Test normal forms
def test_normal_forms():
    table = [
        ([0, 0], 0),
        ([0, 1], 1),
        ([1, 0], 1),
        ([1, 1], 1)
    ]
    
    # Test SDNF
    sdnf, sdnf_i = build_sdnf(table, ['a', 'b'])
    assert "¬a∧b" in sdnf or "b∧¬a" in sdnf
    assert "a∧¬b" in sdnf or "¬b∧a" in sdnf
    assert "a∧b" in sdnf
    assert sorted(sdnf_i) == [1, 2, 3]
    
    # Test SKNF
    sknf, sknf_i = build_sknf(table, ['a', 'b'])
    assert sknf == "(a∨b)"
    assert sknf_i == [0]
    
    # Test term combination
    assert combine_terms([], " & ") == ""
    assert combine_terms(["a"], " & ") == "a"
    assert combine_terms(["a", "b"], " ∨ ") == "a ∨ b"

# Test numeric forms
def test_numeric_forms():
    table = [
        ([0, 0], 0),
        ([0, 1], 1),
        ([1, 0], 1),
        ([1, 1], 1)
    ]
    sdnf_nums, sknf_nums = get_numeric_forms(table)
    assert sorted(sdnf_nums) == [1, 2, 3]
    assert sknf_nums == [0]
    
    dec, bin_str = get_index_form(table)
    assert dec == 7
    assert bin_str == "0111"

# Test main function with mocked input
def test_main(monkeypatch, capsys):
    # Test with simple AND expression
    monkeypatch.setattr('builtins.input', lambda _: "a & b")
    main()
    captured = capsys.readouterr()
    assert "Таблица истинности:" in captured.out
    assert "СДНФ:" in captured.out
    assert "СКНФ:" in captured.out
    
    # Test with empty expression
    with pytest.raises(Exception):
        main("")

def test_main_with_input():
    # Test with direct input
    result = main("a & b")
    # Add assertions based on what main() returns or prints
    
def test_main_with_mock(monkeypatch, capsys):
    # Test with mocked input
    monkeypatch.setattr('builtins.input', lambda _: "a | b")
    main()
    captured = capsys.readouterr()
    assert "Таблица истинности:" in captured.out        
