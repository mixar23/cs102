num_16 = input()
s = 0
num_16_1 = ('')

if num_16[0] == '-':
    for i in range(1,len(num_16)):
        num_16_1 += num_16[i]
    Truth =True
    num_16 = num_16_1
else:
    Truth = False


for i in enumerate(num_16):
    x,y = i
    if y == 'A':
        y = 10
    elif y == 'B':
        y = 11
    elif y == 'C':
        y = 12
    elif y == 'D':
        y = 13
    elif y == 'E':
        y = 14 
    elif y == 'F':
        y = 15
    y = int(y)
    s += y*16**(len(num_16)-x-1)
s = bin(s)
binary = ('')
for i in range(2,len(s)):
    binary += s[i]
if Truth:
    additional_code = ('')
    for i in binary:
        if i == '1':
            additional_code += '0'
        else:
            additional_code += '1'
    length = len(additional_code)
    additional_code_int = int(additional_code)
    additional_code_int += 1
    k = 0
    while '2' in set(str(additional_code_int)):
        additional_code_int -= 10**k
        k += 1
        additional_code_int += 10**k
    additional_code = (length-len(str(additional_code_int)))*'0'+str(additional_code_int)
    print(additional_code)
else:
    print(binary)

