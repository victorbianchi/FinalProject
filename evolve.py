"""
Top level module running the main game function.
This script randomly generates the initial
population of bipedals and the testing terrain.
After evaluating each bipedal's performance, the
generation is breed to produce the next.
"""

# import modules
import copy
import view
from sim import Simulation as Sim
from terrain import Terrain
from bipedal import Bipedal as Biped
from algo import Population as Pop
from log_data import Data

num_gen = 50
size_gen = 10
num_shown = 5


def main():

    # Create first generation
    pool = Pop(size_gen)

    # Step through generations
    for _ in range(num_gen):

        # initialize data histogram for sim visualization
        hist = Data()
        terrain = Terrain(400, 4)

        # create pybox2d dynamic bodies based on individual's gene
        gen = [Biped(pool.population[i].name, pool.population[i].gene)
               for i in range(size_gen)]

        for k, biped in enumerate(gen):

            # specify terrain and biped to race
            race = Sim(terrain, biped)

            if not hist.terrain:
                hist.set_terrain(terrain)

            # run simulation without visualization
            score, bb, time = race.run(1e4)

            # store sim data and fitness evaluation
            pool.population[k].fitness = score
            hist.timelines[biped.name] = race.history.timelines['timeline']

        # resort gene pool
        pool.population = list(
            sorted(pool.population, key=lambda x: x.fitness))

        # visualize top bipeds' simulations
        shown = pool.population[-num_shown:]
        timelines = [s.name for s in shown]
        view.start()
        view.run(hist, timelines, speed=3)

        # evolve gene pool
        pool.evolve()


if __name__ == '__main__':
    main()
