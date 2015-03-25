
def evaluation(node):
    return node.cost + heuristic(node)


def h1(node):
    raise NotImplementedError


def h2(node):
    raise NotImplementedError


# TODO asignarle la que se pase por parametro al programa, no cablearla!
heuristic = h1
