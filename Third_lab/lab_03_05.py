'''
 Операции cо словарями
'''
d2 = {'apples': 5, 'bag': 'basket','bananas': 3, 'oranges': 2}
d5 = d2.copy() # создание копии словаря
print("Dict d5 copying d2 = ", d5)
# получение значения по ключу
print("Get dict value by key d5['bag']: ", d5["bag"])
print("Get dict value by key d5.get('bag'): ",d5.get('bag'))
print("Get dict keys d5.keys(): ", d5.keys()) #список ключей
print("Get dict values d5.values(): ", d5.values()) #список значений
print("\n")

myInfo = {'surname':'Popovskiy','name':'Alexandr','middlaename':'Alexandrovich','day':'28','month':'February','year':'2001','university':'ITMO'}
print(myInfo.keys())
print(myInfo.values())