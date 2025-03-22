EXPONENT_BIAS = 127
MANTISSA_BITS = 23

def add_ieee754(num1, num2):
    def float_to_binary(num):
        sign = 0 if num >= 0 else 1
        num = abs(num)
        exponent = EXPONENT_BIAS
        while num >= 2:
            num /= 2
            exponent += 1
        while num < 1:
            num *= 2
            exponent -= 1
        mantissa = int((num - 1) * (2 ** MANTISSA_BITS))
        return f"{sign:01b}{exponent:08b}{mantissa:023b}"

    bin1 = float_to_binary(num1)
    bin2 = float_to_binary(num2)

    result = num1 + num2
    bin_result = float_to_binary(result)

    print(f"Number 1 (Binary): {bin1}")
    print(f"Number 2 (Binary): {bin2}")
    print(f"Result (Binary): {bin_result}")
    print(f"Result (Decimal): {result}")