import env, agent, algo

maxGenerations = 16384
size = 1

if __name__ == "__main__":

    for i in range(1, maxGenerations + 1):
        pop = algo.Population(size=size, crossover=0.8, elitism=0.2, mutation=0.3)
        print("Generation %d:" % i)
        total_fitness = 0
        terrain = env.Terrain()
        terrain.reset()
        running = True
        agents = [agent.Agent(pop.population[c], terrain.world) for c in range(size)]
        for c in range(size):
            agents[c].define_hull()
            agents[c].define_legs()
        print(agents)

        while(running):
            terrain._render(agents)
            for c in range(size):
                agents[c].walk()

        pop.population = list(sorted(agents, key=lambda x: x.fitness))
        print("Average Fitness of population", i, "=", sum([pop.population[i].fitness for i in range(size)])/size)
        pop.evolve()
    else:
        print("Maximum generations reached without success.")
