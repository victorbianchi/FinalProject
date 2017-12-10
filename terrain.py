import sys, math
import numpy as np

import Box2D
from Box2D.b2 import (edgeShape, circleShape, fixtureDef, polygonShape, revoluteJointDef, contactListener)

import gym
from gym import spaces
from gym.utils import colorize, seeding

class Terrain(gym.Env):
    def __init__(self):
        self.window_size = [600, 400]
        self.viewer = None
        self.world = Box2D.b2World()
        self.terrain_length = self.window_size[0]
        self.terrain_height = self.window_size[1]/4
        self.start = 20
        self.friction = 2.5
        self._seed()

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def make_slope(self):

        y = self.terrain_height
        self.terrain = []
        self.terrain_x = []
        self.terrain_y = []
        slope = 0.0

        for x in range(self.terrain_length):
            self.terrain_x.append(x)
            # TODO: Test what this actually does
            slope = 0.5*slope + 0.01*np.sign(self.terrain_height - y)
            if x > self.start:
                slope += self.np_random.uniform(-1, 1)  #1
            y += slope

            self.terrain_y.append(y)

    def create_terrain(self):
        self.terrain_poly = []
        for i in range(self.terrain_length-1):
            poly = [
                (self.terrain_x[i],   self.terrain_y[i]),
                (self.terrain_x[i+1], self.terrain_y[i+1])
                ]
            t = self.world.CreateStaticBody(
                fixtures = fixtureDef(
                    shape=edgeShape(vertices=poly),
                    friction = self.friction,
                    categoryBits=0x0001,
                ))
            color = (0.3, 1.0 if i%2==0 else 0.8, 0.3)
            t.color1 = color
            t.color2 = color
            self.terrain.append(t)
            color = (0.4, 0.6, 0.3)
            poly += [ (poly[1][0], 0), (poly[0][0], 0) ]
            self.terrain_poly.append( (poly, color) )
        self.terrain.reverse()


    def draw(self, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return

        from gym.envs.classic_control import rendering
        if self.viewer is None:
            self.viewer = rendering.Viewer(self.window_size[0], self.window_size[1])

        self.viewer.draw_polygon([(0,0),(self.window_size[0], 0),
                                  (self.window_size[0],self.window_size[1]),
                                  (0,self.window_size[1]),],color=(0.9, 0.9, 1.0))

        for poly, color in self.terrain_poly:
            self.viewer.draw_polygon(poly, color=color)

        for obj in self.terrain:
            for f in obj.fixtures:
                trans = f.body.transform
                if type(f.shape) is circleShape:
                    t = rendering.Transform(translation=trans*f.shape.pos)
                    self.viewer.draw_circle(f.shape.radius, 30, color=obj.color1).add_attr(t)
                    self.viewer.draw_circle(f.shape.radius, 30, color=obj.color2, filled=False, linewidth=2).add_attr(t)
                else:
                    path = [trans*v for v in f.shape.vertices]
                    self.viewer.draw_polygon(path, color=obj.color1)
                    path.append(path[0])
                    self.viewer.draw_polyline(path, color=obj.color2, linewidth=2)

        return self.viewer.render(return_rgb_array = mode=='rgb_array')

if __name__ == "__main__":
    terrain = Terrain()
    terrain.make_slope()
    terrain.create_terrain()
    while True:
        terrain.draw()
