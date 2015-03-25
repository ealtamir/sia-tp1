from evaluation import heuristic


def greedy(self, node):
    self._frontier.pqpush(heuristic(node), node)

