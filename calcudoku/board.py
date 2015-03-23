from calcudoku.block import Block
from calcudoku.exceptions.game_exceptions import InvalidBlockShapeException, \
    BlockOverlapException
from calcudoku.utilities.constants import COL, POINTS, ROW


class Board():
    def __init__(self, n):
        self.board_size = n

        # Contains tuples of the form (block, block_points)
        self.blocks = {}

        self.board = [[None] * n] * n
        self.blockNum = 0


    def addBlock(self, block, points):
        if self.pointsAreInvalid(points):
            msg = "All the squares in the block should be adjacent"
            raise InvalidBlockShapeException(msg)

        self.blocks[block.id] = (block, points)

        for (x, y) in points:
            if self.board[x][y] is not None:
                msg = "Block overlap at (%d, %d)." % (x, y)
                raise BlockOverlapException(msg)
            self.board[x][y] = block
        self.blockNum += 1


    def pointsAreInvalid(self, points):
        raise NotImplementedError()


    def solvesGame(self, state):
        """
        Game is solved when the number of solutions matches the number
        of blocks. This works because no invalid solution will ever go
        inside the solutions data structure.
        """
        if state.numberOfSolutions() == self.blockNum:
            return True
        return False


    def haveSameSolutions(self, state1, state2):
        return state1.hasSameSolutionsAs(state2)


    def ruleIsApplicable(self, state, block_id, solution):
        """
        This is one of the most important functions. It checks whether the
        solution for the block of id, "block_id", is valid for the current state
        of the board. It's critical that this functions executes swiftly.
        """
        block, points = self.blocks[block_id]

        assert(len(points) == len(solution))

        for i in range(len(points)):
            if self.cant_place_value_at_point(state, solution[i], points[i]):
                return False
        return True


    def cant_place_value_at_point(self, state, solution, point):
        row_occupied = state.is_row_occupied(solution, point[ROW])
        if row_occupied:
            return True

        col_occupied = state.is_col_occupied(solution, point[COL])
        if col_occupied:
            return True
        return False


    def getBlockSolutions(self):
        solutions = []
        for id, block in self.blocks.items():
            for move in block.getMoves():
                solutions.append((id, move, self.blocks[id][POINTS]))
        return solutions

