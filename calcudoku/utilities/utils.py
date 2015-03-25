import sys
import time

from array import array
from calcudoku.exceptions.game_exceptions import \
    InvalidCommandLineArgumentException
from calcudoku.utilities.constants import DEFAULT_ARRAY_TYPE


DEFAULT_PARAMETERS = {
    'problem_board' : 'four_by_four_sum_board',
    'search_algo' : 'DFS',
    'cost_func' : '_',
    'heuristic_func' : '_'
}


def get_problem_parameters():
    parameters = DEFAULT_PARAMETERS
    commands = (
        lambda x : parameters.update({'problem_board' : x}),
        lambda x : parameters.update({'search_algo' : x}),
        lambda x : parameters.update({'cost_func' : x}),
        lambda x : parameters.update({'heuristic_func' : x})
    )
    if len(sys.argv) <= 1:
        print("%s RUNNING WITH DEFAULT ARGUMENTS %s" % ("*" * 40, "*" * 40))
    else:
        if not len(commands) < len(sys.argv):
            msg = "Expected 4 arguments, got %d" % len(sys.argv)
            raise InvalidCommandLineArgumentException(msg)

        for i, arg in enumerate(sys.argv):
            if i == 0:
                continue # script name
            if not (arg.isalpha() and len(arg) < 20):
                msg = "Command argument %s with number" \
                      " %d is invalid" % (str(arg), i)
                raise InvalidCommandLineArgumentException(msg)

            commands[i - 1](arg)
    return parameters


def create_taken_matrix(n, init_matrix=None):
    if init_matrix:
        assert(len(init_matrix) == n)
        matrix = [array(DEFAULT_ARRAY_TYPE, init_matrix[i]) for i in range(n)]
    else:
        init_vector = [0] * n
        matrix = [array(DEFAULT_ARRAY_TYPE, init_vector) for i in range(n)]
    return matrix


def save_results(results):
    data = '\n'.join(["%s = %s" % (key, str(val))
                      for key, val in results.iteritems()])
    name = 'solutions/%s.txt' % results['test_name']
    with open(name, 'w') as f:
        f.write(data)


def timed(f):
    def timed_func(*args, **kwargs):
        print("%s> Starting timed function" % ("=" * 30))
        start = time.clock()
        results, board = f(*args, **kwargs)
        end = time.clock()
        print("=" * 60)
        print("CPU Time: %02f" % (end - start))
        results['cpu_time'] = (end - start)
        results['test_name'] = board.name
        results['test_identifier'] = board.identifier
        save_results(results)
    return timed_func

