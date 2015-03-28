from calcudoku.exceptions.game_exceptions import InvalidSolutionException
from calcudoku.utilities.constants import ROW, COL, DEFAULT_COST
from search_problem_solver.exceptions.engine_exceptions import \
    NotApplicableException
from search_problem_solver.rule import Rule


class CDRule(Rule):
    """
    Abstract Rule class that must be completed with appropiate methods.
    """
    def __init__(self, block_id, solution, points, board, cost=DEFAULT_COST):
        self.cost = cost
        self.block_id = block_id
        self.solution = solution
        self.points = points
        self.board = board

        if len(solution) != len(points):
            raise InvalidSolutionException("There must \
            be a solution for each point.")

    def __repr__(self):
        s = "<"
        for i in range(len(self.points)):
            s += "(%d, %d) = %d, " % (self.points[i][ROW], self.points[i][COL], self.solution[i])
        s += ">"
        return s

    def applyRule(self, state):
        rule_is_applicable = self.board.rule_is_applicable(
            state, self.block_id, self.solution)
        if not rule_is_applicable:
            raise NotApplicableException()

        return state.create_next_state(self.board, self.block_id, self.solution)
