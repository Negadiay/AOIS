BIT_LENGTH = 8
PRECISION = 8

def to_binary(n, bits=BIT_LENGTH):
    if n == 0:
        return '0' * bits

    binary = []
    is_negative = n < 0
    n = abs(n)

    while n > 0:
        binary.append(str(n % 2))
        n //= 2

    binary = binary[::-1]

    while len(binary) < bits:
        binary.insert(0, '0')

    if is_negative:
        binary = ['1' if bit == '0' else '0' for bit in binary]
        carry = 1
        for i in range(len(binary) - 1, -1, -1):
            if binary[i] == '1' and carry == 1:
                binary[i] = '0'
            elif carry == 1:
                binary[i] = '1'
                carry = 0

    return ''.join(binary)

def to_binary_fraction(n, precision=PRECISION):
    binary = ""
    while precision:
        n *= 2
        bit = int(n)
        binary += str(bit)
        n -= bit
        precision -= 1
    return binary

def convert_decimal_to_binary(decimal_number):
    integer_part = int(decimal_number)
    fractional_part = decimal_number - integer_part

    def direct_code(integer, fraction):
        sign_bit = '1' if integer < 0 else '0'
        binary_integer = to_binary(abs(integer), bits=BIT_LENGTH - 1)
        return f"{sign_bit}{binary_integer}.{to_binary_fraction(fraction)}"

    def inverse_code(integer, fraction):
        if integer >= 0:
            return f"0{to_binary(integer, bits=BIT_LENGTH - 1)}.{to_binary_fraction(fraction)}"
        else:
            binary = to_binary(abs(integer), bits=BIT_LENGTH - 1)
            inverse = ''.join('1' if bit == '0' else '0' for bit in binary)
            return f"1{inverse}.{to_binary_fraction(fraction)}"

    def additional_code(integer, fraction):
        if integer >= 0:
            return f"0{to_binary(integer, bits=BIT_LENGTH - 1)}.{to_binary_fraction(fraction)}"
        else:
            binary = to_binary(abs(integer), bits=BIT_LENGTH - 1)
            inverse = ''.join('1' if bit == '0' else '0' for bit in binary)
            additional = bin(int(inverse, 2) + 1)[2:]
            additional = additional.rjust(BIT_LENGTH - 1, '0')
            return f"1{additional}.{to_binary_fraction(fraction)}"

    direct = direct_code(integer_part, fractional_part)
    inverse = inverse_code(integer_part, fractional_part)
    additional = additional_code(integer_part, fractional_part)

    return direct, inverse, additional
