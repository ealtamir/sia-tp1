from calcudoku.cdproblem import CDProblem
from calcudoku.examples.fourByFourSumBoard import FourByFourSumBoard
from calcudoku.examples.fourByFourTetraOpBoard import FourByFourQuadOpBoard
from calcudoku.utilities.utils import timed, get_problem_parameters
from search_problem_solver.engine import SearchProblemSolver

boards = {
    'four_by_four_sum_board' : FourByFourSumBoard,
    'four_by_four_quad_op_board' : FourByFourQuadOpBoard
}


@timed
def solve_problem(parameters):
    board_problem = boards[parameters['problem_board']]()
    board = board_problem.buildBoard()
    problem = CDProblem(board)
    engine = SearchProblemSolver(problem, parameters['search_algo'])
    return engine.solve(), board_problem


def main():
    parameters = get_problem_parameters()
    solve_problem(parameters)


if __name__ == '__main__':
    main()
