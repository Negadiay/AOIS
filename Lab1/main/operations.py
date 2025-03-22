from conversion import to_binary, to_binary_fraction

BIT_LENGTH = 8
PRECISION = 8


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
            additional = bin(int(inverse, 2) + 1)[2:].zfill(BIT_LENGTH - 1)
            return f"1{additional}.{to_binary_fraction(fraction)}"

    direct = direct_code(integer_part, fractional_part)
    inverse = inverse_code(integer_part, fractional_part)
    additional = additional_code(integer_part, fractional_part)

    return direct, inverse, additional


def add_in_additional_code(num1, num2):
    print(f"Number 1 entered: {num1}")
    print(f"Number 2 entered: {num2}")

    result = num1 + num2
    direct, inverse, additional = convert_decimal_to_binary(result)
    print(f"Result: {int(result)}")
    print(f"Direct code: {direct.split('.')[0]}")
    print(f"Inverse code: {inverse.split('.')[0]}")
    print(f"Additional code: {additional.split('.')[0]}")


def subtract_in_additional_code(num1, num2):
    num2 = -num2
    add_in_additional_code(num1, num2)


def multiply_direct_code(num1, num2):
    result = num1 * num2
    direct, inverse, additional = convert_decimal_to_binary(result)
    print(f"Result: {int(result)}")
    print(f"Direct code: {direct.split('.')[0]}")
    print(f"Inverse code: {inverse.split('.')[0]}")
    print(f"Additional code: {additional.split('.')[0]}")


def divide_direct_code(num1, num2):
    result = num1 / num2
    integer_part = int(result)
    fractional_part = result - integer_part

    frac_binary = to_binary_fraction(fractional_part, precision=5)

    int_direct, int_inverse, int_additional = convert_decimal_to_binary(integer_part)

    direct_result = f"{int_direct.split('.')[0]}.{frac_binary}"
    inverse_result = f"{int_inverse.split('.')[0]}.{frac_binary}"
    additional_result = f"{int_additional.split('.')[0]}.{frac_binary}"

    print(f"Result: {result:.5f}")
    print(f"Direct code: {direct_result}")
    print(f"Inverse code: {inverse_result}")
    print(f"Additional code: {additional_result}")