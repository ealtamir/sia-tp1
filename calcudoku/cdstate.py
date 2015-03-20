from search_problem_solver.state import State


class CDState(State):
    """
    Abstract subclass that only enforces a compare method between states.
    """
    def __init__(self, board, solutions=tuple()):
        self.board = board
        self.solutions = solutions


    def compare(self, state):
        if self.board.satisfies(state) and self.board.satisfies(self):
            return True

        if len(self.solutions) != len(state.solutions):
            return False







