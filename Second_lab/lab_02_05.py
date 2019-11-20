import math
import random

row = input()
letters = []
for i in range(len(row)):
    letters.append(row[i])
m = math.factorial(len(row))
words = []
k = 0
while k != m:
    row2 = ('')
    for i in range(len(row)):
        row2 += random.choice(letters)
    if not row2  in words:
        k += 1
    words.append(row2)
for i in words:
    print(i)
