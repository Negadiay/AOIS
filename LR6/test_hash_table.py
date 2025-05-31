import pytest
from unittest.mock import patch
from main import HashTable, menu

def test_create_and_read():
    ht = HashTable()
    assert ht.create("Африка", "Материк, второй по величине") is True
    assert ht.read("Африка")["определение"] == "Материк, второй по величине"

def test_create_duplicate_key():
    ht = HashTable()
    ht.create("Амазонка", "Крупнейший тропический лес")
    with pytest.raises(Exception, match="Ключ 'Амазонка' уже существует"):
        ht.create("Амазонка", "Река в Южной Америке")

def test_read_nonexistent_key():
    ht = HashTable()
    assert ht.read("Антарктида") is None

def test_update_existing_key():
    ht = HashTable()
    ht.create("Евразия", "Крупнейший материк")
    assert ht.update("Евразия", "Самый большой континент планеты")
    assert ht.read("Евразия")["определение"] == "Самый большой континент планеты"

def test_update_nonexistent_key():
    ht = HashTable()
    with pytest.raises(Exception, match="Ключ 'Гималаи' не найден"):
        ht.update("Гималаи", "Горная система в Азии")

def test_delete_existing_key():
    ht = HashTable()
    ht.create("Сибирь", "Обширный регион в России")
    assert ht.delete("Сибирь")
    assert ht.read("Сибирь") is None

def test_delete_nonexistent_key():
    ht = HashTable()
    with pytest.raises(Exception, match="Ключ 'Урал' не найден"):
        ht.delete("Урал")

def test_collision_and_rehashing():
    ht = HashTable(size=3)
    ht.create("Лес", "Экосистема, покрытая деревьями")
    ht.create("Гора", "Возвышенность на поверхности земли")
    ht.create("Остров", "Участок суши, окружённый водой")
    assert ht.read("Лес")["определение"] == "Экосистема, покрытая деревьями"
    assert ht.read("Гора")["определение"] == "Возвышенность на поверхности земли"
    assert ht.read("Остров")["определение"] == "Участок суши, окружённый водой"
    ht.delete("Лес")
    assert ht.read("Лес") is None

def test_table_full():
    ht = HashTable(size=2)
    ht.create("Река", "Поток воды, текущий по руслу")
    ht.create("Озеро", "Замкнутый водоём")
    with pytest.raises(Exception, match="Хеш-таблица полна"):
        ht.create("Пустыня", "Засушливая область")

@patch("builtins.input", side_effect=[
    "1", "Тайга", "Бореальный лес в северном полушарии",
    "2", "Тайга",
    "3", "Тайга", "Тип хвойного леса в России",
    "4", "Тайга",
    "5",
    "6"
])
def test_menu_flow(mock_input, capsys):
    menu()
    out = capsys.readouterr().out
    assert "Термин 'Тайга' успешно добавлен." in out
    assert "Определение: Бореальный лес в северном полушарии" in out
    assert "Термин 'Тайга' успешно обновлен." in out
    assert "Термин 'Тайга' успешно удален." in out
    assert "Программа завершена." in out
