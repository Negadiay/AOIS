import pytest
from evaluator import apply_op, apply_not, evaluate_postfix, generate_table
from utils import list_append

def test_apply_not():
    assert apply_not(1) == 0
    assert apply_not(0) == 1

def test_apply_op():
    assert apply_op("&", 1, 1) == 1
    assert apply_op("&", 1, 0) == 0
    assert apply_op("|", 0, 1) == 1
    assert apply_op("|", 0, 0) == 0
    assert apply_op("->", 0, 1) == 1
    assert apply_op("->", 1, 0) == 0
    assert apply_op("~", 1, 1) == 1
    assert apply_op("~", 1, 0) == 0
    assert apply_op("invalid", 1, 1) == 0

def test_evaluate_postfix():
    postfix = ["a", "b", "&"]
    values = {"a": 1, "b": 1}
    assert evaluate_postfix(postfix, values) == 1
    values = {"a": 1, "b": 0}
    assert evaluate_postfix(postfix, values) == 0
    postfix = ["a", "!", "b", "|"]
    values = {"a": 0, "b": 1}
    assert evaluate_postfix(postfix, values) == 1
    postfix = ["a", "b", "->"]
    values = {"a": 1, "b": 0}
    assert evaluate_postfix(postfix, values) == 0
    postfix = ["a", "b", "~"]
    values = {"a": 1, "b": 1}
    assert evaluate_postfix(postfix, values) == 1

def test_generate_table():
    postfix = ["a", "b", "&"]
    variables = ["a", "b"]
    table = generate_table(postfix, variables)
    expected = [
        ([0, 0], 0),
        ([0, 1], 0),
        ([1, 0], 0),
        ([1, 1], 1)
    ]
    assert len(table) == len(expected)
    for (combo, result), (exp_combo, exp_result) in zip(table, expected):
        assert combo == exp_combo
        assert result == exp_result

    postfix = ["a"]
    variables = ["a"]
    table = generate_table(postfix, variables)
    expected = [([0], 0), ([1], 1)]
    assert len(table) == len(expected)
    for (combo, result), (exp_combo, exp_result) in zip(table, expected):
        assert combo == exp_combo
        assert result == exp_result