import sys, math
import numpy as np

import Box2D
from Box2D.b2 import (edgeShape, circleShape, fixtureDef, polygonShape, revoluteJointDef, contactListener)

import gym
from gym import spaces
from gym.utils import colorize, seeding

wndw_height = 400
wndw_width = 600
step = 1
length = wndw_width
height = wndw_height/4
grass_length = 10
start = 20
friction = 2.5

class Terrain(gym.Env):

    FPS = 50
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second' : FPS
    }

    def __init__(self):
        self._seed()
        self.viewer = None

        self.world = Box2D.b2World()
        self.terrain = None

        self.prev_shaping = None
        self._reset()

        high = np.array([np.inf]*24)
        self.action_space = spaces.Box(np.array([-1,-1,-1,-1]), np.array([+1,+1,+1,+1]))
        self.observation_space = spaces.Box(-high, high)

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _destroy(self):
        if not self.terrain: return
        for t in self.terrain:
            self.world.DestroyBody(t)
        self.terrain = []

    def _generate_terrain(self):
        GRASS, _STATES_ = range(2)
        state    = GRASS
        velocity = 0.0
        y        = height
        counter  = start
        oneshot  = False
        self.terrain   = []
        self.terrain_x = []
        self.terrain_y = []

        for i in range(length):
            x = i*step
            self.terrain_x.append(x)

            if state==GRASS and not oneshot:
                velocity = 0.8*velocity + 0.01*np.sign(height - y)
                if i > start: velocity += self.np_random.uniform(-.25, .25)   #1
                y += velocity

            oneshot = False
            self.terrain_y.append(y)
            counter -= 1
            if counter==0:
                counter = self.np_random.randint(grass_length/2, grass_length)
                state = GRASS
                oneshot = True

        self.terrain_poly = []
        for i in range(length-1):
            poly = [
                (self.terrain_x[i],   self.terrain_y[i]),
                (self.terrain_x[i+1], self.terrain_y[i+1])
                ]
            t = self.world.CreateStaticBody(
                fixtures = fixtureDef(
                    shape=edgeShape(vertices=poly),
                    friction = friction,
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

    def _reset(self):
        self._destroy()
        self.game_over = False
        self.prev_shaping = None

        self._generate_terrain()


    def _render(self, agents, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return

        from gym.envs.classic_control import rendering
        if self.viewer is None:
            self.viewer = rendering.Viewer(wndw_width, wndw_height)
        self.viewer.set_bounds(0, wndw_width, 0, wndw_height)

        self.viewer.draw_polygon( [(0,0),(wndw_width, 0),(wndw_width, wndw_height),(0,wndw_height),], color=(0.9, 0.9, 1.0) )

        for poly, color in self.terrain_poly:
            self.viewer.draw_polygon(poly, color=color)

        legs = [item for sublist in [agents[c].legs for c in range(len(agents))] for item in sublist]
        hulls = [agents[c].hull for c in range(len(agents))]
        self.drawlist = self.terrain + legs + hulls

        for obj in self.drawlist:
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

        flagy1 = height
        flagy2 = flagy1 + 50
        x = step*3
        self.viewer.draw_polyline( [(x, flagy1), (x, flagy2)], color=(0,0,0), linewidth=2 )
        f = [(x, flagy2), (x, flagy2-10), (x+25, flagy2-5)]
        self.viewer.draw_polygon(f, color=(0.9,0.2,0) )
        self.viewer.draw_polyline(f + [f[0]], color=(0,0,0), linewidth=2 )

        return self.viewer.render(return_rgb_array = mode=='rgb_array')
