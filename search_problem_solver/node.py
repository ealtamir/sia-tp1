
class Node():

    def __init__(self, state, cost):
        self.parent = None
        self.state = state
        self.cost = cost

    def __repr__(self):
        return "Node with state: %s" % self.state.__str__()

    def getSolution(self):
        if self.parent is None:
            return self.state.__str__()
        return "%s\n%s" % self.parent.getSolution(), self.state


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
