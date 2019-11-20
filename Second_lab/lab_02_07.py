num_12 = input()
num_14 = ('')
s = 0
for i in enumerate(num_12):
    x,y = i
    if y == 'A':
        y = 10
    elif y == 'B':
        y = 11
    y = int(y)
    s += y*12**(len(num_12)-x-1)
number = 14 
while s > 0:
    f = str(s % 14)
    if f == '10':
        f = "A"
    elif f == '11':
        f = 'B'
    elif f == '12':
        f = 'C'
    elif f == '13':
        f = 'D'
    num_14 = f + num_14
    s //= 14
print(num_14)