import pytest
from main import BinaryMatrixProcessor, run_menu

@pytest.fixture
def processor():
    return BinaryMatrixProcessor()

def test_initialization(processor):
    assert processor.matrix_size == 16
    assert len(processor.data_matrix) == 16
    assert all(len(row) == 16 for row in processor.data_matrix)

def test_display_matrix(capsys, processor):
    processor.display_matrix()
    captured = capsys.readouterr()
    expected_first_line = "0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1\n"
    assert expected_first_line in captured.out

def test_extract_column_invalid_index(processor):
    with pytest.raises(ValueError, match="Индекс столбца должен быть между 0 и 15"):
        processor.extract_column_as_word(16)

def test_logical_xor(processor):
    result = processor._logical_xor(0, 1)
    assert result == 1
    result = processor._logical_xor(1, 1)
    assert result == 0

def test_logical_xnor(processor):
    result = processor._logical_xnor(1, 1)
    assert result == 1
    result = processor._logical_xnor(1, 0)
    assert result == 0

def test_logical_not_x1_and_x2(processor):
    result = processor._logical_not_x1_and_x2(0, 1)
    assert result == 1
    result = processor._logical_not_x1_and_x2(1, 1)
    assert result == 0

def test_logical_x1_or_not_x2(processor):
    result = processor._logical_x1_or_not_x2(1, 0)
    assert result == 1
    result = processor._logical_x1_or_not_x2(0, 1)
    assert result == 0

def test_apply_column_logic_xor(capsys, processor):
    processor.apply_column_logic(1, 0, 1, 2)
    captured = capsys.readouterr()
    assert "Логическая операция 'XOR (f6: !x1 * x2 + x1 * !x2)' применена. Результат записан в столбец 2." in captured.out
    word = processor.extract_column_as_word(2)
    assert len(word) == 16

def test_apply_column_logic_invalid_indices(capsys, processor):
    processor.apply_column_logic(1, 16, 0, 0)
    captured = capsys.readouterr()
    assert "Предоставлен недопустимый индекс столбца." in captured.out

def test_apply_column_logic_invalid_function(capsys, processor):
    processor.apply_column_logic(5, 0, 1, 2)
    captured = capsys.readouterr()
    assert "Неизвестный выбор логической функции: 5" in captured.out

def test_to_decimal(processor):
    binary = [1, 0, 1, 0]
    assert processor._to_decimal(binary) == 10

def test_to_binary_list(processor):
    decimal = 10
    assert processor._to_binary_list(decimal, 4) == [1, 0, 1, 0]

def test_add_in_additional_code(processor):
    bits_a = [1, 0, 1, 0]  # 10 in decimal
    bits_b = [0, 0, 1, 1]  # 3 in decimal
    result = processor._add_in_additional_code(bits_a, bits_b)
    assert result == [0, 1, 1, 0, 1]  # 13 in decimal, padded to 5 bits

def test_process_arithmetic_operation_null_matrix(capsys, processor):
    processor.data_matrix = None
    processor.process_arithmetic_operation("111")
    captured = capsys.readouterr()
    assert "Матрица не инициализирована." in captured.out

def test_process_arithmetic_operation_invalid_key(capsys, processor):
    processor.process_arithmetic_operation("12")
    captured = capsys.readouterr()
    assert "Неверный ключ проверки. Должна быть 3-битная двоичная строка (например, '111')." in captured.out

def test_process_arithmetic_operation_no_matching_key(capsys, processor):
    original_matrix = [row[:] for row in processor.data_matrix]  # Copy original matrix
    processor.process_arithmetic_operation("111")
    captured = capsys.readouterr()
    assert "Арифметические операции завершены для ключа V '111'." in captured.out
    # Check that matrix remains unchanged since no column has V-part [1,1,1]
    assert processor.data_matrix == original_matrix

def test_process_arithmetic_operation_boundary_sum(capsys, processor):
    # Modify a column to have V-part [0,0,0] and A-part, B-part summing to a large value
    processor.data_matrix[0][0] = 0  # V-part [0,0,0] for column 0
    processor.data_matrix[1][0] = 0
    processor.data_matrix[2][0] = 0
    processor.data_matrix[3][0] = 1  # A-part [1,1,1,1]
    processor.data_matrix[4][0] = 1
    processor.data_matrix[5][0] = 1
    processor.data_matrix[6][0] = 1
    processor.data_matrix[7][0] = 1  # B-part [1,1,1,1]
    processor.data_matrix[8][0] = 1
    processor.data_matrix[9][0] = 1
    processor.data_matrix[10][0] = 1
    processor.process_arithmetic_operation("000")
    captured = capsys.readouterr()
    assert "Арифметические операции завершены для ключа V '000'." in captured.out
    word = processor.extract_column_as_word(0)
    expected_sum = processor._to_decimal([1,1,1,1]) + processor._to_decimal([1,1,1,1])  # 15 + 15 = 30
    expected_bits = processor._to_binary_list(30, 5)[-5:]  # [1,1,1,1,0]
    assert word[11:16] == expected_bits

