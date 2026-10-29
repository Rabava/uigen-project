import os
import sys
import json # Неиспользуемый импорт

# 1. БЕЗОПАСНОСТЬ: Захардкоженные секреты
DB_PASSWORD = "super_secret_password123!"
API_KEY = "sk-1234567890abcdef"

# 2. СТИЛЬ И ЛОГИКА: Плохое именование, магические числа, отсутствие типизации
def CalculateTotal(ItemsList):
    t = 0
    for i in range(len(ItemsList)):
        # Магическое число 1.2, отсутствие проверки на наличие ключа 'price'
        t = t + ItemsList[i]['price'] * 1.2
    return t

# 3. ЛОГИКА: Потенциальный IndexError (выход за границы)
def getFirstElement(arr):
    return arr[0]

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
def add_to_list(item, my_list=[]):
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