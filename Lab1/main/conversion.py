BIT_LENGTH = 8
PRECISION = 8

def to_binary(n, bits=BIT_LENGTH):
    return bin(n & int("1"*bits, 2))[2:].zfill(bits)

def to_binary_fraction(n, precision=PRECISION):
    binary = ""
    while precision:
        n *= 2
        bit = int(n)
        binary += str(bit)
        n -= bit
        precision -= 1
    return binary