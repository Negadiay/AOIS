from conversion import convert_decimal_to_binary
from operations import (
    add_in_additional_code,
    subtract_in_additional_code,
    multiply_direct_code,
    divide_direct_code
)
from ieee754 import add_ieee754

def main():
    while True:
        print("Menu:")
        print("1. Convert decimal number to binary (direct, additional, inverse codes)")
        print("2. Add two numbers in additional code")
        print("3. Subtract two numbers in additional code")
        print("4. Multiply two numbers in direct code")
        print("5. Divide two numbers in direct code")
        print("6. Add two positive floating-point numbers (IEEE-754-2008 standard)")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            decimal_number = float(input("Enter a decimal number: "))
            direct, inverse, additional = convert_decimal_to_binary(decimal_number)
            print(f"Direct code: [{direct}]")
            print(f"Inverse code: [{inverse}]")
            print(f"Additional code: [{additional}]")
        elif choice == '2':
            num1 = int(input("Enter the first decimal number: "))
            num2 = int(input("Enter the second decimal number: "))
            add_in_additional_code(num1, num2)
        elif choice == '3':
            num1 = int(input("Enter the minuend (decimal number): "))
            num2 = int(input("Enter the subtrahend (decimal number): "))
            subtract_in_additional_code(num1, num2)
        elif choice == '4':
            num1 = int(input("Enter the first decimal number: "))
            num2 = int(input("Enter the second decimal number: "))
            multiply_direct_code(num1, num2)
        elif choice == '5':
            num1 = int(input("Enter the dividend (decimal number): "))
            num2 = int(input("Enter the divisor (decimal number): "))
            divide_direct_code(num1, num2)
        elif choice == '6':
            num1 = float(input("Enter the first positive floating-point number: "))
            num2 = float(input("Enter the second positive floating-point number: "))
            add_ieee754(num1, num2)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
