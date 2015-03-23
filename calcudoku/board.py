from calcudoku.block import Block
from calcudoku.exceptions.game_exceptions import InvalidBlockShapeException, \
    BlockOverlapException, SolutionSizeError


BLOCK_ID = 0
SOLUTION = 1

class Board():

    def __init__(self, n):
        self.board_size = n
        self.blocks = {}
        self.board = [[None] * n] * n


    def addBlock(self, block, points):
        if self.pointsAreInvalid(points):
            raise InvalidBlockShapeException("All the squares in the block should be adjacent")

        self.blocks[block.id] = (block, points)

        for (x, y) in points:
            if self.board[x][y] is not None:
                raise BlockOverlapException("Block overlap at (%d, %d)." % (x, y))
            self.board[x][y] = block


    def pointsAreInvalid(self, points):
        raise NotImplementedError()


    def satisfies(self, state):
        raise NotImplementedError()
        if state.isGoal():
            return True
        else:
            pass # TODO: Check that state satisfies all blocks
        return False


    def haveSameSolutions(self, state1, state2):
        len_sols1 = len(state1.solutions)
        len_sols2 = len(state2.solutions)

        if len_sols1 != len_sols2:
            raise SolutionSizeError()

        for i in range(len_sols1):
            id1 = state1.solutions[i][BLOCK_ID]
            id2 = state2.solutions[i][BLOCK_ID]
            solution1 = state1.solutions[i][SOLUTION]
            solution2 = state2.solutions[i][SOLUTION]

            if id1 != id2 or solution1 != solution2:
                return False
        return True


    @classmethod
    def buildBoard(cls):
        n = 4
        board = Board(n)
        # http://www.conceptispuzzles.com/index.aspx?uri=puzzle/euid/010000002a6e5cbaa22408b0fa6312c6db4a88d62fc9f2953642b5523645754c48602f610e4c2ebd5db5f5de7b35b1720896f2dd/play
        blocks = (
            (Block(2, '+', 5, n), ((0, 0), (0, 1))),
            (Block(2, '+', 7, n), ((1, 0), (2, 0))),
            (Block(2, '/', 2, n), ((1, 1), (2, 1))),
            (Block(2, '*', 8, n), ((1, 2), (2, 2))),
            (Block(2, '/', 4, n), ((3, 0), (3, 1))),
            (Block(2, '%', 3, n), ((3, 2),)),
            (Block(2, '+', 3, n), ((2, 3), (3, 3))),
            (Block(2, '%', 3, n), ((3, 2),)),
            (Block(2, '-', 3, n), ((0, 2), (0, 3))),
        )

        for block, points in blocks:
            board.addBlock(block, points)

        return blocks


