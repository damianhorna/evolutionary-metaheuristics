from aem.heuristics.heuristic import Heuristic
from aem.heuristics.random import Random
from aem.shared.experiment_result import ExperimentResult
import numpy as np
import time

class AlterHeuristic(Heuristic):
    def __init__(self, graph, action_factory):
        super().__init__(graph)
        self.action_factory = action_factory

    def run(self, seed=None, number_of_experiments=1) -> ExperimentResult:
        if seed:
            np.random.seed(seed)
        start_cycles = []
        for i in range(number_of_experiments):
            start_cycles.append(Random(self.graph).build_cycle(np.random.randint(self.graph.no_of_vertices())))

        cycles = []
        times = []
        for cycle in start_cycles:
            improved = True
            start_time = time.time()
            while improved:
                cycle, improved = self.alter_cycle(cycle)
            cycles.append(cycle)
            times.append(time.time()-start_time)
        lengths = []
        for c in cycles:
            c_length = self.graph.compute_cycle_length(c)
            lengths.append(c_length)

        lengths = np.array(lengths)
        best_cycle_idx = int(np.argmin(lengths))

        return ExperimentResult(average_len=np.mean(lengths),
                                min_len=np.min(lengths),
                                max_len=np.max(lengths),
                                best_cycle=cycles[best_cycle_idx],
                                method_classname=self.__class__.__name__+" "+self.action_factory.__class__.__name__,
                                time_average=np.mean(times),
                                time_min=np.min(times),
                                time_max=np.max(times)
                                )
