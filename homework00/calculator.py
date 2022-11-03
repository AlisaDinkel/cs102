"""Calculator"""

from math import *


def calc(command_calc, x_calc, y_calc=0):

    """Operations"""
    if command_calc == "+":
        return x_calc + y_calc
    if command_calc == "-":
        return x_calc - y_calc
    if command_calc == "*":
        return x_calc * y_calc
    if command_calc == "/":
        return x_calc / y_calc
    if command_calc == "^":
        return x_calc**y_calc
    if command_calc == "^2":
        return x_calc**2
    if command_calc == "ln":
        return log(x_calc)
    if command_calc == "lg":
        return log(x_calc, 10)
    if command_calc == "sin":
        return sin(x_calc)
    if command_calc == "cos":
        return cos(x_calc)
    if command_calc == "tan":
        return tan(x_calc)


def num_system(num, base_num_system):

    """Numeral system"""
    new_num = ""
    while num > 0:
        new_num = str(num % base_num_system) + new_num
        num //= base_num_system
    return new_num


while True:
    print("Available operations : +, -, /, *, ^2, ^, ln, lg, tan, cos, sin, numeral system")
    command = input("Enter operation: ")

    if command in ("+", "-", "*", "/", "^"):

        x = input("Enter first number: ")
        while not x.isdigit():
            print("Invalid number")
            x = input("Enter first number: ")
        y = input("Enter second number: ")
        while not y.isdigit():
            print("Invalid number")
            y = input("Enter second number: ")
        x = float(x)
        y = float(y)
        if command == "+":
            print(f"{x} + {y} = {calc(command, x, y)}")
        if command == "-":
            print(f"{x} - {y} = {calc(command, x, y)}")
        if command == "*":
            print(f"{x} * {y} = {calc(command, x, y)}")
        if command == "/":
            if y != 0:
                print(f"{x} / {y} = {calc(command, x, y)}")
            else:
                print("Can't divide by 0. Try again.")
                continue
        if command == "^":
            print(f"{x} ^ {y} = {calc(command, x, y)}")

    elif command in ("^2", "ln", "lg"):

        x = input("Enter first number: ")
        while not x.isdigit():
            print("Invalid number")
            x = input("Enter first number: ")
        x = float(x)

        if command == "^2":
            print(f"{x} ^ 2 = {calc(command, x)}")
        if command == "ln":
            print(f"ln{x} = {calc(command, x)}")
        if command == "lg":
            print(f"lg{x} = {calc(command, x)}")

    elif command in ("sin", "cos", "tan"):

        x = input("Enter angle in rad: ")
        while not x.isdigit():
            print("Invalid number")
            x = input("Enter angle in rad: ")
        x = float(x)

        if command == "sin":
            print(f"sin{x} = {calc(command, x)}")
        if command == "cos":
            print(f"cos{x} = {calc(command, x)}")
        if command == "tan":
            print(f"tan{x} = {calc(command, x)}")

    elif command == "numeral system":

        x = input("Enter first number: ")
        while not x.isdigit():
            print("Invalid number")
            x = input("Enter first number: ")
        x = int(x)
        base = input("Base (2-9): ")
        while not base.isdigit():
            print("Invalid base")
            base = input("Base (2-9): ")
        base = int(base)
        print("Result ", num_system(x, base))

    else:
        print("Invalid operation")

    s = input("Continue: Yes/No?\n")
    if s == "No":
        print("STOP")
        break
