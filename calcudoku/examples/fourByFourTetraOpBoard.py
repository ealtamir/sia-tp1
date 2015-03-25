from calcudoku.block import Block
from calcudoku.board import Board
from calcudoku.examples.calcudoku_board import CalcudokuBoard


class FourByFourQuadOpBoard(CalcudokuBoard):

    def __init__(self):
        n = 4
        name = 'four_by_four_quad_op_board'
        identifier = '4v4,+-*%'
        CalcudokuBoard.__init__(self, n, name, identifier)

    def buildBoard(self):
        board = Board(self.n)
        n = self.n
        # http://www.conceptispuzzles.com/index.aspx?uri=puzzle/euid/010000005c90ba9cef752592c2821489f10a64d344d5b21e759e4fc8f0ba743bbc0cedc056ef0d7eed01882f941b20a55e2b3215/play
        blocks = (
            (Block(2, '+', 5, n), ((0, 0), (0, 1))),
            (Block(2, '-', 3, n), ((0, 2), (0, 3))),
            (Block(2, '+', 7, n), ((1, 0), (2, 0))),
            (Block(2, '/', 2, n), ((1, 1), (2, 1))),
            (Block(2, '*', 8, n), ((1, 2), (2, 2))),
            (Block(1, '+', 3, n), ((1, 3),)),
            (Block(2, '/', 4, n), ((3, 0), (3, 1))),
            (Block(1, '+', 3, n), ((3, 2),)),
            (Block(2, '+', 3, n), ((2, 3), (3, 3)))
        )

        for block, points in blocks:
            board.addBlock(block, points)

        return board

