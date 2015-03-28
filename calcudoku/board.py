from calcudoku.exceptions.game_exceptions import InvalidBlockShapeException, \
    BlockOverlapException
from calcudoku.utilities.constants import COL, POINTS, ROW, BLOCK_ID, SOLUTION


class Board():
    def __init__(self, n):
        self.board_size = n

        # Contains tuples of the form (block, block_points)
        self.blocks = {}

        self.board = [[ None for i in range(n)] for j in range(n)]
        self.blockNum = 0

    def add_block(self, block, points):
        if self.points_are_invalid(points):
            msg = "All the squares in the block should be adjacent"
            raise InvalidBlockShapeException(msg)

        self.blocks[block.id] = (block, points)

        for (x, y) in points:
            if self.board[x][y] is not None:
                msg = "Block overlap at (%d, %d)." % (x, y)
                raise BlockOverlapException(msg)
            self.board[x][y] = block
        self.blockNum += 1

    def points_are_invalid(self, points):
        # TODO: Chequesr que todos los puntos sean adyacentes
        # raise NotImplementedError()
        return False

    def solve_game(self, state):
        """
        Game is solved when the number of solutions matches the number
        of blocks. This works because no invalid solution will ever go
        inside the solutions data structure.
        """
        if state.number_of_solutions() == self.blockNum:
            return True
        return False

    def have_same_solutions(self, state1, state2):
        return state1.has_same_solutions_as(state2)

    def rule_is_applicable(self, state, block_id, solution):
        """
        This is one of the most important functions. It checks whether the
        solution for the block of id, "block_id", is valid for the current state
        of the board. It's critical that this functions executes swiftly.
        """
        if state.already_solved(block_id):
            return False

        block, points = self.blocks[block_id]

        unoccupied = self.check_occupancy_matrices(state, solution, points)
        return unoccupied

    def check_occupancy_matrices(self, state, solution, points):
        for i in range(len(points)):
            if self.cant_place_value_at_point(state, solution[i], points[i]):
                return False
        return True

    def check_for_colliding_solutions(self, solution, points):
        sol_len = len(solution)
        pairs = ( (i, j) for i in range(sol_len)
                 for j in range(sol_len) if i > j )
        for i, j in pairs:
            if solution[i] == solution[j]:
                row_collision = points[i][ROW] == points[j][ROW]
                col_collision = points[i][COL] == points[j][COL]
                if row_collision or col_collision:
                    return True
        return False

    def cant_place_value_at_point(self, state, solution, point):
        row_occupied = state.is_row_occupied(solution, point[ROW])
        if row_occupied:
            return True

        col_occupied = state.is_col_occupied(solution, point[COL])
        if col_occupied:
            return True
        return False

    def get_block_solutions(self):
        solutions = []
        for block, points in self.blocks.itervalues():
            for move in block.get_moves():
                solutions.append((block.id, move, self.blocks[block.id][POINTS]))
        solutions = self.remove_useless_solutions(solutions)
        solutions = self.establish_solution_ordering(solutions)
        return solutions

    def remove_useless_solutions(self, solutions):
        useful_solutions = []
        sol_num = len(solutions)
        for solution in solutions:
            if len(solution[POINTS]) == 1:
                useful_solutions.append(solution)
            elif self.is_valid_solution(solution):
                useful_solutions.append(solution)
            else:
                print("Solution discarded: %s" % str(solution))
        new_sol_num = len(useful_solutions)
        print("Discarded %d useless solutions." % (sol_num - new_sol_num))
        return useful_solutions

    def is_valid_solution(self, solution):
        POINTS = 2 # The global constant is 1, in this case it should be 2
        length = len(solution[POINTS])
        values = ((s1, s2) for s1 in xrange(length)
                  for s2 in xrange(length) if s1 != s2)
        for s1, s2 in values:
            have_same_solution_value = solution[SOLUTION][s1] == solution[SOLUTION][s2]
            same_row = solution[POINTS][s1][ROW] == solution[POINTS][s2][ROW]
            same_col = solution[POINTS][s1][COL] == solution[POINTS][s2][COL]

            if have_same_solution_value and (same_row or same_col):
                return False
        return True

    def establish_solution_ordering(self, solutions):
        solutions = self.sort_by_correct_solution_probability(solutions)
        print(solutions)
        return solutions

    def sort_by_correct_solution_probability(self, solutions):
        probability = {}
        for solution in solutions:
            if solution[BLOCK_ID] in probability:
                probability[solution[BLOCK_ID]] += 1
            else:
                probability[solution[BLOCK_ID]] = 1

        solutions.sort(key=lambda solution: probability[solution[BLOCK_ID]])
        return solutions

