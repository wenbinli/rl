import numpy as np

class agent(object):
	def __init__(self, n_actions = 1, discount = 0.99, agent_type = 'random'):
		self.num_actions = n_actions
		self.discount = 0.99
		self.agent_type = agent_type

	def act(self, state):
		if agent_type == 'random':
			action = np.random.randint(self.num_actions)
		return action