def test_compare_binary_words(processor):
    word_a = [1, 0, 1]
    word_b = [1, 0, 0]
    is_greater, is_lesser = processor._compare_binary_words(word_a, word_b)
    assert is_greater == True
    assert is_lesser == False

def test_sort_matrix_columns_ascending(capsys, processor):
    processor.sort_matrix_columns(sort_ascending=True)
    captured = capsys.readouterr()
    assert "Столбцы матрицы отсортированы." in captured.out
    word_0 = processor.extract_column_as_word(0)
    word_1 = processor.extract_column_as_word(1)
    is_greater, is_lesser = processor._compare_binary_words(word_0, word_1)
    assert not is_greater  # First column should not be greater than second after ascending sort

def test_sort_matrix_columns_descending(capsys, processor):
    processor.sort_matrix_columns(sort_ascending=False)
    captured = capsys.readouterr()
    assert "Столбцы матрицы отсортированы." in captured.out
    word_0 = processor.extract_column_as_word(0)
    word_1 = processor.extract_column_as_word(1)
    is_greater, is_lesser = processor._compare_binary_words(word_0, word_1)
    assert is_greater  # First column should be greater than second after descending sort

def test_run_menu_display_matrix(monkeypatch, capsys):
    inputs = iter(['1', '6'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    run_menu()
    captured = capsys.readouterr()
    assert "--- Меню Операций с Матрицей ---" in captured.out
    assert "0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1" in captured.out
    assert "Выход из программы." in captured.out

def test_run_menu_extract_column_invalid(monkeypatch, capsys):
    inputs = iter(['2', '16', '6'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    run_menu()
    captured = capsys.readouterr()
    assert "Недопустимый номер столбца." in captured.out
    assert "Выход из программы." in captured.out

def test_run_menu_extract_column_non_numeric(monkeypatch, capsys):
    inputs = iter(['2', 'abc', '6'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    run_menu()
    captured = capsys.readouterr()
    assert "Неверный ввод. Пожалуйста, введите число." in captured.out
    assert "Выход из программы." in captured.out

def test_run_menu_apply_logic_valid(monkeypatch, capsys):
    inputs = iter(['3', '1', '0', '1', '2', '6'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    run_menu()
    captured = capsys.readouterr()
    assert "Доступные логические функции:" in captured.out
    assert "Логическая операция 'XOR (f6: !x1 * x2 + x1 * !x2)' применена. Результат записан в столбец 2." in captured.out
    assert "Выход из программы." in captured.out

def test_run_menu_apply_logic_invalid_function(monkeypatch, capsys):
    inputs = iter(['3', '5', '6'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    run_menu()
    captured = capsys.readouterr()
    assert "Недопустимый выбор функции. Введите число от 1 до 4." in captured.out
    assert "Выход из программы." in captured.out

def test_run_menu_apply_logic_invalid_indices(monkeypatch, capsys):
    inputs = iter(['3', '1', '16', '0', '0', '6'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    run_menu()
    captured = capsys.readouterr()
    assert "Недопустимые номера столбцов." in captured.out
    assert "Выход из программы." in captured.out

def test_run_menu_arithmetic_operation_valid(monkeypatch, capsys):
    inputs = iter(['4', '111', '6'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    run_menu()
    captured = capsys.readouterr()
    assert "Арифметические операции завершены для ключа V '111'." in captured.out
    assert "Выход из программы." in captured.out

def test_run_menu_arithmetic_operation_invalid_key(monkeypatch, capsys):
    inputs = iter(['4', '12', '6'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    run_menu()
    captured = capsys.readouterr()
    assert "Неверный ключ проверки. Должна быть 3-битная двоичная строка (например, '111')." in captured.out
    assert "Выход из программы." in captured.out

def test_run_menu_sort_ascending(monkeypatch, capsys):
    inputs = iter(['5', 'да', '6'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    run_menu()
    captured = capsys.readouterr()
    assert "Столбцы матрицы отсортированы." in captured.out
    assert "Выход из программы." in captured.out

def test_run_menu_sort_descending(monkeypatch, capsys):
    inputs = iter(['5', 'нет', '6'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    run_menu()
    captured = capsys.readouterr()
    assert "Столбцы матрицы отсортированы." in captured.out
    assert "Выход из программы." in captured.out

def test_run_menu_invalid_choice(monkeypatch, capsys):
    inputs = iter(['7', '6'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    run_menu()
    captured = capsys.readouterr()
    assert "Неверный выбор. Пожалуйста, попробуйте еще раз." in captured.out
    assert "Выход из программы." in captured.out