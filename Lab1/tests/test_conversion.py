import pytest
from conversion import to_binary, to_binary_fraction, convert_decimal_to_binary

def test_to_binary_positive():
    assert to_binary(5) == '00000101'
    assert to_binary(255) == '11111111'
    assert to_binary(1, 4) == '0001'
    assert to_binary(0, 4) == '0000'

def test_to_binary_negative():
    assert to_binary(-5) == '11111011'
    assert to_binary(-1, 4) == '1111'
    assert to_binary(-128, 8) == '10000000'

if __name__ == "__main__":
    pytest.main()
