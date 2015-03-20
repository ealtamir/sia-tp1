from calcudoku.board import Board
from calcudoku.cdstate import CDState
from search_problem_solver.problem import Problem


class CDProblem(Problem):

    def __init__(self, n):
        self.board = Board(n)

    def getInitialState(self):
        return CDState(self.board)

    def getGoalState(self):
        return CDState(self.board, (), isGoal=True)

    def getRules(self):
        raise NotImplementedError()

    def getHValue(self, state):
        raise NotImplementedError()
