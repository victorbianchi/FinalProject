from random import (choice, random, randint)
import view

__all__ = ['Chromosome', 'Population']


class Chromosome:
    """
    This class is used to define a chromosome for the gentic algorithm
    simulation.
    This class is essentially nothing more than a container for the details
    of the chromosome, namely the gene (the string that represents our
    target string) and the fitness (how close the gene is to the target
    string).
    Note that this class is immutable.  Calling mate() or mutate() will
    result in a new chromosome instance being created.
    """
    # [leg height, leg width]
    gene_range = [[50, 100], [50, 100], [50, 100]]

    def __init__(self, gene):
        self.gene = gene
        self.fitness = 0
        self.name = self.get_name

    def mate(self, mate):
        """
        Method used to mate the chromosome with another chromosome,
        resulting in a new chromosome being returned.
        """

        # random int on the range of length of gene
        pivot = randint(0, len(self.gene) - 1)

        # generates two mismatched genes
        gene1 = self.gene[:pivot] + mate.gene[pivot:]
        gene2 = mate.gene[:pivot] + self.gene[pivot:]

        return Chromosome(gene1), Chromosome(gene2)

    def mutate(self):
        """
        Method used to generate a new chromosome based on a change in a
        random character in the gene of this chromosome.  A new chromosome
        will be created, but this original will not be affected.
        """

        # randomly change a character of the chromosome
        gene = self.gene
        idx = randint(0, len(gene) - 1)
        delta = randint(-int(gene[idx] / 2), int(gene[idx] / 2))
        gene[idx] += delta

        return Chromosome(gene)

    @staticmethod
    def _update_fitness(gene):
        """
        Helper method used to return the fitness for the chromosome based
        on its gene.
        """
        fitness = 0
        for a, b in zip(gene, Chromosome._target_gene):
            fitness += abs(a - b)

        return fitness

    @staticmethod
    def gen_random():
        """
        A convenience method for generating a random chromosome with a random
        gene.
        """
        gene = []
        for min_val, max_val in Chromosome.gene_range:
            gene.append(randint(min_val, max_val) / 50.0)

        return gene

    # consider __str__ or __repr__, so that you can print or format chromosomes
    # and pick up this representation automatically – also the cognitive load
    # for the maintainer is lower, since those are standard methods.
    def get_name():
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))


class Population:
    """
    A class representing a population for a genetic algorithm simulation.
    A population is simply a sorted collection of chromosomes
    (sorted by fitness) that has a convenience method for evolution.  This
    implementation of a population uses a tournament selection algorithm for
    selecting parents for crossover during each generation's evolution.
    Note that this object is mutable, and calls to the evolve()
    method will generate a new collection of chromosome objects.
    """

    _tournamentSize = 3

    def __init__(self, size=2084, crossover=0.8, elitism=0.1, mutation=0.03):
        self.elitism = elitism
        self.mutation = mutation
        self.crossover = crossover

        buf = []
        # _ is conventional for an unused variable
        for _ in range(size):
            buf.append(Chromosome(Chromosome.gen_random()))
        self.population = list(sorted(buf, key=lambda x: x.fitness))

    def _tournament_selection(self):
        """
        A helper method used to select a random chromosome from the
        population using a tournament selection algorithm.
        """
        best = choice(self.population)
        # This code chooses the best among Population._tournamentSize+1 choices,
        # which is slightly misleading.
        for _ in range(Population._tournamentSize):
            cont = choice(self.population)
            if cont.fitness > best.fitness:
                best = cont
        # You can also use:
        #   choices = [choice(self.population) for _ in range(Population._tournamentSize)]
        #   return max(choices, key=lambda x: x.fitness)
        # or, to avoid actually allocating memory for a list:
        #   choices = (choice(self.population) for _ in range(Population._tournamentSize))
        #   return max(choices, key=lambda x: x.fitness)
        # or just:
        #   return max((choice(self.population) for _ in range(Population._tournamentSize))),
        #               key=lambda x: x.fitness)
        # These last two choices run the same as what you've written (except with only
        # Population._tournamentSize choices.)
        #
        # If you define Chromosome.__lt__(self, other): return self.fitness < other.fitness
        # then you can use simply:
        #    return max(choice(self.population) for _ in range(Population._tournamentSize))
        # here and:
        #   sorted(buf, key=lambda x: x.fitness)
        # in Population.__init__.
        return best

    def _selectParents(self):
        """
        A helper method used to select two parents from the population using a
        tournament selection algorithm.
        """

        return (self._tournament_selection(), self._tournament_selection())

    def evolve(self):
        """
        Method to evolve the population of chromosomes.
        """
        size = len(self.population)
        # floor is safer than round, to insure that idx will never exceed the
        # size of self.population. This will also insure an even distribution at
        # the ends of the range; else, zero may be under-represented.
        idx = int(round(size * self.elitism))
        buf = self.population[:idx]

        while idx < size:
            if random() <= self.crossover:
                (p1, p2) = self._selectParents()
                children = p1.mate(p2)
                for c in children:
                    if random() <= self.mutation:
                        buf.append(c.mutate())
                    else:
                        buf.append(c)
                idx += 2
            else:
                if random() <= self.mutation:
                    buf.append(self.population[idx].mutate())
                else:
                    buf.append(self.population[idx])
                idx += 1

        self.population = list(sorted(buf[:size], key=lambda x: x.fitness))


# Comment code out with # instead of quotes, so it doesn't look like doc strings.
# Better: hide it inside an `if false`. This makes it easier to distinguish
# code from comment, and can help maintainers find references to classes and
# methods that they modify. (If the code is *never* coming back, it should be
# simply removed, and use a git branch or git tag if you want to preserve
# a reference to it.)
# In this case, it's already protected from execution by the `__name__ == "__main__"`
# guard – not sure why you need to disable it. (But if you do, add a comment as to why!)
# if __name__ == "__main__":
#     maxGenerations = 16384
#     size = 20
#     pop = Population(size=size, crossover=0.8, elitism=0.2, mutation=0.3)
#     for i in range(1, maxGenerations + 1):
#         print("Generation %d:" % i)
#         total_fitness = 0
#         for c in range(size):
#             pop.population[c].fitness = view.create(pop.population[c].gene[0]*.3, pop.population[c].gene[1]*.3)
#             print("Character", c, "=", pop.population[c].fitness)
#             total_fitness += pop.population[c].fitness
#         else:
#             print("Average Fitness of population", i, "=", total_fitness/size)
#             pop.population = list(sorted(pop.population, key=lambda x: x.fitness))
#             print([pop.population[i].fitness for i in range(size)])
#             pop.evolve()
#     else:
#         print("Maximum generations reached without success.")
