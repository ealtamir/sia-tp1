from calcudoku.block import Block
from calcudoku.board import Board
from calcudoku.examples.calcudoku_board import CalcudokuBoard


BOARD_NAME = '4v4,+'


class FourByFourSumBoard(CalcudokuBoard):

    def __init__(self):
        n = 4
        name = 'four_by_four_sum_board'
        identifier = '4v4,+'
        CalcudokuBoard.__init__(self, n, name, identifier)

    def build_board(self):
        board = Board(self.n)
        # http://www.conceptispuzzles.com/index.aspx?uri=puzzle/euid/010000002a6e5cbaa22408b0fa6312c6db4a88d62fc9f2953642b5523645754c48602f610e4c2ebd5db5f5de7b35b1720896f2dd/play
        blocks = (
            (Block(2, '+', 4, self.n), ((0, 0), (0, 1))),
            (Block(2, '+', 6, self.n), ((0, 2), (1, 2))),
            (Block(2, '+', 3, self.n), ((1, 0), (2, 0))),
            (Block(2, '+', 7, self.n), ((1, 1), (2, 1))),
            (Block(1, '+', 1, self.n), ((2, 2),)),
            (Block(1, '+', 4, self.n), ((0, 3),)),
            (Block(2, '+', 6, self.n), ((3, 0), (3, 1))),
            (Block(2, '+', 4, self.n), ((3, 2), (3, 3))),
            (Block(2, '+', 5, self.n), ((1, 3), (2, 3)))
        )

        for block, points in blocks:
            board.add_block(block, points)

        return board
