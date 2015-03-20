
class Problem():
	"""
	Abstract Problem class that defines the key elements of the
	informed search problem solver.
	"""
	def getInitialState(self):
		raise NotImplementedError()

	def getGoalState(self):
		raise NotImplementedError()

	def isGoalState(self, state):
		raise NotImplementedError()

	def getRules(self):
		raise NotImplementedError()

	def getHValue(self, state):
		raise NotImplementedError()

