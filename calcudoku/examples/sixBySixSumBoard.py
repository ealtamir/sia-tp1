from calcudoku.block import Block
from calcudoku.board import Board
from calcudoku.examples.calcudoku_board import CalcudokuBoard


BOARD_NAME = '6v6,+'


class SixBySixSumBoard(CalcudokuBoard):

    def __init__(self):
        name = '6x6_sum_board'
        identifier = '6v6,+'
        CalcudokuBoard.__init__(self, 6, name, identifier)

    def buildBoard(self):
        board = Board(self.n)
        n = 6
        # http://www.conceptispuzzles.com/index.aspx?uri=puzzle/euid/01000000bd3e55d2addc1fd16c1d0b54e4330f21f2847ae9fc0e2eb91984dc15987812acf871c6d96630c158785351b257c75bf3/play
        blocks = (
            (Block(3, '+', 6, n), ((0, 0), (1, 0), (1, 1))),
            (Block(1, '+', 4, n), ((0, 1),)),
            (Block(3, '+', 7, n), ((0, 2), (1, 2), (2, 2))),
            (Block(3, '+', 14, n), ((0, 3), (0, 4), (0, 5))),
            (Block(3, '+', 11, n), ((1, 3), (1, 4), (2, 3))),
            (Block(3, '+', 8, n), ((1, 5), (2, 5), (3, 5))),
            (Block(3, '+', 17, n), ((2, 0), (2, 1), (3, 1))),
            (Block(3, '+', 13, n), ((2, 4), (3, 3), (3, 4))),
            (Block(2, '+', 6, n), ((3, 0), (4, 0))),
            (Block(3, '+', 12, n), ((3, 2), (4, 2), (4, 1))),
            (Block(3, '+', 9, n), ((4, 3), (5, 3), (5, 4))),
            (Block(3, '+', 8, n), ((4, 4), (4, 5), (5, 5))),
            (Block(3, '+', 11, n), ((5, 0), (5, 1), (5, 2))),
        )

        for block, points in blocks:
            board.add_block(block, points)

        return board

