import pytest
from parser import is_variable, tokenize, get_variables, get_precedence, to_postfix
from utils import list_append

def test_is_variable():
    assert is_variable("a") == True
    assert is_variable("e") == True
    assert is_variable("f") == False
    assert is_variable("!") == False

def test_tokenize():
    assert tokenize("a & b") == ["a", "&", "b"]
    assert tokenize("a -> b") == ["a", "->", "b"]
    assert tokenize("!a | (b & c)") == ["!", "a", "|", "(", "b", "&", "c", ")"]
    assert tokenize("a ~ b") == ["a", "~", "b"]
    assert tokenize("") == []
    assert tokenize("a  b") == ["a", "b"]

def test_get_variables():
    tokens = ["a", "&", "b", "|", "a"]
    assert get_variables(tokens) == ["a", "b"]
    assert get_variables(["!", "c"]) == ["c"]
    assert get_variables(["(", ")"]) == []
    tokens = ["a", "a", "b", "c", "b"]
    assert get_variables(tokens) == ["a", "b", "c"]

def test_get_precedence():
    assert get_precedence("!") == 4
    assert get_precedence("&") == 3
    assert get_precedence("|") == 2
    assert get_precedence("->") == 1
    assert get_precedence("~") == 1
    assert get_precedence("a") == -1

