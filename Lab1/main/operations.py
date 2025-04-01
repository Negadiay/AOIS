from conversion import to_binary, to_binary_fraction, convert_decimal_to_binary

BIT_LENGTH = 8
PRECISION = 8

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
