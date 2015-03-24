from array import array
import time
from calcudoku.utilities.constants import DEFAULT_ARRAY_TYPE


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
    name = 'calcudoku/solutions/%s.txt' % results['test_name']
    with open(name, 'w') as f:
        f.write(data)


def timed(F):
    def timed_func():
        print("%s> Starting timed function" % ("=" * 30))
        start = time.clock()
        results, board = F()
        end = time.clock()
        print("=" * 60)
        print("CPU Time: %02f" % (end - start))
        results['cpu_time'] = (end - start)
        results['test_name'] = board.name
        results['test_identifier'] = board.identifier
        save_results(results)
    return timed_func

