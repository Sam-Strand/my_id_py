import unittest
from my_id import MyID, MyIDTuple


class TestMyID(unittest.TestCase):
    '''Тесты для класса MyID'''
    
    def test_generate_random(self):
        '''Тест генерации случайных ID'''
        # Генерация должна работать без ошибок
        for _ in range(100):
            uid = MyID()
            self.assertIsInstance(uid, MyID)
            self.assertEqual(len(uid), 22)
            self.assertTrue(uid[0].isalpha())
            self.assertTrue(all(c.isalnum() for c in uid[1:]))
    
    def test_derive_deterministic(self):
        '''Тест детерминированного создания'''
        # Одинаковый source → одинаковый ID
        uid1 = MyID.derive('test')
        uid2 = MyID.derive('test')
        self.assertEqual(uid1, uid2)
        self.assertIsInstance(uid1, MyID)
        self.assertIsInstance(uid2, MyID)
        
        # Разный source → разный ID
        uid3 = MyID.derive('test2')
        self.assertNotEqual(uid1, uid3)
    
    def test_derive_edge_cases(self):
        '''Тест детерминированного создания с edge case'''
        # Пустая строка
        uid1 = MyID.derive('')
        self.assertIsInstance(uid1, MyID)
        self.assertEqual(len(uid1), 22)
        
        # Очень длинная строка
        long_string = 'a' * 1000
        uid2 = MyID.derive(long_string)
        self.assertIsInstance(uid2, MyID)
        
        # Специальные символы
        uid3 = MyID.derive('hello@world#123')
        self.assertIsInstance(uid3, MyID)
    
    def test_valid_string_creation(self):
        '''Тест создания из валидной строки'''
        # Валидный ID
        uid_str = 'A123456789012345678901'
        uid = MyID(uid_str)
        self.assertEqual(str(uid), uid_str)
        self.assertIsInstance(uid, MyID)
        
        # ID с буквами в разных позициях
        test_cases = [
            'AbcDefGhijKlmNopQrstUv',
            'Z098765432109876543210',
            'a123456789012345678901',
            'zABCDEFGHIJKLMNOPQRSTU'
        ]
        for case in test_cases:
            uid = MyID(case)
            self.assertEqual(str(uid), case)
    
    def test_invalid_string_creation(self):
        '''Тест создания из невалидной строки'''
        invalid_cases = [
            ('1234567890123456789012', 'начинается с цифры'),
            ('', 'пустая строка'),
            ('A123', 'слишком короткий'),
            ('A' * 23, 'слишком длинный'),
            ('A12345678901234567890!', 'спецсимвол в конце'),
            ('A123 56789012345678901', 'пробел внутри'),
            ('A12345678901234567890\n', 'перенос строки'),
            ('A12345678901234567890\t', 'табуляция'),
            ('@BCDEFGHIJKLMNOPQRSTUV', 'спецсимвол в начале'),
            ('A12345678901234567890я', 'не-ASCII буква'),
        ]
        
        for value, reason in invalid_cases:
            with self.subTest(value=value, reason=reason):
                with self.assertRaises(ValueError):
                    MyID(value)
    
    def test_wrong_type_creation(self):
        '''Тест создания из неправильного типа'''
        invalid_cases = [
            None,
            123,
            3.14,
            [],
            {},
            True,
            object(),
        ]
        
        for value in invalid_cases:
            with self.subTest(type=type(value).__name__):
                with self.assertRaises(ValueError):
                    MyID(value)
    
    def test_already_myid(self):
        '''Тест передачи уже существующего MyID'''
        uid1 = MyID()
        uid2 = MyID(uid1)  # Должен вернуть тот же объект (или равный)
        self.assertEqual(uid1, uid2)
        self.assertIsInstance(uid2, MyID)
    
    def test_immutability(self):
        '''Тест неизменяемости (как строки)'''
        uid = MyID()
        
        # Строка неизменяема - нельзя изменить символы по индексу
        with self.assertRaises(TypeError):
            uid[0] = 'B'
        
        # Проверка, что это строка (наследник str)
        self.assertIsInstance(uid, str)
        
        # Проверка, что строковые методы возвращают str, не MyID
        upper = uid.upper()
        self.assertIsInstance(upper, str)
        self.assertNotIsInstance(upper, MyID)
        
        lower = uid.lower()
        self.assertIsInstance(lower, str)
        self.assertNotIsInstance(lower, MyID)
        
        # Конкатенация
        concat = uid + 'extra'
        self.assertIsInstance(concat, str)
        self.assertNotIsInstance(concat, MyID)
    
    def test_hash_and_equality(self):
        '''Тест хэширования и сравнения'''
        uid1 = MyID.derive('test')
        uid2 = MyID.derive('test')
        uid3 = MyID.derive('different')
        
        # Равенство
        self.assertEqual(uid1, uid2)
        self.assertNotEqual(uid1, uid3)
        
        # Хэши
        self.assertEqual(hash(uid1), hash(uid2))
        self.assertNotEqual(hash(uid1), hash(uid3))
        
        # Словарь как ключ
        d = {uid1: 'value'}
        self.assertIn(uid2, d)
        self.assertEqual(d[uid2], 'value')
    
    def test_case_sensitivity(self):
        '''Тест чувствительности к регистру'''
        uid1 = MyID('Abcdefghijklmnopqrstuv')
        uid2 = MyID('abcdefghijklmnopqrstuv')  # Другой регистр первого символа
        self.assertNotEqual(uid1, uid2)
    
    def test_string_operations(self):
        '''Тест строковых операций'''
        uid = MyID('A123456789012345678901')
        
        # Унаследованные от str операции
        self.assertEqual(uid[0], 'A')
        self.assertEqual(uid[1:4], '123')
        self.assertEqual(len(uid), 22)
        self.assertTrue(uid.startswith('A'))
        self.assertTrue(uid.endswith('1'))
        self.assertIn('123', uid)
        
        # Методы str
        self.assertEqual(uid.upper(), 'A123456789012345678901')
        self.assertIsInstance(uid.upper(), str)  # Возвращает str, не MyID
        self.assertNotIsInstance(uid.upper(), MyID)


