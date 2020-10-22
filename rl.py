import json
from random import choice, random

def write_to_file(lis, filename):
	with open(filename, "w") as f:
		
		lis = {"|".join([str(y) for y in x[0]]) : x[1] for x in list(lis.items())} 
		f.write(json.dumps(lis))

def read_from_file(filename):
	with open(filename, "r") as f:
		ret = f.read()
		ret = json.loads(ret)
		ret = {tuple([int(y) for y in x[0].split("|")]) : {int(y[0]): y[1]for y in list(x[1].items())} for x in list(ret.items())} 
	return ret

class RL():
	def __init__(self, epsilon=0.5, alpha=0.5, gamma=0.8, xMax=10, yMax=10, filename=None):
		if filename:
			self.table = read_from_file("bananenbrot.json")
		else:
			self.table = {(ball_x, ball_y, paddle) : {1 : 0, 0 : 0, -1 : 0} for ball_x in range(0,xMax+2) for ball_y in range(0,yMax+2) for paddle in range(0,xMax)}
		self.epsilon = epsilon
		self.alpha = alpha
		self.gamma = gamma

	def get_action(self, state):
		#print(state)
		actions = self.table[state]
		if random() < self.epsilon:
			# choose a random action from actions
			#print(actions)
			action = choice(list(actions.keys()))
			#print(action)
		else:
			# get the key corresponding to the highest value from the actions dict
			action = max(actions, key=(lambda key: actions[key]))
		self.last_state_action = state, action
		self.epsilon -= 0.0001
		#print(self.table[state][action])
		return action

	def adjust(self, reward, state):
		if not self.last_state_action:
			return
		old_qvalue = self.table[self.last_state_action[0]][self.last_state_action[1]]
		# get the highest qvalue possible from the current state
		new_state_qvalue = max(list(self.table[state].values()))

		# update the old q value using the qlearning formula
		new_value = old_qvalue + self.alpha * (reward +  self.gamma * new_state_qvalue - old_qvalue)
		self.table[self.last_state_action[0]][self.last_state_action[1]] = new_value
		#print(self.table[self.last_state_action[0]][self.last_state_action[1]])

	def save(self): 
		print(self.table)
		print("hello")
		write_to_file(self.table, "bananenbrot.json")


if __name__ == "__main__":
	x = RL()
	game = BasicGame("PingPong", width=360, height = 500)
	game.start()
