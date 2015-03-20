from search_problem_solver.state import State


class CDState(State):
    """
    Abstract subclass that only enforces a compare method between states.
    """
    def __init__(self, board, solutions=tuple(), isGoal=False):
        self.board = board

        # [(block_id, (square1_val, square2_val...))]
        self.solutions = solutions
        self.isSolution = isGoal


    def compare(self, state):
        if self.board.solvesGame(state) and self.board.solvesGame(self):
            return True

        if len(self.solutions) != len(state.solutions):
            return False

        if self.board.haveSameSolution(self, state):
            return True

        return False


    def isGoal(self):
        return self.isSolution





