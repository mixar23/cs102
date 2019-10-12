import random


def is_prime(n: int) -> bool:
    """
   >>> is_prime(2)
   True
   >>> is_prime(11)
   True
   >>> is_prime(8)
   False
   """

    for i in range(2, n // 2 + 1):
        if n % i == 0:
            return False
    return True


def multiplicative_inverse(e: int, phi: int) -> int:
    """
    >>> multiplicative_inverse(7, 40)
    23
    """
    d = 1
    while (d * e) % phi != 1:
        d += 1
    return (d)


def generate_keypair(p: int, q: int):
    if not (is_prime(p) == True and is_prime(q) == True):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    else:
        n = p * q
        phi = (p - 1) * (q - 1)
        g = 0
        while g != 1:
            e = random.randrange(1, phi)
            g = gcd(e, phi)
        d = multiplicative_inverse(e, phi)
    return ((e, n), (d, n))


def gcd(x: int, y: int) -> int:
    """
   >>> gcd(12, 15)
   3
   >>> gcd(3, 7)
   1
   """

    for i in range(2, x):
        if (x % i == 0) and (y % i == 0):
            return (i)
    return (1)
