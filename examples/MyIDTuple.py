from my_id import MyID, MyIDTuple

# Создание кортежа ID из строки
ids = MyIDTuple('xqqumRbXZ1KdIXDOBLcFTE,xELq0jsA9rgDlTkYXJXz6S,YXtOWu9Uv06iLOItdhPSWl')
# Или из списка
ids = MyIDTuple(['xqqumRbXZ1KdIXDOBLcFTE', MyID(), MyID('YXtOWu9Uv06iLOItdhPSWl')])  # Каждый элемент валидируется

# Доступ к элементам
first_id = ids[0]  # MyID('xqqumRbXZ1KdIXDOBLcFTE')
for uid in ids:
    print(uid)
