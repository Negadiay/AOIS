import pytest
from conversion import to_binary, to_binary_fraction

def test_to_binary_positive():
    assert to_binary(10) == "00001010"

def test_to_binary_negative():
    assert to_binary(-10, bits=8) == "11110110"

def test_to_binary_fraction():
    assert to_binary_fraction(0.5) == "10000000"
    assert to_binary_fraction(0.25) == "01000000"
    assert to_binary_fraction(0.75) == "11000000"

def test_to_binary_fraction_precision():
    assert to_binary_fraction(0.1, precision=5) == "00011"