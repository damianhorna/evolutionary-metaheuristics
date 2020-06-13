import time

from aem.heuristics.alter.action import SwapInnerNodes
from aem.heuristics.greedy import Greedy
from aem.heuristics.lab3.steepest_edge_swap_lom import SteepestEdgeSwapListOfMoves
from aem.heuristics.random import Random
from aem.shared.experiment_result import ExperimentResult
import numpy as np

class ItereteLocalSearchPerturbation(SteepestEdgeSwapListOfMoves, Greedy):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def run_experiment(self, cycle, time_limit=1):
        self.reset()
        start_time = time.time()
        best_cycle = None
        best_cycle_length = None
        iterations = 0
        while time.time()-start_time < time_limit:
            iterations += 1
        #    self.reset()
            improved = True
            while improved:
                cycle, improved = self.alter_cycle(cycle)


            new_cycle_length = self.graph.compute_cycle_length(cycle)
            if best_cycle_length is None or best_cycle_length > new_cycle_length:
                best_cycle_length = new_cycle_length
                best_cycle = cycle.copy()

            # Perturbation
            for _ in range(5):
                a = np.random.randint(len(cycle))
                b = np.random.randint(len(cycle))
                while b == a:
                    b = np.random.randint(len(cycle))
                a = cycle[a]
                b = cycle[b]
                action = SwapInnerNodes(a,b)
                cycle = action.alter(cycle, self.graph, False)
                self.add_new_moves(action, cycle)
                # cycle[a],cycle[b] = cycle[b], cycle[a]

        return best_cycle,iterations
    def run(self, seed=None, time_limit=1,number_of_experiments=1) -> ExperimentResult:
        if seed:
            np.random.seed(seed)
        start_cycles = []
        for i in range(number_of_experiments):
            start_cycles.append(Random(self.graph).build_cycle(np.random.randint(self.graph.no_of_vertices())))

        cycles = []
        iterations = []
        for i in range(number_of_experiments):
            cycle = start_cycles[i]

            c,i = self.run_experiment(cycle, time_limit)
            cycles.append(c)
            iterations.append(i)

        scores = list(map(lambda x: self.graph.compute_cycle_length(x), cycles))
        min_poz = np.argmin(scores)
        return ExperimentResult(
            average_len=np.mean(scores),
            min_len=np.min(scores),
            max_len=np.max(scores),
            best_cycle=cycles[min_poz],
            method_classname=self.__class__.__name__,
            time_average=np.mean(iterations),
            time_min=np.min(iterations),
            time_max=np.max(iterations)
        )