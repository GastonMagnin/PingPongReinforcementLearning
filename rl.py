import json
from random import choice, random
from os.path import isfile

def write_to_file(lis, filename):
	# open the file
	with open(filename, "w") as f:
		# generate a data structure that can be converted to json format
		# -> convert tuple dict keys to strings 
		lis = {"|".join([str(y) for y in x[0]]) : x[1] for x in list(lis.items())} 
		# convert lis to a json string and write it to the file
		f.write(json.dumps(lis))

def read_from_file(filename):
	# open the file
	with open(filename, "r") as f:
		# read the contents and convert them to a pyhton data structure
		ret = f.read()
		ret = json.loads(ret)
		#  convert everything that was changed for json conformity in write_to_file back 
		ret = {tuple([int(y) for y in x[0].split("|")]) : {int(y[0]): y[1]for y in list(x[1].items())} for x in list(ret.items())} 
	return ret

class RL():
	def __init__(self, epsilon=0.5, alpha=0.5, gamma=0.8, xMax=10, yMax=10, start_xV=1, start_yV=1, use_file=True):
		
		self.xV = start_xV
		self.yV = start_yV
		# variables for dynmic field size
		self.xMax = xMax
		self.yMax = yMax
		self.epsilon = epsilon
		self.alpha = alpha
		self.gamma = gamma
		# if the use file flag is set and a file with a qtable for the given parameters
		# (xMax, yMax, xV, yV) is found use the table from that file
		if use_file and isfile(self.generate_filename()):
			# get the table from the file
			self.table = read_from_file(self.generate_filename())
			# since the table is already filled no exploration is necessary 
			self.epsilon = 0
		# otherwise generate a new table
		else:
			# generate a {state : {action : Q(state, action)}} dictionary using ball position, paddle position and ball velocity as state
			self.table = {(ball_x, ball_y, paddle, xV, yV) : {1 : 0, 0 : 0, -1 : 0} for ball_x in range(0,xMax+2) for ball_y in range(0,yMax+2) for paddle in range(0,xMax) for xV in [start_xV, -start_xV] for yV in [start_yV, -start_yV]}
		



	def get_action(self, state):
		"""
		returns an action for the given state using epsilon greedy
		params:
		state: the current state of the game
		"""
		
		# get a dictionary with all actions and their qvalues for this state
		actions = self.table[state]

		# choose a random action with a chance of epsilon, else choose the best available action (highest qvalue)
		if random() < self.epsilon:
			# choose a random action from actions
			action = choice(list(actions.keys()))
		else:
			# get the key(action) corresponding to the highest (q)value from the actions dict
			# in other words get the action with the highest qvalue 
			action = max(actions, key=(lambda key: actions[key]))

		# save the last state and action to use later when adjusting the qvalue
		self.last_state_action = state, action

		# decrement epsilon
		self.epsilon -= 0.0001

		return action

	def adjust(self, reward, state):
		"""
		adjusts the qvalue of the last state action pair(Q(state, action))
		according to {reward} and the highest possible qvalue for the next action
		Q(old_state, action) = Q(old_state, action) + alpha * ({reward} + gamma * max(Q({state}, action)) - Q(old_state, action))
		params:
		{reward}: the reward for the last action taken
		{state}: the new state reached (after taking the last action)
		"""
		if not self.last_state_action:
			return
		# get the old qvalue
		old_qvalue = self.table[self.last_state_action[0]][self.last_state_action[1]]

		# get the highest qvalue possible from the current state
		new_state_qvalue = max(list(self.table[state].values()))

		# update the old q value using the qlearning formula
		new_value = old_qvalue + self.alpha * (reward +  self.gamma * new_state_qvalue - old_qvalue)
		self.table[self.last_state_action[0]][self.last_state_action[1]] = new_value
		

	def save(self): 
		"""
		Saves the current qtable to a file
		"""
		filename = self.generate_filename()
		write_to_file(self.table, filename)

	def generate_filename(self):
		"""
		generates a filename used for saving the current qtable to/retrieving a qtable from a file
		generates a name indicating the states covered in the qtable
		"""
		return f"rl_{self.xMax}_{self.yMax}_{self.xV}_{self.yV}.json"



if __name__ == "__main__":
	x = RL()
	game = BasicGame("PingPong", width=360, height = 500)
	game.start()
