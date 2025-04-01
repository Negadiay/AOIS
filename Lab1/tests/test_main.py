import pytest
from unittest.mock import patch
from main import main

def test_main_menu_option_1(capsys):
    with patch("builtins.input", side_effect=["1", "10.5", "0"]):  
        main()
        captured = capsys.readouterr()
        assert "Direct code: [00001010.10000000]" in captured.out
        assert "Inverse code: [00001010.10000000]" in captured.out
        assert "Additional code: [00001010.10000000]" in captured.out

def test_main_menu_option_2(capsys):
    with patch("builtins.input", side_effect=["2", "15", "10", "0"]):  
        main()
        captured = capsys.readouterr()
        assert "Number 1 entered: 15" in captured.out
        assert "Number 2 entered: 10" in captured.out
        assert "Result: 25" in captured.out
        assert "Direct code: 00011001" in captured.out
        assert "Inverse code: 00011001" in captured.out
        assert "Additional code: 00011001" in captured.out

def test_main_menu_option_3(capsys):
    with patch("builtins.input", side_effect=["3", "20", "5", "0"]):  
        main()
        captured = capsys.readouterr()
        assert "Number 1 entered: 20" in captured.out
        assert "Number 2 entered: -5" in captured.out
        assert "Result: 15" in captured.out
        assert "Direct code: 00001111" in captured.out
        assert "Inverse code: 00001111" in captured.out
        assert "Additional code: 00001111" in captured.out

def test_main_menu_option_4(capsys):
    with patch("builtins.input", side_effect=["4", "5", "4", "0"]):  
        main()
        captured = capsys.readouterr()
        assert "Result: 20" in captured.out
        assert "Direct code: 00010100" in captured.out
        assert "Inverse code: 00010100" in captured.out
        assert "Additional code: 00010100" in captured.out

def test_main_menu_option_5(capsys):
    with patch("builtins.input", side_effect=["5", "10", "3", "0"]):  
        main()
        captured = capsys.readouterr()
        assert "Result: 3.33333" in captured.out
        assert "Direct code: 00000011.01010" in captured.out
        assert "Inverse code: 00000011.01010" in captured.out
        assert "Additional code: 00000011.01010" in captured.out

def test_main_menu_option_6(capsys):
    with patch("builtins.input", side_effect=["6", "1.5", "2.25", "0"]): 
        main()
        captured = capsys.readouterr()
        assert "Number 1 (Binary): 00111111110000000000000000000000" in captured.out
        assert "Number 2 (Binary): 01000000000100000000000000000000" in captured.out
        assert "Result (Binary): 01000000011100000000000000000000" in captured.out
        assert "Result (Decimal): 3.75" in captured.out

def test_main_menu_option_0(capsys):
    with patch("builtins.input", side_effect=["0"]):  
        main()
        captured = capsys.readouterr()
        assert "Menu:" in captured.out  
        assert "0. Exit" in captured.out

def test_main_menu_invalid_choice(capsys):
    with patch("builtins.input", side_effect=["99", "0"]):  
        main()
        captured = capsys.readouterr()
        assert "Invalid choice. Please try again." in captured.out
