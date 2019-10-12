def encrypt_caesar(plaintext: str) -> str:
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    a = ('abcdefghijklmnopqrstuvwxyz')
    b = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    ciphertext = str()
    s = -1
    for i in plaintext:
        s += 1
        for l in range(len(a)):
            if plaintext[s] == a[l]:
                if i != (' '):
                    ciphertext += str(a[(a.index(i) + 3) % 26])
                else:
                    ciphertext += (plaintext[s])
            else:
                if plaintext[s] == b[l]:
                    if i != (' '):
                        ciphertext += str(b[(b.index(i) + 3) % 26])
                    else:
                        ciphertext += (plaintext[s])
    return (ciphertext)


def decrypt_caesar(ciphertext: str) -> str:
    """
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = str()
    a = ('abcdefghijklmnopqrstuvwxyz')
    b = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    s = -1
    for i in ciphertext:
        s += 1
        for l in range(len(a)):
            if ciphertext[s] == a[l]:
                if i != (' '):
                    ciphertext += str(a[(a.index(i) - 3) % 26])
                else:
                    plaintext += (ciphertext[s])
            else:
                if ciphertext[s] == b[l]:
                    if i != (' '):
                        plaintext += str(b[(b.index(i) - 3) % 26])
                    else:
                        plaintext += (ciphertext[s])
    return (plaintext)