class TestMyIDTuple(unittest.TestCase):
    '''Тесты для класса MyIDTuple'''
    
    def test_from_comma_string(self):
        '''Тест создания из строки с запятыми'''
        # Одиночный ID
        t1 = MyIDTuple('A123456789012345678901')
        self.assertEqual(len(t1), 1)
        self.assertIsInstance(t1[0], MyID)
        
        # Несколько ID
        ids = [MyID() for _ in range(3)]
        t2 = MyIDTuple(','.join(map(str, ids)))
        self.assertEqual(len(t2), 3)
        self.assertEqual(t2, tuple(ids))
        
        # С пробелами вокруг запятых
        t3 = MyIDTuple(f'{ids[0]}, {ids[1]},  {ids[2]}')
        self.assertEqual(len(t3), 3)
        self.assertEqual(t3, tuple(ids))
    
    def test_from_list(self):
        '''Тест создания из списка'''
        ids = [MyID() for _ in range(3)]
        
        # Список MyID
        t1 = MyIDTuple(ids)
        self.assertEqual(t1, tuple(ids))
        
        # Список строк
        t2 = MyIDTuple([str(uid) for uid in ids])
        self.assertEqual(t2, tuple(ids))
    
    def test_from_tuple(self):
        '''Тест создания из кортежа'''
        ids = tuple(MyID() for _ in range(3))
        t = MyIDTuple(ids)
        self.assertEqual(t, ids)
        self.assertIsInstance(t, MyIDTuple)
    
    def test_nested_structures(self):
        '''Тест вложенных структур'''
        uid1 = MyID()
        uid2 = MyID()
        uid3 = MyID()
        
        # Вложенные списки/кортежи
        test_cases = [
            [[uid1], [uid2, uid3]],
            (uid1, [uid2, uid3]),
            [[[uid1]], uid2, [[uid3]]],
            [f'{uid1},{uid2}', uid3],
            [f'{uid1}, {uid2}', [uid3]],
        ]
        
        for case in test_cases:
            with self.subTest(case=case):
                t = MyIDTuple(case)
                self.assertEqual(len(t), 3)
                self.assertEqual(set(t), {uid1, uid2, uid3})
    
    def test_empty_cases(self):
        '''Тест пустых случаев'''
        # Пустая строка
        with self.assertRaises(ValueError):
            MyIDTuple('')
        
        # Пустой список
        with self.assertRaises(ValueError):
            MyIDTuple([])
        
        # Строка только с запятыми и пробелами
        with self.assertRaises(ValueError):
            MyIDTuple(' , , , ')
    
    def test_invalid_ids_in_tuple(self):
        '''Тест с невалидными ID в кортеже'''
        valid_id = MyID()
        invalid_cases = [
            f'{valid_id},invalid',
            [valid_id, '123invalid'],
            ('valid_string', valid_id),  # 'valid_string' не MyID
            f'1234567890123456789012,{valid_id}',  # первый невалидный
        ]
        
        for case in invalid_cases:
            with self.subTest(case=case):
                with self.assertRaises(ValueError):
                    MyIDTuple(case)
    
    def test_already_mytuple(self):
        '''Тест передачи уже существующего MyIDTuple'''
        ids = [MyID() for _ in range(3)]
        t1 = MyIDTuple(ids)
        t2 = MyIDTuple(t1)  # Должен вернуть тот же объект
        self.assertEqual(t1, t2)
        self.assertIsInstance(t2, MyIDTuple)
    
    def test_mixed_types(self):
        '''Тест смешанных типов'''
        uid = MyID()
        
        # Смесь MyID и строк
        t1 = MyIDTuple([uid, str(uid)])
        self.assertEqual(len(t1), 2)
        self.assertEqual(t1[0], uid)
        self.assertEqual(t1[1], uid)
        
        # Вложенные структуры со строками
        t2 = MyIDTuple([f'{uid},{uid}', [uid]])
        self.assertEqual(len(t2), 3)
        self.assertTrue(all(isinstance(x, MyID) for x in t2))
    
    def test_duplicates(self):
        '''Тест дубликатов'''
        uid = MyID()
        
        # Дубликаты должны сохраняться
        t = MyIDTuple([uid, uid, uid])
        self.assertEqual(len(t), 3)
        self.assertEqual(t, (uid, uid, uid))
        
        # Строка с дубликатами
        t2 = MyIDTuple(f'{uid},{uid}')
        self.assertEqual(len(t2), 2)
    
    def test_string_methods(self):
        '''Тест строковых методов MyIDTuple'''
        ids = [MyID() for _ in range(3)]
        t = MyIDTuple(ids)
        
        # Проверка, что это кортеж
        self.assertIsInstance(t, tuple)
        self.assertEqual(len(t), 3)
        
        # Доступ по индексу
        self.assertEqual(t[0], ids[0])
        self.assertEqual(t[-1], ids[2])
        
        # Итерация
        for i, uid in enumerate(t):
            self.assertEqual(uid, ids[i])
            self.assertIsInstance(uid, MyID)
    def test_single_id_as_string(self):
        """Один ID в виде строки без запятых (граничный случай рекурсии)"""
        uid = MyID()
        t = MyIDTuple(str(uid))
        self.assertEqual(len(t), 1)
        self.assertEqual(t[0], uid)

    def test_single_id_with_whitespace(self):
        """Один ID с пробелами/табами вокруг (без запятых)"""
        uid = MyID()
        for space in [' ', '\t', '   ']:
            t = MyIDTuple(f'{space}{uid}{space}')
            self.assertEqual(len(t), 1)
            self.assertEqual(t[0], uid)

    def test_single_id_in_list_or_tuple(self):
        """Один ID, обёрнутый в список или кортеж"""
        uid = MyID()
        t1 = MyIDTuple([str(uid)])
        t2 = MyIDTuple((str(uid),))
        t3 = MyIDTuple([uid])
        t4 = MyIDTuple((uid,))
        for t in (t1, t2, t3, t4):
            self.assertEqual(len(t), 1)
            self.assertEqual(t[0], uid)


