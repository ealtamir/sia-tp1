from calcudoku.board import Board
from calcudoku.cdrule import CDRule
from calcudoku.cdstate import CDState
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
        return self.board.solvesGame(state)

    def getRules(self):
        if self.rulesMemo is None:
            self.rulesMemo = []
            # solution : (block_id, (move1, move2, ...),
            #  ((p1a, p1b), (p2a, ...))
            solutions = self.board.getBlockSolutions()
            for solution in solutions:
                rule = CDRule(solution[BLOCK_ID], solution[MOVE],
                              solution[POINTS], self.board)
                self.rulesMemo.append(rule)
        return self.rulesMemo

    def getHValue(self, state):
        raise NotImplementedError()
