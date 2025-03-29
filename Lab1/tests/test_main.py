import pytest
from unittest.mock import patch
from main import main

def test_main_menu_option_1(capsys):
    # Тест для пункта меню 1: Конвертация десятичного числа в двоичное
    with patch("builtins.input", side_effect=["1", "10.5", "0"]):  # Имитация ввода: 1 -> 10.5 -> 0
        main()
        captured = capsys.readouterr()
        # Проверяем, что вывод содержит ожидаемые строки
        assert "Direct code: [00001010.10000000]" in captured.out
        assert "Inverse code: [00001010.10000000]" in captured.out
        assert "Additional code: [00001010.10000000]" in captured.out

def test_main_menu_option_2(capsys):
    # Тест для пункта меню 2: Сложение двух чисел в дополнительном коде
    with patch("builtins.input", side_effect=["2", "15", "10", "0"]):  # Имитация ввода: 2 -> 15 -> 10 -> 0
        main()
        captured = capsys.readouterr()
        assert "Number 1 entered: 15" in captured.out
        assert "Number 2 entered: 10" in captured.out
        assert "Result: 25" in captured.out
        assert "Direct code: 00011001" in captured.out
        assert "Inverse code: 00011001" in captured.out
        assert "Additional code: 00011001" in captured.out

def test_main_menu_option_3(capsys):
    # Тест для пункта меню 3: Вычитание двух чисел в дополнительном коде
    with patch("builtins.input", side_effect=["3", "20", "5", "0"]):  # Имитация ввода: 3 -> 20 -> 5 -> 0
        main()
        captured = capsys.readouterr()
        # Проверяем, что вывод содержит ожидаемые строки
        assert "Number 1 entered: 20" in captured.out
        assert "Number 2 entered: -5" in captured.out
        assert "Result: 15" in captured.out
        assert "Direct code: 00001111" in captured.out
        assert "Inverse code: 00001111" in captured.out
        assert "Additional code: 00001111" in captured.out

def test_main_menu_option_4(capsys):
    # Тест для пункта меню 4: Умножение двух чисел в прямом коде
    with patch("builtins.input", side_effect=["4", "5", "4", "0"]):  # Имитация ввода: 4 -> 5 -> 4 -> 0
        main()
        captured = capsys.readouterr()
        assert "Result: 20" in captured.out
        assert "Direct code: 00010100" in captured.out
        assert "Inverse code: 00010100" in captured.out
        assert "Additional code: 00010100" in captured.out

def test_main_menu_option_5(capsys):
    # Тест для пункта меню 5: Деление двух чисел в прямом коде
    with patch("builtins.input", side_effect=["5", "10", "3", "0"]):  # Имитация ввода: 5 -> 10 -> 3 -> 0
        main()
        captured = capsys.readouterr()
        assert "Result: 3.33333" in captured.out
        assert "Direct code: 00000011.01010" in captured.out
        assert "Inverse code: 00000011.01010" in captured.out
        assert "Additional code: 00000011.01010" in captured.out

def test_main_menu_option_6(capsys):
    # Тест для пункта меню 6: Сложение двух чисел с плавающей точкой (IEEE 754)
    with patch("builtins.input", side_effect=["6", "1.5", "2.25", "0"]):  # Имитация ввода: 6 -> 1.5 -> 2.25 -> 0
        main()
        captured = capsys.readouterr()
        assert "Number 1 (Binary): 00111111110000000000000000000000" in captured.out
        assert "Number 2 (Binary): 01000000000100000000000000000000" in captured.out
        assert "Result (Binary): 01000000011100000000000000000000" in captured.out
        assert "Result (Decimal): 3.75" in captured.out

def test_main_menu_option_0(capsys):
    # Тест для пункта меню 0: Выход
    with patch("builtins.input", side_effect=["0"]):  # Имитация ввода: 0
        main()
        captured = capsys.readouterr()
        assert "Menu:" in captured.out  # Проверяем, что меню отображается
        assert "0. Exit" in captured.out

def test_main_menu_invalid_choice(capsys):
    # Тест для неверного выбора в меню
    with patch("builtins.input", side_effect=["99", "0"]):  # Имитация ввода: 99 -> 0
        main()
        captured = capsys.readouterr()
        assert "Invalid choice. Please try again." in captured.out