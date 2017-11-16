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

<<<<<<< HEAD
for i_episode in range(20):
    observation = env.reset()
    for t in range(100):
        env.render()
        print(observation)
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
=======
# fake contribution

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
>>>>>>> b17014948d627bf685233e5b7a0850635fc01ed1
