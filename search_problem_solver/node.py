class Node():

    def __init__(self, state, cost, parent=None):
        self.parent = parent
        self.state = state
        self.cost = cost

    def __repr__(self):
        return "Node with state: %s" % self.state.__str__()

    def __hash__(self):
        return self.state.__hash__()

    def get_solution(self):
        return self.state.__str__()

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, p):
        self.__parent = p

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        raise NotImplementedError()

    @property
    def cost(self):
        return self.__cost

    @cost.setter
    def cost(self, value):
        raise NotImplementedError()
