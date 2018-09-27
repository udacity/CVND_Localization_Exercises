import localizer 
import random
from copy import deepcopy
from matplotlib import pyplot as plt

class Simulation(object):
	def __init__(self, grid, blur, p_hit,start_pos=None):
		"""

		"""
		self.grid = grid
		self.beliefs = localizer.initialize_beliefs(self.grid)
		self.height = len(grid)
		self.width  = len(grid[0])
		self.blur   = blur
		self.p_hit = p_hit
		self.p_miss = 1.0
		self.incorrect_sense_probability = self.p_miss / (p_hit + self.p_miss)
		self.colors = self.get_colors()
		self.num_colors = len(self.colors)
		if not start_pos:
			self.true_pose = (self.height/2, self.width/2)
		else:
			self.true_pose = start_pos
		self.prev_pose = self.true_pose
		self.prepare_visualizer()

	def prepare_visualizer(self):
		self.X = []
		self.Y = []
		self.P = []

	def get_colors(self):
		all_colors = []
		for row in self.grid:
			for cell in row:
				if cell not in all_colors:
					all_colors.append(cell)
		return all_colors

	def sense(self):
		color = self.get_observed_color()
		beliefs = deepcopy(self.beliefs)
		new_beliefs = localizer.sense(color, self.grid, beliefs, self.p_hit, self.p_miss)
		if not new_beliefs or len(new_beliefs) == 0:
			print "NOTE! The robot doesn't have a working sense function at this point."
			self.beliefs = beliefs
		else:
			self.beliefs = new_beliefs

	def move(self, dy, dx):
		new_y = (self.true_pose[0] + dy) % self.height
		new_x = (self.true_pose[1] + dx) % self.width
		self.prev_pose = self.true_pose
		self.true_pose = (new_y, new_x)
		beliefs = deepcopy(self.beliefs)
		new_beliefs = localizer.move(dy, dx, beliefs, self.blur)
		self.beliefs = new_beliefs


	def get_observed_color(self):
		y,x = self.true_pose
		true_color = self.grid[y][x]
		if random.random() < self.incorrect_sense_probability:
			possible_colors = []
			for color in self.colors:
				if color != true_color and color not in possible_colors:
					possible_colors.append(color)
			color = random.choice(possible_colors)
		else:
			color = true_color
		return color

	def show_beliefs(self,past_turn=False):
		if past_turn:
			X = deepcopy(self.X)
			Y = deepcopy(self.Y)
			P = deepcopy(self.P)
		
		del(self.X[:])
		del(self.Y[:])
		del(self.P[:])
		for y, row in enumerate(self.beliefs):
			for x, belief in enumerate(row):
				self.X.append(x)
				self.Y.append(self.height-y-1) # puts large y ABOVE small y
				self.P.append(5000.0 * belief)
		plt.figure()
		if past_turn:
			plt.scatter(X, Y, s=P, alpha=0.3,color="blue")
			plt.scatter([self.prev_pose[1]], [self.height-self.true_pose[0]-1], color='red', marker="*", s=200, alpha=0.3)
		plt.scatter(self.X,self.Y,s=self.P,color="blue")
		plt.scatter([self.true_pose[1]], [self.height-self.true_pose[0]-1], color='red', marker="*", s=200)
		plt.show()

	def random_move(self):
		dy = random.choice([-1,0,1])
		dx = random.choice([-1,0,1])
		return dy,dx

	def run(self, num_steps=1):
		for i in range(num_steps):
			self.sense()
			dy, dx = self.random_move()
			self.move(dy,dx)