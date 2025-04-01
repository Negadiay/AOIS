import pytest
from ieee754 import add_ieee754

def test_add_ieee754_positive_numbers(capsys):
    add_ieee754(1.5, 2.25)
    captured = capsys.readouterr()
    assert "Number 1 (Binary): 00111111110000000000000000000000" in captured.out
    assert "Number 2 (Binary): 01000000000100000000000000000000" in captured.out
    assert "Result (Binary): 01000000011100000000000000000000" in captured.out  
    assert "Result (Decimal): 3.75" in captured.out

def test_add_ieee754_positive_and_negative(capsys):
    add_ieee754(3.75, -1.25)
    captured = capsys.readouterr()
    assert "Number 1 (Binary): 01000000011100000000000000000000" in captured.out
    assert "Number 2 (Binary): 10111111101000000000000000000000" in captured.out
    assert "Result (Binary): 01000000001000000000000000000000" in captured.out
    assert "Result (Decimal): 2.5" in captured.out

def test_add_ieee754_negative_numbers(capsys):
    add_ieee754(-4.5, -2.5)
    captured = capsys.readouterr()
    assert "Number 1 (Binary): 11000000100100000000000000000000" in captured.out
    assert "Number 2 (Binary): 11000000001000000000000000000000" in captured.out
    assert "Result (Binary): 11000000111000000000000000000000" in captured.out
    assert "Result (Decimal): -7.0" in captured.out
