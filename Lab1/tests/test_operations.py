import pytest
from operations import add_in_additional_code, subtract_in_additional_code, multiply_direct_code, divide_direct_code

def test_add_in_additional_code(capsys):
    add_in_additional_code(5, 3)
    captured = capsys.readouterr()
    assert "Number 1 entered: 5" in captured.out
    assert "Number 2 entered: 3" in captured.out
    assert "Result: 8" in captured.out
    assert "Direct code: 00001000" in captured.out
    assert "Inverse code: 00001000" in captured.out
    assert "Additional code: 00001000" in captured.out

def test_subtract_in_additional_code(capsys):
    subtract_in_additional_code(5, 3)
    captured = capsys.readouterr()
    assert "Number 1 entered: 5" in captured.out
    assert "Number 2 entered: -3" in captured.out
    assert "Result: 2" in captured.out
    assert "Direct code: 00000010" in captured.out
    assert "Inverse code: 00000010" in captured.out
    assert "Additional code: 00000010" in captured.out

def test_multiply_direct_code(capsys):
    multiply_direct_code(5, 3)
    captured = capsys.readouterr()
    assert "Result: 15" in captured.out
    assert "Direct code: 00001111" in captured.out
    assert "Inverse code: 00001111" in captured.out
    assert "Additional code: 00001111" in captured.out

def test_divide_direct_code(capsys):
    divide_direct_code(16, 5)
    captured = capsys.readouterr()
    assert "Result: 3.20000" in captured.out
    assert "Direct code: 00000011.00110" in captured.out
    assert "Inverse code: 00000011.00110" in captured.out
    assert "Additional code: 00000011.00110" in captured.out

if __name__ == "__main__":
    pytest.main()
