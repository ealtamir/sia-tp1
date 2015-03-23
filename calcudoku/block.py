from calcudoku.exceptions.game_exceptions import InvalidBlockOperation


class Block():

    operationsMemo = {}
    block_id = 0

    def __init__(self, squares_num, operation, total, n):
        self.squares_num = squares_num
        self.operation = operation
        self.total = total
        self.board_size = n
        self.id = Block.block_id
        Block.block_id += 1


    def __str__(self):
        return "%d%s" % (self.total, self.__operation)


    def getMoves(self):
        params = (self.total, self.squares_num, self.board_size)
        if params not in Block.operationsMemo:
            combinations = calculateCombinations(self.total, self.squares_num,
                                                 self.board_size)
            Block.operationsMemo[params] = combinations
        else:
            combinations = Block.operationsMemo[params]
        return combinations


    @property
    def operation(self):
        return self.__operation


    @operation.setter
    def operation(self, value):
        if value in ('+', '-', '*', '/', '%'):
            self.__operation = value
        else:
            raise InvalidBlockOperation()


# 6 = 2 + 3 + 1, squares = 3, n = 20
def calculateCombinationsHelper(sum, total, squares, n, checked):
    checked_len = len(checked)
    numbers = (j for j in range(1, n + 1)
               if j + sum <= total and j not in checked)
    combinations = []
    for i in numbers:
        if sum + i == total and checked_len + 1 == squares:
            combinations.append(checked + [i])
        elif sum + i < total and checked_len + 1 < squares:
            new_checked = checked.copy() + [i]
            combinations += calculateCombinationsHelper(sum + i, total,
                                                        squares, n, new_checked)
    return combinations


def calculateCombinations(total, squares, n):
    # TODO: Generalizar esto para todos los tipos de operaciones
    if squares == 1:
        return [total]

    combinations = []
    for i in range(1, n + 1):
        if i < total:
            combinations += calculateCombinationsHelper(i, total,
                                                        squares, n, [i])
    return combinations