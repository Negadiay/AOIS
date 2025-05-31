class BinaryMatrixProcessor:
    def __init__(self, size=16):
        self.matrix_size = size
        # Заранее прописанная матрица
        self.data_matrix = [
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0],
            [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1],
            [0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0],
            [1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1],
            [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
            [1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1],
            [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0]
        ]

    def display_matrix(self):
        if self.data_matrix is None:
            print("Матрица не инициализирована. Пожалуйста, сначала создайте матрицу.")
            return
        for row in self.data_matrix:
            print(" ".join(map(str, row)))

    def extract_column_as_word(self, column_idx):
        if not (0 <= column_idx < self.matrix_size):
            raise ValueError(f"Индекс столбца должен быть между 0 и {self.matrix_size - 1}")

        extracted_word = []
        for row_idx in range(self.matrix_size):
            shifted_row_index = (row_idx + column_idx) % self.matrix_size
            extracted_word.append(self.data_matrix[shifted_row_index][column_idx])
        return extracted_word

    def show_word(self, word_data):
        print(" ".join(map(str, word_data)))

    def _logical_xor(self, bit1, bit2):
        return 1 if ((not bit1 and bit2) or (bit1 and not bit2)) else 0

    def _logical_xnor(self, bit1, bit2):
        return 1 if ((bit1 and bit2) or (not bit1 and not bit2)) else 0

    def _logical_not_x1_and_x2(self, bit1, bit2):
        return 1 if (not bit1 and bit2) else 0

    def _logical_x1_or_not_x2(self, bit1, bit2):
        return 1 if (bit1 or not bit2) else 0

    def apply_column_logic(self, logic_func_choice, col1_idx, col2_idx, target_col_idx):
        if self.data_matrix is None:
            print("Матрица не инициализирована.")
            return

        if not all(0 <= idx < self.matrix_size for idx in [col1_idx, col2_idx, target_col_idx]):
            print("Предоставлен недопустимый индекс столбца.")
            return

        logic_functions = {
            1: (self._logical_xor, "XOR (f6: !x1 * x2 + x1 * !x2)"),
            2: (self._logical_xnor, "XNOR (f9: x1 * x2 + !x1 * !x2)"),
            3: (self._logical_not_x1_and_x2, "NOT x1 AND x2 (f4: !x1 * x2)"),
            4: (self._logical_x1_or_not_x2, "X1 OR NOT x2 (f11: x1 + !x2)")
        }

        selected_func_info = logic_functions.get(logic_func_choice)
        if not selected_func_info:
            print(f"Неизвестный выбор логической функции: {logic_func_choice}")
            return

        selected_func, func_name_display = selected_func_info

        word1 = self.extract_column_as_word(col1_idx)
        word2 = self.extract_column_as_word(col2_idx)
        result_word = [selected_func(word1[i], word2[i]) for i in range(self.matrix_size)]

        for row_idx in range(self.matrix_size):
            shifted_row_index = (row_idx + target_col_idx) % self.matrix_size
            self.data_matrix[shifted_row_index][target_col_idx] = result_word[row_idx]
        print(f"Логическая операция '{func_name_display}' применена. Результат записан в столбец {target_col_idx}.")

    def _to_decimal(self, binary_list):
        return int("".join(map(str, binary_list)), 2)

    def _to_binary_list(self, decimal_val, num_bits):
        return [int(bit) for bit in bin(decimal_val)[2:].zfill(num_bits)]

    def _add_in_additional_code(self, bits_a, bits_b, num_bits=4):
        decimal_a = self._to_decimal(bits_a)
        decimal_b = self._to_decimal(bits_b)
        
        sum_decimal = decimal_a + decimal_b
        
        sum_binary_str = bin(sum_decimal)[2:]
        result_str_padded = sum_binary_str.zfill(5)[-5:] 
        return [int(bit) for bit in result_str_padded]

    def process_arithmetic_operation(self, validation_key):
        if self.data_matrix is None:
            print("Матрица не инициализирована.")
            return
        if not (len(validation_key) == 3 and all(b in '01' for b in validation_key)):
            print("Неверный ключ проверки. Должна быть 3-битная двоичная строка (например, '111').")
            return

        key_bits = [int(b) for b in validation_key]

        for col_index in range(self.matrix_size):
            current_word = self.extract_column_as_word(col_index)

            v_part = current_word[0:3]
            if v_part == key_bits:
                a_part = current_word[3:7]
                b_part = current_word[7:11]

                sum_result_bits = self._add_in_additional_code(a_part, b_part, num_bits=4)
                
                for i in range(5):
                    if 11 + i < self.matrix_size:
                        current_word[11 + i] = sum_result_bits[i]
                
                for row_idx in range(self.matrix_size):
                    shifted_row_index = (row_idx + col_index) % self.matrix_size
                    self.data_matrix[shifted_row_index][col_index] = current_word[row_idx]
        print(f"Арифметические операции завершены для ключа V '{validation_key}'.")

    def _compare_binary_words(self, word_a, word_b):
        is_greater = False
        is_lesser = False
        for i in range(len(word_a)):
            bit_a = word_a[i]
            bit_b = word_b[i]
            
            is_greater_current = is_greater or (bit_a and not bit_b and not is_lesser)
            is_lesser_current = is_lesser or (not bit_a and bit_b and not is_greater)
            
            is_greater, is_lesser = is_greater_current, is_lesser_current
            
        return is_greater, is_lesser

    def sort_matrix_columns(self, sort_ascending=True):
        if self.data_matrix is None:
            print("Матрица не инициализирована.")
            return

        all_words_with_indices = []
        for col_idx in range(self.matrix_size):
            all_words_with_indices.append((self.extract_column_as_word(col_idx), col_idx))

        n = len(all_words_with_indices)
        for i in range(n):
            for j in range(i + 1, n):
                word1_data = all_words_with_indices[i][0]
                word2_data = all_words_with_indices[j][0]

                is_w1_greater, is_w1_lesser = self._compare_binary_words(word1_data, word2_data)

                if (sort_ascending and is_w1_greater) or (not sort_ascending and is_w1_lesser):
                    all_words_with_indices[i], all_words_with_indices[j] = \
                        all_words_with_indices[j], all_words_with_indices[i]

        new_matrix = [[0 for _ in range(self.matrix_size)] for _ in range(self.matrix_size)]
        
        for new_col_idx in range(n):
            sorted_word_data = all_words_with_indices[new_col_idx][0]
            for bit_idx_in_word in range(self.matrix_size):
                actual_matrix_row = (bit_idx_in_word + new_col_idx) % self.matrix_size
                new_matrix[actual_matrix_row][new_col_idx] = sorted_word_data[bit_idx_in_word]
                
        self.data_matrix = new_matrix
        print("Столбцы матрицы отсортированы.")


