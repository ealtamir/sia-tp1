from calcudoku.exceptions.game_exceptions import SolutionSizeError
from calcudoku.utilities.constants import OCCUPIED_VALUE, COL, ROW, BLOCK_ID, \
    SOLUTION
from calcudoku.utilities.utils import create_taken_matrix
from search_problem_solver.state import State


class CDState(State):
    """
    Abstract subclass that only enforces a compare method between states.
    """
    def __init__(self, board, solutions=tuple(),
                 taken_rows=None, taken_cols=None, isGoal=False):
        self.board = board

        # [(block_id, (square1_val, square2_val...))]
        self.solutions = solutions
        self._isSolution = isGoal

        n = self.board.board_size

        # rows are values that a square can take and the column represent
        # the row/column of the board
        # e.g. self.taken_rows[1][3] to check if I can put a 1 in row 3
        self.taken_rows = taken_rows if taken_rows else create_taken_matrix(n)
        self.taken_cols = taken_cols if taken_cols else create_taken_matrix(n)


    @property
    def solutions(self):
        return self.__solutions


    @solutions.setter
    def solutions(self, value):
        assert type(self) is type(dict())
        self.__solutions = value


    def compare(self, state):
        if self.board.solvesGame(state) and self.board.solvesGame(self):
            return True

        if len(self._solutions) != len(state.solutions):
            return False

        if self.board.haveSameSolution(self, state):
            return True

        return False


    def isGoal(self):
        return self._isSolution


    def hasSameSolutionsAs(self, state):
        if not self.haveSameSolutionSize(state):
            raise SolutionSizeError()

        # TODO: Make this use a dictionary because if the solutions are in the wrong order, it fails.
        for i in range(len(state.solutions)):
            id1 = self.solutions[i][BLOCK_ID]
            id2 = state.solutions[i][BLOCK_ID]
            solution1 = self.solutions[i][SOLUTION]
            solution2 = state.solutions[i][SOLUTION]

            if id1 != id2 or solution1 != solution2:
                return False
        return True


    def create_next_state(self, board, block_id, solution):
        new_solutions = self.solutions + (self.block_id, self.solution)
        new_taken_rows = self.refresh_row_occupied_matrix(board,
                                                          block_id, solution)
        new_taken_cols = self.refresh_col_occupied_matrix(board,
                                                          block_id, solution)
        return CDState(board, new_solutions, new_taken_rows, new_taken_cols)


    def haveSameSolutionSize(self, state):
        return len(self.solutions) == len(state.solutions)


    def is_row_occupied(self, value, point):
        return self.check_occupancy(self.taken_rows, value, point)


    def is_col_occupied(self, value, point):
        return self.check_occupancy(self.taken_cols, value, point)


    def check_occupancy(self, arr, value, point):
        return arr[value][point] == OCCUPIED_VALUE


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
            assert(new_matrix[solution[i]][points[i]] == (not OCCUPIED_VALUE))
            new_matrix[solution[i]][points[i]] = OCCUPIED_VALUE
        return new_matrix
