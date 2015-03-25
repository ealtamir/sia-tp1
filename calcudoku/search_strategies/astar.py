from evaluation import evaluation


def a_star(node, frontier):
    frontier.pqpush(evaluation(node), node)
