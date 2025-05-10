import pytest
from utils import str_len, str_get, list_len, list_append, list_contains, list_sort, list_copy

def test_str_len():
    assert str_len("") == 0
    assert str_len("hello") == 5
    assert str_len("a b c") == 5

def test_str_get():
    s = "hello"
    assert str_get(s, 0) == "h"
    assert str_get(s, 4) == "o"
    with pytest.raises(IndexError):
        str_get(s, 5)

def test_list_len():
    assert list_len([]) == 0
    assert list_len([1, 2, 3]) == 3
    assert list_len(["a", "b"]) == 2

def test_list_append():
    lst = [1, 2]
    result = list_append(lst, 3)
    assert result == [1, 2, 3]
    assert lst == [1, 2]  # Original list unchanged
    assert list_append([], 1) == [1]

def test_list_contains():
    lst = [1, 2, 3]
    assert list_contains(lst, 2) == True
    assert list_contains(lst, 4) == False
    assert list_contains([], 1) == False



def test_list_copy():
    lst = [1, 2, 3]
    copy = list_copy(lst)
    assert copy == lst
    assert copy is not lst  # Different object
    copy = list_append(copy, 4)
    assert lst == [1, 2, 3]  # Original unchanged
    assert list_copy([]) == []