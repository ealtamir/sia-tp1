from array import array
from calcudoku.utilities.constants import DEFAULT_ARRAY_TYPE


def create_taken_matrix(n, init_matrix=None):
    if init_matrix:
        assert(len(init_matrix) == n)
        matrix = [array(DEFAULT_ARRAY_TYPE, init_matrix[i]) for i in range(n)]
    else:
        init_vector = [0] * n
        matrix = [array(DEFAULT_ARRAY_TYPE, init_vector) for i in range(n)]
    return matrix
