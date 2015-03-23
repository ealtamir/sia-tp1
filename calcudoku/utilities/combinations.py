import itertools

def calculate_combinations(op, total, squares, n):
    if squares == 1:
        return [total]

    combinations = []
    for i in range(1, n + 1):
        if i < total:
            combinations += operation[op](total, squares, i, n, [i])
    return combinations


# 6 = 2 + 3 + 1, squares = 3, n = 20
def calculate_additions(total, squares, sum, n, checked):
    checked_len = len(checked)
    numbers = (j for j in range(1, n + 1)
               if j + sum <= total and j not in checked)
    combinations = []
    for i in numbers:
        if sum + i == total and checked_len + 1 == squares:
            combinations.append(checked + [i])
        elif sum + i < total and checked_len + 1 < squares:
            new_checked = checked.copy() + [i]
            combinations += calculate_additions(sum + i, total, squares, n, new_checked)
    return combinations


def calculate_subtractions(total, squares, operand, n, checked):
    for i in range(1, n + 1):
        if abs(operand - i) == total and len(checked) + 1 == squares:
            return list(itertools.permutations(checked + [i]))
    return []


def calculate_divisions(total, squares, operand, n, checked):
    i = 1
    while i < operand:
        if operand / i == total:
            return list(itertools.permutations([operand, i]))
        i += 1
    return []


def calculate_products(total, squares, prod, n, checked):
    checked_len = len(checked)
    numbers = (j for j in range(1, n + 1)
               if j * prod <= total and j not in checked)
    combinations = []
    for i in numbers:
        if prod * i == total and checked_len + 1 == squares:
            combinations.append(checked + [i])
        elif prod * i < total and checked_len + 1 < squares:
            new_checked = checked.copy() + [i]
            combinations += calculate_additions(total, squares, prod * i, n, new_checked)
    return combinations


operation = {'+': calculate_additions,
             '-': calculate_subtractions,
             '*': calculate_products,
             '/': calculate_divisions
             }

# TODO store in a data structure without repeated values!
#def calculate_products(total, squares, n, checked):
#    factors = prime_factorization(total)
#    for i in factors:
#        if i > n:
#            raise Exception("Error: block value too big for the board")
#
#    factors = [factors]
#    while len(factors[0]) > squares:
#        factors = squash_products(factors)
#
#    ret = []
#    for i in factors:
#        ret += list(itertools.permutations(i))
#    return ret


#def squash_products(factors):
#    factors_len = len(factors[0])
#
#    i = 0
#    ret = []
#    while i < factors_len:
#        j = i + 1
#        while j < factors_len:
#            aux = []
#            aux.append(factors[i] * factors[j])
#            aux.append(factors[j + 1:])
#            ret.append(aux)
#            j += 1
#        i += 1
#    return ret


#primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


# Works (efficiently) for a limited size, but more than enough for the problem at hand
#def prime_factorization(n):
#    factors = [1]  # Not a prime, but still a possible number in the block!
#    for p in _primes:
#        if p > n:
#            break
#        while n % p == 0:
#            n /= p
#            factors.append(p)
#    return factors
