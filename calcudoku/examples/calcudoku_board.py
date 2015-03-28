
class CalcudokuBoard():

    def __init__(self, n, name, identifier):
        self.n = n
        self.name = name
        self.identifier = identifier

    def build_board(self):
        raise NotImplementedError()

