from search_problem_solver.rule import Rule


class CDRule(Rule):
    """
    Abstract Rule class that must be completed with appropiate methods.
    """
    def __init__(self, cost, name):
        self.cost = cost

    def __str__(self):
        raise NotImplementedError("You must define the rule name here")

    def applyRule(self, state):
        raise NotImplementedError("You must supply this method in the subclass")
