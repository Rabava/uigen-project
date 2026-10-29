# Плохое именование, отсутствие пробелов, магическое число
def CalculateTotal(ItemsList):
    t = 0
    for i in range(len(ItemsList)):
        t = t + ItemsList[i]['price'] * 1.2  # Магическое число 1.2 (налог)
    return t

# Потенциальная ошибка выхода за границы массива
def getFirstElement(arr):
    return arr[0]

# Плохая обработка исключений (слишком общая)
def divide(a, b):
    try:
        return a / b
    except:
        return 0