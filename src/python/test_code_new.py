import os
import sys

# 1. БЕЗОПАСНОСТЬ: Захардкоженные секреты
DB_PASSWORD = os.environ["DB_PASSWORD"]
API_KEY = os.environ["API_KEY"]

# 2. СТИЛЬ И ЛОГИКА: Плохое именование, магические числа, отсутствие типизации
from collections.abc import Iterable

TAX_MULTIPLIER: float = 1.2

def calculate_total(items: Iterable[dict]) -> float:
    total = 0.0
    for item in items:
        price = float(item.get("price", 0))
        total += price * TAX_MULTIPLIER
    return total

# 3. ЛОГИКА: Потенциальный IndexError (выход за границы)
from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")

def get_first_element(arr: Sequence[T]) -> T | None:
    return arr[0] if arr else None

# 4. БЕЗОПАСНОСТЬ: Опасное выполнение кода (eval)
def run_user_input(user_input):
    eval(user_input)

# 5. БЕЗОПАСНОСТЬ: SQL-инъекция
def get_user_by_id(user_id):
    # Прямая подстановка переменной в SQL-запрос
    query = f"SELECT * FROM users WHERE id = {user_id}"
    print(f"Executing: {query}")
    return query

# 6. PYTHONIC: Изменяемый аргумент по умолчанию (Mutable Default Argument)
def add_to_list(item, my_list=None):
    if my_list is None:
        my_list = []
    my_list.append(item)
    return my_list

# 7. СЛОЖНОСТЬ: Глубокая вложенность и плохая обработка исключений
def process_data(data):
    try:
        for item in data:
            if item > 10:
                if item % 2 == 0:
                    if item != 14:
                        print("Valid item")
                    else:
                        pass
                else:
                    pass
    except: # Слишком общая обработка исключений (перехватывает даже Ctrl+C)
        return 0