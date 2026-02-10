import re
import secrets
import string
import hashlib
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler
from typing import Any


class MyID(str):
    '''
    Класс для уникальных идентификаторов длиной 22 символа:
    - Первый символ — буква (A-Z, a-z)
    - Остальные 21 символ — буквы или цифры (A-Z, a-z, 0-9)
    
    Особенности:
    1. MyID() → создаёт новый случайный uid.
    2. MyID(value) → проверяет формат переданного значения. Если неверный, кидает ValueError.
    3. MyID.derive(source) → создаёт детерминированный uid из строки source (через SHA256).
    4. Интеграция с Pydantic через __get_pydantic_core_schema__.
    
    Примеры:
        MyID()             # новый случайный uid
        MyID('A123456789012345678901')  # валидный uid
        MyID('123456...')  # ValueError, т.к. первый символ не буква
    '''

    _pattern = re.compile(r'^[a-zA-Z][a-zA-Z0-9]{21}$')
    _letters = string.ascii_letters
    _letters_digits = _letters + string.digits

    def __new__(cls, *args: Any) -> 'MyID':
        '''
        Создание нового uid.
        
        Варианты:
        - MyID()             → генерируется случайный uid
        - MyID(value: str)   → проверяется валидность value
            - если value валиден → возвращается объект MyID (строка)
            - если value невалиден → ValueError
        '''
        if len(args) == 0:
            value = cls._generate()
        else:
            value = args[0]
            if not isinstance(value, str) or not cls._pattern.fullmatch(value):
                raise ValueError(f'Invalid uid format: {value}')
        return super().__new__(cls, value)

    @classmethod
    def _generate(cls) -> 'MyID':
        '''
        Генерация случайного uid:
        - первый символ случайная буква
        - остальные 21 символ — буквы или цифры
        '''
        first = secrets.choice(cls._letters)
        rest = ''.join(secrets.choice(cls._letters_digits) for _ in range(21))
        return cls.__new__(cls, first + rest)

    @classmethod
    def derive(cls, source: str) -> 'MyID':
        '''
        Детерминированное создание uid из строки source.
        Всегда возвращает один и тот же uid для одного source.
        '''
        digest = hashlib.sha256(source.encode()).digest()
        first = cls._letters[digest[0] % len(cls._letters)]
        rest = ''.join(cls._letters_digits[b % len(cls._letters_digits)] for b in digest[1:22])
        return cls(first + rest)

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type, handler: GetCoreSchemaHandler):
        '''
        Интеграция с Pydantic:
        - при валидации value:
            - если value уже MyID → возвращается как есть
            - иначе → пытается создать MyID(value) (валидация + ValueError)
        - сериализация → строка
        '''
        def validate(value: str) -> MyID:
            if isinstance(value, cls):
                return value
            return cls(value)
        return core_schema.no_info_plain_validator_function(
            function=validate,
            serialization=core_schema.plain_serializer_function_ser_schema(str)
        )


class MyIDTuple(tuple):
    '''
    Валидируемый кортеж MyID, который принимает:
    - строку через запятую
    - список/кортеж с вложенностью
    - комбинированно, включая ['id1,id2']
    Рекурсивно разворачивает и возвращает одномерный tuple MyID.
    '''
    def __new__(cls, value):
        def flatten(v):
            if isinstance(v, str):
                if ',' not in v:
                    return [MyID(v)]
                parts = [x.strip() for x in v.split(',') if x.strip()]
                result = []
                for p in parts:
                    result.extend(flatten(p))
                return result
            if isinstance(v, (list, tuple)):
                result = []
                for item in v:
                    result.extend(flatten(item))
                return result
            if isinstance(v, MyID):
                return [v]

            raise ValueError(f'Невалидный элемент: {v!r}')

        if isinstance(value, cls):
            return value

        items = tuple(flatten(value))
        if not items:
            raise ValueError('пустой список MyID')

        return super().__new__(cls, items)

    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler):
        def validate(value):
            try:
                return cls(value)
            except Exception as e:
                raise ValueError(f'Невалидный MyIDTuple: {e}') from e

        return core_schema.no_info_plain_validator_function(
            function=validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda v: ','.join(str(x) for x in v)
            )
        )


if __name__ == '__main__':
    print(MyID.derive("hello world"))
    # Примеры использования
    print('Случайные uid:')
    for _ in range(10):
        print(MyID())  # новые случайные uid

    print('\nДетерминированные uid (из строки "hello"):')
    for _ in range(3):
        print(MyID.derive('hello'))  # всегда один и тот же uid для "hello"

    print('\nВалидация:')
    for value in [
        None, # Не валидно → ValueError
        MyID(),  # уже MyID → возвращается сам объект
        str(MyID()),  # валидная строка → создаётся новый MyID с той же строкой
        'A123456789012345678901',  # валидно → создаётся MyID
        '1234567890123456789012',  # невалидно (начинается с цифры) → ValueError
    ]:
        try:
            print(f"{value!r} -> {MyID(value)}")
        except ValueError as e:
            print(f"{value!r} -> Error: {e}")

    # Пример использования MyIDTuple
    t = MyIDTuple('xqqumRbXZ1KdIXDOBLcFTE,xELq0jsA9rgDlTkYXJXz6S,YXtOWu9Uv06iLOItdhPSWl')

    print(t)  # -> ('xqqumRbXZ1KdIXDOBLcFTE', 'xELq0jsA9rgDlTkYXJXz6S', 'YXtOWu9Uv06iLOItdhPSWl')    

    try:
        MyIDTuple('невалидныйID, xELq0jsA9rgDlTkYXJXz6S')
    except ValueError as e:
        print('Ошибка:', e)
