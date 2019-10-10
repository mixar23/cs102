def encrypt_caesar(plaintext:str,n:int) -> str:
    a = ('abcdefghijklmnopqrstuvwxyz')
    b =('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    ciphertext = str()
    s=-1
    for i in plaintext:
        s+=1
        for l in range(len(a)):
            if plaintext[s]==a[l]:
                if i != (' '):
                    ciphertext+=str(a[(a.index(i)+n)%26])
                else:
                    ciphertext+=(" ")
            else:
                if plaintext[s]==b[l]:
                    if i != (' '):
                        ciphertext+=str(b[(b.index(i)+n)%26])
                    else:
                        ciphertext+=(" ")
    print('Result: ',ciphertext)
    return(ciphertext)
def decrypt_caesar(ciphertext:str,n:int) ->str:
    plaintext=str()
    a = ('abcdefghijklmnopqrstuvwxyz')
    b =('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    s=-1
    for i in ciphertext:
        s+=1
        for l in range(len(a)):
            if ciphertext[s]==a[l]:
                if i != (' '):
                    ciphertext+=str(a[(a.index(i)-n)%26])
                else:
                    ciphertext+=(" ")
            else:
                if ciphertext[s]==b[l]:
                    if i != (' '):
                        plaintext+=str(b[(b.index(i)-n)%26])
                    else:
                        plaintext+=(" ")
    print('Result: ',plaintext)
    return(plaintext)
x=input('Enter text: ')
k=int(input('Enter shift: '))
g=input('Encrypt text?(yes/no): ')
if g==('yes'):
    encrypt_caesar(x,k)
elif g==('no'):
    decrypt_caesar(x,k)
else:
    print('incorret input')"# cs102" 
