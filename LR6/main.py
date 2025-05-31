class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * size
        self.count = 0

    def _hash_function(self, key):
        hash_value = sum(ord(char) for char in key) % self.size
        return hash_value

    def _find_slot(self, key, insert=False):
        index = self._hash_function(key)
        original_index = index
        steps = 0

        while steps < self.size:
            if self.table[index] is None:
                if insert:
                    return index
                return None, None
            elif self.table[index][0] == key:
                return index, self.table[index][1]
            index = (index + 1) % self.size
            steps += 1

        if insert:
            return None
        return None, None

    def create(self, key, definition):
        if self.count >= self.size:
            raise Exception("Хеш-таблица полна")
        
        index, value = self._find_slot(key, insert=False)
        if value is not None:
            raise Exception(f"Ключ '{key}' уже существует")
        
        index = self._find_slot(key, insert=True)
        if index is None:
            raise Exception("Невозможно вставить: нет свободных слотов")
        
        self.table[index] = (key, {"определение": definition})
        self.count += 1
        return True

    def read(self, key):
        index, value = self._find_slot(key)
        if index is None:
            return None
        return value

    def update(self, key, definition=None):
        index, value = self._find_slot(key)
        if index is None:
            raise Exception(f"Ключ '{key}' не найден")
        
        if definition:
            self.table[index] = (key, {"определение": definition})
        return True

    def delete(self, key):
        index, _ = self._find_slot(key)
        if index is None:
            raise Exception(f"Ключ '{key}' не найден")
        
        keys_to_rehash = []
        self.table[index] = None
        self.count -= 1
        next_index = (index + 1) % self.size
        while self.table[next_index] is not None:
            keys_to_rehash.append(self.table[next_index])
            self.table[next_index] = None
            self.count -= 1
            next_index = (next_index + 1) % self.size
        
        for key_to_move, value_to_move in keys_to_rehash:
            self.create(key_to_move, value_to_move["определение"])
        return True

    def display(self):
        print("\n--- Содержимое хеш-таблицы ---")
        print("{:<5} {:<20} {:<40}".format("Индекс", "Термин", "Определение"))
        print("-" * 67)
        for i, item in enumerate(self.table):
            if item is not None:
                key = item[0]
                definition = item[1]["определение"]
                print("{:<5} {:<20} {:<40}".format(i, key, definition))
            else:
                print("{:<5} {:<20} {:<40}".format(i, "Пусто", "Пусто"))
        print("-" * 67)


def menu():
    ht = HashTable()
    while True:
        print("\n=== Географическая хеш-таблица ===")
        print("1. Создать термин (Create)")
        print("2. Прочитать термин (Read)")
        print("3. Обновить термин (Update)")
        print("4. Удалить термин (Delete)")
        print("5. Показать таблицу")
        print("6. Выйти")
        choice = input("Выберите действие (1-6): ")

        try:
            if choice == "1":
                key = input("Введите географический термин: ")
                definition = input("Введите определение: ")
                ht.create(key, definition)
                print(f"Термин '{key}' успешно добавлен.")
                ht.display()

            elif choice == "2":
                key = input("Введите термин для поиска: ")
                result = ht.read(key)
                if result:
                    print(f"Термин: {key}")
                    print(f"Определение: {result['определение']}")
                else:
                    print(f"Термин '{key}' не найден.")

            elif choice == "3":
                key = input("Введите термин для обновления: ")
                definition = input("Введите новое определение (или оставьте пустым): ")
                definition = definition if definition else None
                ht.update(key, definition)
                print(f"Термин '{key}' успешно обновлен.")
                ht.display()

            elif choice == "4":
                key = input("Введите термин для удаления: ")
                ht.delete(key)
                print(f"Термин '{key}' успешно удален.")
                ht.display()

            elif choice == "5":
                ht.display()

            elif choice == "6":
                print("Программа завершена.")
                break

            else:
                print("Неверный выбор. Пожалуйста, выберите число от 1 до 6.")

        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    menu()
