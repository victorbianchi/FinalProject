
import Box2D
from Box2D.b2 import (world, polygonShape, circleShape,
                      staticBody, dynamicBody)
from log_data import Data

# by convention, constants are capitalized
MIN_MOVE = 0.5
MAX_STUCK_TIME = 2


class Simulation:
    def __init__(self, terrain, biped, save=False):
        self.terrain = terrain
        self.biped = biped

        # Create the world
        self.sim_world = world(gravity=(0, -10), doSleep=True)
        # Create the terrain (static ground body)
        self.terrain.world = self.sim_world
        self.terrain.build(self.sim_world)

        x0, y0 = self.terrain.get_spawn_pos()
        self.biped.build(self.sim_world, x0, y0)

        self.tracker = self.biped.tracker
        self.starting_position = self.tracker[0]  # just x coordinate

        # Only init history after terrain was built
        self.history = Data(self.terrain)

    def run(self, n_iter=-1, speed=1.):
        "Returns dist covered and whether it is over (bool)"
        stuck_time = 0

        time_step = speed / 60.  # 60 Hz by default
        vel_iters, pos_iters = 6, 2  # apparently good
        i = 0
        while True:
            self.sim_world.Step(time_step, vel_iters, pos_iters)
            if self.history:
                self.history.save_state(self.biped)

            # check if we're moving forward
            position = self.tracker[0]
            distance = position - self.starting_position
            if distance < MIN_MOVE:
                stuck_time += time_step
            else:
                stuck_time = 0

            # if we're stuck for too long finish the loop
            if stuck_time > MAX_STUCK_TIME:
                print("Stuck in one place")
                return distance, True, n_iter

            i += 1
            if n_iter > 0 and i > n_iter:
                # or:
                #   if i > n_iter > 0:
                # don't try this in other programming languages, though!
                print("Reached max time", n_iter * time_step, "s")
                return distance, False, n_iter

            if self.tracker[1] < 0:

                print("Fell off the cliff")
                return distance, True, n_iter

        # return final distance
        print("Normal")
        return (distance, False, n_iter)
