import pytest
from io import StringIO
from contextlib import redirect_stdout

from main import (
    evaluate_expression,
    get_variables,
    generate_truth_table,
    build_sdnf,
    build_sknf,
    get_numeric_forms,
    get_index_form,
    print_truth_table,
)

def test_evaluate_expression():
    assert evaluate_expression("a & b", {"a": 1, "b": 1}) == 1
    assert evaluate_expression("a & b", {"a": 1, "b": 0}) == 0
    assert evaluate_expression("a | b", {"a": 0, "b": 0}) == 0
    assert evaluate_expression("a -> b", {"a": 1, "b": 0}) == 0
    assert evaluate_expression("a -> b", {"a": 0, "b": 1}) == 1
    assert evaluate_expression("a ~ b", {"a": 1, "b": 1}) == 1
    assert evaluate_expression("a ~ b", {"a": 1, "b": 0}) == 0
    assert evaluate_expression("a & !b", {"a": 1, "b": 0}) == 1


def test_get_variables():
    assert get_variables("a & b | c") == ['a', 'b', 'c']
    assert get_variables("e & d") == ['d', 'e']
    assert get_variables("x & y") == []  # вне диапазона a-e


def test_generate_truth_table():
    table = generate_truth_table("a & b", ["a", "b"])
    expected = [
        ([0, 0], 0),
        ([0, 1], 0),
        ([1, 0], 0),
        ([1, 1], 1),
    ]
    assert table == expected


def test_build_sdnf():
    table = generate_truth_table("a & b", ["a", "b"])
    sdnf, indexes = build_sdnf(table, ["a", "b"])
    assert sdnf == "(a∧b)"
    assert indexes == [3]


def test_build_sknf():
    table = generate_truth_table("a & b", ["a", "b"])
    sknf, indexes = build_sknf(table, ["a", "b"])
    assert sknf == "(a∨b) ∧ (a∨¬b) ∧ (¬a∨b)"
    assert indexes == [0, 1, 2]


def test_get_numeric_forms():
    table = generate_truth_table("a & b", ["a", "b"])
    sknf, sdnf = get_numeric_forms(table)
    assert sknf == ['0', '1', '2']
    assert sdnf == ['3']


def test_get_index_form():
    table = generate_truth_table("a & b", ["a", "b"])
    decimal, binary = get_index_form(table)
    assert decimal == 1
    assert binary == "0001"


def test_print_truth_table(capsys):
    table = generate_truth_table("a & b", ["a", "b"])
    print_truth_table(table, ["a", "b"], "a & b")
    captured = capsys.readouterr()
    assert "a | b | a & b" in captured.out
    assert "0 | 0 |   0" in captured.out
    assert "1 | 1 |   1" in captured.out