class TestIntegration(unittest.TestCase):
    '''Интеграционные тесты'''
    
    def test_pydantic_integration(self):
        '''Тест интеграции с Pydantic (упрощённый)'''
        from pydantic import BaseModel, ValidationError
        
        class TestModel(BaseModel):
            id: MyID
            ids: MyIDTuple
        
        # Валидные данные
        uid = MyID()
        model = TestModel(
            id=uid,
            ids=f'{uid},{MyID()}'
        )
        self.assertIsInstance(model.id, MyID)
        self.assertIsInstance(model.ids, MyIDTuple)
        
        # Невалидные данные через Pydantic
        with self.assertRaises(ValidationError):
            TestModel(id='invalid', ids='valid')
        
        # Сериализация
        data = model.model_dump()
        self.assertIsInstance(data['id'], str)
        self.assertIsInstance(data['ids'], str)
    
    def test_in_dict_and_set(self):
        '''Тест использования в словарях и множествах'''
        uid1 = MyID.derive('test1')
        uid2 = MyID.derive('test1')  # Такой же как uid1
        uid3 = MyID.derive('test2')
        
        # Словарь
        d = {uid1: 'value1', uid3: 'value2'}
        self.assertIn(uid2, d)
        self.assertEqual(d[uid2], 'value1')
        
        # Множество
        s = {uid1, uid3}
        self.assertIn(uid2, s)
        self.assertEqual(len(s), 2)  # uid1 и uid3, uid2 это дубликат uid1


