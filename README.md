# MyID

Python библиотека для работы с уникальными идентификаторами фиксированной длины.

## Особенности
- **Безопасная генерация** - Использование криптографически безопасного генератора
- **Детерминированное создание** - Возможность генерации ID из исходных данных
- **Фиксированный формат** - Строгий формат: 22 символа (буква + буквы/цифры)
- **Интеграция с Pydantic** - Полная поддержка валидации в Pydantic моделях
- **Простота использования** - Интуитивно понятный API

## Установка
### Способ 1: Установка из репозитория (требуется Git)
```bash
pip install git+https://github.com/Sam-Strand/my_id_py.git
```

### Способ 2: Установка готового пакета (без Git)
```bash
pip install https://github.com/Sam-Strand/my_id_py/releases/download/v1.0.2/my_id-1.0.2-py3-none-any.whl
```

## Быстрый старт
```python
from my_id import MyID

# Создание случайного ID
uid = MyID()
print(f"Случайный ID: {uid}")
# Пример: A1b2C3d4E5f6G7h8I9j0K1

# Создание детерминированного ID из строки
consistent_id = MyID.derive("hello world")
print(f"Детерминированный ID: {consistent_id}")
# Всегда одинаковый для одних и тех же данных: DpN9xpaiPUuDGbVcki1P8v

# Валидация существующего ID
try:
    valid_id = MyID("B123456789012345678901")
    print(f"Валидный ID: {valid_id}")
except ValueError as e:
    print(f"Ошибка: {e}")
```

# MyIDTuple

Создает кортеж (`tuple`) из MyID переданных строкой через запятую.
Наследуется от tuple, содержит кортеж валидных MyID.
Актуально для валидации параметров get запросов.

## Пример
```python
# Создание кортежа ID из строки
ids = MyIDTuple('xqqumRbXZ1KdIXDOBLcFTE,xELq0jsA9rgDlTkYXJXz6S,YXtOWu9Uv06iLOItdhPSWl')
# Или из списка
ids = MyIDTuple(['xqqumRbXZ1KdIXDOBLcFTE', MyID(), MyID('YXtOWu9Uv06iLOItdhPSWl')])  # Каждый элемент валидируется

# Доступ к элементам
first_id = ids[0]  # MyID('xqqumRbXZ1KdIXDOBLcFTE')
for uid in ids:
    print(uid)
```
