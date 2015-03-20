
class State():
    """
    Abstract subclass that only enforces a compare method between states.
    """
    def compare(self, state):
        raise NotImplementedError("Must be defined in concrete subclass.")
