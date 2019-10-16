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
    ciphertext = str()
    for i in plaintext:
        id = ord(i)
        if ('a' <= i < 'x') or ('A' <= i < 'X'):
            id += 3
        elif ('x' <= i <= 'z') or ('X' <= i <= 'Z'):
            id -= 23
        ciphertext += chr(id)
    return ciphertext


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
    for i in ciphertext:
        id = ord(i)
        if ('d' <= i < 'z') or ('D' <= i < 'Z'):
            id -= 3
        elif ('a' <= i <= 'c') or ('A' <= i <= 'C'):
            id += 23
        plaintext += chr(id)
    return plaintext
