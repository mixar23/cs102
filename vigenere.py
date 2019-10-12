def encrypt_vigenere(plaintext:str,keyword:str) -> str:
     a = ('abcdefghijklmnopqrstuvwxyz')
     b =('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
     ciphertext=str()
     s = 0
     for l in plaintext:
         k = 0
         for n in range(26):
             if l == a[n]:
                 s+=1
                 ciphertext += str(a[(a.index(l)+a.index(keyword[s%len(keyword)]))%26])
             elif l == b[n]:
                 s+=1
                 ciphertext += str(b[(b.index(l)+b.index(keyword[s%len(keyword)]))%26])
             else:
                    k += 1
         if k == 26:
             ciphertext+=(' ')
     return(ciphertext)
def decrypt_vigenere(ciphertext:str,keyword:str) -> str:
     a = ('abcdefghijklmnopqrstuvwxyz')
     b =('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
     plaintex=str()
     s = 0
     for l in ciphertext:
         k = 0
         for n in range(26):
             if l == a[n]:
                 s+=1
                 plaintex += str(a[(a.index(l)-a.index(keyword[s%len(keyword)]))%26])
             elif l == b[n]:
                 s+=1
                 plaintex += str(b[(b.index(l)-b.index(keyword[s%len(keyword)]))%26])
             else:
                    k += 1
         if k == 26:
             plaintex+=(' ')
     return(plaintex)     
