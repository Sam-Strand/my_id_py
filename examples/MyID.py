from my_id import MyID

# Создание случайного ID
uid = MyID()
print(f'Случайный ID: {uid}')
# Пример: A1b2C3d4E5f6G7h8I9j0K1

# Создание детерминированного ID из строки
consistent_id = MyID.derive('hello world')
print(f'Детерминированный ID: {consistent_id}')
# Всегда одинаковый для одних и тех же данных: DpN9xpaiPUuDGbVcki1P8v

# Валидация существующего ID
try:
    valid_id = MyID('B123456789012345678901')
    print(f'Валидный ID: {valid_id}')
except ValueError as e:
    print(f'Ошибка: {e}')