def run_menu():
    processor = BinaryMatrixProcessor()

    while True:
        print("\n--- Меню Операций с Матрицей ---")
        print("1. Отобразить текущую матрицу")
        print("2. Прочитать слово из столбца")
        print("3. Применить логическую функцию к словам")
        print("4. Выполнить арифметическое сложение (Aj + Bj по ключу V)")
        print("5. Отсортировать столбцы матрицы")
        print("6. Выйти из программы")

        choice = input("Введите ваш выбор: ")

        if choice == "1":
            processor.display_matrix()

        elif choice == "2":
            if processor.data_matrix is None:
                print("Матрица еще не создана. Пожалуйста, сначала создайте ее.")
                continue
            try:
                col_num = int(input(f"Введите номер столбца (0-{processor.matrix_size - 1}): "))
                if 0 <= col_num < processor.matrix_size:
                    word = processor.extract_column_as_word(col_num)
                    print(f"Слово в столбце {col_num}:")
                    processor.show_word(word)
                else:
                    print("Недопустимый номер столбца.")
            except ValueError:
                print("Неверный ввод. Пожалуйста, введите число.")

        elif choice == "3":
            if processor.data_matrix is None:
                print("Матрица еще не создана. Пожалуйста, сначала создайте ее.")
                continue
            print("Доступные логические функции:")
            print("  1. XOR (f6: !x1 * x2 + x1 * !x2)")
            print("  2. XNOR (f9: x1 * x2 + !x1 * !x2)")
            print("  3. NOT x1 AND x2 (f4: !x1 * x2)")
            print("  4. X1 OR NOT x2 (f11: x1 + !x2)")
            
            try:
                func_choice = int(input("Выберите функцию (1-4): "))
                if not (1 <= func_choice <= 4):
                    print("Недопустимый выбор функции. Введите число от 1 до 4.")
                    continue

                col1 = int(input("Введите номер первого исходного столбца (0-15): "))
                col2 = int(input("Введите номер второго исходного столбца (0-15): "))
                res_col = int(input("Введите номер целевого столбца для результата (0-15): "))
                if all(0 <= c < processor.matrix_size for c in (col1, col2, res_col)):
                    processor.apply_column_logic(func_choice, col1, col2, res_col)
                    processor.display_matrix()
                else:
                    print("Недопустимые номера столбцов.")
            except ValueError:
                print("Неверный ввод. Пожалуйста, введите числа.")

        elif choice == "4":
            if processor.data_matrix is None:
                print("Матрица еще не создана. Пожалуйста, сначала создайте ее.")
                continue
            v_key_input = input("Введите 3-битный ключ проверки (например, '101'): ")
            processor.process_arithmetic_operation(v_key_input)
            processor.display_matrix()

        elif choice == "5":
            if processor.data_matrix is None:
                print("Матрица еще не создана. Пожалуйста, сначала создайте ее.")
                continue
            sort_order = input("Сортировать по возрастанию? (да/нет): ").lower()
            asc = sort_order.startswith("д")
            processor.sort_matrix_columns(asc)
            processor.display_matrix()

        elif choice == "6":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Пожалуйста, попробуйте еще раз.")

if __name__ == "__main__":
    run_menu()