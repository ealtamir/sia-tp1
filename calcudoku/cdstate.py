from calcudoku.exceptions.game_exceptions import SolutionSizeError
from calcudoku.utilities.constants import OCCUPIED, COL, ROW, BLOCK_ID, \
    SOLUTION, NOT_OCCUPIED, POINTS, BLOCK
from calcudoku.utilities.utils import create_taken_matrix
from search_problem_solver.state import State


class CDState(State):
    """
    Abstract subclass that only enforces a compare method between states.
    """
    def __init__(self, board, solutions=dict(),
                 taken_rows=None, taken_cols=None, isGoal=False):
        self.board = board

        # {block_id: [val1, val2, ...], ... }
        self.solutions = solutions
        self._isSolution = isGoal

        n = self.board.board_size

        # rows are values that a square can take and the column represent
        # the row/column of the board
        # e.g. self.taken_rows[1][3] to check if I can put a 1 in row 3
        self.taken_rows = taken_rows if taken_rows else create_taken_matrix(n)
        self.taken_cols = taken_cols if taken_cols else create_taken_matrix(n)

    def __str__(self):
        s = "State: "
        goalBoard = [[ None for i in range(self.board.board_size)] for j in range(self.board.board_size)]
        for key in self.solutions:
            block = self.board.blocks[key]
            solution = self.solutions[key]
            s += "<%s: %s, %s> - " % (block[BLOCK], block[POINTS], str(solution))
            i = 0
            for x,y in block[POINTS]:
                goalBoard[x][y] = solution[i]
                i += 1
        return goalBoard

    def __hash__(self):
        return sum((key.__hash__() + val.__hash__()
                    for key, val in self.solutions.items())) * 31

    @property
    def solutions(self):
        return self.__solutions

    @solutions.setter
    def solutions(self, value):
        assert(type(self) is type(dict()))
        self.__solutions = value

    def compare(self, state):
        if self is state:
            return True

        if len(self.solutions) != len(state.solutions):
            return False

        #if self.board.haveSameSolutions(self, state):
        #    return True

        if self.__hash__() == state.__hash__():
            return True

        return False

    def isGoal(self):
        return self._isSolution

    def hasSameSolutionsAs(self, state):
        assert(self.haveSameSolutionSize(state))

        for key in self.solutions.iterkeys():
            if key not in state.solutions:
                return False

            solution1 = self.solutions[key]
            solution2 = state.solutions[key]

            if solution1 != solution2:
                return False
        return True

    def create_next_state(self, board, block_id, solution):
        new_solutions = self.solutions.copy()
        new_solutions[block_id] = solution
        new_taken_rows = self.refresh_row_occupied_matrix(board,
                                                          block_id, solution)
        new_taken_cols = self.refresh_col_occupied_matrix(board,
                                                          block_id, solution)
        return CDState(board, new_solutions, new_taken_rows, new_taken_cols)

    def haveSameSolutionSize(self, state):
        return len(self.solutions) == len(state.solutions)

    def is_row_occupied(self, solution, point):
        return self.check_occupancy(self.taken_rows, solution, point)

    def is_col_occupied(self, solution, point):
        return self.check_occupancy(self.taken_cols, solution, point)

    def check_occupancy(self, arr, solution, point):
        # solutions are in the range (1, n) we want (0, n - 1)
        return arr[solution - 1][point] == OCCUPIED

    def refresh_row_occupied_matrix(self, board, block_id, solution):
        _, points = self.board.blocks[block_id]
        points = [points[i][ROW] for i in range(len(points))]
        return self.refresh_occupied_matrix(self.taken_rows, solution, points)

    def refresh_col_occupied_matrix(self, board, block_id, solution):
        _, points = self.board.blocks[block_id]
        points = [points[i][COL] for i in range(len(points))]
        return self.refresh_occupied_matrix(self.taken_cols, solution, points)

    def refresh_occupied_matrix(self, taken_rows, solution, points):
        new_matrix = create_taken_matrix(self.board.board_size, taken_rows)
        for i in range(len(solution)):
            assert(new_matrix[solution[i] - 1][points[i]] == NOT_OCCUPIED)
            # solutions are in the range (1, n) we want (0, n - 1)
            new_matrix[solution[i] - 1][points[i]] = OCCUPIED
        return new_matrix

    def numberOfSolutions(self):
        return len(self.solutions)

    def already_solved(self, block_id):
        return block_id in self.solutions
