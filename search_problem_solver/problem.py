
class Problem():
	"""
	Abstract Problem class that defines the key elements of the
	informed search problem solver.
	"""
	def get_initial_state(self):
		raise NotImplementedError()

	def get_goal_state(self):
		raise NotImplementedError()

	def is_goal_state(self, state):
		raise NotImplementedError()

	def get_rules(self):
		raise NotImplementedError()

	def get_HValue(self, state):
		raise NotImplementedError()

