import random
import math


def is_prime(n: int) -> bool:
    """
   >>> is_prime(2)
   True
   >>> is_prime(11)
   True
   >>> is_prime(8)
   False
   """
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    x = math.floor(n ** (1 / 2))
    for i in range(3, x, 2):
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

    while x != y:
        if x > y:
            x = x - y
        else:
            y = y - x
    return (x)
