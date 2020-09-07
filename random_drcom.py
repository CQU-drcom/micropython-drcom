import os


def randint(a, b):
    assert b - a + 1 < 0xFFFFFFFF
    rint = int.from_bytes(os.urandom(4), 'little')
    return a + rint % (b - a + 1)
