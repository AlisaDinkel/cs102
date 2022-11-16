"""Калькулятор"""

from math import *

priors = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3, "s": 4, "c": 4, "t": 4, "l": 4, "n": 4, "g": 4}


def calc(command_calc, x_calc, y_calc=0):

    """Калькулятор операций"""
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
    if command_calc in ("ln", "n"):
        return log(x_calc)
    if command_calc in ("lg", "l"):
        return log(x_calc, 10)
    if command_calc in ("sin", "s"):
        return sin(x_calc)
    if command_calc in ("cos", "c"):
        return cos(x_calc)
    if command_calc in ("tg", "t"):
        return tan(x_calc)


def num_system(num, base_num_system):

    """Перевод числа из десятичной системы в другую с основанием от 2 до 9"""
    digits = "0123456789"
    res = ""
    while num > 0:
        res = digits[num % base_num_system] + res
        num = num // base_num_system
    return res if res != "" else 0


def is_float(num):
    """Проверка, что число вещественное"""
    try:
        float(num)
    except ValueError:
        return False
    return True


def brackets_are_ok(string_eq):
    """Проверка, корректно ли стоят скобки в выражении"""
    brackets = 0
    for char in string_eq:
        if char == "(":
            brackets += 1
        elif char == ")":
            brackets -= 1
            if brackets < 0:
                ok_flag = False
                break
    else:
        ok_flag = not brackets
    return ok_flag


def get_string_eq(given=None):
    """Получение выражения со скобочками или без"""
    string_eq = input("Введите выражение > ") if given is None else given
    if brackets_are_ok(string_eq):
        string_eq = (
            string_eq.replace(" ", "")
            .replace("ctg", "g")
            .replace("sin", "s")
            .replace("cos", "c")
            .replace("tg", "t")
            .replace("lg", "l")
            .replace("ln", "n")
        )
        return string_eq
    return "Скобки стоят неправильно!"


def solve(string_eq: str):
    """Решение полноценного выражения"""
    if string_eq == "":
        return ""
    if is_float(string_eq):
        return float(string_eq)
    in_brackets = 0
    best_opt = 5
    found_outside_brackets = -1
    for i, char in enumerate(string_eq):
        if char == "(":
            in_brackets += 1
        elif char == ")":
            in_brackets -= 1
        elif char in "+-*/^sctlng":
            if in_brackets == 0 and priors[char] <= best_opt:
                found_outside_brackets = i
                best_opt = priors[char]
    if found_outside_brackets == -1:
        if string_eq[0] == "(" and string_eq[-1] == ")":
            return solve(string_eq[1:-1])
        return string_eq
    inner_1 = solve(string_eq[:found_outside_brackets])
    inner_2 = solve(string_eq[found_outside_brackets + 1 :])
    operand = string_eq[found_outside_brackets]

    if inner_1 == "" and is_float(inner_2):
        return calc(operand, 0.0, float(inner_2)) if operand == "-" else calc(operand, float(inner_2))
    if is_float(inner_1) and is_float(inner_2):
        return calc(operand, float(inner_1), float(inner_2))
    return inner_1 if inner_2.isspace() else inner_2


while True:
    print("Доступные операции: +, -, /, *, ^2, ^, ln, lg, tg, cos, sin, numeral system, expression")
    command = input("Введите операцию: ")
    if command in ("+", "-", "*", "/", "^"):

        while True:
            try:
                x = float(input("Введите первое число: "))
                break
            except ValueError:
                print("Некорректное число. Попробуйте заново.")

        while True:
            try:
                y = float(input("Введите второе число: "))
                break
            except ValueError:
                print("Некорректное число. Попробуйте заново.")
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
                print("На 0 делить нельзя.")
                continue
        if command == "^":
            print(f"{x} ^ {y} = {calc(command, x, y)}")

    elif command in ("^2", "ln", "lg"):

        if command == "^2":
            while True:
                try:
                    x = float(input("Введите число: "))
                    break
                except ValueError:
                    print("Некорректное число. Попробуйте заново.")

            print(f"{x} ^ 2 = {calc(command, x)}")

        if command == "ln":
            while True:
                try:
                    x = float(input("Введите число: "))
                    if x > 0:
                        print(f"ln{x} = {calc(command, x)}")
                        break
                    print("Число должно быть положительным.")
                except ValueError:
                    print("Некорректное число. Попробуйте заново.")

        if command == "lg":
            while True:
                try:
                    x = float(input("Введите число: "))
                    if x > 0:
                        print(f"lg{x} = {calc(command, x)}")
                        break
                    print("Число должно быть положительным.")
                except ValueError:
                    print("Некорректное число. Попробуйте заново.")

    elif command in ("sin", "cos", "tg"):

        while True:
            try:
                x = float(input("Введите число: "))
                break
            except ValueError:
                print("Некорректное число. Попробуйте заново.")

        if command == "sin":
            print(f"sin{x} = {calc(command, x)}")
        if command == "cos":
            print(f"cos{x} = {calc(command, x)}")
        if command == "tg":
            print(f"tg{x} = {calc(command, x)}")

    elif command == "numeral system":

        while True:
            x = int(input("Введите число: "))
            if int(x) != x or x < 0:
                print("Число должны быть целым неотрицательным!")
                continue
            break

        while True:
            base = int(input("Введите основание СС: "))
            if int(base) != base or base < 0:
                print("Число должны быть целым неотрицательным!")
                continue
            elif not 2 <= base <= 9:
                print("Основание CC должно быть в диапазоне [2, 9]")
                continue
            else:
                break

        print("Result: ", num_system(x, base))

    elif command == "expression":

        print(solve(get_string_eq()))

    else:

        print("Invalid operation")

    s = input("Continue: Yes/No?\n")
    if s == "No":
        print("STOP")
        break
