import heapq


class PriorityQueue():
    def __init__(self):
        self._data = []

    def pqpush(self, node):
        heapq.heappush(self._data, (node.evaluation(), node))

    def pqpop(self):
        return heapq.heappop(self._data)[1]