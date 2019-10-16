def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    while len(plaintext) > len(keyword):
        keyword += keyword
    ciphertext = str()
    if keyword.isupper():
        for i in range(len(plaintext)):
            n = ord(plaintext[i])
            x = ord(keyword[i])
            if n + (x % 65) > 90:
                ciphertext += chr(n + (x % 65) - 26)
            else:
                ciphertext += chr(n + (x % 65))
    else:
        for i in range(len(plaintext)):
            n = ord(plaintext[i])
            x = ord(keyword[i])
            if (n + (x % 97)) > 122:
                ciphertext += chr(n + (x % 97) - 26)
            else:
                ciphertext += chr(n + (x % 97))

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    while len(ciphertext) > len(keyword):
        keyword += keyword
    plaintext = str()
    if keyword.isupper():
        for i in range(len(ciphertext)):
            n = ord(ciphertext[i])
            x = ord(keyword[i])
            print(n, x)
            if n >= x:
                plaintext += chr(n - (x % 65))
            else:
                plaintext += chr(n + 26 - (x % 65))
    else:
        for i in range(len(ciphertext)):
            n = ord(ciphertext[i])
            x = ord(keyword[i])
            if n >= x:
                plaintext += chr(n - (x % 97))
            else:
                plaintext += chr(n + 26 - (x % 97))

    return (plaintext)