class TestEdgeCases(unittest.TestCase):
    '''Тесты экстремальных случаев'''
    
    def test_boundary_lengths(self):
        '''Тест граничных длин'''
        # Минимальная валидная длина (22 символа)
        min_valid = 'A' + '1' * 21
        uid = MyID(min_valid)
        self.assertEqual(len(uid), 22)
        
        # Проверка на один символ меньше
        too_short = 'A' + '1' * 20
        with self.assertRaises(ValueError):
            MyID(too_short)
        
        # Проверка на один символ больше
        too_long = 'A' + '1' * 22
        with self.assertRaises(ValueError):
            MyID(too_long)
    
    def test_all_possible_first_chars(self):
        '''Тест всех возможных первых символов'''
        # Все буквы должны быть валидны
        for char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
            uid_str = char + '1' * 21
            uid = MyID(uid_str)
            self.assertEqual(uid[0], char)
    
    def test_special_unicode(self):
        '''Тест Unicode символов'''
        # Не-ASCII символы не должны быть валидны
        invalid_cases = [
            'Á123456789012345678901',  # Unicode буква
            'А123456789012345678901',  # Кириллица
            '😀123456789012345678901',  # Emoji
        ]
        
        for case in invalid_cases:
            with self.assertRaises(ValueError):
                MyID(case)
    
    def test_whitespace_variations(self):
        '''Тест различных пробельных символов'''
        uid = MyID()
        uid_str = str(uid)
        
        # Проверка, что пробелы вокруг не допускаются
        for whitespace in [' ', '\t', '\n', '\r', '\f', '\v']:
            with self.assertRaises(ValueError):
                MyID(whitespace + uid_str)
            
            with self.assertRaises(ValueError):
                MyID(uid_str + whitespace)
            
            with self.assertRaises(ValueError):
                MyID(f'{uid_str[0]}{whitespace}{uid_str[1:]}')


def run_tests():
    '''Запуск всех тестов'''
    # Создание test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMyID)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMyIDTuple))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestIntegration))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestEdgeCases))
    
    # Запуск с детальным выводом
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Вывод статистики
    print(f'\n{'='*60}')
    print(f'Тестов запущено: {result.testsRun}')
    print(f'Успешно: {result.testsRun - len(result.failures) - len(result.errors)}')
    if result.failures:
        print(f'Провалено: {len(result.failures)}')
        for test, traceback in result.failures:
            print(f'\nПровален: {test}')
            print(traceback)
    if result.errors:
        print(f'Ошибок: {len(result.errors)}')
        for test, traceback in result.errors:
            print(f'\nОшибка в: {test}')
            print(traceback)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    print('Запуск тестов для MyID и MyIDTuple...')
    success = run_tests()
    exit(0 if success else 1)
