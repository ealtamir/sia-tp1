from calcudoku.cdstate import CDState
from calcudoku.exceptions.game_exceptions import InvalidSolutionException
from search_problem_solver.exceptions.engine_exceptions import \
    NotApplicableException
from search_problem_solver.rule import Rule


# Coordinates of the board
X = 0
Y = 1

class CDRule(Rule):
    """
    Abstract Rule class that must be completed with appropiate methods.
    """
    def __init__(self, block_id, solution, points, board, cost=None):
        self.cost = cost
        self.block_id = block_id
        self.solution = solution
        self.points = points
        self.board = board

        if len(solution) != len(points):
            raise InvalidSolutionException("There must \
            be a solution for each point.")


    def __str__(self):
        s = "["
        for i in len(self.points):
            s += "(%d, %d) = %d, " % (self.points[i][X], self.points[i][Y],
                                      self.solution[i])
        s += "]"
        return s


    def applyRule(self, state):
        ruleIsApplicable = self.board.solutionIsValid(
            state, self.block_id, self.solution)
        if not ruleIsApplicable:
            raise NotApplicableException()

        new_solutions = state.solutions + (self.block_id, self.solution)
        new_state = CDState(self.board, new_solutions)
        return new_state
