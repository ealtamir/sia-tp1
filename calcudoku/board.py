from operator import itemgetter
from calcudoku.block import Block
from calcudoku.exceptions.game_exceptions import InvalidBlockShapeException, \
    BlockOverlapException
from calcudoku.utilities.constants import COL, POINTS, ROW, BLOCK_ID


class Board():
    def __init__(self, n):
        self.board_size = n

        # Contains tuples of the form (block, block_points)
        self.blocks = {}

        self.board = [[ None for i in range(n)] for j in range(n)]
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
        # TODO: Chequesr que todos los puntos sean adyacentes
        # raise NotImplementedError()
        return False

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
        if state.already_solved(block_id):
            return False

        block, points = self.blocks[block_id]

        assert(len(points) == len(solution))

        colliding_solutions = self.check_for_colliding_solutions(solution,
                                                                 points)
        if colliding_solutions:
            return False

        unoccupied = self.check_occupancy_matrices(state, solution, points)
        return unoccupied

    def check_occupancy_matrices(self, state, solution, points):
        for i in range(len(points)):
            if self.cant_place_value_at_point(state, solution[i], points[i]):
                return False
        return True

    def check_for_colliding_solutions(self, solution, points):
        sol_len = len(solution)
        pairs = ( (i, j) for i in range(sol_len)
                 for j in range(sol_len) if i > j )
        for i, j in pairs:
            if solution[i] == solution[j]:
                row_collision = points[i][ROW] == points[j][ROW]
                col_collision = points[i][COL] == points[j][COL]
                if row_collision or col_collision:
                    return True
        return False

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
        for block, points in self.blocks.itervalues():
            for move in block.getMoves():
                solutions.append((block.id, move, self.blocks[block.id][POINTS]))
        return solutions
