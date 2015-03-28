from calcudoku.cdrule import CDRule
from calcudoku.cdstate import CDState
from calcudoku.utilities.constants import SOLUTION
from search_problem_solver.problem import Problem

BLOCK_ID = 0
MOVE = 1
POINTS = 2


class CDProblem(Problem):

    def __init__(self, board):
        self.board = board
        self.goalState = None
        self.rulesMemo = None

    def get_initial_state(self):
        return CDState(self.board)

    def get_goal_state(self):
        if self.goalState is None:
            self.goalState = CDState(self.board, isGoal=True)
        return self.goalState

    def is_goal_state(self, state):
        return self.board.solve_game(state)

    def get_rules(self, state=None):
        if self.rulesMemo is None:
            self.rulesMemo = self.init_rules()
        return self.rulesMemo

    def get_HValue(self, state):
        raise NotImplementedError()

    def init_rules(self):
        rules = []
        # solution : (block_id, (move1, move2, ...),
        #  ((p1a, p1b), (p2a, ...))
        solutions = self.board.get_block_solutions()
        for solution in solutions:
            rule = CDRule(solution[BLOCK_ID], tuple(solution[MOVE]), solution[POINTS], self.board)
            rules.append(rule)
        print("Created %d rules" % len(rules))
        return rules

