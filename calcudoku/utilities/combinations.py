def calculate_combinations(op, total, squares, n):
    if squares == 1:
        return [total]

    combinations = []
    for i in range(1, n + 1):
        combinations += operation[op](total, squares, i, n, [i])
    return combinations


# 6 = 2 + 3 + 1, squares = 3, n = 20
def calculate_additions(total, squares, sum, n, checked):
    return calculate_helper(addition, total, squares, sum, n, checked)


def calculate_products(total, squares, prod, n, checked):
    return calculate_helper(product, total, squares, prod, n, checked)


def calculate_subtractions(total, squares, v, n, checked):
    return calculate_helper(subtraction, total, squares, v, n, checked)


def calculate_divisions(total, squares, v, n, checked):
    for i in range(1, n + 1):
        if float(v) / i == total:
            return [[v, i], [i, v]]
    return []


def calculate_helper(op, total, squares, v, n, checked):
    checked_len = len(checked)
    numbers = (j for j in range(1, n + 1)
               if op(j, v) <= total)
    combinations = []
    for i in numbers:
        if op(v, i) == total and checked_len + 1 == squares:
            combinations.append(checked + [i])
        elif op(v, i) < total and checked_len + 1 < squares:
            new_checked = list(checked) + [i]
            combinations += calculate_helper(op, total, squares, op(v, i), n, new_checked)
    return combinations


def product(a, b):
    return a * b


def addition(a, b):
    return a + b


def subtraction(a, b):
    return abs(a - b)


operation = {
    '+': calculate_additions,
    '-': calculate_subtractions,
    '*': calculate_products,
    '/': calculate_divisions
}

if __name__ == '__main__':
    print(calculate_combinations('/', 4, 2, 12))
    print(calculate_combinations('+', 16, 3, 12))
