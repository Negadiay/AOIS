import pytest
import re
from main import print_table, print_coverage_table, print_karnaugh_map, main
from parser import tokenize, get_variables, to_postfix
from evaluator import generate_table
from minimizer import build_sdnf, build_sknf, minimize_terms_calc_table

# Fixture for test expression (a&b)
@pytest.fixture
def test_expression():
    expr = "(a&b)"
    tokens = tokenize(expr)
    variables = get_variables(tokens)
    postfix = to_postfix(tokens)
    table = generate_table(postfix, variables)
    return {
        'expr': expr,
        'variables': variables,
        'tokens': tokens,
        'postfix': postfix,
        'table': table
    }

# Helper to normalize output for comparison
def normalize_output(text):
    return re.sub(r'\s+', ' ', text.strip())

# Test print_table function
def test_print_table(test_expression, capsys):
    table = test_expression['table']
    variables = test_expression['variables']
    expr = test_expression['expr']
    print_table(table, variables, expr)
    captured = capsys.readouterr().out

    # Expected output for (a&b)
    expected_lines = [
        "a | b | (a&b)",
        "-" * 10,  # Separator matches actual output (10 dashes)
        "0 | 0 |   0",
        "0 | 1 |   0",
        "1 | 0 |   0",
        "1 | 1 |   1"
    ]
    captured_lines = captured.split('\n')
    for expected in expected_lines:
        assert any(expected.strip() in line.strip() for line in captured_lines), f"Expected line '{expected}' in truth table"

# Test SDNF and SKNF term generation
def test_sdnf_sknf_terms(test_expression):
    table = test_expression['table']
    variables = test_expression['variables']
    sdnf_terms = build_sdnf(table, variables)
    sknf_terms = build_sknf(table, variables)

    # Expected SDNF terms (1 minterm)
    expected_sdnf_terms = [
        [('a', 1), ('b', 1)]  # ab
    ]
    assert len(sdnf_terms) == 1, f"SDNF term count: expected 1, got {len(sdnf_terms)}"
    for term in sdnf_terms:
        assert term in expected_sdnf_terms, f"Unexpected SDNF term: {term}"

    # Expected SKNF terms (3 maxterms)
    expected_sknf_terms = [
        [('a', 0), ('b', 0)],  # !a!b
        [('a', 0), ('b', 1)],  # !ab
        [('a', 1), ('b', 0)]   # a!b
    ]
    assert len(sknf_terms) == 3, f"SKNF term count: expected 3, got {len(sknf_terms)}"
    for term in sknf_terms:
        assert term in expected_sknf_terms, f"Unexpected SKNF term: {term}"

# Test main with empty expression
def test_main_empty_expression(capsys, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "")
    main()
    captured = capsys.readouterr().out
    assert "Ошибка: Нет переменных в выражении" in captured, "Empty expression not handled"

# Test main with too many variables
def test_main_too_many_variables(capsys, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "(a&b&c&d&e&f)")
    main()
    captured = capsys.readouterr().out
    assert "Ошибка: list index out of range" in captured, "Too many variables not handled"

# Test main with invalid expression
def test_main_invalid_expression(capsys, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "a & z")
    main()
    captured = capsys.readouterr().out
    assert "Ошибка:" in captured, "Invalid expression not handled"

# Test main with constant false expression
def test_main_constant_false(capsys, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "a & !a")
    main()
    captured = capsys.readouterr().out
    assert "СДНФ пустая (функция всегда 0)" in captured, "Constant false SDNF not handled"

# Test main with constant true expression
def test_main_constant_true(capsys, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "a | !a")
    main()
    captured = capsys.readouterr().out
    assert "СКНФ пустая (функция всегда 1)" in captured, "Constant true SKNF not handled"

# Test main with single variable expression
def test_main_single_variable(capsys, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "a")
    main()
    captured = capsys.readouterr().out
    assert "Таблица истинности:" in captured, "Single variable truth table not printed"
    assert "Исходная СДНФ: a" in captured, "Single variable SDNF incorrect"
    assert "Исходная СКНФ: a" in captured, "Single variable SKNF incorrect"
    assert "Минимизированная СДНФ: a" in captured, "Single variable minimized SDNF incorrect"
    assert "Минимизированная СКНФ: a" in captured, "Single variable minimized SKNF incorrect"