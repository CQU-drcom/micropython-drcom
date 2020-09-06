import os


def randint(a, b):
    assert a - b + 1 < 0xFFFFFFFF
    rint = int.from_bytes(os.urandom(4), 'little')
    return a + rint % (a - b + 1)
