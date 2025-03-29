import pytest
from operations import (
    add_in_additional_code,
    subtract_in_additional_code,
    multiply_direct_code,
    divide_direct_code,
    convert_decimal_to_binary
)

def test_convert_decimal_to_binary_positive():
    # Тест для положительного числа
    direct, inverse, additional = convert_decimal_to_binary(10.5)
    assert direct == "00001010.10000000"
    assert inverse == "00001010.10000000"
    assert additional == "00001010.10000000"

def test_convert_decimal_to_binary_negative():
    # Тест для отрицательного числа
    direct, inverse, additional = convert_decimal_to_binary(-10.5)
    assert direct == "10001010.10000000"
    assert inverse == "11110101.10000000"
    assert additional == "11110110.10000000"

def test_add_in_additional_code(capsys):
    # Тест сложения двух положительных чисел
    add_in_additional_code(15, 10)
    captured = capsys.readouterr()
    assert "Number 1 entered: 15" in captured.out
    assert "Number 2 entered: 10" in captured.out
    assert "Result: 25" in captured.out
    assert "Direct code: 00011001" in captured.out
    assert "Inverse code: 00011001" in captured.out
    assert "Additional code: 00011001" in captured.out

def test_subtract_in_additional_code(capsys):
    # Тест вычитания (15 - 5)
    subtract_in_additional_code(15, 5)
    captured = capsys.readouterr()
    assert "Number 1 entered: 15" in captured.out
    assert "Number 2 entered: -5" in captured.out
    assert "Result: 10" in captured.out
    assert "Direct code: 00001010" in captured.out
    assert "Inverse code: 00001010" in captured.out
    assert "Additional code: 00001010" in captured.out

def test_multiply_direct_code(capsys):
    # Тест умножения (5 * 4)
    multiply_direct_code(5, 4)
    captured = capsys.readouterr()
    assert "Result: 20" in captured.out
    assert "Direct code: 00010100" in captured.out
    assert "Inverse code: 00010100" in captured.out
    assert "Additional code: 00010100" in captured.out

def test_divide_direct_code(capsys):
    # Тест деления (10 / 3)
    divide_direct_code(10, 3)
    captured = capsys.readouterr()
    assert "Result: 3.33333" in captured.out
    assert "Direct code: 00000011.01010" in captured.out
    assert "Inverse code: 00000011.01010" in captured.out
    assert "Additional code: 00000011.01010" in captured.out