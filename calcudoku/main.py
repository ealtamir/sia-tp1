import time

from calcudoku.cdproblem import CDProblem
from calcudoku.examples.fourByFourSumBoard import FourByFourSumBoard
from calcudoku.utilities.utils import timed
from search_problem_solver.engine import SearchProblemSolver



@timed
def main():
    board_problem = FourByFourSumBoard()
    board = board_problem.buildBoard()
    problem = CDProblem(board)
    engine = SearchProblemSolver(problem, 'DFS')
    return engine.solve(), board_problem

if __name__ == '__main__':
    main()
