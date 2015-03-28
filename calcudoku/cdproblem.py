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

    def getInitialState(self):
        return CDState(self.board)

    def getGoalState(self):
        if self.goalState is None:
            self.goalState = CDState(self.board, isGoal=True)
        return self.goalState

    def isGoalState(self, state):
        return self.board.solve_game(state)

    def getRules(self, state=None):
        if self.rulesMemo is None:
            self.rulesMemo = self.init_rules()
        return self.rulesMemo

    def getHValue(self, state):
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

