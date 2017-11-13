import sys, math
import numpy as np

import Box2D
from Box2D.b2 import (edgeShape, circleShape, fixtureDef, polygonShape, revoluteJointDef, contactListener)

import gym
from gym import spaces
from gym.utils import colorize, seeding

# Create an environment 

GAME = 'BipedalWalkerHardcore-v2'
env = gym.make(GAME)


# class World():

# 	def __init__(self):
# 		self.viwer = None

# 		self.world = Box2D.b2World()

# 	def make_path(self,x):
# 		pass 


# if __name__== "__main__":
env.reset()
while True:
	env.render()

