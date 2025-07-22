#!/usr/bin/env python3

def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b


def main():
    print("🧮 Python Calculator")
    print("Operations: +, -, *, /")

    try:
        num1 = float(input("Enter first number: "))
        operation = input("Enter operation (+, -, *, /): ").strip()
        num2 = float(input("Enter second number: "))

        if operation == '+':
            result = add(num1, num2)
        elif operation == '-':
            result = subtract(num1, num2)
        elif operation == '*':
            result = multiply(num1, num2)
        elif operation == '/':
            result = divide(num1, num2)
        else:
            print("❌ Invalid operation!")
            return

        print(f"✅ Result: {num1} {operation} {num2} = {result}")

    except ValueError as e:
        print(f"❌ Error: {e}")
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    main()
