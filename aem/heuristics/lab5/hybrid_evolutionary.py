import time
from collections import defaultdict

from aem.heuristics.alter.action import SwapInnerNodes
from aem.heuristics.greedy import Greedy
from aem.heuristics.lab3.steepest_edge_swap_lom import SteepestEdgeSwapListOfMoves
from aem.heuristics.random import Random
from aem.shared.experiment_result import ExperimentResult
import numpy as np


class HybridEvolutionary(SteepestEdgeSwapListOfMoves, Greedy):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run_experiment(self, start_population, time_limit=1):
        population = np.array(start_population)
        self.reset()
        start_time = time.time()
        generations = 0
        while time.time()-start_time < time_limit:
            generations += 1
            # wylosuj dwa różne rozwiązania z rozk. równomiernego
            two_random = np.random.choice(population[:,0], 2, replace=False)
            parent_a = two_random[0]
            parent_b = two_random[1]
            # rekombinacja
            y = self.recombine(parent_a, parent_b)
            # local search
            improved = True
            self.reset()
            while improved:
                y, improved = self.alter_cycle(y)
            # jeżeli y jest lepsze od najgorszego i rozne od wszystkich w pop
            # dodaj y do pop i usun najgorsze
            worst_in_pop_idx = np.argmax(population[:,1])
            worst_in_pop = population[worst_in_pop_idx]
            y_fitness = self.graph.compute_cycle_length(y)
            if y_fitness < worst_in_pop[1]: # sprawdz czy przypadkiem y nie znajduje sie juz w populacji
                population[worst_in_pop_idx] = np.array((y, y_fitness))

        return population[np.argmin(population[:,1])][0],generations

    def find_longest_common_sequence(self, list_a, list_b, poz_a, poz_b):
        first = -1
        while list_a[poz_a+first] == list_b[poz_b+first]:
            first -= 1
        first += 1

        last = 1
        while list_a[(poz_a+last)%len(list_a)] == list_b[(poz_b+last)%len(list_b)]:
            last += 1
        res = []
        poz = first

        while poz != last:
            res.append(list_a[(poz_a+poz)%len(list_a)])
            poz += 1
        return res

    def recombine(self, parent_a, parent_b):
        common_vertices = set(parent_a).intersection(set(parent_b))
        indexes_a = {v:i for i,v in enumerate(parent_a)}
        indexes_b = {v:i for i,v in enumerate(parent_b)}

        commons = []
        commons_length = 0
        used_nodes = set()
        while len(common_vertices) > 0:
            idx = common_vertices.pop()
            common_vertices.add(idx)
            poz_a = indexes_a[idx]
            poz_b = indexes_b[idx]
            com = self.find_longest_common_sequence(parent_a, parent_b, poz_a, poz_b)
            com_reverse = self.find_longest_common_sequence(parent_a, parent_b[::-1], poz_a, (len(parent_b)-poz_b-1))
            if len(com) < len(com_reverse):
                com = com_reverse
            for c in com:
                common_vertices.remove(c)

            if len(com) > 1:
                commons_length += len(com)
                commons.append(com)
                for x in com:
                    used_nodes.add(x)
        while commons_length != len(parent_a):

            #x = parent_a[np.random.randint(len(parent_a))]
            if np.random.randn() < 0:
                x = np.random.choice(parent_a)
            else:
                x = np.random.choice(parent_b)

            if x not in used_nodes:
                commons.append([x])
                commons_length += 1
                used_nodes.add(x)

        np.random.shuffle(commons)
        #commons.sort(key=lambda x: indexes_a[x[0]] if x[0] in indexes_a else indexes_b[x[0]])
        res = []

        for x in commons:
            res.extend(x)

        return res

    def run(self, seed=None, time_limit=1, population_size=20, number_of_experiments=1) -> ExperimentResult:
        if seed:
            np.random.seed(seed)
        start_populations = defaultdict(list)
        for i in range(number_of_experiments):
            for _ in range(population_size):
                chromosome = Random(self.graph).build_cycle(np.random.randint(self.graph.no_of_vertices()))
                fitness = self.graph.compute_cycle_length(chromosome)
                start_populations[i].append((chromosome, fitness))

        cycles = []
        generations_number = []
        for i in range(number_of_experiments):
            start_population = start_populations[i]

            c,g = self.run_experiment(start_population, time_limit)
            cycles.append(c)
            generations_number.append(g)

        scores = list(map(lambda x: self.graph.compute_cycle_length(x), cycles))
        min_poz = np.argmin(scores)
        return ExperimentResult(
            average_len=np.mean(scores),
            min_len=np.min(scores),
            max_len=np.max(scores),
            best_cycle=cycles[min_poz],
            method_classname=self.__class__.__name__,
            time_average=np.mean(generations_number),
            time_min=np.min(generations_number),
            time_max=np.max(generations_number)
        )