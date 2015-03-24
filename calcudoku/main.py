from calcudoku.cdproblem import CDProblem
from calcudoku.examples.fourByFourSumBoard import buildBoard
from search_problem_solver.engine import SearchProblemSolver


def main():
    board = buildBoard()
    problem = CDProblem(board)
    engine = SearchProblemSolver(problem, 'BFS')
    engine.solve()


if __name__ == '__main__':
    main()
