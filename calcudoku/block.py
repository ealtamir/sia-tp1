from calcudoku.utilities.combinations import calculate_combinations
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
            combinations = calculate_combinations(self.operation, self.total, self.squares_num, self.board_size)
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


